# Verificação da skill Agent-Native

Data: 2026-10-17.

Registro da verificação inicial, anterior ao laboratório executável. A execução
posterior com app real está documentada em [report.md](report.md), com comandos,
testes e evidências nesta pasta. As limitações abaixo descrevem somente a etapa
inicial e não devem ser usadas como resultado do laboratório.

## Entrega

- Skill em inglês com núcleo comportamental curto e cinco referências temáticas.
- Catálogo por finalidade, com componentes, responsabilidade de pacote e fontes.
- README de instalação e integração à tabela principal, preservando alterações anteriores.
- Vinte consultas de ativação, quatro cenários e quatro fixtures sintéticas.

O conteúdo cobre fundamentos e UI. Integrações avançadas, operação e deploy
recebem encaminhamento documental. Nenhum app foi criado ou executado para esta
verificação; as fixtures não constituem exemplos executáveis do framework.

## Verificações estruturais

- `node maintenance/validate_skill.mjs skills/agent-native`: aprovado.
- `python3 maintenance/eval_skills.py validate-datasets`: aprovado.
- `git diff --check`: aprovado.
- Links locais dos sete documentos Markdown: resolvidos.
- Fontes externas: páginas oficiais em inglês e fontes oficiais do GitHub
  verificadas durante a pesquisa e a checagem de links. O endereço de
  documentação de customização estava indisponível e foi substituído por um
  permalink da skill oficial correspondente.
- A descrição usa YAML em uma linha porque o parser atual do avaliador de
  ativação não interpreta escalares multilinha. O validador estrutural aceita
  ambos. Nenhum código do avaliador foi alterado.

## Avaliação com agentes e ferramentas

Foram produzidas oito respostas: quatro com a skill e quatro sem ela. Cada par
recebeu a mesma fixture, sem navegação externa, instalação de dependências ou
acesso a um app real. Workers foram reutilizados somente dentro da mesma variante.

A revisão qualitativa do agente principal encontrou respostas seguras nas duas
variantes. Com a skill, as respostas acrescentaram nomes e fronteiras de
componentes, distinção entre constraints e versões resolvidas, caminhos de
contexto e sincronização, e obrigações de providers/adapters. Isso não estabelece
superioridade estatística nem comprova uma integração funcional.

Artefatos locais, ignorados pelo Git:

- `maintenance/evals-out/agent-native-tool-eval-v1/review.html`: visualizador dos oito resultados.
- `maintenance/evals-out/agent-native-tool-eval-v1/review-notes.md`: comparação qualitativa.
- `maintenance/evals-out/agent-native-tool-eval-v1/case-*/`: prompts, respostas e metadados.

## Avaliação por modelo

O harness existente executou o modelo configurado
`google/gemini-3.5-flash-lite`, sem ferramentas, usando suas próprias respostas
e classificações como evidência de avaliação.

- Ativação: 58 acertos em 60 execuções, com três repetições por consulta.
- Treino: 35/36. Validação: 23/24. Nenhuma falha de infraestrutura nesse run.
- Houve uma omissão isolada em seleção de chat Toolkit e outra em customização
  de AgentSidebar. As duas consultas acertaram nas outras duas repetições.
- O avaliador automático atribuiu aprovação integral a 3/4 respostas com skill
  e 2/4 sem skill. Esses números não são métricas certificadas: a revisão
  encontrou pelo menos uma atribuição excessiva, no cenário 3 com skill, cujo
  texto não exige explicitamente conferir exports/providers instalados.
- No cenário 1, o modelo leve omitiu a ressalva sobre compatibilidade de API.
  O critério de conclusão do núcleo foi reforçado para exigir essa declaração
  quando faltam evidências da instalação. Uma nova execução pareada focada
  ainda apresentou a omissão nas duas variantes. Essa limitação permanece
  documentada; as respostas dos agentes com ferramentas declararam a ausência
  de evidências de versão.

Artefatos: `maintenance/evals-out/agent-native-live-v2/` e
`maintenance/evals-out/agent-native-focused-v3/`. A execução inicial
`agent-native-live-v1` foi interrompida após identificar a leitura incorreta da
descrição YAML multilinha e não representa a versão entregue.

O classificador lexical também foi executado. Seu resultado final foi 30/60,
com rejeição de todas as consultas positivas por sobreposição com cláusulas
negativas. Ele não interpreta adequadamente esse domínio e não foi usado para
atestar ativação por modelo. Seus artefatos ficam em
`maintenance/evals-out/agent-native-description-v2/`.

## Limitações e manutenção

Não foram executados typecheck, build, navegador ou chamadas reais de actions de
um app Agent-Native. Os cenários avaliam orientação e limites de evidência.
Resultados de avaliações geradas por modelo precisam de revisão contextual.

`graphify update .` foi tentado, mas o executável aponta para um interpretador
Python removido. O grafo não foi atualizado e a instalação global não foi
modificada. A consulta inicial usou leitura direta do grafo como fallback.

As fontes e o commit inspecionado estão registrados na referência
`skills/agent-native/references/documentation.md`. Ao alterar comportamento ou
catálogo, reavaliar os cenários afetados e conservar a distinção entre fonte
documental, hipótese, resposta gerada e execução comprovada.
