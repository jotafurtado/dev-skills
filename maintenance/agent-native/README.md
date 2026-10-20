# Laboratório real da skill Agent-Native

Este laboratório compara duas implementações independentes do mesmo pedido no
scaffold oficial Chat standalone. Ambas recebem as skills oficiais. Apenas a
candidata recebe `skills/agent-native`. Não há deploy ou commit automático.

`report.md` registra a matriz, resultados e limitações. `evidence/` conserva
versões, respostas, avaliações e resultados selecionados sem credenciais.
`implementations/` conserva o delta completo de cada implementação, com hash do
arquivo original, e o lockfile resolvido. O app, banco, dependências e artefatos
brutos ficam em `.agent-native-fixture/`, ignorado pelo Git.

## Preparação reproduzível

Pré-requisitos desta execução: Node 24.22.0, Bun 1.4.2 e pnpm 10.29.1. O próprio
scaffold declara Node >=22.22.0. Não confundir o requisito com a versão testada.

Em checkout sem `.agent-native-fixture/`:

```sh
node maintenance/agent-native/prepare.mjs
```

O script cria o scaffold com o CLI publicado `@agent-native/core@0.209.2`, usa o
lockfile congelado, verifica a linha de base, aplica os deltas com checagem de
hash e executa typecheck, testes, build e doctor em sequência. Ele reproduz os
artefatos gerados, não repete a geração independente por agentes.

Não substitua `node_modules` por symlink entre apps: o Nitro/Vite desta versão
não carregou o worker a partir de uma árvore fora da raiz do app nesta execução.
Também não execute build e servidor de desenvolvimento sobre a mesma cópia ao
mesmo tempo. A primeira execução concorrente foi interrompida após timeouts.

## Execução de navegador e agente

Use uma variante por vez. Em um terminal, na raiz da variante:

```sh
NODE_ENV=development AGENT_NATIVE_DISABLE_AUTO_DEV_ACCOUNT=1 \
AUTH_SKIP_EMAIL_VERIFICATION=1 AGENT_ENGINE=ai-sdk:openrouter \
AGENT_MODEL=google/gemini-3.5-flash-lite \
pnpm exec agent-native dev --port 4311
```

`OPENROUTER_API_KEY` deve existir somente no ambiente do servidor. Os testes
criam contas locais descartáveis via Better Auth. Não há bypass de sessão. Não
use essas configurações de verificação de e-mail em um deploy público.

Em outro terminal, na raiz do repositório:

```sh
LAB_URL=http://localhost:4311 LAB_VARIANT=candidate \
LAB_RESULTS="$PWD/.agent-native-fixture/evidence/candidate-browser.json" \
node .agent-native-fixture/harness/node_modules/playwright/cli.js test \
  --config maintenance/agent-native/playwright.config.ts
```

Para o controle, altere porta e `LAB_VARIANT=control`. O mesmo teste verifica a
mesma semântica; dois adaptadores refletem contratos legítimos diferentes:
`?id=` versus `?taskId=`, e conclusão implícita versus `{ completed: true }`.

Os testes de erro de UI usam resposta HTTP simulada. Os demais usam o servidor,
banco e sessão reais. O teste OpenRouter chama o runtime de chat do framework,
registra eventos SSE e confirma o efeito por action de leitura e tela. Sem chave,
o teste fica explicitamente ignorado, impedindo tratar isso como aprovação total.
Traces estão desativados para não conservar cookies de sessão nas evidências.

O executável de produção compilado recusa PGlite mesmo com `NODE_ENV=development`.
Isso foi observado e registrado; use o servidor de desenvolvimento para este
laboratório PGlite. Build aprovado não certifica deploy ou runtime de produção.

## Avaliações de ativação

As vinte consultas existentes são executadas três vezes cada pelo harness do
repositório. O primeiro conjunto novo está em `holdout-queries.json`; como
influenciou um ajuste, seus resultados são de desenvolvimento. As dez consultas
cegas finais estão em `holdout-queries-final.json`, escritas após o congelamento
da skill registrado em `evidence/frozen-skill.json`.
Para reproduzir a validação reservada, copie todos os `SKILL.md` do catálogo para
uma árvore temporária, substitua apenas o dataset de agent-native pelo holdout e
execute o mesmo harness com `--skills-dir`. Preserve o catálogo concorrente.

```sh
python3 maintenance/eval_skills.py run --skill agent-native --judge live \
  --out maintenance/evals-out/agent-native-real-app-final
node maintenance/agent-native/evaluate-holdout.mjs \
  maintenance/evals-out/agent-native-real-app-blind-final \
  maintenance/agent-native/holdout-queries-final.json
node maintenance/validate_skill.mjs skills/agent-native
python3 maintenance/eval_skills.py validate-datasets
graphify update .
git diff --check
```

Respostas geradas e passes do avaliador não provam compatibilidade ou execução.
A revisão manual em `evidence/model-review.md` identifica divergências.
