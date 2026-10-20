import { test, expect, type BrowserContext, type Page, type APIRequestContext } from '@playwright/test';
import { randomUUID } from 'node:crypto';
import { mkdir, writeFile } from 'node:fs/promises';

interface Task { id: string; title: string; completed: boolean }
const baseURL = process.env.LAB_URL ?? 'http://localhost:4311';
const variant = process.env.LAB_VARIANT ?? 'candidate';
const evidence = new URL('../../../.agent-native-fixture/evidence/', import.meta.url);
const password = 'Local-fixture-password-2026!';
const actions = '/_agent-native/actions/';

test.beforeAll(async ({ request }) => {
  await expect.poll(async () => {
    try { return (await request.get('/_agent-native/auth/session', { timeout: 5000 })).status(); }
    catch { return 0; }
  }, { timeout: 60_000 }).toBe(200);
});

async function login(request: APIRequestContext, email: string, register = true) {
  if (register) expect((await request.post('/_agent-native/auth/register', { data: { email, password } })).status()).toBe(200);
  expect((await request.post('/_agent-native/auth/login', { data: { email, password } })).status()).toBe(200);
}
async function account(context: BrowserContext) {
  const email = `lab-${randomUUID()}@example.com`;
  await login(context.request, email);
  return email;
}
async function create(request: APIRequestContext, title: string): Promise<Task> {
  const response = await request.post(actions + 'create-task', { data: { title } });
  expect(response.status()).toBe(200);
  return response.json() as Promise<Task>;
}
async function list(request: APIRequestContext): Promise<Task[]> {
  const response = await request.get(actions + 'list-tasks');
  expect(response.status()).toBe(200);
  return response.json() as Promise<Task[]>;
}
async function complete(request: APIRequestContext, id: string) {
  return request.post(actions + 'complete-task', { data: variant === 'control' ? { id, completed: true } : { id } });
}
function captureTab(page: Page) {
  let tabId = '';
  page.on('request', request => { const id = request.headers()['x-agent-native-browser-tab']; if (id) tabId = id; });
  return () => tabId;
}
async function state(request: APIRequestContext, key: string, tabId: string): Promise<unknown> {
  const response = await request.get('/_agent-native/application-state/' + encodeURIComponent(tabId ? `${key}:${tabId}` : key), { headers: { 'X-Agent-Native-Browser-Tab': tabId } });
  if (response.status() === 404) return null;
  expect(response.status()).toBe(200);
  const body = await response.text();
  return body ? JSON.parse(body) as unknown : null;
}
interface AgentEvent { type: string; tool?: string; input?: Record<string, unknown>; result?: string }
async function chat(request: APIRequestContext, message: string, tabId: string, label: string, threadId = randomUUID()) {
  const response = await request.post('/_agent-native/agent-chat', {
    headers: { 'X-Agent-Native-Browser-Tab': tabId },
    data: { message, browserTabId: tabId, threadId, engine: 'ai-sdk:openrouter', model: 'google/gemini-3.5-flash-lite', effort: 'low' }, timeout: 110_000,
  });
  const body = await response.text();
  await mkdir(evidence, { recursive: true });
  await writeFile(new URL(`${variant}-${process.env.LAB_RUN ?? 'final'}-${label}.sse`, evidence), body);
  expect(response.status(), body.slice(0, 1000)).toBe(200);
  const events = body.split('\n').filter(line => line.startsWith('data: ')).map(line => JSON.parse(line.slice(6)) as AgentEvent);
  expect(events.some(event => event.type === 'done')).toBe(true);
  return { body, threadId, events };
}

test('actions: validation, persistence, anonymous and cross-owner boundaries', async ({ browser, context, request }) => {
  await account(context);
  const other = await browser.newContext({ baseURL });
  await account(other);
  expect((await request.get(actions + 'list-tasks')).status()).toBe(401);
  expect((await request.post(actions + 'create-task', { data: { title: 'anonymous' } })).status()).toBe(401);
  const invalid = await context.request.post(actions + 'create-task', { data: { title: '   ' } });
  expect(invalid.status()).toBe(400);
  const task = await create(context.request, 'Private persisted task');
  expect(await list(context.request)).toContainEqual(expect.objectContaining({ id: task.id, completed: false }));
  expect(await list(other.request)).toEqual([]);
  expect((await complete(other.request, task.id)).status()).toBe(404);
  expect((await complete(context.request, task.id)).status()).toBe(200);
  expect(await list(context.request)).toContainEqual(expect.objectContaining({ id: task.id, completed: true }));
  const spoof = await context.request.post(actions + 'create-task', { data: { title: 'Spoof ownership', ownerEmail: 'foreign@example.com' } });
  expect([200, 400]).toContain(spoof.status());
  expect(await list(other.request)).toEqual([]);
  await other.close();
});

test('UI: loading, empty, create by keyboard, complete, failure without success', async ({ page, context }) => {
  await account(context);
  const tab = captureTab(page);
  let releaseRead: () => void = () => {};
  const pendingRead = new Promise<void>(resolve => { releaseRead = resolve; });
  await page.route('**/_agent-native/actions/list-tasks*', async route => { await pendingRead; await route.continue(); });
  await page.goto('/tasks');
  try { await expect(page.getByText(/Carregando tarefas/)).toBeVisible(); }
  finally { releaseRead(); }
  await expect(page.getByText(/Você ainda não tem tarefas/)).toBeVisible();
  await expect.poll(tab).not.toBe('');
  await expect.poll(() => state(context.request, 'navigation', tab())).toMatchObject({ view: 'tasks' });
  await page.locator('#task-title').fill('Keyboard task');
  await expect(page.getByRole('button', { name: 'Criar Tarefa', exact: true })).toBeEnabled();
  await page.locator('#task-title').press('Enter');
  await expect(page.getByRole('status').filter({ hasText: 'Tarefa criada.' })).toBeVisible();
  await expect(page.getByRole('heading', { name: 'Keyboard task' })).toBeFocused();
  await page.getByLabel('Concluir Keyboard task', { exact: true }).click();
  await expect(page.getByRole('status').filter({ hasText: 'Tarefa concluída.' })).toBeVisible();
  expect((await list(context.request)).find(task => task.title === 'Keyboard task')?.completed).toBe(true);
  await page.route('**/_agent-native/actions/create-task', route => route.fulfill({ status: 500, contentType: 'application/json', body: JSON.stringify({ error: 'Falha de teste', statusMessage: 'Falha de teste' }) }));
  await page.locator('#task-title').fill('Must not persist');
  await page.getByRole('button', { name: 'Criar Tarefa', exact: true }).click();
  await expect(page.getByRole('alert')).toBeVisible();
  await expect(page.getByRole('status').filter({ hasText: 'Tarefa criada.' })).toHaveCount(0);
  expect((await list(context.request)).some(task => task.title === 'Must not persist')).toBe(false);
});

test('UI: list error is recoverable', async ({ page, context }) => {
  await account(context);
  await page.route('**/_agent-native/actions/list-tasks*', route => route.fulfill({ status: 500, contentType: 'application/json', body: '{"error":"Falha de leitura"}' }));
  await page.goto('/tasks');
  await expect(page.getByRole('button', { name: 'Tentar Novamente' })).toBeVisible();
  await page.unroute('**/_agent-native/actions/list-tasks*');
  try { await page.getByRole('button', { name: 'Tentar Novamente' }).click({ timeout: 3000 }); }
  catch { await expect(page.getByText(/Você ainda não tem tarefas/)).toBeVisible(); }
  await expect(page.getByText(/Você ainda não tem tarefas/)).toBeVisible();
});

test('sync: same owner in a second authenticated session', async ({ browser, context, page }) => {
  const email = await account(context);
  const other = await browser.newContext({ baseURL });
  await login(other.request, email, false);
  const second = await other.newPage();
  await page.goto('/tasks'); await second.goto('/tasks');
  await expect(second.getByText(/Você ainda não tem tarefas/)).toBeVisible();
  await page.locator('#task-title').fill('Cross-session task');
  await page.getByRole('button', { name: 'Criar Tarefa', exact: true }).click();
  await expect(second.getByText('Cross-session task', { exact: true })).toBeVisible({ timeout: 75_000 });
  const task = (await list(context.request)).find(task => task.title === 'Cross-session task')!;
  expect((await complete(other.request, task.id)).status()).toBe(200);
  await expect(page.getByRole('region', { name: 'Tarefa Aberta' }).or(page.getByRole('article', { name: 'Tarefa Aberta' })).getByText('Concluída')).toBeVisible({ timeout: 75_000 });
  await other.close();
});

test('context: selected task is published and removed after route change', async ({ page, context }) => {
  await account(context); const tab = captureTab(page);
  const task = await create(context.request, 'Context task');
  await page.goto(`/tasks?${variant === 'control' ? 'taskId' : 'id'}=${task.id}`);
  await expect(page.getByRole('heading', { name: 'Context task' })).toBeVisible();
  await expect.poll(tab).not.toBe('');
  await expect.poll(() => state(context.request, 'selection', tab())).toMatchObject({ id: task.id });
  await page.getByRole('link', { name: /Get started|Primeiros Passos|Início|Home/i }).first().click();
  await expect(page).toHaveURL(/\/home$/);
  await expect.poll(() => state(context.request, 'selection', tab())).toBeNull();
});

test('interaction: narrow screen and keyboard retain usable controls', async ({ page, context }) => {
  await account(context); await page.setViewportSize({ width: 390, height: 844 });
  await page.goto('/tasks'); await page.locator('#task-title').fill('Narrow task');
  await expect(page.getByRole('button', { name: 'Criar Tarefa', exact: true })).toBeEnabled();
  await page.locator('#task-title').press('Tab');
  await expect(page.getByRole('button', { name: 'Criar Tarefa', exact: true })).toBeFocused();
  await page.keyboard.press('Enter');
  await expect(page.getByRole('heading', { name: 'Narrow task' })).toBeVisible();
  expect(await page.evaluate(() => document.documentElement.scrollWidth <= window.innerWidth)).toBe(true);
  await page.screenshot({ path: new URL(`${variant}-narrow.png`, evidence).pathname, fullPage: true });
});

test('real OpenRouter agent: create, navigate once, context, complete, chat continuity', async ({ page, context }) => {
  test.skip(!process.env.OPENROUTER_API_KEY, 'Credencial OpenRouter ausente');
  await account(context); const tab = captureTab(page);
  const navigationTrace: Array<Record<string, unknown>> = [];
  page.on('request', request => { if (request.url().includes('/application-state') && /navigate|navigation/.test(request.url())) navigationTrace.push({ kind: 'request', method: request.method(), url: request.url(), data: request.postData() }); });
  page.on('response', response => { if (response.url().includes('/application-state') && response.url().includes('navigate')) void response.text().then(body => navigationTrace.push({ kind: 'response', url: response.url(), body })).catch(() => {}); });
  page.on('framenavigated', frame => { if (frame === page.mainFrame()) navigationTrace.push({ kind: 'navigation', url: frame.url() }); });
  page.on('console', message => { if (message.type() === 'error') navigationTrace.push({ kind: 'console', text: message.text() }); });
  await page.goto('/tasks'); await expect(page.locator('#task-title')).toBeVisible();
  await page.bringToFront();
  await expect.poll(tab).not.toBe('');
  await expect.poll(() => state(context.request, 'navigation', tab())).toMatchObject({ view: 'tasks' });
  const title = `Real agent ${randomUUID()}`;
  let transitions = 0;
  let previousUrl = page.url();
  page.on('framenavigated', frame => {
    if (frame !== page.mainFrame() || frame.url() === previousUrl) return;
    previousUrl = frame.url();
    if (frame.url().includes('/tasks?')) transitions++;
  });
  const creation = await chat(context.request, `Create exactly one private task titled "${title}" using create-task, then use navigate to open it. Do not write code.`, tab(), 'agent-create');
  expect(creation.events.filter(event => event.type === 'tool_start' && event.tool === 'create-task')).toHaveLength(1);
  expect(creation.events.filter(event => event.type === 'tool_start' && event.tool === 'navigate')).toHaveLength(1);
  await writeFile(new URL(`${variant}-${process.env.LAB_RUN ?? 'final'}-navigation-before.json`, evidence), JSON.stringify({ tabId: tab(), url: page.url(), navigation: await state(context.request, 'navigation', tab()), command: await state(context.request, 'navigate', tab()) }, null, 2));
  try { await expect(page.getByRole('heading', { name: title })).toBeVisible({ timeout: 35_000 }); }
  finally { await writeFile(new URL(`${variant}-${process.env.LAB_RUN ?? 'final'}-navigation-after.json`, evidence), JSON.stringify({ tabId: tab(), url: page.url(), navigation: await state(context.request, 'navigation', tab()), command: await state(context.request, 'navigate', tab()), globalCommand: await state(context.request, 'navigate', ''), trace: navigationTrace }, null, 2)); }
  const rows = (await list(context.request)).filter(task => task.title === title);
  expect(rows).toHaveLength(1); expect(transitions).toBe(1);
  expect(navigationTrace.filter(event => event.kind === 'request' && event.method === 'DELETE' && String(event.url).includes('/navigate:'))).toHaveLength(1);
  const read = await chat(context.request, 'Call view-screen, identify the currently open task by id and title, then complete that task using complete-task. Do not navigate.', tab(), 'agent-complete', creation.threadId);
  expect(read.body).toContain(rows[0].id); expect(read.body).toContain('view-screen'); expect(read.body).toContain('complete-task');
  expect((await list(context.request)).find(task => task.id === rows[0].id)?.completed).toBe(true);
  await expect(page.getByRole('region', { name: 'Tarefa Aberta' }).or(page.getByRole('article', { name: 'Tarefa Aberta' })).getByText('Concluída')).toBeVisible({ timeout: 75_000 });
  await page.goto(`/chat/${creation.threadId}`);
  await expect(page.locator('[contenteditable="true"], textarea').first()).toBeVisible();
  await expect(page.getByText(title, { exact: false }).first()).toBeVisible();
  const threads = await context.request.get('/_agent-native/agent-chat/threads');
  expect(threads.status()).toBe(200);
  expect(await threads.text()).toContain(creation.threadId);
});
