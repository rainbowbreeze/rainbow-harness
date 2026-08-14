import fs from 'fs';
import path from 'path';
import { fileURLToPath } from 'url';

const __filename = fileURLToPath(import.meta.url);
const __dirname = path.dirname(__filename);
export const workspaceRoot = path.resolve(__dirname, '..');

export function getBrainDir() {
  let brainDir = '';

  // 1. Check environment variable
  if (process.env.BRAIN_PATH) {
    brainDir = path.resolve(process.env.BRAIN_PATH);
  } 
  // 2. Check .brainpath file in workspace root
  else {
    const dotPath = path.join(workspaceRoot, '.brainpath');
    if (fs.existsSync(dotPath)) {
      const customPath = fs.readFileSync(dotPath, 'utf-8').trim();
      if (customPath) {
        brainDir = path.resolve(workspaceRoot, customPath);
      }
    }
  }

  // 3. Fallback to default ./BRAIN
  if (!brainDir) {
    brainDir = path.join(workspaceRoot, 'BRAIN');
  }

  // Invariant Guard: BRAIN_PATH must NEVER equal WORKSPACE_ROOT
  if (path.resolve(brainDir) === path.resolve(workspaceRoot)) {
    console.error(`\n❌ Configuration Error: BRAIN_PATH (${brainDir}) cannot be equal to WORKSPACE_ROOT (${workspaceRoot}).`);
    console.error(`Knowledge base data must live in a dedicated subfolder (e.g. ./BRAIN) or an external directory.\n`);
    process.exit(1);
  }

  if (!fs.existsSync(brainDir)) {
    console.error(`\n❌ Error: Brain directory does not exist at: ${brainDir}`);
    console.error(`Please create the directory or run: mkdir -p "${brainDir}"\n`);
    process.exit(1);
  }

  return brainDir;
}
