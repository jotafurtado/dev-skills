# Investigação da navegação no teste real

## Conclusão

A causa raiz ainda não está demonstrada. A falha observada no controle fica entre a execução da ação no servidor e a leitura do comando pelo navegador. O material disponível não justifica corrigir o roteador, trocar a aba, alterar autenticação ou atribuir o resultado a uma corrida.

Esta investigação foi somente leitura dos aplicativos e do pacote instalado. Nenhum arquivo dos aplicativos ou do pacote foi alterado e nenhum teste adicional foi executado.

## Evidência observada

- `.agent-native-fixture/evidence/control-final-agent-create.sse:33-35`: o agente chama `navigate` com `/tasks?taskId=...`, e recebe exatamente o retorno previsto pela ação atual, `Navegação solicitada.`. A ação tem `await writeAppStateForCurrentTab(...)` antes desse retorno. Portanto, a execução não falhou visivelmente antes do retorno do helper.
- `control-final-navigation-after.json`: o navegador permanece em `/tasks`, publica o estado sem seleção e recebe repetidamente `missing` para `navigate:d5ba00b6-56fe-468d-9d5e-802447df09ba`. As consultas finais ao comando global e ao comando dessa aba retornam `null`. O trecho capturado não contém DELETE desse comando.
- `candidate-final-navigation-after.json`: uma consulta recebe o comando com `_writeId`, o cliente envia DELETE e a URL passa a `/tasks?id=56739cbf-f244-4f2e-885d-68d6ef17874b`. O aviso de `flushSync` aparece nessa sequência bem-sucedida, depois da recepção/consumo do comando. Não explica a ausência do comando no controle.
- A versão atual de `candidate/actions/navigate.ts` é idêntica à cópia `candidate-navigate-before-debug.ts`. A melhora após instrumentação/HMR não constitui uma alteração de código permanente capaz de explicar a correção.

## Caminho do código oficial instalado

Referências abaixo relativas a `control/node_modules/@agent-native/core/dist/` dentro de `.agent-native-fixture/`.

1. `agent/production-agent.js:8125-8132` normaliza `body.browserTabId`, usa o contexto como fallback e registra o resultado em `requestRunCtx.browserTabId`. `:6175-6180` preserva o contexto e seu `run` na execução da ação.
2. `application-state/script-helpers.js:3-19` resolve o identificador de sessão pelo contexto, capacidade ou usuário ambiente. `:68-86` normaliza a aba e gera `key:tabId`. `:105-107` escreve o comando usando a aba do contexto. `:24-28` aguarda `appStatePut`.
3. `application-state/store.js:86-96` aguarda um INSERT/UPSERT em `application_state`, com chave composta por `session_id` e `key`, e só então emite a mudança. A leitura em `:50-58` exige a mesma sessão e a mesma chave.
4. `client/route-state.js:204-226` monta o comando por aba; o fallback global é desativado por padrão. `:151-165` consulta o comando. `:175-190` apaga o comando recebido e invoca `onCommand`. Logo, comando ausente interrompe o caminho antes da chamada de navegação e antes de `flushSync`.
5. `server/request-context.js:109-122` guarda o AsyncLocalStorage em `globalThis.__agentNativeRequestContextAls`. A simples existência de mais de uma importação do módulo não prova divergência de contexto.
6. `server/action-discovery.js:255-272` importa ações via `importRuntimeSourceModule`. `server/runtime-source-module.js:11-25` tenta importação nativa e só usa Jiti em erro de extensão TS. Há superfícies diferentes de carregamento a comparar, mas nenhuma captura atual identifica qual delas executou a ação problemática.
7. `db/client.js:1722-1734` possui override de executor por AsyncLocalStorage local ao módulo; os clientes PGlite, por sua vez, usam registros no objeto `process` (`:215-225`). Esses detalhes impedem concluir simplesmente que módulos duplicados equivalem a bancos duplicados.

## Diagnóstico mínimo recomendado

No controle, instrumentar uma única execução, sem HMR intermediário, e guardar apenas metadados não secretos:

1. Na entrada da ação, registrar PID, URL do módulo, `_writeId`, aba normalizada e um hash da identidade/sessão. Não registrar cookie, token, configuração bruta ou URL de banco.
2. Imediatamente após o write, ler o mesmo comando no mesmo contexto e registrar somente presença e `_writeId`. Isso separa ausência na escrita de divergência na leitura HTTP posterior.
3. No handler HTTP de application-state, registrar PID, aba/chave consultada e hash da mesma identidade/sessão; comparar com o write. Se necessário, registrar somente um hash da identidade do banco configurado e um identificador do executor, nunca a URL ou credenciais.
4. Correlacionar INSERT, SELECT e DELETE pela chave e pelo `_writeId`. Capturar a execução desde antes da ação, sem lacunas. Um DELETE de outro consumidor precisa de evidência própria.
5. Repetir após reinício limpo com os mesmos arquivos, antes de experimentar alterações. HMR pode mudar carregamento e estado; a comparação atual não controla essa variável.

Se write e read imediato coincidirem, mas o GET HTTP não, a correção deve atingir a diferença comprovada de sessão, chave, executor ou banco. Se o read imediato já falhar, investigar o write/executor. Se ambos enxergarem o comando e o cliente não navegar, somente então investigar consumo e roteamento. Não há base atual para prescrever um patch específico de produção.

## Evidência adicional após reinício

- `candidate-browser-cold-recheck2.json` registra o teste real completo como `passed`, sem retries, com duração do teste de 110.227 ms. Conforme a execução registrada pelo responsável pelo teste, o candidato foi reiniciado com a ação original, sem instrumentação e sem HMR durante a execução. Isso demonstra que o sucesso não depende da presença dos logs temporários.
- `control-browser-diagnostic.json` registra o mesmo fluxo real como `passed`, sem retries, com duração do teste de 97.242 ms. Nessa execução o controle foi reiniciado com diagnóstico temporário na ação.
- `.agent-native-fixture/control-dev-diagnostic.log:39`, marcador `[lab-navigate-control]`, registra `actionUser` e `stateUser` iguais, aba `a4e5c48a-a21c-458d-b8b4-026fb3b275d7`, leitura de navegação `{view: tasks, path: /tasks}` e comando armazenado em `navigate:a4e5c48a-a21c-458d-b8b4-026fb3b275d7`. O comando contém `/tasks?taskId=c9d308b6-2b8f-4a34-afd0-d7e100b17c61` e `_writeId` `59cf52e0-aeea-4e67-9cfa-447dbb9daf61`.
- Essa captura confirma coincidência de usuário, aba e armazenamento nessa execução bem-sucedida. Ela não reconstrói os metadados internos da execução inicial que falhou.

O resultado inicial do controle, 6/7, permanece preservado como evidência distinta. A execução completa `control-browser-canonical.json`, após remoção dos diagnósticos, também terminou em 6/7. Em `control-canonical-navigation-after.json`, as consultas voltam a indicar comando ausente, sem DELETE e sem seleção na URL. Esse resultado repete o sintoma inicial; não demonstra sua causa raiz. Houve ainda uma execução intermediária em que o fluxo real passou, preservada em `control-browser-verified.json`, cuja falha foi de medição da recuperação da lista.

## Defeito distinto comprovado no controle sem instrumentação

A execução `control-plain-restart` revelou um defeito de precedência de argumentos do aplicativo de controle. Ele explica esta nova tentativa, mas não explica retroativamente o comando ausente em `control-final`.

- `control-plain-restart-agent-create.sse:33-35`: `navigate` recebe simultaneamente `view: tasks`, `taskId: de2757f7-ca6a-406a-8c21-c7db56ed2a13` e `path: /tasks`. O retorno informa `path: /tasks`.
- `control/actions/navigate.ts:17-20`: a ação valida a propriedade da tarefa, mas só constrói uma URL com `taskId` quando `args.path` está ausente. Com `/tasks` explícito, mantém esse caminho e inclui o `taskId` apenas como campo separado no comando.
- `control/app/hooks/use-navigation-state.ts:35-36`: o cliente prefere `command.path` a `pathForCommand(command)`. Assim, o campo separado `taskId` não participa do caminho quando existe `path: /tasks`.
- `control-plain-restart-navigation-after.json`: o GET devolve o comando com ambos os campos, `_writeId: 4226378f-e788-48f8-a96b-f96eacf1a007`, e há exatamente um DELETE correspondente. A URL permanece `/tasks`, conforme o caminho efetivamente solicitado. A entrega funcionou; a seleção da tarefa foi descartada pela precedência dos argumentos.
- `candidate/actions/navigate.ts:30-32`: quando `args.id` existe, o candidato reconstrói `/tasks?id=...` mesmo com `args.path` presente. Portanto, não possui essa mesma precedência nessa combinação de argumentos.

Se esse aplicativo fosse objeto de correção, a mudança mínima seria definir uma precedência explícita entre identificador da tarefa e caminho, ou rejeitar combinações conflitantes. O baseline medido não foi alterado. A execução inicial `control-final`, na qual o SSE já continha o caminho completo com `?taskId=...`, continua classificada separadamente como ausência de entrega sem causa raiz demonstrada.
