# Guia de validação

Como provar, ponta a ponta, que a feature funciona. Todos os comandos partem da raiz do repositório.

## Pré-requisitos

- Python 3.13+ (`python3 --version`)
- Node.js, apenas para o validador de pacote de skill
- Nenhuma dependência externa; nenhum acesso à rede

## Linha de base, antes de mudar qualquer coisa

```bash
python3 -m unittest discover -s tests
```

31 testes devem passar. Esse é o piso: nenhuma alteração pode reduzi-lo.

---

## V1 — Índice compacto existe, é derivado e cabe no orçamento

```bash
IDX=skills/laravel-filament-5-ui-ux/references/visual-catalog-index.md
B=skills/laravel-filament-5-ui-ux/scripts/build_catalog_index.py

python3 $B --output /tmp/index-a.md
python3 $B --output /tmp/index-b.md
diff /tmp/index-a.md /tmp/index-b.md    # determinismo
diff /tmp/index-a.md $IDX               # arquivo versionado em dia
wc -c $IDX
```

**Esperado**: as três comparações silenciosas. O arquivo fica abaixo de 7.805 bytes, isto é, 10% do catálogo (SC-001) — a projeção medida dá ~7,0 KB, então a folga é de cerca de 10% e qualquer campo extra na linha de pattern estoura o orçamento; as 22 linhas de pattern trazem identificador, superfícies, objetivos, contextos responsivos, referência roteada e contagem de evidências; a seção de vocabulário lista as 6 dimensões; `available_width` não aparece em lugar nenhum.

Cobre FR-001, FR-002, FR-004, SC-001.

## V2 — Deriva do índice é detectada

```bash
python3 skills/laravel-filament-5-ui-ux/scripts/validate_visual_catalog.py   # passa

# introduza a deriva de propósito
sed -i '' 's/| 9 |/| 99 |/' skills/laravel-filament-5-ui-ux/references/visual-catalog-index.md
python3 skills/laravel-filament-5-ui-ux/scripts/validate_visual_catalog.py   # reprova

git checkout skills/laravel-filament-5-ui-ux/references/visual-catalog-index.md
```

**Esperado**: a segunda execução sai com erro apontando a divergência e instruindo a regeneração.

Cobre FR-003, SC-007.

## V3 — Vocabulário inválido falha de forma visível

```bash
Q=skills/laravel-filament-5-ui-ux/scripts/query_visual_catalog.py

python3 $Q --surface form --goal organise-stable-groups        # erro com sugestão
python3 $Q --surface form --goal organize-stable-groups        # seleciona
python3 $Q --surface fromm --goal organize-stable-groups       # erro na dimensão surface
python3 $Q --list-vocabulary                                   # 6 listas
python3 $Q --help                                              # choices visíveis
```

**Esperado**: o erro do objetivo grafado à britânica nomeia a dimensão e sugere `organize-stable-groups` — o cenário que hoje devolve a paleta de modais e notificações com trace completo e nenhum aviso. Nenhuma seleção é produzida em caso de erro. `--available-width` deixa de ser aceita.

Cobre FR-006, FR-007, FR-008, SC-002.

## V4 — Pergunta sobre celular seleciona o pattern responsivo

```bash
python3 $Q --surface table --goal transform-record-hierarchy-responsively \
  --responsive-context mobile-first
```

**Esperado**: `selected_pattern` é `responsive-identity-centred-table`, não `action-feedback-overlays`. É o cenário do eval #10.

Cobre FR-010, FR-011, SC-003.

## V5 — Nenhuma consulta válida volta vazia

```bash
python3 - <<'PY'
import importlib.util, itertools, json, pathlib
root = pathlib.Path("skills/laravel-filament-5-ui-ux")
spec = importlib.util.spec_from_file_location("q", root / "scripts/query_visual_catalog.py")
q = importlib.util.module_from_spec(spec); spec.loader.exec_module(q)
cat = json.loads((root / "references/visual-catalog.json").read_text())["patterns"]
surfaces = sorted({s for p in cat for s in p["surface"]})
goals = sorted({g for p in cat for g in p["goals"]})
workflows = sorted({w for p in cat for w in p["workflows"]})
empty = [
    (s, g, w)
    for s, g, w in itertools.product(surfaces, goals, workflows)
    if not q.query_catalog(surface=s, goal=g, workflow=w)["candidates"]
]
print("combinacoes vazias:", len(empty))
PY
```

**Esperado**: zero. Hoje a matriz equivalente tem 60% de recusas.

Cobre FR-012, SC-004.

## V6 — O SKILL.md descreve um fluxo executável

Leitura, não comando. Verifique que:

- o passo de consulta apresenta a leitura do índice como via primária, e a ferramenta como alternativa condicionada à disponibilidade de execução;
- nenhum caminho é relativo ao diretório de trabalho;
- não há instruções de sincronização, folhas de revisão ou validação de catálogo — elas migraram para o `README.md`;
- o roteamento para referências aparece uma única vez, como tabela;
- a seção de autoridade e escapes e a delegação a `laravel-filament-v5` continuam presentes e com a mesma força (FR-016).

```bash
node skills/laravel-filament-5-ui-ux/scripts/validate_skill.mjs
python3 skills/laravel-filament-5-ui-ux/scripts/release_install_smoke.py
```

Cobre FR-013, FR-014, FR-015, FR-016, SC-005.

## V7 — Evidência pontuada

```bash
python3 skills/laravel-filament-5-ui-ux/scripts/run_forward_evals.py \
  --agent claude-code \
  --output skills/laravel-filament-5-ui-ux/evals/forward-runs/claude-code.json
```

`--output` é obrigatória. Os perfis `codex` e `cursor` permanecem em `AGENT_COMMANDS` — a suíte de testes verifica suas strings de invocação; o que sai são os arquivos gravados, não os perfis.

Depois, pontue cada asserção lendo o transcript e preenchendo `verdict` e `evidence`.

**Esperado**: 15 resultados; toda asserção com veredito e citação; `review_required` cai para falso apenas quando nenhuma continuar `unscored`; `codex.json` e `cursor.json` não existem mais. Reprovação registrada é resultado válido — a análise prevê que o cenário #10 reprove no eixo de evidência de imagem.

Cobre FR-017, FR-018, FR-019, SC-006.

## V8 — Suíte completa e documentação sincronizada

```bash
python3 -m unittest discover -s tests
```

**Esperado**: a suíte cresce dos 31 atuais com, no mínimo, os três grupos de FR-020 — vocabulário inválido por dimensão, deriva do índice e seleção responsiva de tabela. As 15 referências a `available_width` no arquivo de testes foram atualizadas.

Confira também que `README.md` lista todos os arquivos existentes da skill, que o campo `scope` do catálogo descreve as nove superfícies, e que a versão em `SKILL.md` é `1.1.0`.

Cobre FR-020, FR-021, FR-022, SC-008.

---

## Ordem sugerida

`V1 → V2 → V3 → V4 → V5 → V6 → V8 → V7`. V7 fica por último porque pontua o comportamento final: rodá-lo antes gera evidência de um estado intermediário.
