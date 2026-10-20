import fs from 'node:fs';
import path from 'node:path';
import { spawnSync } from 'node:child_process';
import { createHash } from 'node:crypto';
const repository = path.resolve(import.meta.dirname, '../..');
const laboratory = path.join(repository, '.agent-native-fixture');
const run = (command, args, cwd) => {
  const result = spawnSync(command, args, { cwd, stdio: 'inherit', env: { ...process.env, NODE_ENV: 'development' } });
  if (result.status !== 0) throw new Error(`${command} exited ${result.status}`);
};
fs.mkdirSync(laboratory, { recursive: true });
if (fs.existsSync(path.join(laboratory, 'pristine'))) throw new Error('O laboratório já existe. Preserve-o e escolha outro checkout para reproduzir.');
run('bunx', ['--package', '@agent-native/core@0.209.2', 'agent-native', 'create', 'pristine', '--template', 'chat', '--standalone'], laboratory);
const pristine = path.join(laboratory, 'pristine');
fs.copyFileSync(path.join(import.meta.dirname, 'implementations/pnpm-lock.yaml'), path.join(pristine, 'pnpm-lock.yaml'));
run('pnpm', ['install', '--frozen-lockfile'], pristine);
for (const check of ['typecheck', 'test', 'build', 'agent-native:doctor']) run('pnpm', [check], pristine);
for (const variant of ['control', 'candidate']) {
  const target = path.join(laboratory, variant);
  fs.cpSync(pristine, target, { recursive: true, filter: source => !['node_modules', 'data', '.output', '.react-router', '.generated', '.agent-native'].includes(path.basename(source)) });
  if (variant === 'candidate') fs.cpSync(path.join(repository, 'skills/agent-native'), path.join(target, '.agents/skills/agent-native'), { recursive: true });
  const snapshot = JSON.parse(fs.readFileSync(path.join(import.meta.dirname, `implementations/${variant}.json`), 'utf8'));
  for (const change of snapshot.changes) {
    const destination = path.resolve(target, change.path);
    if (!destination.startsWith(target + path.sep)) throw new Error('Caminho de snapshot inválido.');
    const actual = fs.existsSync(destination) ? createHash('sha256').update(fs.readFileSync(destination)).digest('hex') : null;
    if (actual !== change.beforeSha256) throw new Error(`Scaffold divergiu: ${change.path}`);
    fs.mkdirSync(path.dirname(destination), { recursive: true }); fs.writeFileSync(destination, change.content);
  }
  run('pnpm', ['install', '--frozen-lockfile'], target);
  for (const check of ['typecheck', 'test', 'build', 'agent-native:doctor']) run('pnpm', [check], target);
}
const harness = path.join(laboratory, 'harness');
fs.mkdirSync(harness, { recursive: true }); fs.copyFileSync(path.join(import.meta.dirname, 'package.json'), path.join(harness, 'package.json'));
run('bun', ['install'], harness);
run('node', ['node_modules/playwright/cli.js', 'install', 'chromium'], harness);
const link = path.join(import.meta.dirname, 'node_modules');
if (!fs.existsSync(link)) fs.symlinkSync(path.join(harness, 'node_modules'), link, 'dir');
