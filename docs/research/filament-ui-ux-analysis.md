# Análise da skill laravel-filament-5-ui-ux — nota de preparação para spec

> **Nota:** documento superado por [ADR-0002](../adr/0002-reference-compositions-over-evidence-lookup.md). Retido como evidência do momento que motivou aquela decisão; o corpo não é atualizado depois — nomes, caminhos e conclusões refletem o estado do repositório na data abaixo. Para o estado atual, consulte `docs/adr/`.

Data da análise: 3 de agosto de 2026.

Este documento registra a análise de valor e entrega da skill
`laravel-filament-5-ui-ux` para o agente de coding, com evidência empírica
levantada por execução direta (não apenas leitura de código). Serve como nota
de preparação para uma spec a ser iniciada com o workflow `specify`
(`speckit-specify`).

## Veredito

A skill entrega valor real, mas não pela camada que apresenta como seu
diferencial.

O valor está na prosa das 9 referências e nos dados do catálogo
(`references/visual-catalog.json`). É conteúdo genuinamente bom: decisões de
composição condicionadas à tarefa (ex.: "use tabela padrão quando pessoas
comparam os mesmos fatos entre registros pares; não troque por cards por
decoração"), com `prefer_when` / `avoid_when` / evidência oficial linkada.
É exatamente o tipo de julgamento que um agente de coding não deriva sozinho
do docs oficial.

A camada de tooling (`scripts/query_visual_catalog.py`) está, hoje, com valor
negativo: não foi exercitada em nenhuma das 15 execuções registradas em
`evals/forward-runs/codex.json`, tem um caminho relativo quebrado no
`SKILL.md`, e quando é exercitada manualmente erra em cenários centrais da
própria suíte de evals da skill.

O contrato de delegação com `laravel-filament-v5` é o ponto mais forte da
arquitetura — é mútuo (o `SKILL.md` do v5 tem uma seção "Design authority
inside Filament" que delega de volta, mais um fallback mínimo em
`references/ui-composition.md` para quando esta skill não está instalada).

## Método

- Leitura de todos os arquivos da skill (`SKILL.md`, `README.md`,
  `RELEASE.md`, `references/*.md`, `references/visual-catalog.json`,
  `scripts/*.py`).
- Execução direta de `scripts/query_visual_catalog.py` com ~200 combinações
  de `surface` × `workflow` × `available_width`, para montar uma matriz de
  alcançabilidade.
- Execução com vocabulário inválido (`--goal` com typo) para verificar o
  comportamento de fail-open.
- Grep dos 15 transcripts em `evals/forward-runs/codex.json` por menção ao
  script de query e por IDs de screenshot oficiais citados no trace.
- Leitura de `scripts/run_forward_evals.py` para entender como os forward
  runs foram gerados (harness, flags de sandbox/tools).
- Execução da suíte de testes (`python3 -m unittest discover -s tests`) — 31
  testes, todos passam, todos em caminho feliz com vocabulário correto.

## Defeitos, por severidade

### 1. Vocabulário indescobrível + falha silenciosa no `--goal` (defeito nº 1, composto)

Isoladamente cada metade é menor. Juntas produzem seleção errada com
aparência de confiança.

O script exige tokens de um vocabulário controlado: 30 `goals`, 7
`workflows`, 34 `information_shapes`, 24 `relationships`. Documentados em
toda a prosa da skill: 2 tokens (`organize-stable-groups` no exemplo do
`SKILL.md`, `compose-ordinary-fields` no header de uma referência). Não há
`--list-vocabulary`, `--help` com choices, nem `choices=` no argparse. Para
descobrir os tokens válidos o agente precisa ler os 78 KB de
`visual-catalog.json`.

E `--goal` falha aberto: token não reconhecido cai no `else` de
`query_visual_catalog.py:83` e devolve todos os patterns da surface,
ordenados por score. Exemplo reproduzido:

```
--surface form --goal organise-stable-groups  (typo britânico)
  → selected_pattern: "action-feedback-overlays"   # modais e notificações
  → 14 candidatos, 8 screenshots de evidência, requires_direct_inspection: true
```

A pergunta era sobre agrupamento de formulário. A resposta é a paleta de
modais/notificações — com trace completo e nenhum aviso.

### 2. `--workflow` e `--available-width` são filtros duros, com mensagem de erro que aponta para a causa errada

`query_visual_catalog.py:34-35` usa `-100` em vez de score baixo para
`workflow`/`available_width` fora do conjunto do pattern. Matriz de
alcançabilidade (todas as combinações surface × workflow × width):

| surface | (workflow,width) que retornam algo |
|---|---|
| schema | 14/21 |
| form | 12/21 |
| record-detail | 11/21 |
| table | 9/21 |
| action-feedback | 9/21 |
| panel-shell | 8/21 |
| authentication | 6/21 |
| infolist | 4/21 |
| dashboard | 2/21 |

75 de 189 combinações (40%) retornam resultado; as outras 60% levantam
`ValueError` sempre com a mesma mensagem:

> `No reviewed visual pattern matches the requested surface. Use official
> Filament 5 evidence and record the catalog gap.`

A mensagem é factualmente errada nesses casos: a surface casa. O que não
casou foi `workflow` ou `available_width`. A mensagem instrui o agente a
abandonar o catálogo e "registrar a lacuna" — o pior resultado possível para
um gate descrito como obrigatório. Exemplo com vocabulário 100% válido:

```
--surface dashboard --goal support-operational-decisions --workflow parallel --available-width wide
  → ValueError   # o pattern exige workflow="monitoring"; nada documentado diz isso
```

### 3. O eixo `narrow` está furado — e quebra justamente cenários da própria suíte de evals

`narrow` é vocabulário vivo (7 patterns de form o aceitam), então o agente
vai usá-lo. Mas:

| surface | patterns com `narrow` |
|---|---|
| dashboard | 0 |
| infolist | 0 |
| table | 1 — `action-feedback-overlays` |
| record-detail | 1 — `action-feedback-overlays` |

`responsive-identity-centred-table` — o pattern que existe especificamente
para o caso mobile, com 12 screenshots incluindo
`tables/layout/stack/mobile` — declara `available_width: ["standard",
"wide"]`. Logo:

```
--surface table --goal transform-record-hierarchy-responsively --available-width narrow
  → selected: action-feedback-overlays
```

O eval #10 da própria skill é exatamente esse caso ("On phones, the current
version merely squeezes the six desktop columns…"). Os evals #11, #12 e #13
também descrevem cenários "on phones" — e `dashboard`/`infolist` têm zero
patterns `narrow`. A dimensão `available_width` está modelando "largura de
projeto do pattern", não "largura disponível na pergunta", e os dois
sentidos colidem exatamente no ponto que mais importa.

### 4. Os dois gates centrais não foram executados em nenhuma das 15 execuções registradas

Grep nos 15 transcripts de `evals/forward-runs/codex.json`:

- 0/15 mencionam `query_visual_catalog.py`, `python3` ou `.py` — o passo 2
  do fluxo "Mandatory" nunca aparece. Os agentes leram `visual-catalog.json`
  e os `.md` direto, por caminho absoluto.
- 0/15 citam um único ID de screenshot oficial (`schemas/layout/...`,
  `tables/layout/...`, `forms/fields/...`). O passo 6 manda o trace conter
  `Evidence: schemas/layout/tabs/vertical`; o que saiu foi `Evidence:
  reviewed local catalog selects vertical tabs for stable peer groups`.

Duas causas contribuem, vale separar. O `codex` rodou com `--sandbox
read-only`, que permite executar comandos — não há prova de que o harness
bloqueou o script, ele simplesmente não foi usado. Já o perfil
`claude-code` no mesmo harness (`run_forward_evals.py:22`) usa `--tools
""`, o que torna o passo obrigatório estruturalmente impossível de
executar. Além disso, o `SKILL.md` documenta o comando como caminho
relativo (`python3 scripts/query_visual_catalog.py`), que falha a partir de
qualquer cwd real — a skill instalada fica em `~/.claude/skills/<name>/`, o
agente está no projeto do usuário.

Conclusão defensável: o passo 2 é opcional de fato, e o resultado continuou
bom sem ele. Isso reforça onde está o valor real (item 1 do veredito).

### 5. Os evals nunca foram pontuados

Os 15 resultados têm `status: "recorded"` e `review_required: true`.
`recorded` significa apenas "exit code 0". As `assertions` estão no JSON,
sem nenhum veredito ao lado. O `RELEASE.md` fala em "review each listed
assertion before recording a pass" — não há registro de que isso
aconteceu. A skill está em `1.0.0` sem evidência revisada de comportamento.

Os 31 testes unitários passam, mas todos usam vocabulário correto e
caminhos felizes. Nenhum cobre: goal desconhecido, workflow inválido,
`narrow`, ou a mensagem de erro.

### 6. Contexto desperdiçado no SKILL.md

- A seção `## Verification` (linhas 60-70) é fluxo de manutenção do
  catálogo — `sync_visual_catalog.py`, `build_review_sheets.py`. O agente
  de coding nunca vai sincronizar o catálogo. Isso pertence só ao
  README/RELEASE; é contexto gasto numa tarefa que o consumidor não
  executa.
- O passo 3 (linha 29) é um parágrafo único de ~1.400 caracteres com 9
  rotas encadeadas e três "also read". Como bloco de decisão isso é
  hostil: o agente tende a puxar múltiplas referências de uma vez. A
  tabela "Current routed coverage" logo abaixo já contém a mesma
  informação em forma legível — o parágrafo é redundante.

### 7. Deriva de documentação

O bloco `## Structure` do `README.md` omite
`references/responsive-record-layouts.md`,
`references/dashboard-composition.md`, `references/release-verification.md`,
`scripts/run_forward_evals.py` e `scripts/release_install_smoke.py`. O
campo `scope` dentro de `visual-catalog.json` ainda diz "page-level schema
and form composition plus ordinary field presentation" — a versão
pré-merge, embora o catálogo já cubra tabelas, dashboards e panel shells.

Nota operacional: `laravel-filament-v5` está instalado em
`~/.claude/skills/`, esta skill não. Hoje o v5 delega para algo ausente e
cai no fallback mínimo (`references/ui-composition.md`).

## Melhorias propostas, em ordem de retorno

**Alta — corrige seleção errada**

1. `choices=` no argparse para as 4 dimensões, derivadas do catálogo, mais
   `--list-vocabulary`. Elimina o typo silencioso na origem e dá
   autodescoberta sem ler 78 KB.
2. Trocar o fail-open do `--goal` por erro explícito com sugestão dos goals
   válidos da surface (`difflib.get_close_matches`).
3. `--workflow` / `--available-width` viram sinais de preferência (score
   positivo, sem `-100`), e a mensagem de erro passa a nomear a dimensão
   que não casou, listando os valores aceitos para aquela surface.
4. Reparar o eixo `narrow`: adicionar `narrow` a
   `responsive-identity-centred-table`, `operational-dashboard` e
   `record-detail-infolist` — ou redefinir a dimensão como "contexto
   responsivo pedido" em vez de "largura de projeto", e ajustar os 22
   patterns. A segunda opção é a correta conceitualmente; a primeira é a
   mais barata.

**Alta — corrige execução**

5. Caminho absoluto no comando do `SKILL.md` (resolver o diretório da
   skill em runtime), ou — dado o resultado 0/15 — assumir que ler o JSON
   é o caminho real e degradar o passo 2 de "obrigatório" para "quando
   exec estiver disponível", com a leitura direta documentada como via
   primária.
6. Testes para os quatro modos de falha acima (1-3). São os únicos casos
   que pegariam os defeitos descritos.

**Média**

7. Mover `## Verification` do `SKILL.md` para o `README.md`. Substituir o
   parágrafo do passo 3 pela tabela de roteamento já existente. Ganho:
   ~250 tokens e uma decisão mais nítida.
8. Pontuar os 15 evals existentes contra suas assertions e registrar o
   veredito — inclusive porque o #10 provavelmente reprova no eixo da
   evidência de screenshot.
9. Sincronizar `README.md` `## Structure` e o campo `scope` do catálogo.

## Escopo sugerido para a spec

A spec deveria cobrir os itens 1-6 (alta prioridade) como núcleo, com 7-9
como limpeza incluída se o custo for baixo. Não deveria expandir o catálogo
de patterns nem mexer no conteúdo de composição visual — esse conteúdo já
está validado como o ponto forte da skill.
