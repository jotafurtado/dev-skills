# Revisão independente das avaliações de modelo

A pontuação automática favorece a skill, mas contém aprovações sem evidência suficiente. Os oito textos são propostas sobre fixtures sintéticos, não implementação nem teste de integração. A leitura de todos os grading.json registra 21/21 asserções com skill e 18/21 sem skill; esses números são do avaliador, não uma revalidação independente.

## Cobertura e limites

Foram lidos SKILL.md, evals/evals.json, quatro fixtures, oito response.txt e seus grading.json; todos os 60 registros de trigger do final e os 30 do holdout-full-catalog. Não foram executados testes de app nesta revisão. Os números 0.198.0/0.198.1 são evidência ficcional do caso 002. O Core instalado em .agent-native-fixture/pristine é 0.209.2, portanto não comprova compatibilidade com essas versões nem com os casos sem versão. Sua declaração dist/client/use-action.d.ts:124,140 confirma a existência atual de useActionQuery/useActionMutation; dist/client/chat/runtime.d.ts:671 confirma createHttpAgentChatRuntime. Existência de símbolo não comprova composição, autorização ou comportamento de sync no app.

## Achados

1. **Caso 001: escopo de leitura e entradas inválidas não sustentam o passe integral.** output-001-with_skill/outputs/response.txt:18-19 exige ownership para a mutação, mas :25 apenas manda buscar a lista, sem filtro pelo ator. grading.json aprova a asserção 2, que exige escopo de leituras e escritas. :33-36 propõe sucesso e caller negado, sem caso concreto de entrada inválida; a asserção 5 também passa. O mesmo requisito de entrada inválida falta no controle, embora ele receba passe na asserção 5. O controle aborda filtro de listagem explicitamente. A exigência está em skills/agent-native/evals/evals.json:10-14.

2. **Caso 003: a nota do controle aceita uma escolha genérica como escolha documentada.** output-003-no_skill/outputs/response.txt:3-6 diz apenas Toolkit UI; não escolhe uma família específica adequada ao layout, mas grading.json marca a asserção 1 como verdadeira. Na resposta com skill, :5 lista três componentes e três APIs sem fonte instalada; :10 acrescenta access/authorize/assertAccess como alternativas, sem contrato demonstrado. :14 suspende a implementação até verificar versões e tipos, o que é correto e limita essas sugestões a pistas. Não há prova de que todas se componham no app alvo. A referência à autorização é uma orientação de segurança, não validação desses três nomes como APIs.

3. **Caso 004: passe não comprova investigação do primitivo nem checagem de versão.** A asserção 1 exige investigar o primitivo instalado; ambas as respostas mandam corrigir o import sem apresentar essa investigação. A asserção 4 exige checagem de versão para sync; não consta em nenhuma das respostas. Mesmo assim, ambos os grading.json aprovam as duas. Na resposta com skill, :10 mistura Hypothesis/Verified e afirma causalidade de quebra do roteamento; :36 prescreve substituir queries com garantia de participação automática no refresh. O fixture declara que causas permanecem hipóteses e não fornece fonte instalada. No controle, :20-24 chama sintomas e inferências de Verified Framework Behavior; duplicação de comandos e cache stale são observações do fixture, não uma prova geral de semântica do framework. São falhas de calibração da certeza, não resultados de runtime.

4. **Caso 002: conclusão de compatibilidade é limitada corretamente.** Ambas as respostas preservam pins, rejeitam upgrade não solicitado e deep import, e reconhecem ausência de tipos. A resposta com skill lista resoluções exatas, mas não reproduz nem contrasta explicitamente a constraint ^0.198.0; seu passe na asserção 1 é mais generoso que a formulação literal. Nenhuma das versões sintéticas deve ser relatada como versão realmente testada.

## Triggers, todas as repetições

| Conjunto | Tentativas | Acertos | Falhas | Taxa |
| --- | ---: | ---: | ---: | ---: |
| final, existing20, três repetições | 60 | 58 | 2 | 96,67% |
| holdout-full-catalog, dez queries, três repetições | 30 | 29 | 1 | 96,67% |

Todas as falhas são falsos negativos, com selected_skills vazio e expected_should_trigger=true:

- final/agent-native/trigger-002-run-2/grading.json: “Pick the right @agent-native/toolkit chat surface for a full-page assistant.” As repetições 1 e 3 passam.
- final/agent-native/trigger-006-run-1/grading.json: “Customize AgentSidebar in an Agent-Native app without losing threads or attachments.” As repetições 2 e 3 passam.
- holdout-full-catalog/agent-native/trigger-000-run-1/grading.json: “No app @agent-native/core, a lista atualiza após clique, mas não após uma escrita de outra aba. Corrija o opt-in de sync.” As repetições 2 e 3 passam.

Os prefixos final e holdout-full-catalog acima significam maintenance/evals-out/agent-native-real-app-final e maintenance/evals-out/agent-native-real-app-holdout-full-catalog. Todos os caminhos output-... são relativos ao diretório agent-native do final. Os 90 registros não mostram falha persistente de uma query nas três repetições; mostram seleção instável em três queries positivas. Não sustentam alegação de 100% de seleção nem de validação comportamental do app.


## Reavaliação final-v2

Revisão distinta, preservando a análise v1 acima. Foram relidos os oito response.txt e grading.json de maintenance/evals-out/agent-native-real-app-final-v2/agent-native e todos os 90 grading.json de trigger, incluindo maintenance/evals-out/agent-native-real-app-holdout-v2/agent-native. A skill agora exige separar sintomas, causas suspeitas, evidência instalada e comportamento executado. Esta execução não permite atribuir causalidade ou melhoria estatística à alteração de instrução.

### Resultados registrados e divergências de avaliação

- **Pontuação e infraestrutura:** com skill, 20/21 asserções aprovadas e três de quatro casos aprovados. Sem skill, 15/16 asserções aprovadas nos três casos efetivamente graduados e dois de três casos aprovados. output-001-no_skill/grading.json tem infrastructure=protocol, passed=null e não tem assertion_results nem summary. Há resposta e raw_reply do juiz, mas não há nota validada; não se deve convertê-lo em reprovação ou aprovação. benchmark.json também o registra como infrastructure_skipped=1.
- **001, candidato, aprovação excessiva:** output-001-with_skill/outputs/response.txt:11-12 exige identidade e ownership na escrita; :17 manda listar tarefas, sem explicitar escopo de leitura. grading.json aprova a asserção 2 que exige leituras e escritas. A tabela :30-34 não contém cenário de entrada inválida, mas passa a asserção 5. A nota :36 reconhece importações não verificadas. O controle descreve ownership também para fetching e nega visualização de tarefas de terceiros (:14-18, :31-32), mas não declara falta de compatibilidade/API instalada nem propõe teste concreto de entrada inválida; isso é leitura independente do texto, sem substituir o resultado protocol.
- **002, candidato, passe factual indevido:** output-002-with_skill/outputs/response.txt:9 menciona apenas Toolkit 0.198.1. Core 0.198.0 e constraint ^0.198.0 estão ausentes da resposta inteira. grading.json aprova a asserção 1 mesmo assim. A orientação de composição local, sem upgrade ou deep import, permanece adequada. No controle, :5 afirma que inventário de skills e falha de build confirmam o que é exportável; esses elementos não substituem tipos/exports. :12-14 condiciona a troca de import à descoberta de export real e prevê fallback local; não afirma que o substituto já foi verificado.
- **003, candidato, falha reconhecida:** output-003-with_skill/outputs/response.txt:4-5 fornece componentes e imports sem a verificação instalada exigida; grading.json corretamente reprova a asserção 5. Isso diverge da ressalva explícita da resposta com skill na v1. :4-5 não explica preservação dos adaptadores dos controles locais, apesar do passe na asserção 4. O controle novamente recebe passe na asserção 1 dizendo somente existing Core-backed chat and Toolkit UI (:4), sem escolher família concreta para o layout; na asserção 3, a evidência :10 aborda autorização, sem estabelecer credenciais no servidor. A rejeição a API keys em local storage aparece em :6, mas não completa sozinha o requisito server-side.
- **003, limite da checagem atual:** no Core 0.209.2 instalado, dist/client/agent-chat/index.d.ts:20 exporta useChatThreads e :35 reexporta chat/runtime.js, que declara createHttpAgentChatRuntime em dist/client/chat/runtime.d.ts:671. Portanto o import proposto em :5 encontra suporte nesse pacote atual. Isso não valida a versão desconhecida do fixture, a composição com Toolkit nem streaming executado. Igualmente, dist/client/hooks/index.d.ts:9 exporta useActionQuery/useActionMutation, confirmando o caminho citado no candidato 001 apenas nesta versão instalada.
- **004, aprovação excessiva e certeza ainda mal calibrada:** ambos os grading.json aprovam investigação do primitivo instalado (asserção 1), mas as respostas apenas identificam e recomendam trocar o hook local, sem evidência da investigação. Ambos aprovam a asserção 4 sem checagem de versão. output-004-with_skill/outputs/response.txt:9-11 usa Hypothesis verified by file context e afirma que bypass quebra a integração; o fixture informa o import e sintomas, não comprova essa causalidade. :27-29 acrescenta que escritas próprias acionam refetch contínuo, sem trace. :52-55 propõe teste de escrita pelo agente, mas não teste separado de escrita pela UI, apesar do passe na asserção 6. O controle rotula :17-20 como Verified Framework Behavior, misturando sintomas observados na narrativa e causas não verificadas; :46-57 testa escrita pela UI e segundo usuário, mas não escrita local pelo agente. Também não apresenta implementação explícita de limpeza de seleção no plano, embora a verifique no cenário :46-48. Nenhuma dessas propostas equivale a teste executado.

Os caminhos output-... desta seção são relativos a maintenance/evals-out/agent-native-real-app-final-v2/agent-native; os caminhos dist/... são relativos a .agent-native-fixture/pristine/node_modules/@agent-native/core. O veredito independente identifica lacunas, sem inventar uma nova nota total para substituir o juiz.

### Triggers v2, todas as repetições

| Conjunto | Tentativas | Acertos | Falhas | Taxa |
| --- | ---: | ---: | ---: | ---: |
| final-v2, existing20 | 60 | 58 | 2 | 96,67% |
| holdout-v2, catálogo completo | 30 | 27 | 3 | 90% |

Todos os erros são falsos negativos com expected_should_trigger=true e selected_skills=[]. Demais 85 registros passam.

- maintenance/evals-out/agent-native-real-app-final-v2/agent-native/trigger-002-run-2/grading.json: “Pick the right @agent-native/toolkit chat surface for a full-page assistant.” Repetições 1 e 3 passam. Mesmo índice de falha da v1.
- maintenance/evals-out/agent-native-real-app-final-v2/agent-native/trigger-006-run-2/grading.json: “Customize AgentSidebar in an Agent-Native app without losing threads or attachments.” Repetições 1 e 3 passam. Na v1, falhava a repetição 1, e não a 2; a divergência é de repetição, sem prova de mudança de capacidade.
- maintenance/evals-out/agent-native-real-app-holdout-v2/agent-native/trigger-000-run-1/grading.json, trigger-000-run-2/grading.json e trigger-000-run-3/grading.json: “No app @agent-native/core, a lista atualiza após clique, mas não após uma escrita de outra aba. Corrija o opt-in de sync.” As três repetições falham. Na v1, apenas a primeira falhava. É falso negativo persistente nesta execução para sync explícito em app confirmado, dentro do escopo declarado da skill.

O total agregado é 85/90 acertos de seleção nesta execução. Não constitui estimativa independente da taxa populacional nem validação de comportamento do app. Os resultados v2 não sustentam alegação de melhoria estatística sobre v1.


## Auditoria final-v3

Versão final auditada separadamente, sem apagar ou selecionar apenas resultados favoráveis de v1/v2. Foram lidos os oito textos e oito grading.json de maintenance/evals-out/agent-native-real-app-final-v3/agent-native, além dos 60 triggers desse diretório e 30 de maintenance/evals-out/agent-native-real-app-holdout-v3/agent-native. A descrição passou a dizer real-time or cross-tab synchronization. Os testes reais de app pertencem a outra matriz e não alteram as notas destes textos sintéticos.

### Resultado automático e erro de protocolo

benchmark.json registra três casos aprovados com skill, nenhum reprovado e um ignorado por infraestrutura; sem skill, três aprovados e um reprovado. A taxa automática 100% com skill usa apenas três casos graduados. output-001-with_skill/grading.json contém infrastructure=protocol e passed=null, sem assertion_results/summary válidos. Sua resposta está disponível e é analisada abaixo; não se deve convertê-la em aprovação nem reprovação do modelo. As asserções graduadas somam 16/16 com skill e 20/21 sem skill. Não são a classificação independente.

### Classificação manual de cada asserção

S = sustentada pelo texto no escopo de proposta, P = parcial, N = ausente ou contrariada. P não significa teste executado. A1…A6 seguem a ordem literal de skills/agent-native/evals/evals.json. Cada célula contém a classificação e linhas de outputs/response.txt. Todos os diretórios output-... nesta seção pertencem a maintenance/evals-out/agent-native-real-app-final-v3/agent-native.

| Resposta | A1 | A2 | A3 | A4 | A5 | A6 |
| --- | --- | --- | --- | --- | --- | --- |
| output-001-with_skill | S :9-13 | P :11-16 | S :12-21 | N :1-33 | S :27-32 | não aplicável |
| output-001-no_skill | P :14-16,22 | P :15,22,30-31 | S :18-23 | N :1-39 | P :29-38 | não aplicável |
| output-002-with_skill | N :6,11 | S :9-13 | S :4-7 | S :4-7 | S :15-17 | não aplicável |
| output-002-no_skill | S :5 | P :5-7,11 | S :10-13 | S :10-13 | P :15-17 | não aplicável |
| output-003-with_skill | P :4 | S :4,9 | S :7,9 | P :8 | N :1-10 | não aplicável |
| output-003-no_skill | P :4,7 | S :7 | P :12-13 | S :8 | S :9 | não aplicável |
| output-004-with_skill | P :9,23 | S :27-31 | P :12-14,33-35 | P :13,16,38 | P :15,24 | P :44-55 |
| output-004-no_skill | P :8,26 | P :9,30,45 | P :10,33 | P :23,35-37 | P :11,27 | P :43-53 |

Fundamento das classificações e divergências frente ao juiz:

- **001:** candidato escopa escrita e resolução contextual, mas não manda filtrar a listagem pelo ator (:16,27); não reconhece ausência de versão/tipos e recomenda APIs diretamente. O controle unifica helper, sem estabelecer um contrato tipado compartilhado; diz autenticar e comparar ownerId, mas não explicita derivação server-side em vez de confiar no ownerId submetido. Seus checks negam acesso e preveem erro de validação, mas não exercitam sucesso via agente nem resultado visível do write feito por ele. O candidato propõe explicitamente taskId ausente/malformado (:32), diferença favorável específica frente a suas versões anteriores, sem evidência de execução. A4 falta em ambos; o juiz reprova A4 no controle e não produz nota protocol válida no candidato.
- **002:** o candidato omite Core 0.198.0 e constraint ^0.198.0; seu passe automático A1 cita somente 0.198.x (:6) e não se sustenta. O controle cita versões e constraint, mas prioriza build/manifest/skills em vez de tornar tipos e exports instalados autoridade explícita; reconhece ausência de declarações, sem deixar claro o contrato público ainda não resolvido. :17 trata como dúvida se ProjectSettingsFilter é fictício, embora o fixture declare que o nome foi inventado. Ambos rejeitam upgrade e import privado corretamente. Runtime behavior until verified against types (:17 do candidato) não deve ser entendido como execução comportamental comprovada por tipos.
- **003:** candidato lista três superfícies (:4), sem escolher composição apropriada para duas colunas; não menciona preservação dos adaptadores dos controles locais e não exige verificar versão/exports antes de implementar. O passe automático A5 cita :1-9, que não contém esse gate. Controle preserva adaptadores e adia código até obter contratos (:8-9), mas permanece genérico quanto à família concreta; também rejeita localStorage sem dizer explicitamente que as credenciais ficam no servidor. Logo os passes automáticos A1 e A3 do controle são mais amplos que a evidência literal. No pacote Toolkit 0.209.2 realmente instalado, dist/app/chat/index.d.ts:16,19 exporta AgentPanel/AgentChatSurface/AssistantChat pelo caminho público app/chat. Isso confirma nomes nessa instalação, não a compatibilidade desconhecida do fixture nem a composição proposta.
- **004:** candidato agora nomeia useAgentRouteState e caminho público (:9), mas não mostra investigação instalada; na instalação Core 0.209.2, dist/client/navigation/index.d.ts:2 confirma esse export. A fonte não valida substituir o hook customizado diretamente sem preservar suas integrações. Nenhum texto exige verificar versão antes do sync, embora ambos recebam passe A4. Ambos reconhecem cache e ação em termos de hipótese/plano, sem rastrear concretamente completion, keys, invalidation e refetch; centralizam tab identity sem tratar request-source/consumo do framework explicitamente. Candidato propõe UI write e segundo tab, mas não agent write local (:44-55); controle não propõe agent write nem execução explícita de escrita em segundo tab/usuário (:43-53). Os passes A6 integrais não se sustentam. No controle, validação contra active project/actor context (:30) não estabelece inequivocamente identidade confiável, leitura escopada e autorização server-side. Seu rótulo Verified Framework Behavior (:13-17) continua misturando sintomas do fixture com causalidade inferida. Candidato usa coluna Hypothesized Cause vs. Framework Contract, mas faz afirmações causais categóricas sobre refresh e loops (:12-15), sem trace/teste.

Não foi calculada pontuação substituta agregada a partir de S/P/N: são avaliações por requisito, úteis para localizar o que o passe automático não comprova. Os tipos atuais consultados estão em .agent-native-fixture/pristine/node_modules/@agent-native/{core,toolkit}; ambos são 0.209.2. Os números 0.198.x permanecem ficcionais do fixture.

### Triggers final-v3, todas as repetições

| Conjunto | Tentativas | Acertos | Falhas | Taxa |
| --- | ---: | ---: | ---: | ---: |
| final-v3, existing20 | 60 | 60 | 0 | 100% |
| holdout-v3, catálogo completo | 30 | 27 | 3 | 90% |
| Total desta execução | 90 | 87 | 3 | 96,67% |

Nenhum trigger tem erro de infraestrutura. As três falhas são falsos negativos da mesma query positiva, expected_should_trigger=true e selected_skills=[], nos arquivos:

- maintenance/evals-out/agent-native-real-app-holdout-v3/agent-native/trigger-002-run-1/grading.json
- maintenance/evals-out/agent-native-real-app-holdout-v3/agent-native/trigger-002-run-2/grading.json
- maintenance/evals-out/agent-native-real-app-holdout-v3/agent-native/trigger-002-run-3/grading.json

Texto literal comum: “Our Agent-Native workspace needs owner-scoped SQL reads and authenticated mutations. Review the installed action context before implementing.”

A query de sync que falhou nas três repetições v2 agora passa nas três repetições v3. A query de SQL/autenticação acima, que passava em v2, agora falha nas três. O holdout permanece 27/30 apesar da troca de descrição; o conjunto principal chegou a 60/60 nesta execução. Isso registra a migração das falhas e o acerto observado, sem alegar melhoria estatística, causalidade da mudança de wording ou cobertura comportamental do app.


## Holdout final cego após congelamento

Correção metodológica: o conjunto anteriormente chamado holdout foi consultado durante ajustes de desenvolvimento e influenciou a descrição de sync entre v2 e v3. Portanto v1/v2/v3 desse conjunto devem ser lidos como validação de desenvolvimento, não teste final cego. Seus resultados permanecem registrados acima, incluindo 27/30 na v3; não foram substituídos por seleção favorável de tentativas.

O novo conjunto maintenance/agent-native/holdout-queries-final.json contém dez queries novas. Segundo o registro de execução, foi criado após o congelamento, sem ajuste posterior da skill. O arquivo maintenance/agent-native/evidence/frozen-skill.json registra frozenAt=2026-10-18T02:44:18.272Z. Nesta auditoria, os seis SHA-256 atuais foram recalculados e conferem integralmente com o registro: SKILL.md e references/actions-data.md, architecture.md, context-sync.md, documentation.md e ui-toolkit.md. Isso comprova identidade atual com o conteúdo congelado, não constitui por si só prova independente da cronologia de criação das queries.

Foram conferidos todos os 30 grading.json e 30 outputs/selection.json em maintenance/evals-out/agent-native-real-app-blind-final/agent-native, três repetições para cada query de índice 000 a 009. Query e expected_should_trigger conferem com holdout-queries-final.json em todos os registros; seleção salva confere com selected_skills e o resultado passed corresponde à comparação esperado/triggered. Não há erro de infraestrutura ou inconsistência nessas verificações.

| Conjunto final | Tentativas | Acertos | Falhas | Taxa |
| --- | ---: | ---: | ---: | ---: |
| Principal original, final-v3 | 60 | 60 | 0 | 100% |
| Novo holdout final cego | 30 | 29 | 1 | 96,67% |
| Composição descritiva | 90 | 89 | 1 | 98,89% |

A única falha é falso negativo em maintenance/evals-out/agent-native-real-app-blind-final/agent-native/trigger-001-run-1/grading.json, com expected_should_trigger=true, triggered=false e selected_skills=[]. Texto literal: “The public Toolkit import in our @agent-native/core application no longer resolves after a lockfile refresh. Inspect the resolved packages and repair the integration without an unrelated upgrade.” As repetições 2 e 3 da mesma query passam. As outras nove queries passam nas três repetições.

O resultado final é 60/60 no principal mais 29/30 no novo conjunto cego, composição de 89/90. Somente as 30 tentativas novas pertencem ao teste final cego; as 60 originais não se tornam cegas por agregação. Isso não elimina os falsos negativos observados anteriormente nem demonstra ganho estatístico ou comportamento correto de runtime. Nenhum conteúdo da skill foi ajustado nesta auditoria.
