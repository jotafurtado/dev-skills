# Contrato — consulta ao catálogo

Superfície: `scripts/query_visual_catalog.py`, e a função `query_catalog()` que os testes exercitam diretamente. Via **alternativa**, condicionada à disponibilidade de execução; a via primária é ler `references/visual-catalog-index.md`.

## Linha de comando

```
python3 <skill>/scripts/query_visual_catalog.py
  --surface <termo>              obrigatório
  --goal <termo>                 obrigatório
  --workflow <termo>             opcional
  --responsive-context <termo>   opcional
  --information-shape <termo>    opcional
  --relationship <termo>         opcional

python3 <skill>/scripts/query_visual_catalog.py --list-vocabulary
```

### Mudanças em relação à versão 1.0.0

| Item | Antes | Depois |
|---|---|---|
| `--available-width` | obrigatória | **removida** |
| `--workflow` | obrigatória, eliminatória | opcional, peso |
| `--responsive-context` | opcional, eliminatória | opcional, peso |
| `--information-shape`, `--relationship` | opcionais, eliminatórias | opcionais, peso |
| `--list-vocabulary` | inexistente | lista os termos aceitos por dimensão |
| termo inválido em `--goal` | aceito em silêncio, seleção arbitrária | erro nomeando a dimensão |

Toda dimensão declara `choices` derivadas do catálogo, para que `--help` seja autodescritivo.

## Função

```python
query_catalog(
    *,
    surface: str,
    goal: str,
    workflow: str | None = None,
    responsive_context: str | None = None,
    information_shape: str | None = None,
    relationship: str | None = None,
) -> dict
```

O parâmetro `available_width` deixa de existir. A validação de vocabulário vive aqui, não apenas em `argparse` — é assim que os testes a exercitam.

## Comportamento

### Seleção

1. Restringe aos patterns revisados cuja `surface[]` contém o termo. **Única dimensão restritiva.**
2. Soma peso por dimensão que casa. Nenhuma dimensão subtrai; o valor `-100` deixa de existir.
3. O corte por pontuação não negativa (`query_visual_catalog.py:72`) é removido junto. Hoje ele seria inócuo — o menor `selection_weight` do catálogo é zero —, mas mantê-lo deixaria a invariante de conjunto não vazio dependendo de um dado que ninguém verifica.
4. Ordena por peso decrescente, desempatando por identificador para manter determinismo.
5. Prefere, entre os melhor pontuados, os que atendem ao objetivo informado.

**Invariante**: consulta com vocabulário válido para superfície com patterns revisados nunca retorna conjunto vazio.

### Falha

| Entrada | Resultado |
|---|---|
| Termo fora do vocabulário, em qualquer dimensão | Erro nomeando a dimensão e listando as sugestões mais próximas; sem sugestão próxima, lista os termos válidos daquela dimensão. Nenhuma seleção é produzida. |
| Superfície inválida | Mesmo tratamento. Deixa de ser tratada como lacuna de catálogo. |
| Combinação válida sem correspondência exata | **Não é falha.** Retorna os candidatos da superfície ordenados. |

A mensagem `"No reviewed visual pattern matches the requested surface. Use official Filament 5 evidence and record the catalog gap."` é removida: era factualmente errada nos casos em que aparecia, porque a superfície casava.

## Retorno

Estrutura preservada — `query`, `candidates`, `selected_pattern`, `decision_trace` —, exceto que `query` não contém mais `available_width`.
