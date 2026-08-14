#!/usr/bin/env node

import fs from 'fs';
import path from 'path';
import { getBrainDir } from './resolve-brain.js';

const brainDir = getBrainDir();

function parseFrontmatter(content) {
  const match = content.match(/^---\r?\n([\s\S]*?)\r?\n---/);
  if (!match) return null;
  const yamlBlock = match[1];
  const data = {};
  
  for (const line of yamlBlock.split('\n')) {
    const colonIdx = line.indexOf(':');
    if (colonIdx > 0 && !line.startsWith(' ') && !line.startsWith('-')) {
      const key = line.slice(0, colonIdx).trim();
      let value = line.slice(colonIdx + 1).trim();
      
      if (value.startsWith('[') && value.endsWith(']')) {
        try {
          value = JSON.parse(value.replace(/'/g, '"'));
        } catch {
          value = value.slice(1, -1).split(',').map(s => s.trim().replace(/^["']|["']$/g, ''));
        }
      } else {
        value = value.replace(/^["']|["']$/g, '');
      }
      data[key] = value;
    }
  }
  return { frontmatter: data, rawYaml: yamlBlock, body: content.slice(match[0].length) };
}

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
    } else if (entry.isFile() && entry.name.endsWith('.md')) {
      files.push(fullPath);
    }
  }
  return files;
}

function runLint() {
  console.log(`🔍 Running Knowledge Base Linter targeting: ${brainDir}\n`);
  let errors = [];
  let warnings = [];

  const aliasMap = new Map();
  const idMap = new Map();

  // Scan all subdirectories inside brainDir
  const subdirs = fs.readdirSync(brainDir, { withFileTypes: true })
    .filter(d => d.isDirectory() && d.name !== '.raw' && d.name !== '.git')
    .map(d => d.name);

  const allFiles = [];
  for (const dirName of subdirs) {
    const dirPath = path.join(brainDir, dirName);
    allFiles.push(...getAllMarkdownFiles(dirPath));
  }

  for (const filePath of allFiles) {
    const relPath = path.relative(brainDir, filePath);
    const basename = path.basename(filePath);
    if (basename === 'README.md') continue;

    const content = fs.readFileSync(filePath, 'utf-8');
    const parsed = parseFrontmatter(content);

    if (!parsed) {
      errors.push(`[${relPath}] Missing or malformed YAML frontmatter.`);
      continue;
    }

    const { frontmatter, body } = parsed;

    // Check Universal Base Schema Mandatory Fields
    const requiredFields = ['type', 'id', 'title', 'updated_at'];
    for (const field of requiredFields) {
      if (!frontmatter[field]) {
        errors.push(`[${relPath}] Missing mandatory Universal Base field: "${field}"`);
      }
    }

    // Check that ID matches the filename slug
    const expectedId = path.basename(filePath, '.md');
    if (frontmatter.id && frontmatter.id !== expectedId) {
      warnings.push(`[${relPath}] ID "${frontmatter.id}" does not match filename slug "${expectedId}"`);
    }

    // Check ID collisions
    if (frontmatter.id) {
      if (idMap.has(frontmatter.id)) {
        errors.push(`[${relPath}] Duplicate ID "${frontmatter.id}" also defined in [${idMap.get(frontmatter.id)}]`);
      } else {
        idMap.set(frontmatter.id, relPath);
      }
    }

    // Check Universal Base Recommended Fields
    if (!frontmatter.status) {
      warnings.push(`[${relPath}] Missing recommended field "status" (e.g. active, draft, in-progress).`);
    }
    if (!frontmatter.tags) {
      warnings.push(`[${relPath}] Missing recommended field "tags".`);
    }

    // Check Two-Layer separator
    if (!body.includes('\n---') && !body.includes('\r\n---')) {
      warnings.push(`[${relPath}] Missing two-layer divider (---) separating Compiled Truth from Timeline.`);
    }

    // Check Aliases collisions
    if (frontmatter.aliases && Array.isArray(frontmatter.aliases)) {
      for (const alias of frontmatter.aliases) {
        const normAlias = alias.toLowerCase().trim();
        if (aliasMap.has(normAlias)) {
          warnings.push(`[${relPath}] Alias collision "${alias}" already defined in [${aliasMap.get(normAlias)}]`);
        } else {
          aliasMap.set(normAlias, relPath);
        }
      }
    }

    // Check Markdown Link Integrity
    const linkRegex = /\[([^\]]+)\]\(([^)]+)\)/g;
    let linkMatch;
    while ((linkMatch = linkRegex.exec(body)) !== null) {
      const linkTarget = linkMatch[2];
      if (linkTarget.startsWith('http://') || linkTarget.startsWith('https://') || linkTarget.startsWith('#') || linkTarget.startsWith('mailto:')) {
        continue;
      }
      const targetClean = linkTarget.split('#')[0];
      const targetAbs = path.resolve(path.dirname(filePath), targetClean);
      if (!fs.existsSync(targetAbs)) {
        errors.push(`[${relPath}] Broken relative link: "${linkTarget}"`);
      }
    }
  }

  console.log(`Scanned ${allFiles.length} markdown files in brain directory.`);
  
  if (warnings.length > 0) {
    console.log(`\n⚠️  Warnings (${warnings.length}):`);
    warnings.forEach(w => console.log(`   - ${w}`));
  }

  if (errors.length > 0) {
    console.error(`\n❌ Errors (${errors.length}):`);
    errors.forEach(e => console.error(`   - ${e}`));
    console.error('\n❌ Lint check failed.');
    process.exit(1);
  } else {
    console.log('\n✅ All lint checks passed successfully!');
  }
}

runLint();
