# Contrato — índice compacto

Artefato: `references/visual-catalog-index.md`. Gerado por `scripts/build_catalog_index.py`, verificado por `scripts/validate_visual_catalog.py`. **Via primária** de seleção de pattern.

## Forma

```markdown
# Filament 5 visual pattern index

Generated from references/visual-catalog.json. Do not edit by hand.

## Patterns

| Pattern | Surfaces | Goals | Responsive contexts | Reference | Evidence |
|---|---|---|---|---|---|
| action-feedback-overlays | action-feedback, form, record-detail, schema, table | ... | mobile-first, desktop-with-mobile-fallback | references/action-feedback-composition.md | 9 |
| ... 22 linhas, ordenadas por identificador ...

## Vocabulary

**Surfaces** (9): ...
**Goals** (30): ...
**Workflows** (7): ...
**Information shapes** (34): ...
**Relationships** (24): ...
**Responsive contexts** (2): desktop-with-mobile-fallback, mobile-first
```

Conteúdo em inglês, como todo arquivo sob `skills/` (Princípio II).

## Regras de geração

| Regra | Detalhe |
|---|---|
| Fonte única | Todo valor vem do catálogo. O gerador não tem tabela própria, o que exige o campo `routed_reference` por pattern. |
| Ordenação estável | Patterns por identificador; toda lista em ordem alfabética. Sem isso a comparação de deriva gera falso positivo. |
| Cobertura | Todos os patterns com `status: "reviewed"`. Um pattern não revisado não entra. |
| Exclusão | `available_width` não aparece (FR-004). `selection_weight` e campos de prosa também não. |
| Orçamento | Abaixo de 10% do tamanho do catálogo. |

## Verificação de deriva

`validate_visual_catalog.py` regenera o índice em memória e compara com o arquivo versionado. Diferença reprova, com mensagem indicando regeneração.

A mesma passagem verifica que todo pattern declara `routed_reference` e que o caminho aponta para um arquivo existente — sem isso o índice publicaria uma rota quebrada e o agente leria nada.

Casos que a checagem precisa pegar:

- pattern adicionado ou removido do catálogo
- objetivo, superfície ou contexto responsivo renomeado
- `routed_reference` alterado
- contagem de evidências alterada
- índice editado à mão

## Consumo

O `SKILL.md` aponta o índice como primeira leitura do passo de consulta. O agente:

1. lê o índice, identifica superfície e objetivo, escolhe o pattern;
2. abre a entrada correspondente em `references/visual-catalog.json` para sinais de seleção, variantes, alternativas, quando evitar e evidência;
3. abre a `routed_reference` indicada para a prosa de composição.

O índice nunca substitui os passos 2 e 3 — ele encurta a descoberta, não a decisão.
