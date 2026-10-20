import fs from 'node:fs';
import path from 'node:path';
import { spawnSync } from 'node:child_process';
const repository = path.resolve(import.meta.dirname, '../..');
const target = path.join(repository, '.agent-native-fixture/holdout-skills');
fs.mkdirSync(target, { recursive: true });
for (const entry of fs.readdirSync(path.join(repository, 'skills'), { withFileTypes: true })) {
  const source = path.join(repository, 'skills', entry.name, 'SKILL.md');
  if (!entry.isDirectory() || !fs.existsSync(source)) continue;
  fs.mkdirSync(path.join(target, entry.name), { recursive: true }); fs.copyFileSync(source, path.join(target, entry.name, 'SKILL.md'));
}
const dataset = path.join(target, 'agent-native/evals'); fs.mkdirSync(dataset, { recursive: true });
fs.copyFileSync(process.argv[3] ?? path.join(import.meta.dirname, 'holdout-queries.json'), path.join(dataset, 'eval_queries.json'));
const result = spawnSync('python3', ['maintenance/eval_skills.py', '--skills-dir', target, 'run', '--skill', 'agent-native', '--judge', 'live', '--out', process.argv[2] ?? 'maintenance/evals-out/agent-native-holdout'], { cwd: repository, stdio: 'inherit' });
process.exitCode = result.status ?? 1;
