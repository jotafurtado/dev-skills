# Nova versão e fechamento de pendências

Data: 2026-10-04

Esta entrega fecha as correções de implementação identificadas nos intents e nas pesquisas. As verificações determinísticas e de instalação passaram. A avaliação paga foi executada e preservada, mas seus grades semânticos não são um certificado de qualidade: há aprovações contestáveis, registradas abaixo. Não foi iniciado outro ciclo de reescrita das skills para aumentar o score.

## Versões

O repositório versiona cada skill, não a coleção inteira.

| Skill | Versão |
| --- | --- |
| `implement-with-subagents` | 1.2.3 |
| `laravel-filament-v5` | 3.3.3 |
| `laravel-filament-v5-ui-ux` | 2.1.3 |
| `laravel-nova-5` | 2.0.2 |
| `prepare-commit` | 1.4.2 |
| `sdd-workflow` | 2.0.1 |

Este registro descreve a verificação anterior ao commit e à publicação. A implementação preservou o índice previamente preparado pelo usuário; o prepare-commit opera com autorização separada.

## Classificação das pendências

A triagem com Jev classificou 98 seções de intents e pesquisas, após excluir oito seções vazias ou de navegação. Nenhum texto foi truncado. Resultado: 29 acionáveis, 12 mistas, 55 de referência e duas concluídas. Foram escaladas 63 seções acionáveis ou incertas; o rótulo do modelo foi usado para localizar trabalho, não para concluir que um achado histórico continuava aberto.

Os problemas do antigo catálogo visual, do query engine e dos transcripts de forward evaluation foram substituídos pela arquitetura de composições da [ADR 0002](../adr/0002-reference-compositions-over-evidence-lookup.md). Não foram recriados componentes retirados apenas para fazer uma auditoria antiga parecer verde. A pesquisa sobre SDD permanece como registro das decisões que já embasaram a skill.

## Correções e achados da auditoria v2

| Achado | Fechamento |
| --- | --- |
| 1. Seam de APIs nas composições de tabela | `references/table.md` encaminha pressupostos de assinatura e versão para o inventário e a verificação da skill core. |
| 2. Pareamento condicionado a disponibilidade indefinida | As duas skills definem a descoberta por arquivo legível e `name` exato, com precedência concreta. O checker de manutenção e os cenários de instalação exercitam esse contrato. |
| 3. Invariantes de segurança duplicadas | A referência de segurança aponta para o invariante canônico no core, mantendo os exemplos aplicáveis. |
| 4. Changelog sobrecarregando o fluxo principal | A implementação atual de `prepare-commit` já encaminha essa ramificação para `references/changelog.md`. |
| 5. Fronteira de commit dependente do host | O fluxo atual usa Git, preserva staged preexistente e condiciona operações ao pedido do usuário; não exige uma API específica de host. |
| 6. Política de idioma duplicada | A decisão fica no Preflight e é reutilizada pelos destinos de texto. |
| 7. Entradas de formulário e shell sobrepostas | Estrutura de página e tratamento de campos têm handoffs explícitos; as variantes do shell distinguem `When` e `Not when`. |
| 8. Inventário no payload instalado | Os ativos de manutenção ficam fora de `skills/`; o install smoke rejeita vazamentos de inventário e scripts. |
| 9. Description longa do core | A description atual já estava reduzida. Não foi reescrita a partir de falhas de validação. |
| 10. Pesquisa e tooling antigos | A análise antiga está marcada como substituída; o sincronizador atual se chama `sync_screenshot_inventory.py`. |

A repetição de exemplos autocontidos, como `ActionGroup`, foi mantida quando necessária para que a composição possa ser colada. Não foram fundidas as duas skills Filament.

## Validador e harness

- O validador usa YAML real, com dependência fixada em `package-lock.json`, em vez de converter toda entrada para string.
- Tipos dos campos padrão, mappings de metadata, chaves duplicadas, valores vazios e limites são verificados. A extensão booleana `disable-model-invocation` tem política explícita.
- Fixtures são carregadas pelo conteúdo. Baseline e candidato recebem os mesmos bytes e a mesma instrução base.
- O candidato recebe o `SKILL.md` completo e as referências selecionadas pelo roteamento, sem corte silencioso de 6.000 caracteres.
- JSON inválido, booleanos de tipo errado, resultados ausentes ou duplicados, ranges inválidos, respostas vazias e truncamento são falhas de protocolo/infraestrutura, não falhas da skill.
- O grader retorna IDs de assertivas e intervalos de linhas. O código extrai a citação literal, sem pedir ao modelo que recopie namespaces PHP dentro de JSON.
- Respostas geradas sobrevivem a falhas do grader. Raw replies, duração e telemetria disponível são persistidos; telemetria ausente permanece null.
- `mock` é simulação. `description` é um ativador lexical, não um gerador de evidência de output.
- Há benchmark por skill e resumo do repositório. `--output-only` permite executar apenas outputs. O gate não exige que o baseline passe e não aprova um bucket live inteiramente skipped.

## Verificações comprovadas

| Verificação | Resultado observado |
| --- | --- |
| `python3 -m unittest discover -s tests` | 77 testes passaram. |
| `eval_skills.py validate-datasets` | Todos os datasets válidos: seis skills, 121 queries com train/validation e 23 casos de output. |
| Validador nas seis skills | Todas válidas. |
| Composições Filament | 22 patterns, 76 variantes, nenhuma lacuna de cobertura. |
| APIs Filament | 64 classes e 13 casos de enum resolvidos contra Filament 5.7.6. |
| Instalação limpa | Codex, Claude Code e Cursor; UI/UX separada e pareada com core: seis cenários passaram. |
| Descoberta do sibling | O checker encontrou a skill vizinha pelo contrato de arquivo e nome. |
| Novos fixtures PHP | Os três arquivos passaram em `php -l`. |
| Gate sem credenciais | Seis outputs skipped, zero falhas atribuídas à skill e exit code 1 para o bucket live vazio. |
| Conclusão por SHA | Smoke em repositório Git temporário: objeto commit real, conteúdo integrado e ticket concluído com esse SHA. Não foi criado commit no repositório principal. |

Os cenários de frontier, isolamento de falha, integração, review e conclusão são verificações controladas do modelo de manutenção. Não provam a execução de uma orquestração completa em todos os hosts.

## Avaliação real e seus limites

Modelo: `google/gemini-3.5-flash-lite`, via OpenRouter.

### Ativação

Foram executadas três repetições de cada query: 358 de 363 passaram, sem skips de infraestrutura. As três regressões exigidas passaram em todas as repetições:

- API funcional Filament carrega core, sem UI/UX.
- Polish visual carrega UI/UX, sem core.
- Migração entre projetos confirmados Nova 4 não carrega Nova 5.

Positivos de validação: core Filament 12/12, UI/UX 15/15 e Nova 5 11/15. Todos acima de 0,5. `prepare-commit` ficou em 12/12, portanto o antigo residual lexical abaixo de 0,5 não descreve a ativação deste modelo.

Os cinco misses restantes foram quatro execuções positivas de Nova (lens e testes de autorização) e uma de widgets Filament. Não foram escondidos nem usados para editar descriptions a partir da validação.

### Outputs

A primeira execução gerou 46 respostas, mas 20 grades falharam no protocolo. Os erros incluíam JSON com escaping inválido, texto de assertiva alterado e citações reescritas. Essa execução foi mantida.

Após a mudança para IDs e intervalos, as mesmas 46 respostas foram reavaliadas, sem novas chamadas de geração. Resultado: 45 grades válidos no protocolo e um skip no baseline Nova. Há pelo menos um par candidato/baseline com grade persistido para cada uma das seis skills.

Isso fecha a ausência de uma execução paga e de artefatos comparáveis. Não demonstra que todo verdict está correto. A revisão encontrou, entre outros exemplos:

- `prepare-commit`, caso 1 com skill: o output afirma commit concluído sem ferramentas e não mostra status final; o modelo aprovou a assertiva sobre estado final.
- `implement-with-subagents`, caso 1 com skill: o output pede confirmação para iniciar a wave; o modelo aprovou que workers tinham sido disparados.
- Nova, caso 1 com skill: dois tenants em fixtures e um `not()->toThrow()` não demonstram autorização negada ou isolamento cross-tenant, apesar da aprovação do grader.
- APIs de versão instalada: reconhecer o pin do lockfile não substitui a verificação de assinatura contra vendor source.

Portanto, os scores agregados permanecem **avaliações brutas do modelo**, não métricas de qualidade auditadas. Quotes literais evitam evidência inventada, mas não tornam verdadeiro o julgamento sobre elas. Os gates de qualidade dos outputs não estão todos verdes. A [fase 0006](../plans/0006-record-benchmarks-and-gates.md) explicitamente exclui um segundo ciclo de melhoria para aumentar o score.

A avaliação é de prompts isolados, sem ferramentas. Não prova staging, commits, execução de testes, filas ou compatibilidade completa em um projeto consumidor. As limitações relevantes também estão nos datasets e nos artifacts.

## Artefatos locais e reprodução

Os diretórios gerados são gitignored e ficam fora do payload instalado:

- `maintenance/evals-out/release-2026-10-04/`: geração original, 363 execuções de ativação e primeira tentativa de grading.
- `maintenance/evals-out/release-2026-10-04-regraded/`: grades por intervalos, origem das respostas e timing exclusivamente da reavaliação nos casos de output; os triggers vêm da execução original.
- `maintenance/evals-out/release-protocol-smoke-2026-10-04/`: output-only e gate sem credenciais.

O README contém os comandos permanentes. A reavaliação pontual usou um script descartável que preservou a origem de cada resposta e o timing original; ele foi removido após a execução.

A triagem Jev dos outputs preservou a mesma rubrica antes e depois da mudança do protocolo. Ela serviu para escalonar grades contestáveis, não para certificar automaticamente todos os outputs. A inspeção manual de grades sinalizados encontrou os problemas exemplificados acima; não certificou os demais. Nenhum input do batch foi truncado. Custos Jev observados: US$ 0,0032 na triagem de documentos, US$ 0,0038 na primeira triagem de outputs e US$ 0,0050 na segunda.

## Decisão de encerramento

Manter as correções comprovadas, registrar as falhas e encerrar os ciclos pagos. Não converter um benchmark semântico contestável em selo de qualidade nem reescrever skills apenas para fazer o modelo aprová-las. Uma avaliação operacional completa exige um agente com ferramentas e um projeto consumidor, não mais repetições deste mesmo prompt isolado.
