# Documento de Requisitos — Módulo de Motor de Cálculo EVM (Monitoramento)

## Introdução

Este documento especifica os requisitos do Módulo de Motor de Cálculo EVM da plataforma de gestão de projetos baseada em Earned Value Management. O módulo é o núcleo analítico do sistema, responsável por calcular automaticamente as métricas derivadas de EVM — variações (SV, CV), índices de desempenho (SPI, CPI) e projeções (EAC, ETC, VAC, TCPI) — a partir das métricas base (PV, EV, AC) já fornecidas pelos módulos anteriores.

O módulo depende de dois módulos predecessores:

- **Módulo de Estruturação e Baseline** (spec: `project-structuring-baseline`): fornece os models `Project`, `WbsNode`, `Baseline`, `AuditLog`, `User`, e os services `AggregationService`, `PvDistributionService`, `BaselineService`. Fornece o PV (Planned Value) via distribuição na Baseline e o BAC (Budget at Completion).
- **Módulo de Apontamento e Medição** (spec: `measurement-tracking`): fornece os models `Measurement`, `ActualCost`, `WeightedMilestone`, e o service `EvCalculationService`. Fornece o EV (Earned Value) via medições e o AC (Actual Cost) via registros de custo real.

O `EvCalculationService` existente já calcula PV, EV e AC agregados no nível do projeto via `getEvmMetrics()`. Este módulo **estende** esse service (ou cria um novo `EvmCalculationEngine`) para calcular todas as métricas derivadas, agregar métricas em qualquer nível da EAP (não apenas no projeto), e consolidar métricas no nível de portfólio (múltiplos projetos).

As funcionalidades principais incluem:

- Cálculo de variações de cronograma (SV) e custo (CV) por pacote de trabalho e agregado
- Cálculo de índices de desempenho (SPI, CPI) com tratamento de divisão por zero
- Cálculo de projeções de custo final (EAC, ETC, VAC) e índice de desempenho necessário (TCPI)
- Agregação bottom-up de todas as métricas derivadas, do pacote de trabalho ao projeto
- Consolidação de métricas no nível de portfólio (múltiplos projetos)
- Classificação semafórica (Verde/Amarelo/Vermelho) baseada em limiares configuráveis de SPI e CPI
- Serialização e deserialização do snapshot completo de métricas EVM

## Glossário

- **Projeto**: Entidade raiz do planejamento EVM. Definida no módulo de Estruturação e Baseline.
- **Pacote_de_Trabalho**: Nível mais baixo da EAP (WBS), unidade de medição do EVM. Definido como `WbsNode` do tipo `work_package`.
- **Nó_EAP**: Elemento genérico da hierarquia da EAP. Pode ser Fase, Entrega ou Pacote de Trabalho.
- **Baseline**: Versão congelada do plano do projeto. Contém o snapshot com BAC e distribuição de PV.
- **Data_de_Status**: Data de corte (Status Date) para a qual os cálculos de EVM são processados. Definida no model `Project`.
- **BAC (Budget at Completion)**: Orçamento total planejado para um Pacote de Trabalho, conforme a Baseline ativa.
- **PV (Planned Value)**: Valor planejado acumulado até a Data_de_Status. Calculado pelo `PvDistributionService`.
- **EV (Earned Value)**: Valor agregado, calculado como BAC × % Complete. Calculado pelo `EvCalculationService`.
- **AC (Actual Cost)**: Custo real incorrido até a Data_de_Status. Registrado via `ActualCost`.
- **SV (Schedule Variance)**: Variação de cronograma. Calculada como EV - PV. Valor positivo indica adiantamento.
- **CV (Cost Variance)**: Variação de custo. Calculada como EV - AC. Valor positivo indica economia.
- **SPI (Schedule Performance Index)**: Índice de desempenho de cronograma. Calculado como EV / PV. Valor maior que 1 indica adiantamento.
- **CPI (Cost Performance Index)**: Índice de desempenho de custo. Calculado como EV / AC. Valor maior que 1 indica economia.
- **EAC (Estimate at Completion)**: Estimativa de custo final. Calculada como AC + (BAC - EV) / CPI.
- **ETC (Estimate to Complete)**: Estimativa para terminar. Calculada como EAC - AC.
- **VAC (Variance at Completion)**: Variação no término. Calculada como BAC - EAC.
- **TCPI (To-Complete Performance Index)**: Índice de desempenho necessário para terminar no orçamento. Calculado como (BAC - EV) / (BAC - AC).
- **Motor_de_Cálculo_EVM**: Service responsável por calcular todas as métricas derivadas de EVM a partir de PV, EV e AC.
- **Portfólio**: Conjunto de todos os Projetos da plataforma. As métricas de portfólio são a consolidação (soma) das métricas de todos os projetos.
- **Roll_Up**: Processo de agregação bottom-up das métricas, dos Pacotes de Trabalho até o nível do Projeto e do Projeto até o Portfólio.
- **Classificação_Semafórica**: Sistema de cores (Verde, Amarelo, Vermelho) que indica a saúde de um Pacote de Trabalho, Nó_EAP ou Projeto com base nos valores de SPI e CPI.
- **Limiar_de_Tolerância**: Valores configuráveis que definem os limites entre as faixas da Classificação_Semafórica.
- **Snapshot_EVM**: Estrutura de dados contendo todas as métricas EVM calculadas para um Nó_EAP ou Projeto em uma Data_de_Status.
- **Gerente_de_Projeto**: Ator que gerencia o projeto e consulta métricas EVM detalhadas.
- **Diretor_de_Portfólio**: Ator que visualiza a saúde consolidada dos projetos no nível de portfólio.

## Requisitos

### Requisito 1: Cálculo de Variações (SV e CV)

**User Story:** Como Gerente_de_Projeto, eu quero que o sistema calcule automaticamente as variações de cronograma (SV) e custo (CV) para cada Pacote de Trabalho e agregado para os níveis superiores da EAP, para que eu possa identificar rapidamente desvios em relação ao plano.

#### Critérios de Aceitação

1. WHEN o Motor_de_Cálculo_EVM processa as métricas de um Pacote_de_Trabalho na Data_de_Status, THE Motor_de_Cálculo_EVM SHALL calcular SV como EV - PV, onde EV e PV são os valores sincronizados para a mesma Data_de_Status.
2. WHEN o Motor_de_Cálculo_EVM processa as métricas de um Pacote_de_Trabalho na Data_de_Status, THE Motor_de_Cálculo_EVM SHALL calcular CV como EV - AC, onde EV e AC são os valores sincronizados para a mesma Data_de_Status.
3. THE Motor_de_Cálculo_EVM SHALL representar SV e CV como valores decimais com até duas casas decimais, onde valores positivos indicam desempenho favorável e valores negativos indicam desempenho desfavorável.
4. THE Motor_de_Cálculo_EVM SHALL agregar SV de um Nó_EAP não-folha como a soma dos SVs de seus filhos diretos, recursivamente até o nível do Projeto.
5. THE Motor_de_Cálculo_EVM SHALL agregar CV de um Nó_EAP não-folha como a soma dos CVs de seus filhos diretos, recursivamente até o nível do Projeto.
6. IF o PV e o EV de um Pacote_de_Trabalho são ambos zero na Data_de_Status, THEN THE Motor_de_Cálculo_EVM SHALL calcular SV como zero.
7. IF o EV e o AC de um Pacote_de_Trabalho são ambos zero na Data_de_Status, THEN THE Motor_de_Cálculo_EVM SHALL calcular CV como zero.

### Requisito 2: Cálculo de Índices de Desempenho (SPI e CPI)

**User Story:** Como Gerente_de_Projeto, eu quero que o sistema calcule automaticamente os índices de desempenho de cronograma (SPI) e custo (CPI) para cada Pacote de Trabalho e agregado para os níveis superiores, para que eu possa avaliar a eficiência do projeto em relação ao plano.

#### Critérios de Aceitação

1. WHEN o Motor_de_Cálculo_EVM processa as métricas de um Pacote_de_Trabalho na Data_de_Status, THE Motor_de_Cálculo_EVM SHALL calcular SPI como EV / PV.
2. WHEN o Motor_de_Cálculo_EVM processa as métricas de um Pacote_de_Trabalho na Data_de_Status, THE Motor_de_Cálculo_EVM SHALL calcular CPI como EV / AC.
3. IF o PV de um Pacote_de_Trabalho é zero na Data_de_Status, THEN THE Motor_de_Cálculo_EVM SHALL retornar SPI como nulo (indeterminado) em vez de causar erro de divisão por zero.
4. IF o AC de um Pacote_de_Trabalho é zero na Data_de_Status, THEN THE Motor_de_Cálculo_EVM SHALL retornar CPI como nulo (indeterminado) em vez de causar erro de divisão por zero.
5. IF o PV é zero e o EV é maior que zero, THEN THE Motor_de_Cálculo_EVM SHALL retornar SPI como nulo, indicando que o trabalho foi realizado antes do planejado sem referência de PV.
6. IF o AC é zero e o EV é maior que zero, THEN THE Motor_de_Cálculo_EVM SHALL retornar CPI como nulo, indicando que há valor agregado sem custo registrado.
7. THE Motor_de_Cálculo_EVM SHALL representar SPI e CPI como valores decimais com até quatro casas decimais.
8. THE Motor_de_Cálculo_EVM SHALL calcular SPI e CPI agregados para Nós_EAP não-folha utilizando os valores agregados de EV, PV e AC (SPI = EV_agregado / PV_agregado, CPI = EV_agregado / AC_agregado), e não como média dos índices dos filhos.

### Requisito 3: Cálculo de Projeções (EAC, ETC, VAC)

**User Story:** Como Gerente_de_Projeto, eu quero que o sistema calcule automaticamente as projeções de custo final (EAC), custo restante (ETC) e variação no término (VAC), para que eu possa antecipar se o projeto terminará dentro do orçamento.

#### Critérios de Aceitação

1. WHEN o Motor_de_Cálculo_EVM processa as métricas de um Pacote_de_Trabalho na Data_de_Status, THE Motor_de_Cálculo_EVM SHALL calcular EAC como AC + (BAC - EV) / CPI, utilizando o CPI calculado no Requisito 2.
2. WHEN o Motor_de_Cálculo_EVM processa as métricas de um Pacote_de_Trabalho na Data_de_Status, THE Motor_de_Cálculo_EVM SHALL calcular ETC como EAC - AC.
3. WHEN o Motor_de_Cálculo_EVM processa as métricas de um Pacote_de_Trabalho na Data_de_Status, THE Motor_de_Cálculo_EVM SHALL calcular VAC como BAC - EAC.
4. IF o CPI é nulo (AC é zero), THEN THE Motor_de_Cálculo_EVM SHALL calcular EAC como BAC - EV (assumindo que o trabalho restante custará conforme o planejado), ETC como BAC - EV, e VAC como zero.
5. IF o EV é igual ao BAC (Pacote_de_Trabalho 100% concluído), THEN THE Motor_de_Cálculo_EVM SHALL calcular EAC como AC, ETC como zero, e VAC como BAC - AC.
6. THE Motor_de_Cálculo_EVM SHALL representar EAC, ETC e VAC como valores decimais com até duas casas decimais.
7. THE Motor_de_Cálculo_EVM SHALL calcular EAC agregado para o Projeto como a soma dos EACs de todos os Pacotes_de_Trabalho folha.
8. THE Motor_de_Cálculo_EVM SHALL calcular ETC agregado para o Projeto como a soma dos ETCs de todos os Pacotes_de_Trabalho folha.
9. THE Motor_de_Cálculo_EVM SHALL calcular VAC agregado para o Projeto como BAC_projeto - EAC_projeto.

### Requisito 4: Cálculo do TCPI (To-Complete Performance Index)

**User Story:** Como Gerente_de_Projeto, eu quero que o sistema calcule o índice de desempenho necessário para terminar o projeto dentro do orçamento (TCPI), para que eu possa avaliar a viabilidade de recuperar desvios de custo.

#### Critérios de Aceitação

1. WHEN o Motor_de_Cálculo_EVM processa as métricas de um Pacote_de_Trabalho na Data_de_Status, THE Motor_de_Cálculo_EVM SHALL calcular TCPI como (BAC - EV) / (BAC - AC).
2. IF o BAC é igual ao AC (todo o orçamento já foi consumido), THEN THE Motor_de_Cálculo_EVM SHALL retornar TCPI como nulo (indeterminado), indicando que não há orçamento restante.
3. IF o EV é igual ao BAC (Pacote_de_Trabalho 100% concluído), THEN THE Motor_de_Cálculo_EVM SHALL retornar TCPI como nulo, pois não há trabalho restante.
4. IF o AC é maior que o BAC (custo já excedeu o orçamento), THEN THE Motor_de_Cálculo_EVM SHALL calcular TCPI normalmente (resultado será negativo), indicando que o orçamento original é inatingível.
5. THE Motor_de_Cálculo_EVM SHALL representar TCPI como valor decimal com até quatro casas decimais.
6. THE Motor_de_Cálculo_EVM SHALL calcular TCPI agregado para o Projeto utilizando os valores agregados: (BAC_projeto - EV_projeto) / (BAC_projeto - AC_projeto).

### Requisito 5: Agregação Bottom-Up de Métricas na EAP

**User Story:** Como Gerente_de_Projeto, eu quero que todas as métricas EVM sejam agregadas automaticamente dos Pacotes de Trabalho até o nível do Projeto, para que eu tenha visibilidade consolidada do desempenho em qualquer nível da EAP.

#### Critérios de Aceitação

1. THE Motor_de_Cálculo_EVM SHALL agregar PV, EV e AC de qualquer Nó_EAP não-folha como a soma dos respectivos valores de seus filhos diretos, recursivamente.
2. THE Motor_de_Cálculo_EVM SHALL agregar SV e CV de qualquer Nó_EAP não-folha como a soma dos respectivos valores de seus filhos diretos, recursivamente.
3. THE Motor_de_Cálculo_EVM SHALL calcular SPI e CPI de qualquer Nó_EAP não-folha utilizando os valores agregados de EV, PV e AC daquele nó (SPI = EV_nó / PV_nó, CPI = EV_nó / AC_nó), aplicando as mesmas regras de divisão por zero do Requisito 2.
4. THE Motor_de_Cálculo_EVM SHALL calcular EAC de qualquer Nó_EAP não-folha como a soma dos EACs de seus Pacotes_de_Trabalho descendentes.
5. THE Motor_de_Cálculo_EVM SHALL produzir o mesmo resultado de agregação independentemente da ordem em que os Pacotes_de_Trabalho são processados (propriedade de confluência).
6. FOR ALL árvores EAP válidas, o PV agregado do Projeto SHALL ser igual à soma dos PVs de todos os Pacotes_de_Trabalho folha na Data_de_Status.
7. FOR ALL árvores EAP válidas, o EV agregado do Projeto SHALL ser igual à soma dos EVs de todos os Pacotes_de_Trabalho folha na Data_de_Status.
8. FOR ALL árvores EAP válidas, o AC agregado do Projeto SHALL ser igual à soma dos ACs de todos os Pacotes_de_Trabalho folha na Data_de_Status.

### Requisito 6: Consolidação de Métricas no Nível de Portfólio

**User Story:** Como Diretor_de_Portfólio, eu quero visualizar as métricas EVM consolidadas de todos os projetos do portfólio, para que eu possa identificar rapidamente quais projetos estão consumindo a margem de lucro global.

#### Critérios de Aceitação

1. WHEN o Diretor_de_Portfólio solicita as métricas do Portfólio, THE Motor_de_Cálculo_EVM SHALL calcular PV_portfólio como a soma dos PVs de todos os Projetos que possuem Data_de_Status definida.
2. WHEN o Diretor_de_Portfólio solicita as métricas do Portfólio, THE Motor_de_Cálculo_EVM SHALL calcular EV_portfólio como a soma dos EVs de todos os Projetos que possuem Data_de_Status definida.
3. WHEN o Diretor_de_Portfólio solicita as métricas do Portfólio, THE Motor_de_Cálculo_EVM SHALL calcular AC_portfólio como a soma dos ACs de todos os Projetos que possuem Data_de_Status definida.
4. THE Motor_de_Cálculo_EVM SHALL calcular SPI_portfólio como EV_portfólio / PV_portfólio, aplicando as mesmas regras de divisão por zero do Requisito 2.
5. THE Motor_de_Cálculo_EVM SHALL calcular CPI_portfólio como EV_portfólio / AC_portfólio, aplicando as mesmas regras de divisão por zero do Requisito 2.
6. THE Motor_de_Cálculo_EVM SHALL calcular BAC_portfólio como a soma dos BACs de todos os Projetos que possuem Baseline ativa.
7. THE Motor_de_Cálculo_EVM SHALL calcular EAC_portfólio como a soma dos EACs de todos os Projetos que possuem Data_de_Status definida.
8. THE Motor_de_Cálculo_EVM SHALL calcular VAC_portfólio como BAC_portfólio - EAC_portfólio.
9. THE Motor_de_Cálculo_EVM SHALL excluir Projetos sem Data_de_Status definida dos cálculos de portfólio, sem causar erro.

### Requisito 7: Classificação Semafórica de Saúde

**User Story:** Como Diretor_de_Portfólio, eu quero que o sistema classifique automaticamente a saúde de cada Pacote de Trabalho, Nó da EAP e Projeto com base em cores semafóricas (Verde, Amarelo, Vermelho), para que eu possa identificar visualmente os itens problemáticos.

#### Critérios de Aceitação

1. THE Motor_de_Cálculo_EVM SHALL classificar a saúde de cronograma de um Nó_EAP ou Projeto como Verde quando SPI >= 1.0, Amarelo quando SPI >= 0.9 e SPI < 1.0, e Vermelho quando SPI < 0.9.
2. THE Motor_de_Cálculo_EVM SHALL classificar a saúde de custo de um Nó_EAP ou Projeto como Verde quando CPI >= 1.0, Amarelo quando CPI >= 0.9 e CPI < 1.0, e Vermelho quando CPI < 0.9.
3. IF o SPI ou CPI é nulo (indeterminado por divisão por zero), THEN THE Motor_de_Cálculo_EVM SHALL classificar a saúde como Cinza (sem dados suficientes).
4. THE Motor_de_Cálculo_EVM SHALL utilizar os Limiares_de_Tolerância padrão (Verde >= 1.0, Amarelo >= 0.9, Vermelho < 0.9) como valores default.
5. THE Motor_de_Cálculo_EVM SHALL classificar a saúde geral de um Nó_EAP ou Projeto como a pior classificação entre cronograma e custo (ex: se cronograma é Verde e custo é Vermelho, a saúde geral é Vermelho).

### Requisito 8: Sincronização de Métricas na Data de Status

**User Story:** Como Gerente_de_Projeto, eu quero que todas as métricas derivadas de EVM sejam calculadas com base nos mesmos valores de PV, EV e AC sincronizados na Data de Status, para que os indicadores sejam consistentes e confiáveis.

#### Critérios de Aceitação

1. THE Motor_de_Cálculo_EVM SHALL utilizar a Data_de_Status do Projeto como referência única para obter PV, EV e AC antes de calcular qualquer métrica derivada.
2. THE Motor_de_Cálculo_EVM SHALL obter o PV cumulativo da Baseline ativa até a Data_de_Status, o EV dos Registros de Medição na Data_de_Status (com carry-forward), e o AC dos Registros de Custo Real na Data_de_Status (com carry-forward), conforme implementado no `EvCalculationService` existente.
3. IF o Projeto não possui Data_de_Status definida, THEN THE Motor_de_Cálculo_EVM SHALL retornar todas as métricas derivadas como zero ou nulo, sem causar erro.
4. IF o Projeto não possui Baseline ativa, THEN THE Motor_de_Cálculo_EVM SHALL retornar todas as métricas derivadas como zero ou nulo, sem causar erro.
5. THE Motor_de_Cálculo_EVM SHALL garantir que o recálculo de métricas derivadas em uma nova Data_de_Status não altere os valores calculados para Datas_de_Status anteriores.

### Requisito 9: Métricas EVM por Nó da EAP

**User Story:** Como Gerente_de_Projeto, eu quero consultar as métricas EVM completas de qualquer nível da EAP (Fase, Entrega ou Pacote de Trabalho), para que eu possa analisar o desempenho em diferentes granularidades.

#### Critérios de Aceitação

1. WHEN o Gerente_de_Projeto solicita as métricas de um Pacote_de_Trabalho, THE Motor_de_Cálculo_EVM SHALL retornar PV, EV, AC, SV, CV, SPI, CPI, BAC, EAC, ETC, VAC e TCPI calculados para aquele pacote na Data_de_Status.
2. WHEN o Gerente_de_Projeto solicita as métricas de um Nó_EAP não-folha (Fase ou Entrega), THE Motor_de_Cálculo_EVM SHALL retornar as métricas agregadas de todos os Pacotes_de_Trabalho descendentes daquele nó.
3. WHEN o Gerente_de_Projeto solicita as métricas do Projeto, THE Motor_de_Cálculo_EVM SHALL retornar as métricas agregadas de todos os Pacotes_de_Trabalho do Projeto.
4. THE Motor_de_Cálculo_EVM SHALL retornar as métricas em uma estrutura de dados padronizada (Snapshot_EVM) contendo todas as métricas, a Data_de_Status e a classificação semafórica.

### Requisito 10: Serialização e Deserialização do Snapshot EVM

**User Story:** Como desenvolvedor, eu quero que o snapshot de métricas EVM seja serializado e deserializado de forma consistente, para que a integridade dos dados seja preservada em operações de leitura, escrita e transmissão para o frontend.

#### Critérios de Aceitação

1. THE Serializador_EVM SHALL formatar o Snapshot_EVM como uma estrutura JSON contendo: pv, ev, ac, bac, sv, cv, spi, cpi, eac, etc_value, vac, tcpi, schedule_health, cost_health, overall_health e status_date.
2. THE Deserializador_EVM SHALL reconstruir o Snapshot_EVM a partir da estrutura JSON serializada, preservando os tipos numéricos (float para valores monetários, float nullable para índices).
3. FOR ALL Snapshots_EVM válidos, serializar e depois deserializar SHALL produzir um Snapshot_EVM equivalente ao original (propriedade de ida e volta).
4. THE Serializador_EVM SHALL representar valores nulos (índices indeterminados) como `null` no JSON, e o Deserializador_EVM SHALL reconstruí-los como nulos.

### Requisito 11: Desempenho e Escalabilidade do Motor de Cálculo

**User Story:** Como Diretor_de_Portfólio, eu quero que o motor de cálculo EVM processe métricas de projetos com milhares de pacotes de trabalho sem degradação perceptível de performance, para que a plataforma seja viável em cenários reais de portfólio.

#### Critérios de Aceitação

1. THE Motor_de_Cálculo_EVM SHALL calcular todas as métricas EVM de um Projeto com até 1000 Pacotes_de_Trabalho em tempo adequado para uso interativo.
2. THE Motor_de_Cálculo_EVM SHALL utilizar eager loading para carregar a árvore EAP completa antes de iniciar a agregação, evitando o problema N+1 de queries.
3. THE Motor_de_Cálculo_EVM SHALL utilizar batch queries para obter medições e custos reais de todos os Pacotes_de_Trabalho de um Projeto em uma única consulta, em vez de consultar pacote por pacote.
4. THE Motor_de_Cálculo_EVM SHALL calcular as métricas de portfólio processando cada Projeto de forma independente e consolidando os resultados, sem carregar todos os Pacotes_de_Trabalho de todos os Projetos simultaneamente.

### Requisito 12: Trilha de Auditoria para Consultas de Métricas

**User Story:** Como Diretor_de_Portfólio, eu quero que as métricas EVM calculadas sejam rastreáveis, para que eu possa verificar a consistência dos dados apresentados nos dashboards.

#### Critérios de Aceitação

1. THE Motor_de_Cálculo_EVM SHALL registrar na Trilha_de_Auditoria quando as métricas EVM de um Projeto são recalculadas devido a alteração na Data_de_Status.
2. THE Motor_de_Cálculo_EVM SHALL registrar na Trilha_de_Auditoria quando as métricas EVM de um Projeto são recalculadas devido a novo registro de medição ou custo real.
3. THE Trilha_de_Auditoria SHALL utilizar o model `AuditLog` existente, registrando a operação como `evm_metrics_calculated` com os valores de PV, EV, AC, SPI e CPI no campo `new_values`.

### Requisito 13: Consistência Matemática das Métricas

**User Story:** Como Gerente_de_Projeto, eu quero que as métricas EVM calculadas sejam matematicamente consistentes entre si, para que eu possa confiar nos indicadores apresentados pelo sistema.

#### Critérios de Aceitação

1. FOR ALL Pacotes_de_Trabalho com métricas calculadas, SV SHALL ser igual a EV - PV, verificável pela relação SV = SPI × PV - PV quando SPI é definido.
2. FOR ALL Pacotes_de_Trabalho com métricas calculadas, CV SHALL ser igual a EV - AC, verificável pela relação CV = CPI × AC - AC quando CPI é definido.
3. FOR ALL Pacotes_de_Trabalho com EAC calculado, ETC SHALL ser igual a EAC - AC.
4. FOR ALL Pacotes_de_Trabalho com EAC calculado, VAC SHALL ser igual a BAC - EAC.
5. FOR ALL Pacotes_de_Trabalho com CPI definido e diferente de zero, EAC SHALL ser igual a AC + (BAC - EV) / CPI.
6. FOR ALL Projetos, o BAC agregado SHALL ser igual à soma dos BACs de todos os Pacotes_de_Trabalho folha (invariante de agregação preservada).
7. FOR ALL Projetos, SV_projeto SHALL ser igual a EV_projeto - PV_projeto, onde EV_projeto e PV_projeto são os valores agregados.
