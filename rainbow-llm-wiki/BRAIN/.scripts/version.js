#!/usr/bin/env node

/**
 * @file version.js
 * @description Zero-dependency version tracking and update checker utility for the Rainbow LLM Wiki.
 * Reads the installed version from BRAIN/.version and workspace package.json,
 * and optionally probes upstream GitHub to verify if a newer release exists.
 */

import fs from 'fs';
import path from 'path';
import https from 'https';
import { getBrainDir } from './resolve-brain.js';

// Resolve the brain data directory (Data Plane) and workspace root (Execution Plane)
const brainDir = getBrainDir();
const workspaceRoot = path.resolve(brainDir, '..');

/**
 * Parses a Semantic Versioning (SemVer) string into [major, minor, patch, preRelease].
 * @param {string} versionStr - e.g. "1.1.0", "v1.2.0-beta.1"
 * @returns {{ major: number, minor: number, patch: number, preRelease: string, valid: boolean }}
 */
export function parseSemver(versionStr) {
  try {
    if (!versionStr || typeof versionStr !== 'string') {
      return { major: 0, minor: 0, patch: 0, preRelease: '', valid: false };
    }
    const cleanStr = versionStr.trim().replace(/^v/, '');
    const [core, preRelease = ''] = cleanStr.split('-');
    const parts = core.split('.').map(p => parseInt(p, 10));

    if (parts.length < 1 || isNaN(parts[0])) {
      return { major: 0, minor: 0, patch: 0, preRelease: '', valid: false };
    }

    return {
      major: parts[0] || 0,
      minor: parts[1] || 0,
      patch: parts[2] || 0,
      preRelease,
      valid: true
    };
  } catch (err) {
    return { major: 0, minor: 0, patch: 0, preRelease: '', valid: false };
  }
}

/**
 * Compares two SemVer version strings.
 * @param {string} v1 - First version (e.g. upstream version)
 * @param {string} v2 - Second version (e.g. installed version)
 * @returns {number} 1 if v1 > v2, -1 if v1 < v2, 0 if v1 === v2
 */
export function compareSemver(v1, v2) {
  const p1 = parseSemver(v1);
  const p2 = parseSemver(v2);

  // Compare major
  if (p1.major !== p2.major) return p1.major > p2.major ? 1 : -1;
  // Compare minor
  if (p1.minor !== p2.minor) return p1.minor > p2.minor ? 1 : -1;
  // Compare patch
  if (p1.patch !== p2.patch) return p1.patch > p2.patch ? 1 : -1;

  // Pre-release handling: absence of pre-release means higher precedence than presence
  if (p1.preRelease === '' && p2.preRelease !== '') return 1;
  if (p1.preRelease !== '' && p2.preRelease === '') return -1;
  if (p1.preRelease !== p2.preRelease) {
    return p1.preRelease.localeCompare(p2.preRelease);
  }

  return 0;
}

/**
 * Reads local installed version information from BRAIN/.version and package.json.
 * @returns {object} Object containing installed version and metadata
 */
export function getInstalledVersion() {
  const result = {
    version: '0.0.0',
    isLegacy: false,
    installedAt: null,
    upstream: 'rainbowbreeze/rainbow-harness',
    ref: 'main',
    source: 'unknown'
  };

  try {
    // 1. Try reading from BRAIN/.version (Primary Data Plane marker)
    const versionFilePath = path.join(brainDir, '.version');
    if (fs.existsSync(versionFilePath)) {
      const rawContent = fs.readFileSync(versionFilePath, 'utf-8');
      const parsed = JSON.parse(rawContent);
      if (parsed.version) {
        result.version = parsed.version;
        result.installedAt = parsed.installed_at || null;
        result.upstream = parsed.upstream || result.upstream;
        result.ref = parsed.ref || result.ref;
        result.source = 'BRAIN/.version';
        return result;
      }
    }
  } catch (err) {
    console.warn(`⚠️ Warning reading ${path.join(brainDir, '.version')}:`, err.message);
  }

  try {
    // 2. Fallback: check workspace package.json
    const packageJsonPath = path.join(workspaceRoot, 'package.json');
    if (fs.existsSync(packageJsonPath)) {
      const rawContent = fs.readFileSync(packageJsonPath, 'utf-8');
      const parsed = JSON.parse(rawContent);
      if (parsed.version) {
        result.version = parsed.version;
        result.source = 'package.json';
        result.isLegacy = true;
        return result;
      }
    }
  } catch (err) {
    console.warn(`⚠️ Warning reading ${path.join(workspaceRoot, 'package.json')}:`, err.message);
  }

  // 3. Unversioned legacy install
  result.isLegacy = true;
  return result;
}

/**
 * Fetches remote version metadata from GitHub raw URL without external dependencies.
 * @param {string} upstream - "owner/repo" (default: "rainbowbreeze/rainbow-harness")
 * @param {string} branch - branch name (default: "main")
 * @returns {Promise<object>}
 */
export function fetchUpstreamVersion(upstream = 'rainbowbreeze/rainbow-harness', branch = 'main') {
  return new Promise((resolve) => {
    // Target upstream package.json for version retrieval
    const url = `https://raw.githubusercontent.com/${upstream}/${branch}/rainbow-llm-wiki/package.json`;

    const request = https.get(url, { headers: { 'User-Agent': 'Rainbow-LLM-Wiki-Agent' } }, (res) => {
      if (res.statusCode < 200 || res.statusCode >= 300) {
        resolve({
          success: false,
          error: `HTTP ${res.statusCode}: ${res.statusMessage}`,
          version: null
        });
        return;
      }

      let data = '';
      res.on('data', (chunk) => { data += chunk; });
      res.on('end', () => {
        try {
          const parsed = JSON.parse(data);
          resolve({
            success: true,
            version: parsed.version || '0.0.0',
            error: null
          });
        } catch (err) {
          resolve({
            success: false,
            error: `Failed to parse upstream response JSON: ${err.message}`,
            version: null
          });
        }
      });
    });

    request.on('error', (err) => {
      resolve({
        success: false,
        error: `Network error querying upstream: ${err.message}`,
        version: null
      });
    });

    // Set 5-second timeout for the probe request
    request.setTimeout(5000, () => {
      request.destroy();
      resolve({
        success: false,
        error: 'Connection timeout connecting to GitHub',
        version: null
      });
    });
  });
}

/**
 * Main CLI entry point.
 */
async function main() {
  const args = process.argv.slice(2);
  const jsonOutput = args.includes('--json');
  const checkRemote = args.includes('--check') || args.includes('-c') || args.length === 0;

  const installed = getInstalledVersion();
  let upstream = null;
  let comparison = null;
  let statusMessage = 'Current installed version inspected.';

  if (checkRemote) {
    upstream = await fetchUpstreamVersion(installed.upstream, installed.ref);
    if (upstream.success && upstream.version) {
      const cmp = compareSemver(upstream.version, installed.version);
      if (cmp > 0) {
        comparison = 'UPDATE_AVAILABLE';
        statusMessage = `Update available: v${installed.version} -> v${upstream.version}`;
      } else if (cmp === 0) {
        comparison = 'UP_TO_DATE';
        statusMessage = `Knowledge base is up to date (v${installed.version}).`;
      } else {
        comparison = 'AHEAD_OF_UPSTREAM';
        statusMessage = `Local version (v${installed.version}) is newer than upstream (v${upstream.version}).`;
      }
    } else {
      statusMessage = `Could not verify upstream version: ${upstream?.error || 'Unknown error'}`;
    }
  }

  if (jsonOutput) {
    console.log(JSON.stringify({
      installed: {
        version: installed.version,
        installedAt: installed.installedAt,
        isLegacy: installed.isLegacy,
        source: installed.source
      },
      upstream: upstream ? {
        version: upstream.version,
        success: upstream.success,
        error: upstream.error
      } : null,
      comparison,
      statusMessage
    }, null, 2));
    return;
  }

  // Human-readable formatted output
  console.log('📦 Rainbow LLM Wiki Version Inspector\n');
  console.log(`- Installed Version : v${installed.version} (${installed.source})`);
  if (installed.installedAt) {
    console.log(`- Installed At      : ${installed.installedAt}`);
  }
  if (installed.isLegacy) {
    console.log(`- Status            : Legacy / Unversioned installation`);
  }

  if (upstream) {
    if (upstream.success) {
      console.log(`- Upstream Version  : v${upstream.version} (github.com/${installed.upstream})`);
      console.log(`\n📋 Status: ${statusMessage}`);
    } else {
      console.log(`- Upstream Probe    : ⚠️ ${upstream.error}`);
    }
  }
}

// Execute CLI when called directly
if (process.argv[1] && path.resolve(process.argv[1]) === path.resolve(new URL(import.meta.url).pathname)) {
  main().catch(err => {
    console.error('Error executing version script:', err);
    process.exit(1);
  });
}
