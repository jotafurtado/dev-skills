# Documento de Requisitos — Módulo de Apontamento e Medição (Execução)

## Introdução

Este documento especifica os requisitos do Módulo de Apontamento e Medição da plataforma de gestão de projetos baseada em EVM (Earned Value Management). O módulo é responsável por coletar os dados reais de execução do projeto — percentual de conclusão (% Complete) e custo real (AC — Actual Cost) — para alimentar o motor de cálculo EVM.

O módulo depende do Módulo de Estruturação e Baseline (spec: `project-structuring-baseline`), que fornece os models `Project`, `WbsNode`, `Baseline`, `AuditLog` e `User` com papéis (`UserRole`). Este módulo não recria essas entidades; ele as estende com novos relacionamentos e introduz novas entidades para registrar medições, custos reais e a Data de Status.

As funcionalidades principais incluem:

- Definição da Data de Status (Status Date) para sincronizar cálculos EVM
- Registro do percentual de conclusão (% Complete) por pacote de trabalho, com suporte a diferentes métodos de medição (0/100, 50/50, Marcos Ponderados, Percentual Físico)
- Registro do custo real (AC) por pacote de trabalho, como input independente (manual ou via integração)
- Cálculo do Earned Value (EV) com base no BAC da Baseline ativa e no % Complete reportado
- Preservação de registros históricos de medições anteriores (imutabilidade de períodos passados)
- Trilha de auditoria para todas as alterações de progresso e custo
- Controle de acesso: líderes de pacote de trabalho reportam progresso apenas nos pacotes atribuídos a eles

## Glossário

- **Projeto**: Entidade raiz do planejamento EVM. Definida no módulo de Estruturação e Baseline.
- **Pacote_de_Trabalho**: Nível mais baixo da EAP (WBS), onde são atribuídos BAC, datas e distribuição de PV. Definido no módulo de Estruturação e Baseline como `WbsNode` do tipo `work_package`.
- **Baseline**: Versão congelada do plano do projeto. Definida no módulo de Estruturação e Baseline.
- **BAC (Budget at Completion)**: Orçamento total planejado para um Pacote de Trabalho, conforme definido na Baseline ativa.
- **Data_de_Status**: Data de corte (Status Date / Data Date) para a qual os cálculos de EVM são processados. Todos os valores de PV, EV e AC devem ser sincronizados para a mesma Data_de_Status.
- **Percentual_Completo**: Percentual de conclusão física (% Complete) de um Pacote de Trabalho em uma determinada Data_de_Status.
- **Método_de_Medição**: Técnica utilizada para determinar o Percentual_Completo de um Pacote de Trabalho. Os métodos suportados são: 0/100, 50/50, Marcos Ponderados e Percentual Físico.
- **Método_0_100**: Método de medição binário. O Pacote de Trabalho é 0% até ser concluído, quando passa a 100%.
- **Método_50_50**: Método de medição que atribui 50% quando o trabalho é iniciado e 100% quando é concluído.
- **Marcos_Ponderados**: Método de medição baseado em marcos intermediários com pesos percentuais pré-definidos. A soma dos pesos de todos os marcos deve ser 100%.
- **Percentual_Físico**: Método de medição onde o Líder_de_Pacote informa livremente o percentual de avanço físico (0% a 100%).
- **Marco_Ponderado**: Marco intermediário dentro de um Pacote de Trabalho, com descrição e peso percentual. Utilizado no método Marcos_Ponderados.
- **EV (Earned Value)**: Valor agregado, calculado como BAC × Percentual_Completo. Representa o valor do trabalho efetivamente realizado.
- **AC (Actual Cost)**: Custo real incorrido em um Pacote de Trabalho até a Data_de_Status. É um input independente — não pode ser derivado do avanço físico.
- **Registro_de_Medição**: Registro que captura o Percentual_Completo e o EV calculado de um Pacote de Trabalho em uma Data_de_Status específica.
- **Registro_de_Custo_Real**: Registro que captura o AC de um Pacote de Trabalho em uma Data_de_Status específica.
- **Líder_de_Pacote**: Usuário responsável por reportar o avanço físico de um ou mais Pacotes de Trabalho. Pode ser um Gerente_de_Projeto ou um usuário com papel específico atribuído ao pacote.
- **Gerente_de_Projeto**: Ator que gerencia o projeto, define a Data_de_Status, configura métodos de medição e pode reportar progresso e custos em qualquer pacote.
- **Diretor_de_Portfólio**: Ator com acesso somente leitura às medições e custos.
- **Trilha_de_Auditoria**: Registro imutável de alterações. Definida no módulo de Estruturação e Baseline (model `AuditLog`).

## Requisitos

### Requisito 1: Definição da Data de Status

**User Story:** Como Gerente_de_Projeto, eu quero definir a Data de Status (Status Date) do projeto, para que todos os cálculos de EVM sejam sincronizados para a mesma data de corte.

#### Critérios de Aceitação

1. WHEN o Gerente_de_Projeto define uma Data_de_Status para um Projeto, THE Sistema SHALL armazenar a Data_de_Status associada ao Projeto.
2. THE Sistema SHALL validar que a Data_de_Status é igual ou posterior à data de início planejada do Projeto.
3. THE Sistema SHALL validar que a Data_de_Status é igual ou anterior à data de fim planejada do Projeto.
4. IF o Projeto não possui Baseline congelada ativa, THEN THE Sistema SHALL impedir a definição da Data_de_Status e informar que é necessário congelar uma Baseline primeiro.
5. WHEN o Gerente_de_Projeto altera a Data_de_Status, THE Sistema SHALL manter os registros históricos de medições e custos de Datas_de_Status anteriores inalterados.
6. THE Sistema SHALL exibir a Data_de_Status atual do Projeto de forma destacada na interface de medição.

### Requisito 2: Configuração do Método de Medição por Pacote de Trabalho

**User Story:** Como Gerente_de_Projeto, eu quero configurar o método de medição de cada Pacote de Trabalho, para que o sistema calcule o percentual de conclusão de acordo com a técnica adequada ao tipo de trabalho.

#### Critérios de Aceitação

1. WHEN o Gerente_de_Projeto configura o Método_de_Medição de um Pacote_de_Trabalho, THE Sistema SHALL armazenar o método selecionado (0/100, 50/50, Marcos_Ponderados ou Percentual_Físico).
2. THE Sistema SHALL definir Percentual_Físico como o Método_de_Medição padrão para novos Pacotes de Trabalho.
3. IF o Gerente_de_Projeto seleciona o método Marcos_Ponderados, THEN THE Sistema SHALL solicitar a definição dos marcos com descrição e peso percentual.
4. THE Sistema SHALL validar que a soma dos pesos de todos os Marcos_Ponderados de um Pacote_de_Trabalho é igual a 100%.
5. IF o Gerente_de_Projeto tenta alterar o Método_de_Medição de um Pacote_de_Trabalho que já possui Registros_de_Medição, THEN THE Sistema SHALL solicitar confirmação e informar que os registros existentes serão preservados, mas novas medições usarão o novo método.
6. IF o Projeto possui Baseline congelada ativa, THEN THE Sistema SHALL permitir a configuração do Método_de_Medição sem necessidade de nova Baseline, pois o método de medição não faz parte do snapshot da Baseline.

### Requisito 3: Atribuição de Responsável por Pacote de Trabalho

**User Story:** Como Gerente_de_Projeto, eu quero atribuir um responsável (Líder de Pacote) a cada Pacote de Trabalho, para que o controle de acesso permita que cada líder reporte progresso apenas nos pacotes sob sua responsabilidade.

#### Critérios de Aceitação

1. WHEN o Gerente_de_Projeto atribui um usuário como Líder_de_Pacote de um Pacote_de_Trabalho, THE Sistema SHALL armazenar a associação entre o usuário e o Pacote_de_Trabalho.
2. THE Sistema SHALL permitir que um Pacote_de_Trabalho tenha no máximo um Líder_de_Pacote atribuído.
3. THE Sistema SHALL permitir que um usuário seja Líder_de_Pacote de múltiplos Pacotes de Trabalho.
4. WHEN o Gerente_de_Projeto remove a atribuição de um Líder_de_Pacote, THE Sistema SHALL remover a associação sem afetar os Registros_de_Medição existentes.
5. IF nenhum Líder_de_Pacote está atribuído a um Pacote_de_Trabalho, THEN THE Sistema SHALL permitir que apenas o Gerente_de_Projeto reporte progresso naquele pacote.

### Requisito 4: Registro de Percentual de Conclusão (% Complete)

**User Story:** Como Líder_de_Pacote, eu quero registrar o percentual de conclusão do meu Pacote de Trabalho na Data de Status atual, para que o sistema calcule o Earned Value (EV) com base no avanço físico real.

#### Critérios de Aceitação

1. WHEN o Líder_de_Pacote registra o Percentual_Completo de um Pacote_de_Trabalho usando o método Percentual_Físico, THE Sistema SHALL armazenar o valor informado (0% a 100%) associado à Data_de_Status atual do Projeto.
2. WHEN o Líder_de_Pacote registra o Percentual_Completo usando o método 0/100, THE Sistema SHALL aceitar apenas os valores 0% ou 100%.
3. WHEN o Líder_de_Pacote registra o Percentual_Completo usando o método 50/50, THE Sistema SHALL aceitar apenas os valores 0%, 50% ou 100%.
4. WHEN o Líder_de_Pacote registra o Percentual_Completo usando o método Marcos_Ponderados, THE Sistema SHALL calcular o Percentual_Completo como a soma dos pesos dos marcos marcados como concluídos.
5. THE Sistema SHALL validar que o Percentual_Completo é um valor numérico entre 0 e 100, com até duas casas decimais.
6. THE Sistema SHALL validar que o Percentual_Completo registrado é igual ou superior ao Percentual_Completo do período anterior para o mesmo Pacote_de_Trabalho (progresso não pode regredir).
7. WHEN o Percentual_Completo é registrado, THE Sistema SHALL calcular o EV como BAC × (Percentual_Completo / 100), utilizando o BAC da Baseline ativa do Projeto.
8. THE Sistema SHALL criar um Registro_de_Medição contendo o Pacote_de_Trabalho, a Data_de_Status, o Percentual_Completo, o EV calculado e o método de medição utilizado.
9. IF o Projeto não possui Data_de_Status definida, THEN THE Sistema SHALL impedir o registro de Percentual_Completo e informar que é necessário definir a Data_de_Status primeiro.
10. IF já existe um Registro_de_Medição para o mesmo Pacote_de_Trabalho e Data_de_Status, THEN THE Sistema SHALL atualizar o registro existente em vez de criar um novo.

### Requisito 5: Registro de Custo Real (Actual Cost)

**User Story:** Como Gerente_de_Projeto, eu quero registrar o custo real (AC) incorrido em cada Pacote de Trabalho na Data de Status atual, para que o sistema possa calcular os indicadores de desempenho de custo (CPI, CV).

#### Critérios de Aceitação

1. WHEN o Gerente_de_Projeto registra o AC de um Pacote_de_Trabalho, THE Sistema SHALL armazenar o valor associado à Data_de_Status atual do Projeto.
2. THE Sistema SHALL validar que o AC é um valor numérico positivo ou zero, com até duas casas decimais.
3. THE Sistema SHALL criar um Registro_de_Custo_Real contendo o Pacote_de_Trabalho, a Data_de_Status e o valor do AC.
4. IF já existe um Registro_de_Custo_Real para o mesmo Pacote_de_Trabalho e Data_de_Status, THEN THE Sistema SHALL atualizar o registro existente em vez de criar um novo.
5. THE Sistema SHALL tratar o AC como input independente do Percentual_Completo. O AC registrado não pode ser derivado automaticamente do avanço físico.
6. IF o Projeto não possui Data_de_Status definida, THEN THE Sistema SHALL impedir o registro de AC e informar que é necessário definir a Data_de_Status primeiro.
7. THE Sistema SHALL exibir o AC em formato monetário BRL (R$) na interface.

### Requisito 6: Imutabilidade de Registros Históricos

**User Story:** Como Diretor_de_Portfólio, eu quero que os registros de medição e custo de períodos anteriores sejam preservados inalterados, para que a curva de tendência do EVM seja rastreável e confiável.

#### Critérios de Aceitação

1. WHEN o Gerente_de_Projeto altera a Data_de_Status para uma data mais recente, THE Sistema SHALL manter todos os Registros_de_Medição e Registros_de_Custo_Real de Datas_de_Status anteriores inalterados.
2. THE Sistema SHALL impedir a edição de Registros_de_Medição de Datas_de_Status anteriores à Data_de_Status atual do Projeto.
3. THE Sistema SHALL impedir a edição de Registros_de_Custo_Real de Datas_de_Status anteriores à Data_de_Status atual do Projeto.
4. THE Sistema SHALL permitir a edição de Registros_de_Medição e Registros_de_Custo_Real apenas para a Data_de_Status atual do Projeto.
5. THE Sistema SHALL exibir os registros históricos em modo somente leitura, permitindo consulta a qualquer período anterior.

### Requisito 7: Cálculo do Earned Value (EV)

**User Story:** Como Gerente_de_Projeto, eu quero que o sistema calcule automaticamente o Earned Value (EV) de cada Pacote de Trabalho e agregue para os níveis superiores da EAP, para que eu possa comparar o valor planejado com o valor efetivamente realizado.

#### Critérios de Aceitação

1. WHEN um Registro_de_Medição é criado ou atualizado, THE Sistema SHALL calcular o EV do Pacote_de_Trabalho como BAC × (Percentual_Completo / 100), utilizando o BAC da Baseline ativa.
2. THE Sistema SHALL agregar o EV dos Pacotes_de_Trabalho para calcular o EV de Entregas, Fases e do Projeto, utilizando soma bottom-up.
3. THE Sistema SHALL recalcular o EV agregado sempre que um Registro_de_Medição for criado ou atualizado.
4. IF o BAC de um Pacote_de_Trabalho na Baseline ativa é zero ou nulo, THEN THE Sistema SHALL calcular o EV como zero para aquele pacote.
5. FOR ALL Pacotes_de_Trabalho com Percentual_Completo igual a 100%, o EV SHALL ser igual ao BAC da Baseline ativa.
6. FOR ALL Pacotes_de_Trabalho com Percentual_Completo igual a 0%, o EV SHALL ser igual a zero.

### Requisito 8: Sincronização de Dados na Data de Status

**User Story:** Como Gerente_de_Projeto, eu quero que todos os cálculos de EVM (PV, EV, AC) sejam sincronizados para a mesma Data de Status, para que as comparações entre planejado, realizado e custo sejam válidas e consistentes.

#### Critérios de Aceitação

1. THE Sistema SHALL utilizar a mesma Data_de_Status do Projeto para consultar PV, EV e AC em qualquer cálculo ou visualização de EVM.
2. WHEN o Sistema exibe métricas de EVM, THE Sistema SHALL obter o PV cumulativo da Baseline ativa até a Data_de_Status, o EV dos Registros_de_Medição na Data_de_Status e o AC dos Registros_de_Custo_Real na Data_de_Status.
3. THE Sistema SHALL impedir a comparação de valores de EV e AC de Datas_de_Status diferentes em uma mesma visualização.
4. IF um Pacote_de_Trabalho não possui Registro_de_Medição para a Data_de_Status atual, THEN THE Sistema SHALL utilizar o último Percentual_Completo registrado em uma Data_de_Status anterior (carry-forward).
5. IF um Pacote_de_Trabalho não possui Registro_de_Custo_Real para a Data_de_Status atual, THEN THE Sistema SHALL utilizar o último AC registrado em uma Data_de_Status anterior (carry-forward).

### Requisito 9: Trilha de Auditoria para Medições e Custos

**User Story:** Como Diretor_de_Portfólio, eu quero que todas as alterações em medições de progresso e custos reais sejam registradas na trilha de auditoria, para que eu possa rastrear quem reportou cada avanço e quando.

#### Critérios de Aceitação

1. WHEN um Registro_de_Medição é criado ou atualizado, THE Sistema SHALL registrar na Trilha_de_Auditoria o usuário, a data/hora, o Pacote_de_Trabalho, a Data_de_Status, o Percentual_Completo anterior e o novo, e o EV anterior e o novo.
2. WHEN um Registro_de_Custo_Real é criado ou atualizado, THE Sistema SHALL registrar na Trilha_de_Auditoria o usuário, a data/hora, o Pacote_de_Trabalho, a Data_de_Status, o AC anterior e o novo.
3. WHEN a Data_de_Status de um Projeto é alterada, THE Sistema SHALL registrar na Trilha_de_Auditoria o usuário, a data/hora, a Data_de_Status anterior e a nova.
4. WHEN o Método_de_Medição de um Pacote_de_Trabalho é alterado, THE Sistema SHALL registrar na Trilha_de_Auditoria o método anterior e o novo.
5. THE Trilha_de_Auditoria SHALL utilizar o model `AuditLog` existente, estendendo as operações registradas para incluir as novas entidades deste módulo.

### Requisito 10: Controle de Acesso para Medições

**User Story:** Como Gerente_de_Projeto, eu quero que o controle de acesso garanta que cada Líder de Pacote reporte progresso apenas nos pacotes sob sua responsabilidade, para que a integridade dos dados de medição seja preservada.

#### Critérios de Aceitação

1. WHILE o usuário possui o papel Gerente_de_Projeto, THE Sistema SHALL permitir registrar Percentual_Completo e AC em qualquer Pacote_de_Trabalho do Projeto.
2. WHILE o usuário é Líder_de_Pacote de um Pacote_de_Trabalho, THE Sistema SHALL permitir registrar Percentual_Completo apenas nos Pacotes_de_Trabalho atribuídos a ele.
3. WHILE o usuário é Líder_de_Pacote, THE Sistema SHALL impedir o registro de AC (custo real é responsabilidade do Gerente_de_Projeto ou Analista Financeiro).
4. WHILE o usuário possui o papel Diretor_de_Portfólio, THE Sistema SHALL permitir visualizar Registros_de_Medição e Registros_de_Custo_Real em modo somente leitura.
5. IF um usuário sem permissão tenta registrar Percentual_Completo ou AC em um Pacote_de_Trabalho, THEN THE Sistema SHALL rejeitar a operação e retornar uma mensagem de acesso negado.

### Requisito 11: Interface de Apontamento de Medição

**User Story:** Como Líder_de_Pacote, eu quero uma interface intuitiva para registrar o avanço físico dos meus Pacotes de Trabalho, para que eu possa reportar o progresso de forma rápida e precisa.

#### Critérios de Aceitação

1. THE Sistema SHALL exibir uma lista dos Pacotes_de_Trabalho do Projeto com a Data_de_Status atual, o Percentual_Completo atual, o EV calculado e o AC registrado.
2. WHEN o Líder_de_Pacote acessa a interface de medição, THE Sistema SHALL filtrar automaticamente os Pacotes_de_Trabalho atribuídos ao usuário logado (exceto para Gerentes_de_Projeto, que veem todos).
3. THE Sistema SHALL exibir o Método_de_Medição configurado para cada Pacote_de_Trabalho e adaptar o formulário de entrada de acordo com o método.
4. WHEN o método é Marcos_Ponderados, THE Sistema SHALL exibir a lista de marcos com checkboxes para marcar os marcos concluídos e calcular automaticamente o Percentual_Completo resultante.
5. THE Sistema SHALL exibir o BAC de cada Pacote_de_Trabalho (conforme Baseline ativa) como referência durante o apontamento.
6. THE Sistema SHALL exibir o histórico de medições anteriores de cada Pacote_de_Trabalho em formato de timeline ou tabela.

### Requisito 12: Marcos Ponderados — Definição e Gestão

**User Story:** Como Gerente_de_Projeto, eu quero definir marcos ponderados para Pacotes de Trabalho que utilizam esse método de medição, para que o avanço físico seja calculado de forma objetiva com base em entregas intermediárias verificáveis.

#### Critérios de Aceitação

1. WHEN o Gerente_de_Projeto define marcos para um Pacote_de_Trabalho com método Marcos_Ponderados, THE Sistema SHALL armazenar cada marco com descrição e peso percentual.
2. THE Sistema SHALL validar que a soma dos pesos de todos os marcos de um Pacote_de_Trabalho é igual a 100%.
3. THE Sistema SHALL validar que cada peso de marco é um valor numérico positivo com até duas casas decimais.
4. THE Sistema SHALL permitir adicionar, editar e remover marcos enquanto o Pacote_de_Trabalho não possuir Registros_de_Medição com marcos concluídos.
5. IF o Gerente_de_Projeto tenta remover um marco que já foi marcado como concluído em um Registro_de_Medição, THEN THE Sistema SHALL rejeitar a remoção e informar que o marco já possui registro de conclusão.
6. THE Sistema SHALL ordenar os marcos por uma sequência definida pelo Gerente_de_Projeto.

### Requisito 13: Serialização e Deserialização de Registros de Medição

**User Story:** Como desenvolvedor, eu quero que os registros de medição sejam serializados e deserializados de forma consistente, para que a integridade dos dados seja preservada em operações de leitura e escrita.

#### Critérios de Aceitação

1. THE Serializador_de_Medição SHALL formatar os dados de marcos concluídos (no método Marcos_Ponderados) como uma estrutura JSON contendo o ID do marco e o status de conclusão.
2. THE Deserializador_de_Medição SHALL reconstruir os dados de marcos concluídos a partir da estrutura JSON serializada.
3. FOR ALL dados válidos de marcos concluídos, serializar e depois deserializar SHALL produzir dados equivalentes aos originais (propriedade de ida e volta).
