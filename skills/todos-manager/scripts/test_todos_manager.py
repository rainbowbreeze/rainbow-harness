#!/usr/bin/env python3
import os
import sys
import json
import subprocess
import unittest
import tempfile
from datetime import datetime

class TestTodosManager(unittest.TestCase):
    def setUp(self):
        # Create an isolated temporary directory for the event database
        self.test_dir = tempfile.TemporaryDirectory()
        self.env = os.environ.copy()
        self.env["BRAIN_TODOSDB_PATH"] = self.test_dir.name
        
        # Path to the target manager script
        self.script_path = os.path.join(os.path.dirname(__file__), "todos_manager.py")
        self.db_path = os.path.join(self.test_dir.name, "todos.json")

    def tearDown(self):
        self.test_dir.cleanup()

    def run_manager(self, *args):
        """Helper to invoke the todos_manager CLI"""
        cmd = [sys.executable, self.script_path] + list(args)
        result = subprocess.run(cmd, env=self.env, capture_output=True, text=True)
        return result

    def test_add_remove_query_flow(self):
        # 1. ADD a todo
        res_add = self.run_manager(
            "add",
            "--title", "Test Todo",
            "--description", "A great test todo",
            "--source", "user-command",
            "--due-date", "2026-10-01"
        )
        self.assertEqual(res_add.returncode, 0, f"Add failed: {res_add.stderr}")
        self.assertIn("Todo was added successfully", res_add.stdout)
        
        # Extract slug
        today_date = datetime.now().strftime("%Y-%m-%d").replace("-", "")
        expected_slug = f"{today_date}-test-todo"
        
        # Verify JSON was written correctly and passed the linter
        self.assertTrue(os.path.exists(self.db_path))
        with open(self.db_path, "r", encoding="utf-8") as f:
            data = json.load(f)
            self.assertEqual(len(data), 1)
            self.assertEqual(data[0]["title"], "Test Todo")
            self.assertEqual(data[0]["slug"], expected_slug)

        # 2. ADD duplicate todo (should trigger linter / duplicate check and fail)
        res_add_dup = self.run_manager(
            "add",
            "--title", "Test Todo",
            "--description", "Duplicate Todo",
            "--source", "user-command",
        )
        self.assertNotEqual(res_add_dup.returncode, 0, "Adding duplicate slug should fail")
        self.assertIn("already exists", res_add_dup.stderr)

        # 3. QUERY todos
        res_query = self.run_manager("query", "--source", "user-command")
        self.assertEqual(res_query.returncode, 0, f"Query failed: {res_query.stderr}")
        query_data = json.loads(res_query.stdout)
        self.assertEqual(len(query_data), 1)
        self.assertEqual(query_data[0]["slug"], expected_slug)
        
        # 4. QUERY empty filter
        res_query_out = self.run_manager("query", "--source", "email")
        self.assertEqual(res_query_out.returncode, 0)
        query_data_out = json.loads(res_query_out.stdout)
        self.assertEqual(len(query_data_out), 0)

        # 5. UPDATE the todo
        res_update = self.run_manager(
            "update",
            "--slug", expected_slug,
            "--title", "Updated Title"
        )
        self.assertEqual(res_update.returncode, 0, f"Update failed: {res_update.stderr}")
        self.assertIn("successfully updated", res_update.stdout)
        
        with open(self.db_path, "r", encoding="utf-8") as f:
            data_updated = json.load(f)
            self.assertEqual(data_updated[0]["title"], "Updated Title")

        # 6. REMOVE the todo by slug
        res_remove = self.run_manager(
            "remove",
            "--slug", expected_slug
        )
        self.assertEqual(res_remove.returncode, 0, f"Remove failed: {res_remove.stderr}")
        self.assertIn("successfully removed", res_remove.stdout)
        
        # Verify JSON is empty
        with open(self.db_path, "r", encoding="utf-8") as f:
            data_empty = json.load(f)
            self.assertEqual(len(data_empty), 0)

if __name__ == '__main__':
    unittest.main(verbosity=2)
