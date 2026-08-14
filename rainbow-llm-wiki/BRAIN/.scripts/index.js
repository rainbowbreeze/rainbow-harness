#!/usr/bin/env node

import fs from 'fs';
import path from 'path';
import { getBrainDir } from './resolve-brain.js';

const brainDir = getBrainDir();

const MECE_DIRS = [
  { dir: 'people', title: 'People (`people/`)' },
  { dir: 'companies', title: 'Companies (`companies/`)' },
  { dir: 'projects', title: 'Projects (`projects/`)' },
  { dir: 'concepts', title: 'Concepts (`concepts/`)' },
  { dir: 'ideas', title: 'Ideas (`ideas/`)' },
  { dir: 'meetings', title: 'Meetings (`meetings/`)' },
  { dir: 'events', title: 'Events (`events/`)' },
  { dir: 'deals', title: 'Deals (`deals/`)' },
  { dir: 'writing', title: 'Writing (`writing/`)' },
  { dir: 'sources', title: 'Sources (`sources/`)' },
  { dir: 'inbox', title: 'Inbox (`inbox/`)' },
  { dir: 'archive', title: 'Archive (`archive/`)' }
];

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
  
  const body = content.slice(match[0].length);
  const summaryMatch = body.match(/^>\s*(.*?)(?:\r?\n|$)/m);
  const summary = summaryMatch ? summaryMatch[1].trim() : '';

  return { frontmatter: data, summary, body };
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
    } else if (entry.isFile() && entry.name.endsWith('.md') && entry.name !== 'README.md') {
      files.push(fullPath);
    }
  }
  return files;
}

function buildIndex() {
  console.log(`📚 Rebuilding Knowledge Base Index & Alias Map in: ${brainDir}\n`);

  const aliasesMap = {};
  let indexContent = `# Knowledge Base Index\n\n> Automatically generated via \`bun run index\` / \`node scripts/index.js\`.\n> Last updated: ${new Date().toISOString().split('T')[0]}\n\n---\n\n`;

  let totalCount = 0;

  for (const section of MECE_DIRS) {
    const dirPath = path.join(brainDir, section.dir);
    const files = getAllMarkdownFiles(dirPath);
    indexContent += `## ${section.title}\n`;

    if (files.length === 0) {
      indexContent += `*No active entries.*\n\n`;
      continue;
    }

    files.sort((a, b) => path.basename(a).localeCompare(path.basename(b)));

    for (const file of files) {
      totalCount++;
      const relPath = path.relative(brainDir, file);
      const content = fs.readFileSync(file, 'utf-8');
      const parsed = parseFrontmatter(content);

      const title = parsed?.frontmatter?.title || path.basename(file, '.md');
      const summary = parsed?.summary || (parsed?.frontmatter?.role ? `${parsed.frontmatter.role}${parsed.frontmatter.company ? ' at ' + parsed.frontmatter.company : ''}` : 'No summary provided');

      indexContent += `- [${title}](${relPath}) — ${summary}\n`;

      // Register aliases
      aliasesMap[title.toLowerCase()] = relPath;
      if (parsed?.frontmatter?.id) {
        aliasesMap[parsed.frontmatter.id.toLowerCase()] = relPath;
      }
      if (parsed?.frontmatter?.aliases && Array.isArray(parsed.frontmatter.aliases)) {
        for (const alias of parsed.frontmatter.aliases) {
          aliasesMap[alias.toLowerCase().trim()] = relPath;
        }
      }
    }
    indexContent += `\n`;
  }

  // Write index.md
  fs.writeFileSync(path.join(brainDir, 'index.md'), indexContent, 'utf-8');
  console.log(`✅ Generated index.md with ${totalCount} indexed entities.`);

  // Write aliases.json
  fs.writeFileSync(path.join(brainDir, 'aliases.json'), JSON.stringify(aliasesMap, null, 2), 'utf-8');
  console.log(`✅ Generated aliases.json with ${Object.keys(aliasesMap).length} alias entries.`);
}

buildIndex();
