#!/usr/bin/env node

import fs from 'fs';
import path from 'path';
import { getBrainDir } from './resolve-brain.js';

const brainDir = getBrainDir();

const MECE_DIRS = [
  'people',
  'companies',
  'projects',
  'ideas',
  'concepts',
  'meetings',
  'events',
  'deals',
  'writing',
  'sources',
  'inbox',
  'archive'
];

function getAllMarkdownFiles(dir) {
  let files = [];
  if (!fs.existsSync(dir)) return files;
  const entries = fs.readdirSync(dir, { withFileTypes: true });
  for (const entry of entries) {
    const fullPath = path.join(dir, entry.name);
    if (entry.isDirectory()) {
      if (entry.name !== '.raw' && entry.name !== 'node_modules' && entry.name !== '.git') {
        files = files.concat(getAllMarkdownFiles(fullPath));
      }
    } else if (entry.isFile() && entry.name.endsWith('.md') && entry.name !== 'README.md') {
      files.push(fullPath);
    }
  }
  return files;
}

function runStats() {
  console.log(`📊 Computing Knowledge Base Metrics for: ${brainDir}\n`);

  let totalEntities = 0;
  let totalTimelineEntries = 0;
  let totalLinks = 0;
  const countsByDir = {};

  const allFiles = [];

  for (const dir of MECE_DIRS) {
    const dirFiles = getAllMarkdownFiles(path.join(brainDir, dir));
    countsByDir[dir] = dirFiles.length;
    totalEntities += dirFiles.length;
    allFiles.push(...dirFiles);
  }

  const linkRegex = /\[([^\]]+)\]\(([^)]+)\)/g;
  const timelineRegex = /^-\s+\*\*\d{4}-\d{2}-\d{2}\*\*/gm;

  for (const file of allFiles) {
    const content = fs.readFileSync(file, 'utf-8');

    // Count links
    let match;
    while ((match = linkRegex.exec(content)) !== null) {
      if (!match[2].startsWith('http') && !match[2].startsWith('mailto:')) {
        totalLinks++;
      }
    }

    // Count timeline entries
    const timelineMatches = content.match(timelineRegex);
    if (timelineMatches) {
      totalTimelineEntries += timelineMatches.length;
    }
  }

  console.log('📂 Entities by Domain:');
  for (const [dir, count] of Object.entries(countsByDir)) {
    console.log(`   - ${dir.padEnd(12)} : ${count}`);
  }

  console.log('\n📈 System Totals:');
  console.log(`   - Total Entities        : ${totalEntities}`);
  console.log(`   - Total Timeline Events : ${totalTimelineEntries}`);
  console.log(`   - Internal Cross-links  : ${totalLinks}`);
  console.log(`   - Link Density          : ${totalEntities > 0 ? (totalLinks / totalEntities).toFixed(2) : 0} links/entity`);
  console.log(`   - Inbox Backlog         : ${countsByDir['inbox']} items`);
  console.log('\n✅ Stats computed successfully.');
}

runStats();
