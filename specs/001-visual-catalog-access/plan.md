# Implementation Plan: Acesso ao catálogo visual da skill Filament 5 UI/UX

**Branch**: `001-visual-catalog-access` | **Date**: 2026-08-04 | **Spec**: [spec.md](./spec.md)

**Input**: Feature specification from `/specs/001-visual-catalog-access/spec.md`

## Summary

Substituir a camada de acesso ao catálogo visual da skill `laravel-filament-5-ui-ux`, mantendo intacto o conteúdo de composição. Três movimentos ligados: (1) um índice compacto gerado a partir de `references/visual-catalog.json` vira a via primária de seleção e a fonte do vocabulário; (2) o modelo de dimensões perde `available_width` como eixo de consulta e passa a ter a superfície como única dimensão restritiva, com todas as demais atuando como peso — o que elimina de vez o caminho de recusa por combinação não encontrada; (3) a evidência de release deixa de ser "exit code 0" e passa a ser veredito por asserção com citação de transcript.

Abordagem técnica: alterações cirúrgicas em Python 3 puro sobre os scripts existentes, mais um gerador/validador de índice novo, mais reescrita do fluxo do `SKILL.md`. Sem dependências externas novas.

## Technical Context

**Language/Version**: Python 3.13+ (ambiente atual: 3.14.6). Biblioteca padrão apenas — `argparse`, `json`, `difflib`, `pathlib`, `unittest`. Node.js apenas para o validador de pacote de skill já existente (`scripts/validate_skill.mjs`).

**Primary Dependencies**: nenhuma externa. Restrição herdada: a skill roda offline após instalada, então nada pode passar a exigir rede.

**Storage**: arquivos versionados. `references/visual-catalog.json` (78 KB, 22 patterns) é a fonte da verdade; `references/screenshot-inventory.json` é a evidência oficial; `evals/forward-runs/*.json` são os registros de execução.

**Testing**: `python3 -m unittest discover -s tests` a partir da raiz do repositório. Suíte única em `tests/test_laravel_filament_5_ui_ux.py`, 31 testes hoje, que carrega os scripts por `importlib.util.spec_from_file_location`.

**Target Platform**: agente de coding em máquina de desenvolvimento, com a skill instalada em `~/.claude/skills/laravel-filament-5-ui-ux/`. O diretório de trabalho é o projeto do usuário, nunca o da skill — origem do defeito de caminho relativo.

**Project Type**: pacote de Agent Skill (`SKILL.md` + `references/` + `scripts/` + `evals/`), distribuído por instalação direta do repositório.

**Performance Goals**: a via primária de seleção deve caber em menos de 10% do volume do catálogo (SC-001), ou seja, abaixo de 7.805 bytes. A projeção definida em `data-model.md` foi medida contra o catálogo real e dá ~7,0 KB — cabe, com cerca de 10% de folga. Consequência para a implementação: a linha de pattern está fechada; acrescentar qualquer campo a ela exige rever SC-001, não improvisar.

**Constraints**: offline após instalação; sem binários de screenshot no repositório; `available_width` permanece no JSON como metadado descritivo, então nenhuma migração de dados destrutiva; o contrato de delegação com `laravel-filament-v5` não pode regredir (FR-016).

**Scale/Scope**: 22 patterns, 9 superfícies, 6 dimensões de vocabulário, 9 arquivos de referência, 15 cenários de avaliação, 31 testes existentes. A feature toca ~8 arquivos e remove 2.

## Constitution Check

*GATE: Must pass before Phase 0 research. Re-check after Phase 1 design.*

| Princípio | Avaliação | Evidência no plano |
|---|---|---|
| I. Evidence-Grounded Accuracy | **Passa** | Nenhuma assinatura de API do Filament é adicionada ou alterada. As evidências oficiais por pattern permanecem intactas; o índice apenas as conta e aponta. |
| II. English-Authored Skills | **Passa** | Todo conteúdo alterado dentro de `skills/` permanece em inglês, incluindo o índice gerado. A spec e o plano em pt-BR vivem em `specs/`, fora da superfície da skill. |
| III. Deep Modules, Progressive Disclosure | **Reforça** | O índice é o mecanismo de divulgação progressiva que faltava: hoje a única fonte é o arquivo de 78 KB. FR-014 e FR-015 removem do `SKILL.md` conteúdo que o consumidor nunca usa. `references/` continua um nível de profundidade. |
| IV. Verified Before Shipped | **Corrige violação existente** | É a razão de ser da feature. FR-006 traz o fail-closed; FR-017/FR-018 tornam o veredito um artefato; FR-019 remove registros que nunca foram evidência. |
| V. Earned Absolutes | **Corrige violação existente** | O passo 2 deixa de ser "Mandatory" — nenhuma das 45 execuções gravadas o executou, então o absoluto não era genuíno. Vira condicional à disponibilidade de execução. |
| VI. Licensing Integrity | **Passa** | Nenhum conteúdo novo vem de fonte externa. O índice é derivado de dados já presentes no repositório. |

**Convenções de repositório**: o glossário `CONTEXT.md` é respeitado; nenhum ADR existente é contrariado. O termo "índice compacto" é novo e deve entrar em `CONTEXT.md` durante a implementação.

**Ciclo de vida da skill**: a entrega inclui rodar a suíte automatizada e revisar as asserções contra transcript real, como exige a seção "Skill Lifecycle & Verification" — é literalmente FR-017.

**Nenhuma violação a justificar.** A seção Complexity Tracking fica vazia.

## Project Structure

### Documentation (this feature)

```text
specs/001-visual-catalog-access/
├── plan.md              # Este arquivo
├── spec.md              # Especificação aprovada
├── research.md          # Fase 0
├── data-model.md        # Fase 1
├── quickstart.md        # Fase 1
├── contracts/           # Fase 1
│   ├── catalog-index.md
│   ├── query-cli.md
│   └── forward-run-record.md
├── checklists/
│   └── requirements.md
└── tasks.md             # Fase 2 (/speckit-tasks — não criado aqui)
```

### Source Code (repository root)

```text
skills/laravel-filament-5-ui-ux/
├── SKILL.md                              # ALTERADO — fluxo, roteamento, remoção da seção de manutenção
├── README.md                             # ALTERADO — Structure sincronizada, seção de manutenção recebida
├── RELEASE.md                            # ALTERADO — 1.1.0, via primária, veredito dos cenários
├── references/
│   ├── visual-catalog.json               # ALTERADO — retags responsivos, campo scope
│   ├── visual-catalog-index.md           # NOVO — índice compacto gerado
│   ├── release-verification.md           # ALTERADO — modelo de evidência de multiagente para agente único
│   ├── screenshot-inventory.json         # intacto
│   └── *.md (9 referências de composição) # intactos
├── scripts/
│   ├── query_visual_catalog.py           # ALTERADO — vocabulário, pesos, remoção de available_width
│   ├── build_catalog_index.py            # NOVO — gera o índice a partir do catálogo
│   ├── validate_visual_catalog.py        # ALTERADO — deriva índice↔catálogo, rotas existentes
│   ├── run_forward_evals.py              # ALTERADO — asserções pontuadas no registro
│   └── sync_visual_catalog.py            # intacto — verificado: só escreve o inventário
└── evals/
    ├── evals.json                        # intacto (15 cenários)
    ├── eval_queries.json                 # intacto (13 consultas de gatilho)
    └── forward-runs/
        ├── claude-code.json              # SUBSTITUÍDO — rodada nova, pontuada
        ├── codex.json                    # REMOVIDO
        └── cursor.json                   # REMOVIDO

tests/
└── test_laravel_filament_5_ui_ux.py      # ALTERADO — 15 referências a available_width + 3 grupos novos

CONTEXT.md                                 # ALTERADO — termo "índice compacto"
```

**Structure Decision**: o repositório é um monorepo de skills sem camada de aplicação. Nenhuma das opções de estrutura do template (projeto único, web, mobile) se aplica: cada skill é um pacote autocontido sob `skills/<nome>/`, e a suíte de testes é única na raiz, em `tests/`. A feature vive inteiramente dentro de `skills/laravel-filament-5-ui-ux/`, mais o arquivo de testes na raiz e o glossário.

**Ordem de implementação imposta por dependência**: os retags do catálogo e o campo `scope` vêm primeiro (dados); o gerador de índice depende deles; a validação de deriva depende do gerador; a mudança de pontuação do `query` é independente e pode ir em paralelo; o `SKILL.md` depende do índice existir; a re-execução dos cenários depende de tudo isso estar pronto, pois pontua o comportamento final.

## Constitution Check — reavaliação após a Fase 1

O desenho introduziu dois artefatos que não estavam previstos no portão inicial. Ambos foram reavaliados:

- **Campo `routed_reference` por pattern** (data-model). Necessário para que o índice permaneça projeção pura do catálogo; sem ele o gerador teria tabela de roteamento própria e viraria uma segunda fonte da verdade. Não afeta o Princípio I (não é assinatura de API) e serve ao Princípio III, porque é o que permite ao índice apontar a referência certa sem inline de conteúdo.
- **`scripts/build_catalog_index.py`**. Script de manutenção, na mesma família de `sync`/`validate`/`build_review_sheets`. Documentado no `README.md`, nunca no `SKILL.md` — coerente com FR-014.

Nenhum princípio passa a ser violado pelo desenho. Os Princípios IV e V continuam sendo corrigidos, não tensionados.

## Complexity Tracking

Sem violações a justificar. A feature remove complexidade: uma dimensão de consulta, um caminho de erro, uma seção do `SKILL.md`, um parágrafo redundante e dois arquivos de registro.
