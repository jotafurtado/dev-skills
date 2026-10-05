# Pesquisa

Investigações datadas que embasaram decisões deste repositório. Enquanto `docs/adr/` registra *o que* foi decidido, esta pasta registra *o que foi apurado antes* — fontes oficiais consultadas, evidência empírica levantada e alternativas descartadas.

| Documento | Data | Assunto |
| --- | --- | --- |
| [release-closure-2026-10-04.md](./release-closure-2026-10-04.md) | 2026-10-04 | Nova versão, fechamento das correções, verificações determinísticas e limites dos grades pagos |
| [skill-eval-description-benchmark-2026-09-08.md](./skill-eval-description-benchmark-2026-09-08.md) | 2026-09-08 | Juiz `description`: regressões Filament/Nova 3/3, evidência de output citada, `--judge live` sem credenciais |
| [skill-eval-mock-benchmark-2026-09-08.md](./skill-eval-mock-benchmark-2026-09-08.md) | 2026-09-08 | Primeiro benchmark do harness (`--judge mock`): taxas por skill, lacunas do mapa de keywords e o que o mock não prova |
| [skills-audit-v2.html](./skills-audit-v2.html) | 2026-08-09 | Auditoria de arquitetura (v2) das duas skills do Filament e da `prepare-commit`: oportunidades de aprofundamento, vazamentos de seam e duplicação, com evidência verificada por execução |
| [filament-ui-ux-analysis.md](./filament-ui-ux-analysis.md) | 2026-08-03 | Análise de valor e entrega da skill de UI/UX do Filament, com evidência levantada por execução direta |
| [skills-audit.md](./skills-audit.md) | 2026-07-13 | Auditoria das skills do repositório: descoberta, precisão, uso de contexto, segurança e verificabilidade |
| [sdd-workflow-research.md](./sdd-workflow-research.md) | 2026-07-13 | Pesquisa oficial sobre o Kiro usada para reformular a skill `sdd-workflow` |

Estes documentos são registros do momento em que foram escritos. Nomes de skills, caminhos de arquivo e conclusões refletem o estado do repositório naquela data e não são atualizados depois — para o estado atual, consulte `docs/adr/`, `CONTEXT.md` e as próprias skills.
