# Documento de Requisitos — Módulo de Estruturação e Baseline

## Introdução

Este documento especifica os requisitos do Módulo de Estruturação e Baseline da plataforma de gestão de projetos baseada em EVM (Earned Value Management). O módulo é responsável por permitir que o Gerente de Projeto crie a Estrutura Analítica do Projeto (EAP/WBS), defina orçamentos por pacote de trabalho, distribua o Planned Value (PV) ao longo do tempo e gerencie versões de Baseline com controle de mudanças e trilha de auditoria.

Este é o primeiro módulo da plataforma e será construído do zero sobre Laravel 13, Filament v5, Inertia.js v3 com Vue 3, Pest v4 e SQLite.

## Glossário

- **Projeto**: Entidade raiz que agrupa toda a estrutura de planejamento EVM. Possui nome, descrição, datas planejadas e um orçamento total (BAC).
- **EAP (Estrutura Analítica do Projeto)**: Decomposição hierárquica do escopo do projeto em Fases, Entregas e Pacotes de Trabalho. Equivalente ao termo WBS (Work Breakdown Structure).
- **Nó_EAP**: Elemento genérico da hierarquia da EAP. Pode ser do tipo Fase, Entrega ou Pacote de Trabalho.
- **Fase**: Primeiro nível de decomposição da EAP, representando uma etapa macro do projeto.
- **Entrega**: Segundo nível de decomposição, representando um produto ou resultado tangível dentro de uma Fase.
- **Pacote_de_Trabalho**: Nível mais baixo da EAP, onde são atribuídos orçamento (BAC), datas de início/fim e distribuição de PV. É a unidade de medição do EVM.
- **BAC (Budget at Completion)**: Orçamento total planejado para um Pacote de Trabalho ou, por agregação, para qualquer nível superior da EAP.
- **PV (Planned Value)**: Valor planejado acumulado até uma determinada data. Representa quanto do orçamento deveria ter sido gasto conforme o plano.
- **Distribuição_PV**: Forma como o BAC de um Pacote de Trabalho é distribuído ao longo do tempo entre suas datas de início e fim, gerando a curva de PV.
- **Baseline**: Versão congelada e aprovada do plano do projeto (EAP + orçamentos + cronograma + distribuição de PV) que serve como referência para medições de EVM.
- **Baseline_Freeze**: Ato de congelar uma Baseline, tornando-a imutável e ativando-a como referência para cálculos de EVM.
- **Versão_Baseline**: Identificador sequencial de cada Baseline congelada. Mudanças após o congelamento geram uma nova versão.
- **Gerente_de_Projeto**: Ator principal do módulo. Cria a EAP, define orçamentos, distribui PV e gerencia Baselines.
- **Diretor_de_Portfólio**: Ator que visualiza a saúde consolidada dos projetos. Neste módulo, tem acesso somente leitura às Baselines.
- **Trilha_de_Auditoria**: Registro imutável de todas as alterações realizadas no sistema, contendo usuário, data/hora, valor anterior e valor novo.
- **RBAC**: Controle de Acesso Baseado em Papéis (Role-Based Access Control), com permissões granulares por funcionalidade.

## Requisitos

### Requisito 1: Criação e Gestão de Projetos

**User Story:** Como Gerente_de_Projeto, eu quero criar e gerenciar projetos na plataforma, para que eu possa organizar o planejamento EVM de cada projeto de forma independente.

#### Critérios de Aceitação

1. WHEN o Gerente_de_Projeto submete os dados de um novo projeto (nome, descrição, data de início planejada, data de fim planejada), THE Sistema SHALL criar o Projeto e exibir a tela de estruturação da EAP.
2. THE Sistema SHALL validar que o nome do Projeto é obrigatório e possui no máximo 255 caracteres.
3. THE Sistema SHALL validar que a data de fim planejada do Projeto é igual ou posterior à data de início planejada.
4. WHEN o Gerente_de_Projeto edita os dados de um Projeto que não possui Baseline congelada, THE Sistema SHALL atualizar os dados do Projeto.
5. IF o Gerente_de_Projeto tenta editar dados de um Projeto que possui Baseline congelada ativa, THEN THE Sistema SHALL bloquear a edição e informar que é necessário criar uma nova Versão_Baseline.

### Requisito 2: Estruturação Hierárquica da EAP

**User Story:** Como Gerente_de_Projeto, eu quero decompor o projeto em Fases, Entregas e Pacotes de Trabalho de forma hierárquica, para que eu possa organizar o escopo e atribuir orçamentos no nível adequado.

#### Critérios de Aceitação

1. WHEN o Gerente_de_Projeto adiciona um Nó_EAP ao Projeto, THE Sistema SHALL solicitar o tipo (Fase, Entrega ou Pacote_de_Trabalho), o nome e o nó pai (quando aplicável).
2. THE Sistema SHALL impor a hierarquia: Fases são filhas do Projeto, Entregas são filhas de Fases, e Pacotes_de_Trabalho são filhos de Entregas.
3. THE Sistema SHALL gerar automaticamente um código hierárquico para cada Nó_EAP (ex: 1.0, 1.1, 1.1.1) baseado na posição na árvore.
4. WHEN o Gerente_de_Projeto reordena um Nó_EAP dentro do mesmo nível hierárquico, THE Sistema SHALL atualizar os códigos hierárquicos de todos os nós afetados.
5. WHEN o Gerente_de_Projeto remove um Nó_EAP que possui filhos, THE Sistema SHALL solicitar confirmação e remover o nó e todos os seus descendentes.
6. THE Sistema SHALL exibir a EAP em formato de árvore hierárquica expansível na interface.
7. IF o Gerente_de_Projeto tenta criar um Pacote_de_Trabalho diretamente sob o Projeto ou sob uma Fase sem Entrega intermediária, THEN THE Sistema SHALL rejeitar a operação e informar a estrutura hierárquica correta.

### Requisito 3: Atribuição de Orçamento (BAC)

**User Story:** Como Gerente_de_Projeto, eu quero atribuir o custo planejado (BAC) a cada Pacote de Trabalho, para que o sistema possa calcular o orçamento total do projeto e gerar a curva de PV.

#### Critérios de Aceitação

1. WHEN o Gerente_de_Projeto informa o BAC de um Pacote_de_Trabalho, THE Sistema SHALL armazenar o valor e recalcular o BAC agregado de todos os nós ancestrais (Entrega, Fase e Projeto).
2. THE Sistema SHALL validar que o BAC de um Pacote_de_Trabalho é um valor numérico positivo com até duas casas decimais.
3. THE Sistema SHALL calcular o BAC de uma Entrega como a soma dos BACs de seus Pacotes_de_Trabalho filhos.
4. THE Sistema SHALL calcular o BAC de uma Fase como a soma dos BACs de suas Entregas filhas.
5. THE Sistema SHALL calcular o BAC do Projeto como a soma dos BACs de todas as Fases.
6. WHEN o Gerente_de_Projeto altera o BAC de um Pacote_de_Trabalho, THE Sistema SHALL recalcular automaticamente os BACs agregados de todos os nós ancestrais.
7. THE Sistema SHALL exibir o BAC agregado em cada nível da EAP na interface hierárquica.

### Requisito 4: Definição de Cronograma

**User Story:** Como Gerente_de_Projeto, eu quero definir datas de início e fim para cada Pacote de Trabalho, para que o sistema possa distribuir o orçamento ao longo do tempo.

#### Critérios de Aceitação

1. WHEN o Gerente_de_Projeto define as datas de início e fim de um Pacote_de_Trabalho, THE Sistema SHALL armazenar as datas e validar que a data de fim é igual ou posterior à data de início.
2. THE Sistema SHALL validar que as datas do Pacote_de_Trabalho estão dentro do intervalo de datas planejadas do Projeto.
3. THE Sistema SHALL calcular a data de início de uma Entrega como a menor data de início entre seus Pacotes_de_Trabalho filhos.
4. THE Sistema SHALL calcular a data de fim de uma Entrega como a maior data de fim entre seus Pacotes_de_Trabalho filhos.
5. THE Sistema SHALL calcular a data de início de uma Fase como a menor data de início entre suas Entregas filhas.
6. THE Sistema SHALL calcular a data de fim de uma Fase como a maior data de fim entre suas Entregas filhas.
7. WHEN o Gerente_de_Projeto altera as datas de um Pacote_de_Trabalho, THE Sistema SHALL recalcular automaticamente as datas agregadas de todos os nós ancestrais.

### Requisito 5: Distribuição do PV ao Longo do Tempo

**User Story:** Como Gerente_de_Projeto, eu quero distribuir o orçamento de cada Pacote de Trabalho ao longo do tempo, para que o sistema gere a curva de Planned Value (PV) cumulativa que servirá de referência para o EVM.

#### Critérios de Aceitação

1. WHEN o Gerente_de_Projeto seleciona distribuição linear para um Pacote_de_Trabalho, THE Sistema SHALL distribuir o BAC uniformemente entre a data de início e a data de fim do Pacote_de_Trabalho, gerando valores de PV por período.
2. WHEN o Gerente_de_Projeto seleciona distribuição personalizada para um Pacote_de_Trabalho, THE Sistema SHALL permitir a entrada manual de valores de PV para cada período entre a data de início e a data de fim.
3. THE Sistema SHALL validar que a soma dos valores de PV distribuídos por período é igual ao BAC do Pacote_de_Trabalho.
4. THE Sistema SHALL calcular o PV cumulativo de cada Pacote_de_Trabalho como a soma acumulada dos valores de PV por período.
5. THE Sistema SHALL agregar o PV cumulativo dos Pacotes_de_Trabalho para calcular o PV cumulativo de Entregas, Fases e do Projeto.
6. IF o Gerente_de_Projeto altera o BAC ou as datas de um Pacote_de_Trabalho que possui distribuição de PV, THEN THE Sistema SHALL solicitar a redistribuição do PV.
7. THE Serializador_PV SHALL formatar a Distribuição_PV como uma estrutura de dados contendo período e valor para cada entrada.
8. THE Deserializador_PV SHALL reconstruir a Distribuição_PV a partir da estrutura de dados serializada.
9. FOR ALL Distribuições_PV válidas, serializar e depois deserializar SHALL produzir uma Distribuição_PV equivalente à original (propriedade de ida e volta).

### Requisito 6: Congelamento de Baseline (Baseline Freeze)

**User Story:** Como Gerente_de_Projeto, eu quero congelar a Baseline do projeto, para que ela sirva como referência imutável para as medições de EVM.

#### Critérios de Aceitação

1. WHEN o Gerente_de_Projeto solicita o congelamento da Baseline, THE Sistema SHALL verificar que todos os Pacotes_de_Trabalho possuem BAC, datas de início/fim e distribuição de PV definidos.
2. IF algum Pacote_de_Trabalho não possui BAC, datas ou distribuição de PV definidos, THEN THE Sistema SHALL rejeitar o congelamento e listar os Pacotes_de_Trabalho incompletos.
3. WHEN todos os Pacotes_de_Trabalho estão completos, THE Sistema SHALL criar uma Versão_Baseline com número sequencial, data de congelamento e snapshot completo da EAP, orçamentos e distribuição de PV.
4. WHILE uma Baseline está congelada, THE Sistema SHALL impedir alterações na EAP, nos orçamentos e nas distribuições de PV associados àquela Versão_Baseline.
5. THE Sistema SHALL manter o histórico de todas as Versões_Baseline do Projeto, permitindo consulta a qualquer versão anterior.
6. THE Sistema SHALL marcar exatamente uma Versão_Baseline como ativa por Projeto. A Versão_Baseline ativa é a referência para cálculos de EVM.

### Requisito 7: Controle de Mudanças de Baseline

**User Story:** Como Gerente_de_Projeto, eu quero criar uma nova versão de Baseline quando houver necessidade de mudança após o congelamento, para que o histórico de planejamento seja preservado e rastreável.

#### Critérios de Aceitação

1. WHEN o Gerente_de_Projeto solicita uma mudança de Baseline, THE Sistema SHALL criar um rascunho de nova Versão_Baseline copiando os dados da Versão_Baseline ativa.
2. WHILE o rascunho de Versão_Baseline está em edição, THE Sistema SHALL permitir alterações na EAP, orçamentos e distribuições de PV do rascunho sem afetar a Versão_Baseline ativa.
3. WHEN o Gerente_de_Projeto solicita o congelamento do rascunho, THE Sistema SHALL aplicar as mesmas validações do Requisito 6 e, se aprovado, congelar o rascunho como nova Versão_Baseline.
4. WHEN uma nova Versão_Baseline é congelada, THE Sistema SHALL registrar a justificativa da mudança fornecida pelo Gerente_de_Projeto.
5. WHEN uma nova Versão_Baseline é congelada, THE Sistema SHALL marcá-la como ativa e desativar a Versão_Baseline anterior, preservando o histórico.

### Requisito 8: Trilha de Auditoria

**User Story:** Como Diretor_de_Portfólio, eu quero que todas as alterações em Baselines, EAP e orçamentos sejam registradas em uma trilha de auditoria, para que eu possa rastrear quem fez cada mudança e quando.

#### Critérios de Aceitação

1. WHEN qualquer alteração é realizada em um Projeto, Nó_EAP, orçamento ou Baseline, THE Sistema SHALL registrar na Trilha_de_Auditoria o usuário, a data/hora, o tipo de operação, o valor anterior e o valor novo.
2. THE Sistema SHALL registrar na Trilha_de_Auditoria as seguintes operações: criação de Projeto, edição de Projeto, criação de Nó_EAP, edição de Nó_EAP, remoção de Nó_EAP, alteração de BAC, alteração de datas, alteração de Distribuição_PV, congelamento de Baseline e mudança de Baseline ativa.
3. THE Trilha_de_Auditoria SHALL ser imutável. O Sistema SHALL impedir a edição ou exclusão de registros de auditoria.
4. WHEN o Diretor_de_Portfólio ou o Gerente_de_Projeto consulta a Trilha_de_Auditoria, THE Sistema SHALL permitir filtrar por Projeto, tipo de operação, usuário e intervalo de datas.

### Requisito 9: Controle de Acesso (RBAC)

**User Story:** Como Diretor_de_Portfólio, eu quero que o acesso às funcionalidades do módulo seja controlado por papéis, para que cada usuário tenha acesso apenas às operações autorizadas.

#### Critérios de Aceitação

1. THE Sistema SHALL definir os papéis Gerente_de_Projeto e Diretor_de_Portfólio com permissões distintas.
2. WHILE o usuário possui o papel Gerente_de_Projeto, THE Sistema SHALL permitir criar, editar e remover Projetos, Nós_EAP, orçamentos, distribuições de PV e Baselines.
3. WHILE o usuário possui o papel Diretor_de_Portfólio, THE Sistema SHALL permitir visualizar Projetos, EAPs, orçamentos, Baselines e Trilha_de_Auditoria em modo somente leitura.
4. IF um usuário sem permissão tenta executar uma operação restrita, THEN THE Sistema SHALL rejeitar a operação e retornar uma mensagem de acesso negado.
5. THE Sistema SHALL associar cada usuário a um ou mais papéis.

### Requisito 10: Agregação Bottom-Up de Métricas

**User Story:** Como Gerente_de_Projeto, eu quero que os valores de BAC e PV sejam automaticamente agregados dos níveis mais baixos da EAP até o nível do Projeto, para que eu tenha visibilidade consolidada do planejamento em qualquer nível.

#### Critérios de Aceitação

1. THE Motor_de_Agregação SHALL calcular o BAC de qualquer Nó_EAP não-folha como a soma dos BACs de seus filhos diretos.
2. THE Motor_de_Agregação SHALL calcular o PV cumulativo de qualquer Nó_EAP não-folha como a soma dos PVs cumulativos de seus filhos diretos, por período.
3. WHEN um Pacote_de_Trabalho é adicionado, removido ou tem seu BAC alterado, THE Motor_de_Agregação SHALL recalcular os valores agregados de todos os nós ancestrais até o nível do Projeto.
4. THE Motor_de_Agregação SHALL produzir o mesmo resultado independentemente da ordem em que os Pacotes_de_Trabalho são processados (propriedade de confluência).
5. FOR ALL árvores EAP válidas, o BAC do Projeto SHALL ser igual à soma dos BACs de todos os Pacotes_de_Trabalho folha.
