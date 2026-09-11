import fs from 'fs';
import path from 'path';
import { fileURLToPath } from 'url';

const __filename = fileURLToPath(import.meta.url);
const __dirname = path.dirname(__filename);

export function getBrainDir() {
  // If running from inside BRAIN/.scripts, the parent directory is BRAIN/
  let brainDir = path.resolve(__dirname, '..');

  // Check if __dirname is .scripts inside brainDir
  if (path.basename(__dirname) === '.scripts') {
    return brainDir;
  }

  // Otherwise fallback to environment variables or root workspace
  if (process.env.BRAIN_PATH) {
    brainDir = path.resolve(process.env.BRAIN_PATH);
  } else {
    const rootDir = path.resolve(__dirname, '..');
    const dotPath = path.join(rootDir, '.brainpath');
    if (fs.existsSync(dotPath)) {
      brainDir = path.resolve(rootDir, fs.readFileSync(dotPath, 'utf-8').trim());
    } else {
      brainDir = path.join(rootDir, 'BRAIN');
    }
  }

  if (!fs.existsSync(brainDir)) {
    console.error(`\n❌ Error: Brain directory does not exist at: ${brainDir}\n`);
    process.exit(1);
  }

  return brainDir;
}
