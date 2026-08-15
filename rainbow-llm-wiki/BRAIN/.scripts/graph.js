#!/usr/bin/env node

import fs from 'fs';
import path from 'path';
import { getBrainDir } from './resolve-brain.js';

const brainDir = getBrainDir();

const MECE_DIRS = [
  'people',
  'companies',
  'schools',
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

function buildGraph() {
  console.log(`🕸️  Extracting Relationship Graph & Backlinks from: ${brainDir}\n`);

  const nodes = new Map();
  const edges = [];
  const edgeSet = new Set();

  const allFiles = [];
  for (const dir of MECE_DIRS) {
    allFiles.push(...getAllMarkdownFiles(path.join(brainDir, dir)));
  }

  for (const file of allFiles) {
    const relPath = path.relative(brainDir, file);
    nodes.set(relPath, { inDegree: 0, outDegree: 0, links: new Set(), backlinks: new Set() });
  }

  const linkRegex = /\[([^\]]+)\]\(([^)]+)\)/g;

  for (const file of allFiles) {
    const sourceRel = path.relative(brainDir, file);
    const content = fs.readFileSync(file, 'utf-8');
    let match;

    while ((match = linkRegex.exec(content)) !== null) {
      const targetUrl = match[2];
      if (targetUrl.startsWith('http') || targetUrl.startsWith('#') || targetUrl.startsWith('mailto:')) continue;

      const targetClean = targetUrl.split('#')[0];
      const targetAbs = path.resolve(path.dirname(file), targetClean);
      const targetRel = path.relative(brainDir, targetAbs);

      if (nodes.has(targetRel) && targetRel !== sourceRel) {
        const edgeKey = `${sourceRel} -> ${targetRel}`;
        if (!edgeSet.has(edgeKey)) {
          edgeSet.add(edgeKey);
          edges.push({ source: sourceRel, target: targetRel, text: match[1] });
        }
        nodes.get(sourceRel).links.add(targetRel);
        nodes.get(targetRel).backlinks.add(sourceRel);
      }
    }
  }

  for (const [nodePath, stats] of nodes.entries()) {
    stats.inDegree = stats.backlinks.size;
    stats.outDegree = stats.links.size;
  }

  console.log(`Knowledge Graph Summary:`);
  console.log(`- Nodes (Entities): ${nodes.size}`);
  console.log(`- Unique Edges: ${edges.length}\n`);

  if (nodes.size > 0) {
    console.log(`Top Connected Entities (by incoming backlinks):`);
    const sortedNodes = Array.from(nodes.entries()).sort((a, b) => b[1].inDegree - a[1].inDegree);
    for (const [nodePath, stats] of sortedNodes.slice(0, 10)) {
      console.log(`  - [${nodePath}] : ${stats.inDegree} backlinks, ${stats.outDegree} outbound links`);
    }
  }

  // Generate Mermaid Diagram
  let mermaid = '```mermaid\ngraph TD\n';
  for (const edge of edges) {
    const sName = path.basename(edge.source, '.md');
    const tName = path.basename(edge.target, '.md');
    mermaid += `    ${sName.replace(/[^a-zA-Z0-9]/g, '_')} --> ${tName.replace(/[^a-zA-Z0-9]/g, '_')}\n`;
  }
  mermaid += '```\n';

  fs.writeFileSync(path.join(brainDir, 'graph.md'), `# Relationship Graph\n\n> Auto-generated relationship graph.\n\n${edges.length > 0 ? mermaid : '*No cross-links present yet.*'}\n`, 'utf-8');
  console.log(`\n✅ Generated graph.md in ${brainDir}`);
}

buildGraph();
