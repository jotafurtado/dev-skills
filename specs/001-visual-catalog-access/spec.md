# Feature Specification: Acesso ao catálogo visual da skill Filament 5 UI/UX

**Feature Branch**: `001-visual-catalog-access`

**Created**: 2026-08-04

**Status**: Draft

**Input**: User description: ".docs/FILAMENT_UI_UX_ANALISE.md — análise de valor e entrega da skill `laravel-filament-5-ui-ux`, com evidência empírica levantada por execução direta"

## Contexto

A skill `laravel-filament-5-ui-ux` entrega valor real através da prosa das 9 referências e dos dados dos 22 patterns do catálogo. A camada de acesso a esse conteúdo — o script de consulta, o passo obrigatório do SKILL.md e o modelo de dimensões — hoje trabalha contra ele: seleciona o pattern errado sem avisar, exige um vocabulário indescobrível, e descreve como obrigatório um passo que nenhuma das 45 execuções gravadas executou.

Esta feature corrige a camada de acesso. **O conteúdo de composição visual não é tocado.**

O consumidor da skill é um agente de coding. Ao longo desta spec, "o agente" significa esse consumidor, e todo requisito é redigido como comportamento observável por ele.

## User Scenarios & Testing *(mandatory)*

### User Story 1 - Escolher um pattern sem carregar o catálogo inteiro (Priority: P1)

Um agente precisa compor uma superfície Filament 5. Ele identifica a superfície e o objetivo do usuário, consulta um índice compacto que lista todos os patterns revisados com suas dimensões, e só então abre a entrada completa do pattern que selecionou. O vocabulário aceito está visível no próprio índice, sem exigir leitura exploratória.

**Why this priority**: é a via primária de uso da skill. Hoje ela não existe de forma barata — a única fonte é um arquivo de 78 KB, e as 45 execuções gravadas mostram que os agentes o carregam inteiro. Sozinha, esta história já entrega uma skill utilizável.

**Independent Test**: dado apenas o índice e o SKILL.md, um agente consegue nomear o pattern correto e o vocabulário exato para três cenários de superfícies diferentes, sem abrir o catálogo completo.

**Acceptance Scenarios**:

1. **Given** um agente com a skill instalada e uma tarefa de composição de formulário, **When** ele segue o fluxo de decisão do SKILL.md, **Then** o índice compacto é a primeira fonte consultada e contém, para cada pattern, o identificador, as superfícies, os objetivos aceitos, os contextos responsivos, a referência roteada e a contagem de evidências oficiais.
2. **Given** o índice compacto, **When** o agente procura os valores aceitos de uma dimensão, **Then** as listas completas de vocabulário estão no próprio índice, sem necessidade de abrir o catálogo completo.
3. **Given** um pattern selecionado a partir do índice, **When** o agente precisa dos detalhes de composição, variantes, alternativas e evidência, **Then** ele abre a entrada correspondente no catálogo completo e a referência roteada indicada.

---

### User Story 2 - Vocabulário inválido falha de forma visível (Priority: P1)

Um agente informa um termo que não pertence ao vocabulário controlado — um erro de digitação, uma variante ortográfica, um termo inventado. Em vez de receber uma seleção plausível e errada, ele recebe uma recusa que nomeia a dimensão inválida e sugere os termos válidos mais próximos.

**Why this priority**: é o defeito de maior severidade da análise e uma violação direta do Princípio IV da constituição ("helpers determinísticos DEVEM falhar fechado com input inválido"). Um objetivo grafado `organise-stable-groups` em vez de `organize-stable-groups` hoje devolve a paleta de modais e notificações, com trace completo e nenhum aviso.

**Independent Test**: informar um termo inválido em cada dimensão do vocabulário e verificar que nenhuma seleção é produzida e que a mensagem nomeia a dimensão e sugere alternativas.

**Acceptance Scenarios**:

1. **Given** uma consulta com um objetivo que não pertence ao vocabulário, **When** ela é submetida, **Then** nenhum pattern é selecionado, a resposta nomeia a dimensão inválida e lista os termos válidos mais próximos.
2. **Given** uma consulta com termo inválido em qualquer outra dimensão do vocabulário controlado, **When** ela é submetida, **Then** o mesmo comportamento se aplica.
3. **Given** um agente que não conhece o vocabulário, **When** ele pede a lista de termos aceitos, **Then** recebe as listas completas por dimensão, idênticas às do catálogo.

---

### User Story 3 - Uma pergunta sobre celular seleciona o pattern responsivo (Priority: P1)

Um agente descreve um problema de composição em telas estreitas — uma tabela que espreme seis colunas no celular, um painel de indicadores, uma página de detalhe. A seleção retorna o pattern que existe para esse caso, e não uma superfície não relacionada.

**Why this priority**: é o cenário do eval #10 e o assunto dos evals #11 a #13. Hoje uma pergunta de tabela em contexto estreito seleciona `action-feedback-overlays` — modais e notificações — porque `responsive-identity-centred-table`, que carrega 12 evidências oficiais incluindo a evidência de tabela empilhada em celular, está marcado como incompatível com telas estreitas.

**Independent Test**: submeter uma consulta de contexto responsivo `mobile-first` para tabela, painel de indicadores e detalhe de registro, e verificar qual pattern ocupa a primeira posição.

**Acceptance Scenarios**:

1. **Given** uma consulta de superfície de tabela em contexto `mobile-first`, **When** ela é submetida, **Then** `responsive-identity-centred-table` é o pattern selecionado.
2. **Given** uma consulta em contexto `mobile-first` para qualquer superfície, **When** ela é submetida, **Then** os patterns daquela superfície são retornados ordenados, com os que declaram `mobile-first` à frente — nenhuma consulta com vocabulário válido retorna conjunto vazio.
3. **Given** um pattern cuja largura de projeto não inclui telas estreitas, **When** o agente consulta o índice, **Then** essa largura não aparece como critério de filtro, evitando que ele descarte o pattern por esse motivo.

---

### User Story 4 - A release traz evidência pontuada (Priority: P2)

Quem avalia a skill antes de instalar consegue ver, por cenário e por asserção, se o comportamento esperado ocorreu de fato, com a citação do transcript que sustenta cada veredito.

**Why this priority**: o Princípio IV é explícito — "exit code sozinho não é veredito". As 45 execuções gravadas estão marcadas `recorded` e `review_required: true`, o que significa apenas que o processo terminou sem erro. Depende das histórias 1 a 3 estarem prontas, já que pontua o comportamento novo.

**Independent Test**: abrir o registro de execuções e verificar que cada asserção dos 15 cenários carrega veredito e citação.

**Acceptance Scenarios**:

1. **Given** os 15 cenários re-executados contra a skill nova, **When** o registro é gravado, **Then** cada asserção carrega um veredito de aprovação ou reprovação e o trecho do transcript que o sustenta.
2. **Given** um registro em que ao menos uma asserção não foi pontuada, **When** ele é inspecionado, **Then** continua marcado como pendente de revisão.
3. **Given** uma asserção reprovada, **When** o registro é gravado, **Then** a reprovação é preservada como resultado legítimo, sem bloquear a gravação das demais.

---

### User Story 5 - O SKILL.md descreve o fluxo que realmente acontece (Priority: P2)

Um agente lê o SKILL.md e encontra um fluxo executável do começo ao fim, sem passos obrigatórios que falham no ambiente real e sem instruções de manutenção que ele nunca vai executar.

**Why this priority**: o passo hoje descrito como obrigatório usa um caminho relativo que falha a partir de qualquer diretório real de trabalho, e nenhuma das 45 execuções gravadas o executou. A seção de manutenção do catálogo gasta contexto num fluxo que o consumidor nunca roda.

**Independent Test**: ler o SKILL.md do início ao fim e verificar que todo passo é executável a partir de um projeto arbitrário e que nenhum descreve manutenção do catálogo.

**Acceptance Scenarios**:

1. **Given** o SKILL.md, **When** o agente chega ao passo de consulta, **Then** a leitura do índice é apresentada como via primária, e a consulta assistida por ferramenta aparece como alternativa condicionada à disponibilidade de execução, com localização resolvida a partir do diretório instalado da skill.
2. **Given** o SKILL.md, **When** ele é lido inteiro, **Then** não contém instruções de sincronização, geração de folhas de revisão ou validação do catálogo.
3. **Given** o passo de roteamento para as referências, **When** o agente precisa decidir o que ler, **Then** encontra a tabela de cobertura roteada como forma única daquela informação, sem parágrafo equivalente duplicando-a.

---

### Edge Cases

- **Combinação válida sem correspondência exata**: uma consulta com vocabulário inteiramente válido cuja combinação nenhum pattern satisfaz retorna os patterns da superfície ordenados por aderência, e não uma recusa. A mensagem que instruía o agente a abandonar o catálogo e registrar uma lacuna deixa de ser emitida nesse caso — ela era factualmente errada, porque a superfície casava.
- **Superfície inexistente**: uma superfície que não pertence ao vocabulário é tratada como vocabulário inválido (História 2), não como lacuna de catálogo.
- **Índice divergente do catálogo**: se o índice compacto deixar de refletir o catálogo — pattern adicionado, objetivo renomeado, referência roteada trocada —, a verificação do repositório reprova antes do envio.
- **Ambiente sem execução de comandos**: o agente segue pela leitura do índice, que é a via primária, sem degradação de resultado.
- **Ambiente sem inspeção de imagens**: comportamento atual preservado — usa a interpretação revisada local e declara a limitação no trace.

## Requirements *(mandatory)*

### Functional Requirements

**Acesso ao catálogo**

- **FR-001**: A skill DEVE publicar um índice compacto de patterns como via primária de seleção, contendo para cada pattern revisado: identificador, superfícies, objetivos aceitos, contextos responsivos, referência roteada correspondente e contagem de evidências oficiais.
- **FR-002**: O índice DEVE conter as listas completas de vocabulário aceito por dimensão, de modo que nenhuma descoberta de vocabulário exija a leitura do catálogo completo.
- **FR-003**: O índice DEVE ser derivado do catálogo, nunca mantido à mão, e a verificação do repositório DEVE reprovar quando o índice divergir do catálogo em qualquer campo projetado.
- **FR-004**: O índice NÃO DEVE expor a largura de projeto do pattern, para que ela não seja lida como critério de filtro (ver FR-008).
- **FR-005**: O catálogo completo DEVE permanecer a fonte da verdade e a única fonte de detalhes de composição, variantes, alternativas, considerações de acessibilidade e evidência por pattern.

**Vocabulário e falha**

- **FR-006**: Uma consulta com termo não pertencente ao vocabulário controlado DEVE ser recusada sem produzir seleção, nomeando a dimensão inválida e sugerindo os termos válidos mais próximos.
- **FR-007**: A skill DEVE oferecer uma forma de listar o vocabulário aceito por dimensão, com conteúdo idêntico ao do catálogo.

**Modelo de dimensões**

- **FR-008**: A largura de projeto do pattern DEVE deixar de ser uma dimensão de consulta e passar a metadado descritivo, deixando de participar da seleção.
- **FR-009**: O contexto responsivo DEVE ser a única dimensão que carrega a exigência responsiva da pergunta.
- **FR-010**: Os contextos responsivos declarados DEVEM descrever com precisão a evidência oficial de cada pattern. `responsive-identity-centred-table` DEVE declarar `mobile-first`, contexto que hoje omite apesar de carregar a evidência de tabela empilhada em celular — é a correção que muda a seleção da História 3. `operational-dashboard` DEVE declarar `mobile-first` pela mesma razão de exatidão descritiva, embora sua superfície tenha um único pattern e a correção não altere qual pattern é retornado. `record-detail-infolist` já declara ambos e não é alterado. Nenhum outro pattern tem seus contextos responsivos alterados.
- **FR-011**: Uma consulta em contexto `mobile-first` DEVE retornar os patterns da superfície ordenados, com os que declaram `mobile-first` à frente, sem eliminar os demais.
- **FR-012**: Todas as dimensões além da superfície — objetivo, fluxo de trabalho, contexto responsivo, forma de informação e relacionamento — DEVEM atuar como preferência de ordenação, e não como eliminação. A superfície é a única dimensão que restringe o conjunto. Consequência: uma consulta com vocabulário válido nunca retorna conjunto vazio para uma superfície que possui patterns revisados, e a recusa por combinação não encontrada deixa de existir como caminho alcançável.

**Superfície da skill**

- **FR-013**: O SKILL.md DEVE apresentar a leitura do índice como via primária e a consulta assistida por ferramenta como alternativa condicionada à disponibilidade de execução, com localização resolvida a partir do diretório instalado da skill, não relativa ao diretório de trabalho.
- **FR-014**: O SKILL.md NÃO DEVE conter instruções de manutenção do catálogo; elas passam a viver na documentação humana.
- **FR-015**: O roteamento para as referências DEVE existir uma única vez, na forma de tabela.
- **FR-016**: A seção de autoridade e escapes e a delegação a `laravel-filament-v5` DEVEM ser preservadas em conteúdo e força — são o ponto mais forte da arquitetura atual e não são alvo desta feature.

**Evidência e release**

- **FR-017**: Os 15 cenários de avaliação DEVEM ser re-executados contra a skill resultante e cada asserção DEVE receber veredito com o trecho de transcript que o sustenta.
- **FR-018**: Um registro de execuções só DEVE deixar o estado de pendente de revisão quando todas as asserções de todos os cenários estiverem pontuadas.
- **FR-019**: Registros de execução anteriores nunca pontuados DEVEM ser removidos, por não constituírem evidência sob o Princípio IV. Na mesma entrega, tanto o documento de release quanto a referência de verificação que ele aponta — `references/release-verification.md`, onde o modelo multiagente de evidência está codificado — DEVEM ser atualizados para não descrever evidência que deixou de existir.
- **FR-020**: A verificação automatizada DEVE cobrir, no mínimo: recusa de vocabulário inválido em cada dimensão, divergência entre índice e catálogo, e seleção do pattern responsivo para uma pergunta `mobile-first` de tabela.
- **FR-021**: A skill DEVE passar a versão 1.1.0, com a documentação de release descrevendo a via primária nova e o veredito dos cenários pontuados.
- **FR-022**: A deriva de documentação DEVE ser corrigida: a estrutura listada na documentação humana passa a incluir os cinco arquivos hoje omitidos, e o campo de escopo do catálogo passa a descrever a cobertura atual, não a anterior à fusão das skills.

### Key Entities

- **Pattern visual**: uma composição oficial revisada do Filament 5. Tem identificador, superfícies em que se aplica, objetivos que atende, formas de informação, relacionamentos, fluxos de trabalho, contextos responsivos, largura de projeto (descritiva), sinais de seleção, quando preferir e quando evitar, alternativas, considerações responsivas e de acessibilidade, evidências oficiais e peso de seleção. São 22, todos com estado revisado.
- **Catálogo**: o conjunto dos patterns mais o escopo declarado. Fonte da verdade.
- **Índice compacto**: projeção derivada do catálogo, com os campos de FR-001 e o vocabulário de FR-002. Via primária de leitura.
- **Vocabulário controlado**: os termos aceitos por dimensão, extraídos do catálogo — 9 superfícies, 30 objetivos, 7 fluxos de trabalho, 34 formas de informação, 24 relacionamentos, 2 contextos responsivos.
- **Cenário de avaliação**: um dos 15 casos com enunciado, saída esperada e asserções. Distinto das 13 consultas de detecção de gatilho, que verificam se a skill deve ou não ser acionada e não fazem parte desta feature.
- **Registro de execução**: o resultado de rodar os 15 cenários contra um agente, com transcript, vereditos por asserção e estado de revisão.

## Success Criteria *(mandatory)*

### Measurable Outcomes

- **SC-001**: Escolher um pattern deixa de exigir a leitura da fonte completa: a via primária de seleção cabe em menos de 10% do volume do catálogo.
- **SC-002**: Nenhum termo fora do vocabulário produz seleção — em 100% das dimensões, um termo inválido resulta em recusa que nomeia a dimensão.
- **SC-003**: O caso do eval #10 — pergunta de tabela em tela estreita — passa a selecionar `responsive-identity-centred-table` em vez de uma superfície não relacionada. Para painel de indicadores e detalhe de registro, os contextos responsivos declarados passam a corresponder à evidência oficial de cada pattern.
- **SC-004**: Toda consulta com vocabulário válido para uma superfície com patterns revisados retorna ao menos um candidato — zero recusas por combinação não encontrada.
- **SC-005**: Todo passo descrito no SKILL.md é executável a partir de um projeto arbitrário, sem depender do diretório de trabalho.
- **SC-006**: 100% das asserções dos 15 cenários têm veredito registrado com citação de transcript; nenhum registro permanece marcado como pendente de revisão.
- **SC-007**: Cada campo do índice compacto corresponde ao catálogo; uma divergência introduzida deliberadamente é detectada pela verificação do repositório.
- **SC-008**: A documentação humana lista todos os arquivos existentes na skill e o escopo declarado descreve as nove superfícies cobertas.

## Assumptions

- O conteúdo de composição visual — as 9 referências e os campos de julgamento dos 22 patterns — está validado e permanece intacto. A feature altera acesso, dimensões e evidência, não recomendações.
- O catálogo não é expandido: nenhum pattern novo, nenhuma superfície nova.
- "Combinação válida sem correspondência" deixa de ser um caminho de erro e passa a degradar para candidatos ordenados. Esta transição não recebe verificação automatizada dedicada, por decisão explícita — as três verificações de FR-020 foram consideradas suficientes.
- A pontuação dos cenários usa um único agente. Reprovações são resultado legítimo: a análise prevê que o cenário #10 provavelmente reprova no eixo de evidência de imagem, e um registro honesto de reprovação atende ao Princípio IV melhor do que 15 aprovações forçadas.
- Registros de execução anteriores de outros agentes são removidos por nunca terem sido pontuados. A cobertura multiagente pode voltar em entrega futura.
- `laravel-filament-v5` não é alterada: seu contrato de delegação descreve autoridade sobre descoberta e composição visual, sem referência ao passo obrigatório ou à ferramenta de consulta, e sobrevive intacto à mudança.
- Instalar a skill em `~/.claude/skills/` é ação do autor fora do repositório e não faz parte da entrega, ainda que hoje `laravel-filament-v5` esteja instalada e esta não.
- A nomenclatura desta spec segue `CONTEXT.md`; termos técnicos das dimensões são mantidos em inglês por serem identificadores de dados, conforme a regra de separação de idiomas do repositório.
- Detalhes de mecanismo — nomes de opções de linha de comando, biblioteca de sugestão de termos próximos, formato exato do arquivo de índice — são decisões de implementação, deliberadamente fora desta spec.
