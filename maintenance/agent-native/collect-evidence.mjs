import fs from 'node:fs';
import path from 'node:path';
const repository = path.resolve(import.meta.dirname, '../..');
const fixture = path.join(repository, '.agent-native-fixture');
const output = path.join(import.meta.dirname, 'evidence');
const key = process.env.OPENROUTER_API_KEY;
function redact(text) {
  let safe = text.replace(/\u001b\[[0-9;?]*[a-zA-Z]/g, '');
  if (key) safe = safe.replaceAll(key, '[REDACTED]');
  safe = safe.replace(/an_session_[a-zA-Z0-9_-]+=[^;\s"\\]+/g, 'test_session=[REDACTED]');
  return safe.replaceAll(repository + '/', '<repository>/');
}
fs.mkdirSync(output, { recursive: true });
for (const name of fs.readdirSync(fixture)) {
  if (!/^(baseline|candidate|control|graphify)-.*\.log$/.test(name)) continue;
  fs.writeFileSync(path.join(output, name), redact(fs.readFileSync(path.join(fixture, name), 'utf8')));
}
for (const name of fs.readdirSync(path.join(fixture, 'evidence'))) {
  if (!/\.(json|sse|md|png|html)$/.test(name)) continue;
  const source = path.join(fixture, 'evidence', name);
  if (name.endsWith('.png')) fs.copyFileSync(source, path.join(output, name));
  else fs.writeFileSync(path.join(output, name), redact(fs.readFileSync(source, 'utf8')));
}
for (const [source, name] of [['agent-native-real-app-final-v2', 'activation-original-v2'], ['agent-native-real-app-holdout-v2', 'activation-holdout-v2'], ['agent-native-real-app-final-v3', 'activation-original-v3'], ['agent-native-real-app-holdout-v3', 'activation-holdout-v3'], ['agent-native-real-app-blind-final', 'activation-blind-final'], ['agent-native-real-app-holdout', 'activation-holdout-single-catalog-diagnostic']]) {
  const original = path.join(repository, 'maintenance/evals-out', source);
  if (fs.existsSync(original)) fs.cpSync(original, path.join(output, name), { recursive: true });
}
let secretFound = false;
function check(directory) {
  for (const entry of fs.readdirSync(directory, { withFileTypes: true })) {
    const file = path.join(directory, entry.name);
    if (entry.isDirectory()) check(file);
    else if (entry.isFile() && key && fs.readFileSync(file).includes(key)) secretFound = true;
  }
}
check(import.meta.dirname);
if (secretFound) throw new Error('Provider credential found in artifacts.');
console.log('Evidence collected; provider credential absent.');
