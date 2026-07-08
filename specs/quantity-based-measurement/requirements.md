# Documento de Requisitos — Método de Medição por Unidades Concluídas (Quantity-Based)

## Introdução

Este documento especifica os requisitos para a adição de um novo método de medição chamado **Unidades Concluídas** ao módulo de Apontamento e Medição da plataforma EVM. O método permite que o responsável pelo pacote de trabalho informe a **quantidade de unidades concluídas** em vez de um percentual, e o sistema calcula automaticamente o percentual de conclusão e o Earned Value (EV).

Este método é especialmente adequado para pacotes de trabalho com escopo quantificável — por exemplo, "340 diagnósticos a realizar", "120 postes a instalar" ou "500 metros de cabo a lançar" — onde cada unidade possui um custo unitário definido em contrato. O avanço físico é medido objetivamente pela contagem de unidades entregues.

O módulo estende a spec `measurement-tracking`, que já suporta quatro métodos de medição: `zero_hundred`, `fifty_fifty`, `weighted_milestones` e `physical_percent`. Este será o quinto método: `quantity_based`.

Depende dos models e serviços existentes: `Project`, `WbsNode`, `Baseline`, `Measurement`, `ActualCost`, `EvCalculationService`, `MeasurementMethod` (enum) e `MeasurementPage` (Filament).

## Glossário

- **Projeto**: Entidade raiz do planejamento EVM. Definida no módulo de Estruturação e Baseline.
- **Pacote_de_Trabalho**: Nível mais baixo da EAP (WBS), onde são atribuídos BAC, datas e distribuição de PV. Definido como `WbsNode` do tipo `work_package`.
- **Baseline**: Versão congelada do plano do projeto. Definida no módulo de Estruturação e Baseline.
- **BAC (Budget at Completion)**: Orçamento total planejado para um Pacote de Trabalho, conforme definido na Baseline ativa.
- **Data_de_Status**: Data de corte (Status Date) para a qual os cálculos de EVM são processados.
- **Método_de_Medição**: Técnica utilizada para determinar o Percentual_Completo de um Pacote de Trabalho. Os métodos existentes são: 0/100, 50/50, Marcos Ponderados e Percentual Físico.
- **Unidades_Concluídas**: Novo método de medição baseado na contagem de unidades físicas concluídas. O percentual de conclusão é calculado automaticamente como `quantidade concluída / quantidade planejada × 100`.
- **Quantidade_Planejada**: Quantidade total de unidades previstas para um Pacote de Trabalho (ex: 340 diagnósticos, 120 postes). Definida pelo Gerente_de_Projeto na configuração do pacote.
- **Quantidade_Concluída**: Quantidade de unidades efetivamente concluídas até a Data_de_Status, informada pelo Líder_de_Pacote durante o apontamento de medição.
- **Custo_Unitário**: Custo por unidade de trabalho, conforme definido em contrato. Utilizado opcionalmente para calcular o AC como `quantidade concluída × custo unitário`.
- **Percentual_Completo**: Percentual de conclusão física de um Pacote de Trabalho, calculado automaticamente no método Unidades_Concluídas como `(Quantidade_Concluída / Quantidade_Planejada) × 100`.
- **EV (Earned Value)**: Valor agregado, calculado como `BAC × (Percentual_Completo / 100)`.
- **AC (Actual Cost)**: Custo real incorrido em um Pacote de Trabalho até a Data_de_Status.
- **Registro_de_Medição**: Registro que captura o Percentual_Completo, o EV calculado e a Quantidade_Concluída de um Pacote de Trabalho em uma Data_de_Status específica.
- **Líder_de_Pacote**: Usuário responsável por reportar o avanço físico de um ou mais Pacotes de Trabalho.
- **Gerente_de_Projeto**: Ator que gerencia o projeto, define a Data_de_Status, configura métodos de medição e pode reportar progresso e custos em qualquer pacote.
- **Serializador_de_Medição**: Componente responsável por formatar os dados de medição para persistência (JSON).
- **Deserializador_de_Medição**: Componente responsável por reconstruir os dados de medição a partir do formato persistido.

## Requisitos

### Requisito 1: Novo Valor no Enum de Método de Medição

**User Story:** Como desenvolvedor, eu quero que o enum `MeasurementMethod` inclua o valor `quantity_based`, para que o sistema reconheça o método de Unidades Concluídas como uma opção válida de medição.

#### Critérios de Aceitação

1. THE Enum_MeasurementMethod SHALL incluir o valor `quantity_based` com label "Unidades Concluídas" em pt-BR.
2. THE Enum_MeasurementMethod SHALL definir uma cor semântica e um ícone para o valor `quantity_based`, seguindo o padrão dos demais valores (implementações de `HasColor` e `HasIcon`).
3. WHEN o valor `quantity_based` é utilizado em formulários ou tabelas do Filament, THE Sistema SHALL exibir o label, a cor e o ícone configurados no enum.

### Requisito 2: Campos de Quantidade Planejada e Custo Unitário no Pacote de Trabalho

**User Story:** Como Gerente_de_Projeto, eu quero definir a quantidade planejada e o custo unitário de um Pacote de Trabalho, para que o sistema possa calcular o percentual de conclusão e opcionalmente o custo real com base nas unidades concluídas.

#### Critérios de Aceitação

1. WHEN o Gerente_de_Projeto configura um Pacote_de_Trabalho com o método Unidades_Concluídas, THE Sistema SHALL exigir o preenchimento do campo Quantidade_Planejada.
2. THE Sistema SHALL validar que a Quantidade_Planejada é um valor numérico inteiro positivo (maior que zero).
3. THE Sistema SHALL armazenar a Quantidade_Planejada na tabela `wbs_nodes` como coluna `planned_quantity`.
4. WHEN o Gerente_de_Projeto configura um Pacote_de_Trabalho com o método Unidades_Concluídas, THE Sistema SHALL permitir o preenchimento opcional do campo Custo_Unitário.
5. THE Sistema SHALL validar que o Custo_Unitário, quando informado, é um valor numérico positivo com até duas casas decimais.
6. THE Sistema SHALL armazenar o Custo_Unitário na tabela `wbs_nodes` como coluna `unit_cost`.
7. THE Sistema SHALL exibir o Custo_Unitário em formato monetário BRL (R$) na interface.
8. IF o Método_de_Medição do Pacote_de_Trabalho não é Unidades_Concluídas, THEN THE Sistema SHALL ignorar os campos Quantidade_Planejada e Custo_Unitário (os campos são relevantes apenas para o método `quantity_based`).
9. IF o Gerente_de_Projeto altera o Método_de_Medição de um Pacote_de_Trabalho para Unidades_Concluídas e a Quantidade_Planejada não está preenchida, THEN THE Sistema SHALL exigir o preenchimento antes de salvar.

### Requisito 3: Registro de Quantidade Concluída na Medição

**User Story:** Como Líder_de_Pacote, eu quero informar a quantidade de unidades concluídas do meu Pacote de Trabalho na Data de Status atual, para que o sistema calcule automaticamente o percentual de conclusão e o Earned Value.

#### Critérios de Aceitação

1. WHEN o Líder_de_Pacote registra uma medição para um Pacote_de_Trabalho com método Unidades_Concluídas, THE Sistema SHALL solicitar a entrada da Quantidade_Concluída em vez do Percentual_Completo.
2. THE Sistema SHALL validar que a Quantidade_Concluída é um valor numérico inteiro não negativo (maior ou igual a zero).
3. THE Sistema SHALL validar que a Quantidade_Concluída é menor ou igual à Quantidade_Planejada do Pacote_de_Trabalho.
4. WHEN a Quantidade_Concluída é registrada, THE Sistema SHALL calcular o Percentual_Completo como `(Quantidade_Concluída / Quantidade_Planejada) × 100`, arredondado para duas casas decimais.
5. WHEN a Quantidade_Concluída é registrada, THE Sistema SHALL calcular o EV como `BAC × (Quantidade_Concluída / Quantidade_Planejada)`, utilizando o BAC da Baseline ativa do Projeto.
6. THE Sistema SHALL armazenar a Quantidade_Concluída no Registro_de_Medição como campo `quantity_completed` na tabela `measurements`.
7. THE Sistema SHALL criar um Registro_de_Medição contendo o Pacote_de_Trabalho, a Data_de_Status, o Percentual_Completo calculado, o EV calculado, o método `quantity_based` e a Quantidade_Concluída.
8. IF já existe um Registro_de_Medição para o mesmo Pacote_de_Trabalho e Data_de_Status, THEN THE Sistema SHALL atualizar o registro existente em vez de criar um novo (upsert).
9. IF o Projeto não possui Data_de_Status definida, THEN THE Sistema SHALL impedir o registro e informar que é necessário definir a Data_de_Status primeiro.

### Requisito 4: Monotonicidade da Quantidade Concluída

**User Story:** Como Gerente_de_Projeto, eu quero que o sistema impeça a regressão da quantidade concluída, para que a integridade do avanço físico seja preservada.

#### Critérios de Aceitação

1. WHEN o Líder_de_Pacote registra uma Quantidade_Concluída para um Pacote_de_Trabalho com método Unidades_Concluídas, THE Sistema SHALL validar que a Quantidade_Concluída é maior ou igual à Quantidade_Concluída do Registro_de_Medição mais recente anterior para o mesmo Pacote_de_Trabalho.
2. IF a Quantidade_Concluída informada é menor que a Quantidade_Concluída do período anterior, THEN THE Sistema SHALL rejeitar o registro e informar a quantidade mínima permitida.

### Requisito 5: Cálculo Opcional do Custo Real (AC) por Unidades

**User Story:** Como Gerente_de_Projeto, eu quero que o sistema sugira o custo real (AC) com base nas unidades concluídas e no custo unitário do contrato, para agilizar o registro de custos quando o custo unitário é conhecido.

#### Critérios de Aceitação

1. WHILE o Pacote_de_Trabalho possui Custo_Unitário definido e método Unidades_Concluídas, WHEN uma medição é registrada, THE Sistema SHALL calcular e exibir o AC sugerido como `Quantidade_Concluída × Custo_Unitário`.
2. THE Sistema SHALL exibir o AC sugerido como valor pré-preenchido no campo de custo real, permitindo que o Gerente_de_Projeto aceite ou altere o valor antes de salvar.
3. THE Sistema SHALL exibir o AC sugerido em formato monetário BRL (R$).
4. IF o Pacote_de_Trabalho não possui Custo_Unitário definido, THEN THE Sistema SHALL manter o campo de custo real vazio, sem sugestão automática.
5. THE Sistema SHALL tratar o AC como input independente do cálculo de EV. O Gerente_de_Projeto pode alterar o valor sugerido livremente antes de salvar.

### Requisito 6: Interface de Apontamento para Unidades Concluídas

**User Story:** Como Líder_de_Pacote, eu quero que a interface de medição exiba um campo de quantidade concluída quando o método do pacote é Unidades Concluídas, para que eu possa reportar o avanço de forma intuitiva e objetiva.

#### Critérios de Aceitação

1. WHEN o método do Pacote_de_Trabalho é Unidades_Concluídas, THE Sistema SHALL exibir um campo numérico para entrada da Quantidade_Concluída em vez do campo de percentual.
2. THE Sistema SHALL exibir a Quantidade_Planejada como referência ao lado do campo de entrada (ex: "X / 340 unidades").
3. THE Sistema SHALL exibir o Percentual_Completo calculado em tempo real conforme o Líder_de_Pacote altera a Quantidade_Concluída.
4. THE Sistema SHALL exibir o EV calculado em tempo real conforme o Líder_de_Pacote altera a Quantidade_Concluída.
5. WHEN o método do Pacote_de_Trabalho é Unidades_Concluídas e o Custo_Unitário está definido, THE Sistema SHALL exibir o AC sugerido em tempo real conforme a Quantidade_Concluída é alterada.
6. THE Sistema SHALL exibir o histórico de medições anteriores incluindo a Quantidade_Concluída registrada em cada período.

### Requisito 7: Compatibilidade com Regras Existentes de Medição

**User Story:** Como desenvolvedor, eu quero que o novo método Unidades Concluídas respeite todas as regras existentes do módulo de medição, para que a integridade do sistema EVM seja preservada.

#### Critérios de Aceitação

1. THE Sistema SHALL aplicar a regra de imutabilidade de registros históricos ao método Unidades_Concluídas: registros de Datas_de_Status anteriores à Data_de_Status atual são somente leitura.
2. THE Sistema SHALL aplicar as regras de controle de acesso existentes ao método Unidades_Concluídas: Líder_de_Pacote registra quantidade apenas nos pacotes atribuídos, Gerente_de_Projeto registra em qualquer pacote, Diretor_de_Portfólio tem acesso somente leitura.
3. THE Sistema SHALL registrar na Trilha_de_Auditoria todas as criações e atualizações de medições com método Unidades_Concluídas, incluindo a Quantidade_Concluída anterior e a nova.
4. THE Sistema SHALL incluir o EV de pacotes com método Unidades_Concluídas na agregação bottom-up de EV para Entregas, Fases e Projeto.
5. THE Sistema SHALL aplicar carry-forward para pacotes com método Unidades_Concluídas: quando não há registro na Data_de_Status atual, utilizar o último registro anterior.
6. THE Sistema SHALL sincronizar os cálculos de PV, EV e AC de pacotes com método Unidades_Concluídas na mesma Data_de_Status do Projeto.

### Requisito 8: Validação de Configuração ao Alterar Método de Medição

**User Story:** Como Gerente_de_Projeto, eu quero que o sistema valide a configuração ao alterar o método de medição de ou para Unidades Concluídas, para que a transição entre métodos seja segura e consistente.

#### Critérios de Aceitação

1. IF o Gerente_de_Projeto altera o Método_de_Medição de um Pacote_de_Trabalho para Unidades_Concluídas e o pacote já possui Registros_de_Medição com outro método, THEN THE Sistema SHALL solicitar confirmação e informar que os registros existentes serão preservados, mas novas medições usarão o novo método.
2. IF o Gerente_de_Projeto altera o Método_de_Medição de Unidades_Concluídas para outro método, THEN THE Sistema SHALL solicitar confirmação e informar que os registros existentes (incluindo Quantidade_Concluída) serão preservados, mas novas medições usarão o novo método.
3. WHEN o Método_de_Medição é alterado de ou para Unidades_Concluídas, THE Sistema SHALL registrar a alteração na Trilha_de_Auditoria com o método anterior e o novo.

### Requisito 9: Serialização e Deserialização da Quantidade Concluída

**User Story:** Como desenvolvedor, eu quero que a quantidade concluída seja serializada e deserializada de forma consistente nos registros de medição, para que a integridade dos dados seja preservada em operações de leitura e escrita.

#### Critérios de Aceitação

1. THE Serializador_de_Medição SHALL armazenar a Quantidade_Concluída como valor inteiro no campo `quantity_completed` da tabela `measurements`.
2. THE Deserializador_de_Medição SHALL reconstruir a Quantidade_Concluída a partir do campo `quantity_completed` do registro de medição.
3. FOR ALL valores válidos de Quantidade_Concluída, gravar no banco e depois ler SHALL produzir um valor equivalente ao original (propriedade de ida e volta).
