# Fase 1 — Modelo de dados

Três entidades mudam de forma nesta feature: o **pattern visual**, o **índice compacto** (nova) e o **registro de execução**. O inventário de screenshots e os cenários de avaliação não mudam.

---

## Pattern visual

Vive em `references/visual-catalog.json`, sob `patterns[]`. 22 entradas, todas com `status: "reviewed"`.

### Campos existentes, não alterados

`id`, `surface[]`, `goals[]`, `information_shapes[]`, `relationships[]`, `workflows[]`, `selection_signals`, `variant_decisions`, `alternatives`, `avoid_when`, `responsive_considerations`, `accessibility_considerations`, `visual_evidence[]`, `selection_weight`, `status`.

### Campos alterados

| Campo | Antes | Depois |
|---|---|---|
| `available_width[]` | dimensão de consulta, filtro eliminatório | metadado descritivo: a largura em que o pattern foi projetado. Permanece no dado, sai da consulta e não aparece no índice. |
| `responsive_contexts[]` | eixo secundário, também eliminatório | única dimensão que carrega a exigência responsiva da pergunta; atua como peso. |

### Campo novo

| Campo | Tipo | Regra |
|---|---|---|
| `routed_reference` | string | Caminho relativo do arquivo de referência de composição que o agente deve ler ao selecionar este pattern (por exemplo `references/table-composition.md`). Obrigatório em todos os 22 patterns. Deve apontar para um arquivo existente. |

**Por que o campo é necessário**: FR-001 exige a referência roteada por pattern no índice, e o roteamento não é derivável da superfície. `form` e `schema` roteiam para três referências distintas conforme o pattern seja de composição de página, de campo ordinário ou de entrada complexa. Sem esse campo, o gerador precisaria embutir uma tabela de roteamento própria, e o índice deixaria de ser projeção pura do catálogo (decisão D2).

### Alterações de valor

| Pattern | Alteração | Efeito na seleção |
|---|---|---|
| `responsive-identity-centred-table` | acrescenta `mobile-first` a `responsive_contexts` | Sim — passa a ser o selecionado para pergunta de tabela em contexto móvel |
| `operational-dashboard` | acrescenta `mobile-first` a `responsive_contexts` | Não — `dashboard` tem um único pattern revisado; correção de exatidão descritiva |
| `record-detail-infolist` | nenhuma — já declara ambos | — |

Nenhum outro pattern tem contextos responsivos alterados.

---

## Catálogo

Objeto raiz de `references/visual-catalog.json`.

| Campo | Alteração |
|---|---|
| `scope` | Reescrito. Hoje diz "page-level schema and form composition plus ordinary field presentation", texto anterior à fusão das skills. Passa a descrever as nove superfícies cobertas. |
| `patterns[]` | Conforme acima. |

---

## Índice compacto *(nova entidade)*

`references/visual-catalog-index.md`. Projeção derivada do catálogo, sem edição manual, sem informação própria.

### Projeção por pattern

| Campo do índice | Origem |
|---|---|
| identificador | `id` |
| superfícies | `surface[]` |
| objetivos | `goals[]` |
| contextos responsivos | `responsive_contexts[]` |
| referência roteada | `routed_reference` |
| contagem de evidências | tamanho de `visual_evidence[]` |

**Excluído deliberadamente**: `available_width` (FR-004 — sua presença convidaria o agente a filtrar por ela, que é o comportamento que a feature elimina), `selection_weight`, e todos os campos de prosa, que continuam sendo motivo para abrir o catálogo.

### Vocabulário

O índice fecha com as listas completas de termos aceitos por dimensão, ordenadas, extraídas do catálogo: superfícies (9), objetivos (30), fluxos de trabalho (7), formas de informação (34), relacionamentos (24), contextos responsivos (2).

### Invariantes

1. Regenerar o índice a partir do catálogo produz byte a byte o arquivo versionado. Qualquer diferença é deriva e reprova a validação.
2. Ordenação estável: patterns por identificador, listas de vocabulário em ordem alfabética. Sem isso a comparação de deriva produz falso positivo.
3. Tamanho abaixo de 10% do catálogo (SC-001).

---

## Registro de execução

`evals/forward-runs/<agente>.json`.

### Antes

```
results[]: { id, status: "recorded", assertions: [string], transcript, stderr }
review_required: true          # constante, nunca derivada
```

`status: "recorded"` significa apenas que o processo terminou com código zero.

### Depois

```
results[]: {
  id,
  status,                       # execução: "recorded" | "failed"
  assertions: [
    { assertion: string, verdict: "pass" | "fail" | "unscored", evidence: string }
  ],
  transcript,
  stderr
}
review_required                 # derivado: verdadeiro enquanto houver qualquer "unscored"
```

### Regras

- `verdict` inicia como `unscored` quando a execução é gravada. Pontuar é ato de revisão posterior.
- `evidence` é o trecho do transcript que sustenta o veredito. Obrigatório para `pass` e `fail`; vazio para `unscored`.
- `review_required` nunca é escrito à mão. É recomputado a cada gravação; um arquivo que se declare revisado com asserções pendentes é inválido.
- `fail` é resultado legítimo e não impede a gravação dos demais.

### Transição de estado

```
gravado (todas unscored, review_required = true)
   → parcialmente pontuado (review_required = true)
      → revisado (nenhuma unscored, review_required = false)
```

### Arquivos

`claude-code.json` é substituído pela rodada nova. `codex.json` (2,4 MB) e `cursor.json` são removidos: nunca foram pontuados e, sob o Princípio IV, nunca constituíram evidência.

---

## Não alterados

- `references/screenshot-inventory.json` — evidência oficial e seu contrato de rastreio.
- `evals/evals.json` — os 15 cenários com enunciado, saída esperada e asserções.
- `evals/eval_queries.json` — as 13 consultas de detecção de gatilho, artefato distinto e fora do escopo.
- As 9 referências de composição — o conteúdo validado que a feature existe para tornar acessível.
