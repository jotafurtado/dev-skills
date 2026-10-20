# Validação da skill Agent-Native em app real

A candidata passou nos sete testes externos da matriz final, incluindo duas
chamadas reais ao OpenRouter. O controle passou em seis e falhou na navegação
pelo agente. As tentativas anteriores expuseram instabilidade de navegação
também na candidata; a investigação e a rechecagem após reinício ficam
registradas abaixo. Não se conclui superioridade estatística a partir deste par.

A ativação final acertou 60/60 nas consultas originais e 29/30 em dez consultas
novas, executadas depois de congelar a skill. O primeiro conjunto reservado
foi usado durante um ajuste e permanece registrado como desenvolvimento.
Portanto, a ativação não atingiu 100%. Uma falha de protocolo do juiz também
impede tratar todos os cenários textuais como graduados.

## Ambiente e linha de base

Execução local em 17/10/2026, sem deploy ou commit. O scaffold foi criado com o
CLI publicado `@agent-native/core@0.209.2`, Chat standalone, usando Bun para
executar o CLI após a preparação por npx não concluir prontamente. O comando
correto foi executado dentro de `.agent-native-fixture/`, com nome `pristine`;
o CLI rejeita um caminho composto como nome do aplicativo.

| Componente | Versão realmente resolvida |
| --- | --- |
| Node | 24.22.0 |
| Bun / pnpm | 1.4.2 / 10.29.1 |
| Core / Toolkit / AgentKit | 0.209.2 / 0.209.2 / 0.209.2 |
| OTel | 0.1.10 |
| React / React Router | 19.3.1 / 8.1.0 |
| Drizzle / PGlite | 0.45.4 / 0.5.10 |
| Vite / Vitest / Playwright | 8.1.0 / 4.1.12 / 1.64.1 |
| Modelo real e avaliador | google/gemini-3.5-flash-lite, via OpenRouter |

Versões, scaffold e inventário das skills oficiais:
[evidence/environment.json](evidence/environment.json). As constraints geradas
foram preservadas; o [lockfile](implementations/pnpm-lock.yaml) fixa a resolução
usada. Requisitos declarados pelo template não são equivalentes às versões
executadas nesta máquina.

A cópia `pristine` permaneceu sem alterações de implementação. Instalação,
typecheck em desenvolvimento, build e doctor passaram. O comando de testes
original não encontrou testes e saiu com código zero; isso não prova qualquer
funcionalidade. O servidor exibiu a autenticação original, e registro/login por
Better Auth foram exercitados. Os workers trabalharam em cópias enquanto as
checagens originais terminavam, em vez de aguardar todas em série. A preservação
da cópia original e os hashes dos arquivos permitem separar baseline e mudança.
O script de reprodução executa essa preparação sequencialmente.

O ambiente herdado gerou avisos de configuração de produção na primeira
checagem; as verificações locais usaram `NODE_ENV=development`. O executável
compilado foi iniciado e recusou PGlite, retornando 503 na sessão. Isso é um
limite documentado do runtime de deploy, não aprovação de produção. Este
laboratório usa o servidor de desenvolvimento com PGlite.

## Implementações independentes

O pedido comum está em [implementation-task.md](implementation-task.md).
Ambas as cópias tinham as skills oficiais. Somente a candidata recebeu nossa
skill. Os workers medidos começaram sem herdar a conversa do agente principal.
A separação é por instruções e diretórios, não por sandbox de filesystem.

Os deltas completos estão em [candidate.json](implementations/candidate.json)
e [control.json](implementations/control.json), acompanhados das
[respostas dos workers](evidence/candidate-response.md) e
[evidências do controle](evidence/control-response.md). São 26 arquivos na
candidata e 16 no controle, diferença influenciada pela inclusão dos rótulos nas
localizações existentes. Volume de código não foi usado como critério de nota.
Os hashes originais e os conteúdos finais foram conferidos em
[snapshot-verification.json](evidence/snapshot-verification.json).

As duas soluções criam tabelas PostgreSQL por migração aditiva e usam Drizzle,
`defineAction`, `context.userEmail` e filtro de proprietário. UI e agente usam
as mesmas actions. Não foi criada uma API paralela para a lista de tarefas.
A candidata rejeita campos extras em criações; o controle os remove. Em ambos,
o proprietário é derivado no servidor e não pode ser escolhido pelo input.

O mesmo teste externo usa dois adaptadores explícitos para contratos válidos:
a candidata abre `?id=` e conclui por `{ id }`; o controle abre `?taskId=` e
conclui por `{ id, completed: true }`. Os critérios de resultado são idênticos.
O código final dos apps não contém a instrumentação temporária de diagnóstico.

## Matriz executada

| Área | Evidência | Candidata | Controle |
| --- | --- | --- | --- |
| Estrutura | Typecheck, build e doctor; imports públicos resolvidos | Aprovado | Aprovado |
| Actions | Quatro testes PGlite por variante; HTTP real valida entradas e leitura após escrita | Aprovado | Aprovado |
| Autorização | Anônimo rejeitado; outra conta não lista nem conclui tarefa alheia; contexto negado nos testes de handlers | Aprovado | Aprovado |
| UI | Carregando, vazio, criar por Enter, concluir, erro de leitura recuperável e falha de escrita sem sucesso | Aprovado | Aprovado |
| Agente real | Runtime do framework via OpenRouter; argumentos, resultados SSE, leitura posterior e tela | Aprovado | Criação comprovada; fluxo interrompido na navegação |
| Contexto | Seleção publicada e removida ao ir para Home; view-screen autorizado identifica tarefa no fluxo real da candidata | Aprovado | Seleção/limpeza aprovadas; etapa real posterior não alcançada |
| Navegação | Uma chamada de ferramenta, uma mudança efetiva de URL e uma exclusão do comando | Aprovado na execução final | Reprovado |
| Sincronização | UI e segunda sessão do mesmo proprietário convergem; escrita do agente aparece na candidata | Aprovado | UI/segunda sessão aprovadas; conclusão pelo agente não alcançada |
| Interação | Teclado, foco no título aberto e viewport 390×844 sem overflow horizontal | Aprovado | Aprovado |

A lista é privada por proprietário. O teste remoto usa duas sessões do mesmo
proprietário; não concede compartilhamento entre proprietários. Isso preserva
a exigência de isolamento. Não se testou colaboração em uma lista multiusuário.

Resultados externos com a mesma versão final do harness:
[candidate-browser-canonical.json](evidence/candidate-browser-canonical.json),
7/7 em 113,8 segundos, e
[control-browser-canonical.json](evidence/control-browser-canonical.json),
6/7 em 68,5 segundos. Nenhum teste foi ignorado, marcado como flaky ou repetido
automaticamente nessas execuções. O controle voltou a apresentar comando de
navegação ausente, sem consumo pelo navegador; a causa desse sintoma continua
indeterminada. O defeito de precedência abaixo pertence a outra tentativa.

O primeiro par completo permanece em
[candidate-browser-final.json](evidence/candidate-browser-final.json) e
[control-browser-final.json](evidence/control-browser-final.json), também 7/7 e
6/7. O [índice de execuções](evidence/browser-attempts.json) conserva os totais
de todas as execuções com resultado JSON, incluindo falhas e diagnósticos.
Os quatro testes locais de cada app usam SQL real em PGlite, com contexto e
armazenamento de app-state simulados. São complementares aos testes de HTTP,
navegador e chat, e não prova isolada do dispatcher do framework.

Apenas as falhas de transporte de leitura/escrita usadas para testar os estados
de erro da UI são simuladas nos testes externos. O teste real usa o endpoint
`/_agent-native/agent-chat`, duas mensagens na mesma thread e o provedor remoto.
A thread é reaberta na UI, seu texto reaparece e o endpoint de threads confirma
a persistência da conversa.

## Evidência de API, contexto e navegação

Cada worker conferiu contratos instalados, além das skills locais. Os pontos
principais são Core `dist/action.d.ts`, `dist/client/use-action.d.ts`,
`dist/client/use-db-sync.d.ts`, `dist/client/route-state.d.ts` e implementação,
`dist/application-state/index.*`, documentação instalada de banco/autorização e
exports públicos de Core e Toolkit. As respostas dos workers registram as
fontes por API. O typecheck e os builds confirmam resolução dos imports nessa
instalação; não certificam outras versões.

A evidência decisiva do fluxo real da candidata é:

- [Criação pelo agente](evidence/candidate-canonical-agent-create.sse), com argumentos e resultado de `create-task` e `navigate`.
- [Estado e transporte da navegação](evidence/candidate-canonical-navigation-after.json), com comando lido, exclusão única e taskId na rota/contexto.
- [Leitura contextual e conclusão](evidence/candidate-canonical-agent-complete.sse), usando `view-screen` e `complete-task`.
- [Renderização estreita](evidence/candidate-narrow.png), também inspecionada visualmente.

O harness passou a contar mudanças efetivas de URL, além de exigir uma única
exclusão do comando. Eventos repetidos do navegador para a mesma URL não são
tratados como duas navegações. Isso não relaxa a exigência de chamada e consumo
únicos do comando.

## Tentativas, falhas e classificação

| Ocorrência | Classificação e tratamento |
| --- | --- |
| npx demorou; nome com caminho foi rejeitado | Preparação do laboratório; CLI oficial executado por Bun, dentro da pasta correta |
| Symlink de node_modules entre apps não carregou worker Nitro | Infraestrutura do laboratório; instalações independentes com o mesmo lockfile |
| Build e navegador concorrentes produziram reset/timeouts | Execução interrompida; não considerada aprovação; builds e fluxos finais separados |
| Expectativa de `{ value }` e JSON para estado vazio estava errada | Erro do harness; corrigido conforme handlers instalados e retestado |
| Dois eventos para a mesma URL contavam como duas navegações | Erro da medição; agora verifica transição efetiva, chamada de ferramenta e exclusão única |
| Teste disparado antes de o servidor reiniciado estar pronto | Erro de prontidão do harness; guard de sessão adicionado |
| Janela fixa de 800 ms não estabilizou a observação do carregamento | Harness passou a reter a resposta até confirmar o estado pendente |
| Botão de retry desapareceu porque a lista já havia se recuperado | Harness aceita recuperação automática comprovada ou retry explícito, sem esperar por botão removido |
| Entrada de texto antes de o cliente estar pronto não disparou criação | Harness aguarda estado de navegação publicado e botão habilitado antes de enviar por Enter |
| Navegação não chegou ao navegador em tentativas anteriores | Falha observada também na candidata; causa raiz não demonstrada pelas primeiras capturas |
| Controle falhou no fluxo real final e novamente no teste focado | Falha mantida no comparativo; não atribuída à skill por inferência |
| Controle recebe taskId com path /tasks e descarta a seleção | Defeito de precedência na implementação de controle; comando entregue e consumido, rota permaneceu sem taskId |
| Juiz marcou requisitos sem evidência literal e teve falha de protocolo | Avaliação textual/modelo; revisão manual, sem converter skip em passe |
| Executável de deploy rejeita PGlite | Limite do framework/configuração de deploy; fora da certificação local |

A investigação de navegação está em
[navigation-investigation.md](evidence/navigation-investigation.md).
A evidência inicial não permite atribuir a perda do comando a flushSync,
duplicação de módulos, autorização, modelo ou defeito da skill. A criação
persistida e o retorno da ferramenta de navegação não provam mudança de tela.
As tentativas diagnósticas e a rechecagem com reinício são registradas nas
respectivas evidências, sem substituir o run final original do controle.
A candidata repetiu o fluxo real após reinício sem instrumentação
(`candidate-browser-cold-recheck2.json`). O controle instrumentado também passou,
mas esse run é diagnóstico. Após remover o diagnóstico, outra tentativa
demonstrou o defeito de precedência de argumentos descrito acima; essa falha já
possui causa concreta no app e não é a mesma ausência inicial de entrega.

## Correções da skill e ativação

Duas alterações pequenas foram feitas em inglês: distinção explícita entre
sintoma, hipótese, contrato instalado e comportamento executado; e descrição
mais concreta de sincronização em tempo real ou entre abas. A primeira veio de
atribuições excessivas nas respostas textuais; a segunda veio de omissão de uma
consulta de sync em todas as repetições da iteração anterior.

| Iteração | Originais, 20×3 | Primeiro conjunto novo, 10×3 | Observação |
| --- | ---: | ---: | --- |
| v1 | 58/60 | 29/30 | Skill antes das correções desta execução |
| v2 | 58/60 | 27/30 | Parágrafo de limites de evidência |
| v3 | 60/60 | 27/30 | Descrição de sincronização mais explícita |

Nesse primeiro conjunto novo, as três falhas v3 são da consulta sobre SQL com escopo
por proprietário e mutações autenticadas. A consulta de sync que falhava em v2
passou em v3, enquanto outra deixou de passar. O total reservado não melhorou.
Isso não demonstra causalidade nem superioridade de uma redação. Como uma
falha desse conjunto influenciou a redação v3, ele deixou de ser um holdout
cego. Essa limitação não foi corrigida apenas renomeando o resultado.

A skill foi congelada, com hashes de núcleo e referências em
[frozen-skill.json](evidence/frozen-skill.json). Só então foram escritas e
executadas dez consultas inéditas em `holdout-queries-final.json`. Nenhum
resultado delas foi usado para alterar a skill. Esse holdout final acertou
29/30, sem falhas de infraestrutura. Houve uma omissão isolada na consulta
sobre import público e atualização de lockfile, na primeira repetição; as
outras duas passaram. O total final é 89/90, e não 100%.

Todas as repetições foram preservadas em `evidence/activation-*`, incluindo um
run diagnóstico reservado com catálogo incompleto. Esse run foi repetido com o
catálogo concorrente completo e não é o resultado principal. Não se escolheram
as melhores repetições por consulta.

O [relatório manual](evidence/model-review.md) revisa todos os textos e triggers
de cada versão e do holdout final. Na v3, `output-001-with_skill` não recebeu nota válida por erro
de protocolo. Os demais passes do juiz não são certificados: há omissões de
versão, escopo de leitura e validação comportamental mesmo em textos aprovados.
Os casos sintéticos com 0.198.x não são evidência de compatibilidade executada;
a instalação realmente testada é 0.209.2.

## Reprodução e entrega

Os comandos estão no [README](README.md). `prepare.mjs` recria o scaffold, aplica
o lockfile e os deltas conferindo hashes, e executa as verificações em sequência.
Os comandos equivalentes foram executados manualmente nesta sessão; o script
completo não foi repetido sobre outra instalação limpa. Os scripts passaram na
checagem sintática e os hashes de replay foram validados.

Aplicativos, dependências, banco e artefatos brutos permanecem em
`.agent-native-fixture/`, ignorada por Git e Graphify. As evidências nesta pasta
não contêm a chave OpenRouter. A busca exata da credencial nos 1.055 arquivos
públicos compilados encontrou zero ocorrências, conforme
[client-secret-scan.json](evidence/client-secret-scan.json). Traces de navegador
ficam desativados para evitar conservar cookies nas evidências entregues.

Validação estrutural da skill e dos datasets aprovada. Graphify foi atualizado
por AST e `git diff --check` foi executado. As alterações anteriores de AGENTS.md,
README.md, `.codex/`, outras skills e fixtures foram preservadas. Nada foi
commitado, enviado a terceiros por mensagem ou publicado.
