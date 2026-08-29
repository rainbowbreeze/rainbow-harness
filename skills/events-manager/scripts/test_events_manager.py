#!/usr/bin/env python3
import os
import sys
import json
import subprocess
import unittest
import tempfile

class TestEventsManager(unittest.TestCase):
    def setUp(self):
        # Create an isolated temporary directory for the event database
        self.test_dir = tempfile.TemporaryDirectory()
        self.env = os.environ.copy()
        self.env["BRAIN_EVENTSDB_PATH"] = self.test_dir.name
        
        # Path to the target manager script
        self.script_path = os.path.join(os.path.dirname(__file__), "events_manager.py")
        self.category = "test_events"
        self.db_path = os.path.join(self.test_dir.name, self.category, "events.json")

    def tearDown(self):
        self.test_dir.cleanup()

    def run_manager(self, *args):
        """Helper to invoke the events_manager CLI"""
        cmd = [sys.executable, self.script_path, "--category", self.category] + list(args)
        result = subprocess.run(cmd, env=self.env, capture_output=True, text=True)
        return result

    def test_add_remove_query_flow(self):
        # 1. ADD an event
        res_add = self.run_manager(
            "add",
            "--title", "Test Concert",
            "--start-date", "2026-10-01",
            "--end-date", "2026-10-02",
            "--description", "A great test concert",
            "--url", "https://example.com/test-concert",
            "--location", "Test Arena"
        )
        self.assertEqual(res_add.returncode, 0, f"Add failed: {res_add.stderr}")
        self.assertIn("Event was added successfully", res_add.stdout)
        
        # Verify JSON was written correctly and passed the linter
        self.assertTrue(os.path.exists(self.db_path))
        with open(self.db_path, "r", encoding="utf-8") as f:
            data = json.load(f)
            self.assertEqual(len(data), 1)
            self.assertEqual(data[0]["titolo"], "Test Concert")
            self.assertEqual(data[0]["slug"], "20261001-test-concert")

        # 2. ADD duplicate event (should trigger linter / duplicate check and fail)
        res_add_dup = self.run_manager(
            "add",
            "--title", "Test Concert",
            "--start-date", "2026-10-01",
            "--end-date", "2026-10-02",
            "--description", "Duplicate Event",
            "--url", "https://example.com/test-concert-2",
            "--location", "Test Arena"
        )
        self.assertNotEqual(res_add_dup.returncode, 0, "Adding duplicate slug should fail")
        self.assertIn("already exists", res_add_dup.stderr)

        # 3. QUERY events (overlap matching)
        res_query = self.run_manager(
            "query",
            "--start-date", "2026-09-30",
            "--end-date", "2026-10-05"
        )
        self.assertEqual(res_query.returncode, 0, f"Query failed: {res_query.stderr}")
        query_data = json.loads(res_query.stdout)
        self.assertEqual(len(query_data), 1)
        self.assertEqual(query_data[0]["slug"], "20261001-test-concert")
        
        # 4. QUERY outside range (should return empty list)
        res_query_out = self.run_manager(
            "query",
            "--start-date", "2026-11-01",
            "--end-date", "2026-11-05"
        )
        self.assertEqual(res_query_out.returncode, 0)
        query_data_out = json.loads(res_query_out.stdout)
        self.assertEqual(len(query_data_out), 0)

        # 5. REMOVE the event by deriving the slug from title and date
        res_remove = self.run_manager(
            "remove",
            "--title", "Test Concert",
            "--start-date", "2026-10-01"
        )
        self.assertEqual(res_remove.returncode, 0, f"Remove failed: {res_remove.stderr}")
        self.assertIn("successfully removed", res_remove.stdout)
        
        # Verify JSON is empty
        with open(self.db_path, "r", encoding="utf-8") as f:
            data_empty = json.load(f)
            self.assertEqual(len(data_empty), 0)

        # 6. ARCHIVE events
        # First, add a past event and a future event
        self.run_manager("add", "--title", "Past Event", "--start-date", "2025-01-01", "--end-date", "2025-01-02", "--url", "http://past", "--location", "Here", "--description", "Desc")
        self.run_manager("add", "--title", "Future Event", "--start-date", "2027-01-01", "--end-date", "2027-01-02", "--url", "http://future", "--location", "Here", "--description", "Desc")
        
        res_archive = self.run_manager("archive", "--before-date", "2026-01-01")
        self.assertEqual(res_archive.returncode, 0, f"Archive failed: {res_archive.stderr}")
        self.assertIn("Archived 1 events", res_archive.stdout)
        
        # Verify active contains only future
        with open(self.db_path, "r", encoding="utf-8") as f:
            data_active = json.load(f)
            self.assertEqual(len(data_active), 1)
            self.assertEqual(data_active[0]["slug"], "20270101-future-event")
            
        # Verify archive contains only past
        archive_path = self.db_path.replace("events.json", "events_archive.json")
        with open(archive_path, "r", encoding="utf-8") as f:
            data_archive = json.load(f)
            self.assertEqual(len(data_archive), 1)
            self.assertEqual(data_archive[0]["slug"], "20250101-past-event")

        # 7. REMOVE non-existent event (should fail safely)
        res_remove_fail = self.run_manager(
            "remove",
            "--slug", "20261001-test-concert"
        )
        self.assertNotEqual(res_remove_fail.returncode, 0)
        self.assertIn("could not be found", res_remove_fail.stderr)

    def test_missing_parameters(self):
        # 1. ADD missing required parameter (e.g. --description)
        res_add_missing = self.run_manager(
            "add",
            "--title", "Test Concert",
            "--start-date", "2026-10-01",
            "--end-date", "2026-10-02",
            "--url", "https://example.com/test-concert",
            "--location", "Test Arena"
        )
        self.assertNotEqual(res_add_missing.returncode, 0, "Add should fail when missing required parameters")
        self.assertIn("the following arguments are required", res_add_missing.stderr)
        self.assertIn("--description", res_add_missing.stderr)

        # 2. REMOVE missing targeting parameters
        res_remove_missing = self.run_manager("remove")
        self.assertNotEqual(res_remove_missing.returncode, 0, "Remove should fail when targeting params are missing")
        self.assertIn("Must provide either --slug OR both --title and --start-date", res_remove_missing.stderr)

        # 3. QUERY missing required parameter
        res_query_missing = self.run_manager("query", "--start-date", "2026-10-01")
        self.assertNotEqual(res_query_missing.returncode, 0, "Query should fail when missing date boundaries")
        self.assertIn("the following arguments are required", res_query_missing.stderr)
        self.assertIn("--end-date", res_query_missing.stderr)

if __name__ == '__main__':
    unittest.main(verbosity=2)
