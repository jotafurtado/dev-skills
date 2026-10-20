import fs from 'node:fs';
import path from 'node:path';
import { createHash } from 'node:crypto';
const repository = path.resolve(import.meta.dirname, '../..');
const root = path.join(repository, '.agent-native-fixture');
const output = path.join(import.meta.dirname, 'implementations');
const ignored = new Set(['node_modules', 'data', '.output', '.nitro', '.vite', '.react-router', '.generated', '.agent-native', '.agents', '.claude', '.git', 'pnpm-lock.yaml']);
function files(directory, prefix = '') {
  return fs.readdirSync(directory, { withFileTypes: true }).flatMap(entry => {
    if (ignored.has(entry.name) || entry.name.startsWith('.env')) return [];
    const relative = path.join(prefix, entry.name);
    return entry.isDirectory() ? files(path.join(directory, entry.name), relative) : entry.isFile() ? [relative] : [];
  });
}
fs.mkdirSync(output, { recursive: true });
const hash = content => createHash('sha256').update(content).digest('hex');
for (const variant of ['control', 'candidate']) {
  const changes = [];
  for (const relative of files(path.join(root, variant))) {
    const actual = fs.readFileSync(path.join(root, variant, relative), 'utf8');
    const source = path.join(root, 'pristine', relative);
    const before = fs.existsSync(source) ? fs.readFileSync(source, 'utf8') : null;
    if (before !== actual) changes.push({ path: relative, beforeSha256: before === null ? null : hash(before), content: actual });
  }
  fs.writeFileSync(path.join(output, `${variant}.json`), JSON.stringify({ scaffold: '@agent-native/core@0.209.2 chat standalone', changes }, null, 2) + '\n');
}
fs.copyFileSync(path.join(root, 'pristine/pnpm-lock.yaml'), path.join(output, 'pnpm-lock.yaml'));
