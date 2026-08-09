# Contrato — registro de execução pontuado

Artefato: `evals/forward-runs/<agente>.json`. Produzido por `scripts/run_forward_evals.py`, completado por revisão humana, verificado pela suíte de testes.

## Estrutura

```json
{
  "schema_version": "<incrementado>",
  "agent": "claude-code",
  "recorded_at": "<ISO 8601 UTC>",
  "source": "evals/evals.json",
  "review_required": true,
  "results": [
    {
      "id": 1,
      "status": "recorded",
      "assertions": [
        {
          "assertion": "The response identifies the form as stable parallel groups rather than a sequence.",
          "verdict": "unscored",
          "evidence": ""
        }
      ],
      "transcript": "...",
      "stderr": ""
    }
  ]
}
```

## Campos

| Campo | Regra |
|---|---|
| `status` | Resultado da execução: `recorded` (código de saída zero) ou `failed`. Não é veredito de comportamento. |
| `assertions[].assertion` | Texto vindo de `evals/evals.json`, sem alteração. |
| `assertions[].verdict` | `unscored` na gravação. `pass` ou `fail` após revisão. |
| `assertions[].evidence` | Trecho do transcript que sustenta o veredito. Obrigatório para `pass` e `fail`; vazio apenas com `unscored`. |
| `review_required` | **Derivado**, nunca escrito à mão: verdadeiro enquanto existir qualquer `unscored`. |

## Invariantes verificáveis

1. Todo `verdict` pertence a `{pass, fail, unscored}`.
2. `verdict` diferente de `unscored` exige `evidence` não vazia.
3. `review_required` é falso se e somente se nenhuma asserção está `unscored`.
4. O conjunto de asserções de cada resultado corresponde ao do cenário homônimo em `evals/evals.json`.
5. Todo cenário de `evals.json` tem exatamente um resultado.

## Pontuação

Pontuar é ato de revisão, lendo o transcript e julgando cada asserção. Não é automatizável por correspondência de texto: as asserções são julgamentos de composição em prosa, e casar palavra-chave produziria veredito falso — pior do que veredito nenhum.

`fail` é resultado legítimo. A análise de origem prevê reprovação do cenário #10 no eixo de evidência de imagem. Nenhum critério desta feature exige 15 aprovações; o critério é que 15 estejam pontuados com citação.

## Escopo dos arquivos

| Arquivo | Destino |
|---|---|
| `claude-code.json` | Substituído por rodada nova contra a skill 1.1.0, pontuada |
| `codex.json` | Removido — 2,4 MB, nunca pontuado, nunca foi evidência |
| `cursor.json` | Removido — mesma razão |

`references/release-verification.md` codifica o modelo de evidência multiagente e é atualizado na mesma entrega para descrever agente único (FR-019).
