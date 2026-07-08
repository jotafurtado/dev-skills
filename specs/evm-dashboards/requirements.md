# Requirements Document — Módulo de Dashboards e Relatórios (Visualização)

## Introduction

Este documento define os requisitos do Módulo de Dashboards e Relatórios da plataforma EVM, correspondente ao Módulo 4.4 do PRD. O módulo consome os dados calculados pelo `EvmCalculationEngine` (Módulo 4.3) e os apresenta em visualizações interativas que permitem ao Gerente de Projeto e ao Diretor de Portfólio monitorar a saúde dos projetos em tempo real.

As três visualizações principais são:

1. **Curva S Interativa** — gráfico de linhas cumulativas de PV, EV e AC ao longo do tempo, com projeção do EAC até o final do projeto.
2. **Matriz SPI × CPI (Bullseye Chart)** — gráfico de dispersão plotando todos os projetos do portfólio em quadrantes de saúde.
3. **Alertas e Faróis** — painel com limites de tolerância configuráveis para destacar pacotes de trabalho problemáticos.

O módulo é puramente de leitura e visualização — não cria novas tabelas no banco de dados. Toda a lógica de cálculo já existe nos services dos módulos anteriores.

## Glossary

- **Dashboard_EVM**: Página Filament customizada que exibe widgets de visualização EVM para um projeto específico.
- **Dashboard_Portfolio**: Página Filament customizada que exibe widgets de visualização EVM consolidados para o portfólio de projetos.
- **Curva_S**: Gráfico de linhas cumulativas sobrepondo PV (Planned Value), EV (Earned Value) e AC (Actual Cost) ao longo do tempo, com projeção do EAC (Estimate at Completion).
- **Bullseye_Chart**: Gráfico de dispersão (scatter plot) que plota projetos em um plano cartesiano SPI × CPI, dividido em quadrantes de saúde.
- **Painel_Farois**: Widget que exibe pacotes de trabalho classificados por farol (Verde, Amarelo, Vermelho) com base nos limiares de tolerância configurados.
- **SCurveDataService**: Service que monta as séries temporais de PV, EV e AC cumulativos por período para alimentar o gráfico da Curva S.
- **EvmCalculationEngine**: Service existente (Módulo 4.3) que calcula todas as métricas derivadas de EVM.
- **EvmSnapshot**: DTO existente (Módulo 4.3) que encapsula todas as métricas EVM calculadas.
- **HealthStatus**: Enum existente (Módulo 4.3) com valores Green, Yellow, Red, Gray para classificação semafórica.
- **PvDistributionService**: Service existente (Módulo 4.1) que fornece a distribuição de PV por período.
- **EvCalculationService**: Service existente (Módulo 4.2) que fornece EV e AC agregados.
- **Limiar_Tolerancia**: Valores numéricos que definem os limites entre as classificações semafóricas (Verde ≥ 1.0, Amarelo ≥ 0.9, Vermelho < 0.9).
- **Projecao_EAC**: Linha tracejada no gráfico da Curva S que projeta o custo estimado (EAC) do ponto atual até o final do projeto.

## Requirements

### Requirement 1: Dados da Curva S (SCurveDataService)

**User Story:** Como Gerente de Projeto, quero que o sistema monte séries temporais de PV, EV e AC cumulativos por período mensal, para que eu possa visualizar a Curva S do meu projeto.

#### Acceptance Criteria

1. WHEN a project with an active frozen baseline and a defined status date is provided, THE SCurveDataService SHALL return an array of monthly periods from the project's planned start date to the planned end date, each containing the cumulative PV, cumulative EV, and cumulative AC values for that period.
2. THE SCurveDataService SHALL calculate cumulative PV for each period by summing the PV distribution values of all work packages up to and including that period.
3. THE SCurveDataService SHALL calculate cumulative EV for each period by summing the earned values from measurements at or before that period for all work packages, using carry-forward logic for periods without explicit measurements.
4. THE SCurveDataService SHALL calculate cumulative AC for each period by summing the actual costs recorded at or before that period for all work packages, using carry-forward logic for periods without explicit records.
5. WHEN a project has no active baseline or no status date, THE SCurveDataService SHALL return an empty array.
6. THE SCurveDataService SHALL include a projection series from the status date period to the project end date, where the final projected value equals the EAC calculated by the EvmCalculationEngine.
7. THE SCurveDataService SHALL return period labels in the format "YYYY-MM" sorted chronologically.

### Requirement 2: Visualização da Curva S

**User Story:** Como Gerente de Projeto, quero visualizar um gráfico de Curva S interativo com as linhas de PV, EV e AC sobrepostas, para que eu possa identificar desvios de prazo e custo ao longo do tempo.

#### Acceptance Criteria

1. THE Dashboard_EVM SHALL display a line chart (Curva_S) with three series: PV (linha azul), EV (linha verde) and AC (linha vermelha), plotted over monthly periods on the x-axis and values monetários cumulativos on the y-axis.
2. THE Curva_S SHALL display a fourth dashed series representing the Projecao_EAC, starting from the current status date period and ending at the project's planned end date with the EAC value.
3. WHEN the project has no active baseline or no status date, THE Dashboard_EVM SHALL display a message informing the user that a baseline and status date are required to view the Curva S.
4. THE Curva_S SHALL display the BAC (Budget at Completion) as a horizontal reference line across the chart.
5. THE Curva_S SHALL format monetary values on the y-axis in BRL (R$) notation.
6. THE Curva_S SHALL display period labels on the x-axis in "MMM/YY" format for readability.

### Requirement 3: Painel de Métricas EVM do Projeto

**User Story:** Como Gerente de Projeto, quero ver um resumo das métricas EVM atuais do meu projeto em cards de destaque, para que eu tenha uma visão rápida da saúde do projeto.

#### Acceptance Criteria

1. THE Dashboard_EVM SHALL display stat widgets showing the current values of PV, EV, AC, BAC, SV, CV, SPI, CPI, EAC, ETC, VAC and TCPI, obtained from the EvmSnapshot of the project.
2. THE Dashboard_EVM SHALL display the HealthStatus classification (schedule, cost, overall) with the corresponding color (success, warning, danger, gray) and icon for each metric card where applicable.
3. WHEN the project has no active baseline or no status date, THE Dashboard_EVM SHALL display all metric values as zero with HealthStatus Gray.
4. THE Dashboard_EVM SHALL format monetary metric values (PV, EV, AC, BAC, SV, CV, EAC, ETC, VAC) in BRL (R$) notation.
5. THE Dashboard_EVM SHALL format index metric values (SPI, CPI, TCPI) with 4 decimal places.
6. WHEN SPI, CPI or TCPI is null, THE Dashboard_EVM SHALL display "N/D" (Não Disponível) instead of a numeric value.

### Requirement 4: Matriz SPI × CPI (Bullseye Chart) do Portfólio

**User Story:** Como Diretor de Portfólio, quero visualizar todos os projetos plotados em uma matriz SPI × CPI, para que eu identifique rapidamente quais projetos estão saudáveis e quais estão críticos.

#### Acceptance Criteria

1. THE Dashboard_Portfolio SHALL display a scatter chart (Bullseye_Chart) with SPI on the x-axis and CPI on the y-axis, plotting one point per project that has a defined status date and valid SPI and CPI values.
2. THE Bullseye_Chart SHALL draw reference lines at SPI = 1.0 and CPI = 1.0, dividing the chart into four quadrants.
3. THE Bullseye_Chart SHALL color each project point according to its OverallHealth classification: green for Green, yellow for Yellow, red for Red, and gray for Gray.
4. THE Bullseye_Chart SHALL display the project name as a label or tooltip for each plotted point.
5. WHEN a project has null SPI or null CPI, THE Bullseye_Chart SHALL exclude that project from the scatter plot.
6. WHEN no projects have valid SPI and CPI values, THE Bullseye_Chart SHALL display a message informing the user that there are no projects with data available for the chart.
7. THE Bullseye_Chart SHALL draw additional reference lines at SPI = 0.9 and CPI = 0.9 to delineate the Yellow/Red threshold zones.

### Requirement 5: Resumo de Saúde do Portfólio

**User Story:** Como Diretor de Portfólio, quero ver um resumo consolidado das métricas EVM do portfólio inteiro, para que eu tenha uma visão geral da saúde financeira e de cronograma de todos os projetos.

#### Acceptance Criteria

1. THE Dashboard_Portfolio SHALL display stat widgets showing the portfolio-level PV, EV, AC, BAC, SV, CV, SPI, CPI, EAC, VAC and OverallHealth, obtained from the portfolio EvmSnapshot.
2. THE Dashboard_Portfolio SHALL display a summary count of projects by HealthStatus category (Green, Yellow, Red, Gray).
3. WHEN no projects have a defined status date, THE Dashboard_Portfolio SHALL display all portfolio metric values as zero with HealthStatus Gray.
4. THE Dashboard_Portfolio SHALL format monetary values in BRL (R$) notation and index values with 4 decimal places.

### Requirement 6: Alertas e Faróis por Pacote de Trabalho

**User Story:** Como Gerente de Projeto, quero visualizar uma lista de pacotes de trabalho classificados por farol (Verde, Amarelo, Vermelho), para que eu identifique rapidamente os pacotes problemáticos que precisam de atenção.

#### Acceptance Criteria

1. THE Painel_Farois SHALL display a table listing all work packages of the project with their current HealthStatus classification based on CPI.
2. THE Painel_Farois SHALL sort work packages by severity: Red first, then Yellow, then Green, then Gray.
3. THE Painel_Farois SHALL display for each work package: name, code, percent complete, EV, AC, CPI, and HealthStatus icon with color.
4. WHEN a work package has CPI < 0.9, THE Painel_Farois SHALL classify it as Red (Crítico).
5. WHEN a work package has CPI >= 0.9 and CPI < 1.0, THE Painel_Farois SHALL classify it as Yellow (Atenção).
6. WHEN a work package has CPI >= 1.0, THE Painel_Farois SHALL classify it as Green (Saudável).
7. WHEN a work package has null CPI (AC = 0), THE Painel_Farois SHALL classify it as Gray (Sem Dados).
8. THE Painel_Farois SHALL allow filtering by HealthStatus category to show only work packages of a specific classification.

### Requirement 7: Limites de Tolerância Configuráveis

**User Story:** Como Gerente de Projeto, quero poder configurar os limites de tolerância dos faróis, para que eu adapte os alertas à realidade do meu projeto.

#### Acceptance Criteria

1. THE Dashboard_EVM SHALL provide a configuration interface where the user can set custom threshold values for the Yellow/Red boundary and the Green/Yellow boundary.
2. WHEN custom thresholds are provided, THE Painel_Farois SHALL use the custom values instead of the default thresholds (Green ≥ 1.0, Yellow ≥ 0.9).
3. IF the user sets a Green/Yellow threshold that is less than or equal to the Yellow/Red threshold, THEN THE Dashboard_EVM SHALL reject the configuration and display a validation error.
4. WHEN no custom thresholds are configured, THE Painel_Farois SHALL use the default thresholds defined in the HealthStatus enum (Green ≥ 1.0, Yellow ≥ 0.9).

### Requirement 8: Navegação e Acesso aos Dashboards

**User Story:** Como usuário da plataforma, quero acessar os dashboards de forma intuitiva a partir da navegação principal, para que eu encontre rapidamente as visualizações que preciso.

#### Acceptance Criteria

1. THE Dashboard_EVM SHALL be accessible as a sub-navigation tab within the Project resource, alongside the existing tabs (EAP, Medições, Baselines).
2. THE Dashboard_Portfolio SHALL be accessible from the main navigation menu of the Filament admin panel.
3. WHILE a user has the role of project_manager, THE Dashboard_EVM SHALL be accessible for projects created by that user.
4. WHILE a user has the role of portfolio_director, THE Dashboard_EVM SHALL be accessible for all projects, and THE Dashboard_Portfolio SHALL be accessible.
5. WHILE a user has the role of project_manager, THE Dashboard_Portfolio SHALL be accessible in read-only mode.

### Requirement 9: Curva S por Nó da EAP

**User Story:** Como Gerente de Projeto, quero visualizar a Curva S filtrada por um nó específico da EAP (Fase ou Entrega), para que eu analise o desempenho de partes específicas do projeto.

#### Acceptance Criteria

1. THE Dashboard_EVM SHALL provide a filter that allows the user to select a specific WBS node (Phase or Deliverable) to scope the Curva S data.
2. WHEN a WBS node filter is applied, THE SCurveDataService SHALL return cumulative PV, EV and AC values only for the descendant work packages of the selected node.
3. WHEN the WBS node filter is cleared, THE SCurveDataService SHALL return data for the entire project.

### Requirement 10: Tabela Comparativa de Projetos no Portfólio

**User Story:** Como Diretor de Portfólio, quero ver uma tabela comparativa com as métricas EVM de todos os projetos, para que eu compare o desempenho entre projetos de forma estruturada.

#### Acceptance Criteria

1. THE Dashboard_Portfolio SHALL display a table listing all projects with columns: project name, status date, BAC, PV, EV, AC, SV, CV, SPI, CPI, EAC, VAC, and OverallHealth.
2. THE Dashboard_Portfolio SHALL allow sorting the table by any numeric column.
3. THE Dashboard_Portfolio SHALL color the OverallHealth column cell according to the HealthStatus color (success, warning, danger, gray).
4. THE Dashboard_Portfolio SHALL format monetary columns in BRL (R$) notation and index columns with 4 decimal places.
5. WHEN a project has no status date, THE Dashboard_Portfolio SHALL display "Sem Data de Status" in the status date column and zero values for all metrics.
