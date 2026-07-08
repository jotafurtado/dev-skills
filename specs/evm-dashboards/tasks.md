# Implementation Plan: Módulo de Dashboards e Relatórios (Visualização)

## Overview

Implementação incremental do Módulo 4.4 — Dashboards e Relatórios — da plataforma EVM. O módulo é puramente de leitura/visualização, consumindo dados dos services existentes (`EvmCalculationEngine`, `EvCalculationService`, `PvDistributionService`, `AggregationService`). A única alteração de schema é a adição da coluna `evm_thresholds` (JSON nullable) na tabela `projects`.

A ordem de implementação segue: migration + model extension → service → widgets → pages → integração final.

## Tasks

- [ ]   1. Migration e extensão do Model Project
    - [ ] 1.1 Criar migration para adicionar coluna `evm_thresholds` (JSON nullable) à tabela `projects`
        - Usar `$table->json('evm_thresholds')->nullable()->after('active_baseline_id')`
        - Executar a migration para validar
        - _Requirements: 7.1, 7.2, 7.4_
    - [ ] 1.2 Estender o model `Project` com `evm_thresholds`
        - Adicionar `'evm_thresholds'` ao `$fillable`
        - Adicionar `'evm_thresholds' => 'array'` ao `casts()`
        - Implementar métodos helper `getGreenThreshold(): float` e `getYellowThreshold(): float` que retornam os valores customizados ou os defaults do `HealthStatus` enum
        - _Requirements: 7.2, 7.4_
    - [ ] 1.3 Estender o enum `HealthStatus` com `fromIndexWithThresholds()`
        - Adicionar método estático `fromIndexWithThresholds(?float $index, float $greenThreshold = self::GREEN_THRESHOLD, float $yellowThreshold = self::YELLOW_THRESHOLD): self`
        - Lógica: null → Gray, index ≥ greenThreshold → Green, index ≥ yellowThreshold → Yellow, else → Red
        - _Requirements: 6.4, 6.5, 6.6, 6.7, 7.2_
    - [ ]\* 1.4 Escrever property test para classificação com limiares customizados
        - **Property 8: Custom threshold classification and validation**
        - Gerar pares (greenThreshold, yellowThreshold) e índices aleatórios com `repeat(100)`
        - Verificar classificação correta e rejeição quando green ≤ yellow
        - **Validates: Requirements 7.2, 7.3, 7.4**

- [ ]   2. Implementar SCurveDataService
    - [ ] 2.1 Criar `app/Services/SCurveDataService.php`
        - Injetar `PvDistributionService` e `EvmCalculationEngine` via construtor
        - Implementar `generate(Project $project, ?WbsNode $scopeNode = null): array`
        - Implementar `generatePeriods()` — lista de "YYYY-MM" do planned_start ao planned_end usando `CarbonPeriod`
        - Implementar `formatLabel()` — converte "YYYY-MM" para "MMM/YY" em pt-BR
        - Implementar `getWorkPackagesInScope()` — coleta WPs do projeto inteiro ou descendentes de um nó
        - Implementar `buildCumulativePv()` — soma running de PV distributions por período
        - Implementar `buildCumulativeEv()` — soma running de earned_value de measurements com carry-forward
        - Implementar `buildCumulativeAc()` — soma running de actual_cost com carry-forward
        - Implementar `buildProjection()` — interpolação linear do AC atual até EAC no período final
        - Retornar array vazio quando projeto sem baseline ativa ou sem status_date
        - _Requirements: 1.1, 1.2, 1.3, 1.4, 1.5, 1.6, 1.7, 9.1, 9.2, 9.3_
    - [ ]\* 2.2 Escrever property test para dados cumulativos da Curva S
        - **Property 1: SCurve cumulative data correctness**
        - Gerar projetos com WPs, PV distributions, measurements e actual costs aleatórios com `repeat(100)`
        - Verificar que PV, EV e AC cumulativos são monotonicamente não-decrescentes
        - Verificar que PV cumulativo = soma running das distribuições PV
        - **Validates: Requirements 1.1, 1.2, 1.3, 1.4**
    - [ ]\* 2.3 Escrever property test para endpoint da projeção = EAC
        - **Property 2: SCurve projection endpoint equals EAC**
        - Gerar projetos com dados EVM válidos com `repeat(100)`
        - Verificar que o último valor não-null da projeção = EAC do `EvmCalculationEngine` (tolerância 0.01)
        - **Validates: Requirements 1.6**
    - [ ]\* 2.4 Escrever property test para formato e ordenação de períodos
        - **Property 3: Period format and chronological ordering**
        - Gerar projetos com datas variadas com `repeat(100)`
        - Verificar formato "YYYY-MM", ordenação ascendente, primeiro período = mês do planned_start, último = mês do planned_end
        - **Validates: Requirements 1.7, 2.6**
    - [ ]\* 2.5 Escrever property test para Curva S com escopo de nó EAP
        - **Property 9: Scoped SCurve data includes only descendant work packages**
        - Gerar árvores EAP com múltiplos nós, selecionar um nó não-folha como filtro com `repeat(100)`
        - Verificar que PV, EV e AC incluem apenas WPs descendentes do nó selecionado
        - **Validates: Requirements 9.2**

- [ ]   3. Checkpoint — Validar service e model
    - Ensure all tests pass, ask the user if questions arise.

- [ ]   4. Implementar widgets do Dashboard EVM do Projeto
    - [ ] 4.1 Criar `EvmStatsWidget` em `app/Filament/Resources/Projects/Widgets/EvmStatsWidget.php`
        - Estender `StatsOverviewWidget`
        - Receber `$projectId` como propriedade Livewire pública
        - Exibir 12 stat cards: PV, EV, AC, BAC, SV, CV, SPI, CPI, EAC, ETC, VAC, TCPI
        - Formatar valores monetários em BRL (R$), índices com 4 casas decimais
        - Exibir "N/D" para SPI, CPI, TCPI quando null
        - Exibir HealthStatus com cor e ícone nos cards de SPI, CPI e overall
        - Quando projeto sem baseline/status_date: valores zero com HealthStatus Gray
        - _Requirements: 3.1, 3.2, 3.3, 3.4, 3.5, 3.6_
    - [ ]\* 4.2 Escrever property test para completude das métricas do stats widget
        - **Property 4: Stats widget metric completeness**
        - Gerar EvmSnapshots aleatórios (incluindo nulls) com `repeat(100)`
        - Verificar que 12 métricas estão presentes com formatação correta
        - **Validates: Requirements 3.1, 3.4, 3.5, 3.6**
    - [ ] 4.3 Criar `SCurveChartWidget` em `app/Filament/Resources/Projects/Widgets/SCurveChartWidget.php`
        - Estender `ChartWidget` com `getType() = 'line'`
        - Receber `$projectId` e `$wbsNodeFilter` como propriedades Livewire
        - Configurar `$pollingInterval = null`
        - Implementar `getData()` com 5 datasets: PV (azul), EV (verde), AC (vermelho), Projeção EAC (tracejada cinza), BAC (horizontal laranja)
        - Implementar `getOptions()` com formatação BRL no eixo Y e labels "MMM/YY" no eixo X
        - Exibir mensagem de estado vazio quando sem dados
        - _Requirements: 2.1, 2.2, 2.3, 2.4, 2.5, 2.6_
    - [ ] 4.4 Criar `WorkPackageHealthWidget` em `app/Filament/Resources/Projects/Widgets/WorkPackageHealthWidget.php`
        - Widget customizado com tabela Filament
        - Receber `$projectId` e limiares (green/yellow) como propriedades Livewire
        - Listar todos os WPs do projeto com: nome, código, % completo, EV, AC, CPI, HealthStatus (ícone + cor)
        - Classificar cada WP usando `HealthStatus::fromIndexWithThresholds()` com limiares do projeto
        - Ordenar por severidade: Red → Yellow → Green → Gray
        - Implementar filtro por HealthStatus
        - Formatar EV e AC em BRL, CPI com 4 casas decimais
        - _Requirements: 6.1, 6.2, 6.3, 6.4, 6.5, 6.6, 6.7, 6.8_
    - [ ]\* 4.5 Escrever property test para classificação e ordenação de WPs por saúde
        - **Property 7: Work package health classification and severity ordering**
        - Gerar WPs com CPI variados (incluindo null) e limiares customizados com `repeat(100)`
        - Verificar classificação correta e ordenação Red → Yellow → Green → Gray
        - **Validates: Requirements 6.1, 6.2, 6.3, 6.4, 6.5, 6.6, 6.7**

- [ ]   5. Implementar widgets do Dashboard do Portfólio
    - [ ] 5.1 Criar `BullseyeChartWidget` em `app/Filament/Widgets/BullseyeChartWidget.php`
        - Estender `ChartWidget` com `getType() = 'scatter'`
        - Configurar `$pollingInterval = null`
        - Implementar `getData()` com datasets de pontos coloridos por OverallHealth (green, yellow, red, gray)
        - Adicionar datasets extras para linhas de referência em SPI=1.0, CPI=1.0, SPI=0.9, CPI=0.9
        - Implementar tooltips com nome do projeto
        - Excluir projetos com SPI ou CPI null
        - Exibir mensagem de estado vazio quando nenhum projeto elegível
        - _Requirements: 4.1, 4.2, 4.3, 4.4, 4.5, 4.6, 4.7_
    - [ ]\* 5.2 Escrever property test para projetos elegíveis no Bullseye Chart
        - **Property 5: Bullseye chart plots eligible projects with correct colors**
        - Gerar conjuntos de projetos com SPI/CPI variados (incluindo null) com `repeat(100)`
        - Verificar que apenas projetos com SPI e CPI não-null são plotados, com cores corretas
        - **Validates: Requirements 4.1, 4.3, 4.5**
    - [ ] 5.3 Criar `PortfolioStatsWidget` em `app/Filament/Widgets/PortfolioStatsWidget.php`
        - Estender `StatsOverviewWidget`
        - Exibir métricas consolidadas do portfólio: PV, EV, AC, BAC, SV, CV, SPI, CPI, EAC, VAC, OverallHealth
        - Exibir contagem de projetos por HealthStatus (Green, Yellow, Red, Gray)
        - Formatar valores monetários em BRL, índices com 4 casas decimais
        - Quando nenhum projeto com status_date: valores zero com HealthStatus Gray
        - _Requirements: 5.1, 5.2, 5.3, 5.4_
    - [ ]\* 5.4 Escrever property test para contagem de saúde do portfólio
        - **Property 6: Portfolio health status counts**
        - Gerar projetos com HealthStatus variados com `repeat(100)`
        - Verificar que soma das contagens = total de projetos com status_date, e cada contagem individual está correta
        - **Validates: Requirements 5.2**
    - [ ] 5.5 Criar `ProjectComparisonWidget` em `app/Filament/Widgets/ProjectComparisonWidget.php`
        - Widget customizado com tabela Filament
        - Listar todos os projetos com colunas: nome, status_date, BAC, PV, EV, AC, SV, CV, SPI, CPI, EAC, VAC, OverallHealth
        - Permitir ordenação por qualquer coluna numérica
        - Colorir coluna OverallHealth conforme HealthStatus
        - Projetos sem status_date: exibir "Sem Data de Status" e valores zero
        - Formatar monetários em BRL, índices com 4 casas decimais
        - _Requirements: 10.1, 10.2, 10.3, 10.4, 10.5_
    - [ ]\* 5.6 Escrever property test para completude da tabela comparativa
        - **Property 10: Project comparison table completeness**
        - Gerar projetos com/sem status_date com `repeat(100)`
        - Verificar que cada projeto tem uma linha com todas as colunas, e projetos sem status_date exibem zeros
        - **Validates: Requirements 10.1, 10.5**

- [ ]   6. Checkpoint — Validar widgets
    - Ensure all tests pass, ask the user if questions arise.

- [ ]   7. Implementar páginas Filament e integração
    - [ ] 7.1 Criar `EvmDashboardPage` em `app/Filament/Resources/Projects/Pages/EvmDashboardPage.php`
        - Custom page com `InteractsWithRecord` no `ProjectResource`
        - Definir `$title = 'Dashboard EVM'`, `$navigationLabel = 'Dashboard EVM'`, `$navigationIcon = 'heroicon-o-chart-bar'`
        - Propriedade Livewire `$wbsNodeFilter` (nullable int) para filtro de nó EAP
        - Implementar `configureThresholdsAction()` — Action modal com formulário para green_threshold e yellow_threshold
        - Validar green_threshold > yellow_threshold, ambos positivos
        - Salvar limiares em `$project->evm_thresholds` via `update()`
        - Criar view Blade `resources/views/filament/resources/projects/pages/evm-dashboard.blade.php`
        - Incluir select para filtro de nó EAP (fases e entregas do projeto)
        - Montar widgets: `EvmStatsWidget`, `SCurveChartWidget`, `WorkPackageHealthWidget`
        - _Requirements: 2.1, 2.3, 3.1, 6.1, 7.1, 7.3, 8.1, 9.1_
    - [ ] 7.2 Registrar `EvmDashboardPage` no `ProjectResource`
        - Adicionar `'evm-dashboard' => EvmDashboardPage::route('/{record}/evm-dashboard')` em `getPages()`
        - Adicionar `EvmDashboardPage::class` ao array de `getRecordSubNavigation()`
        - _Requirements: 8.1_
    - [ ] 7.3 Criar `PortfolioDashboard` em `app/Filament/Pages/PortfolioDashboard.php`
        - Standalone page com `$navigationIcon = 'heroicon-o-chart-pie'`, `$navigationLabel = 'Portfólio'`, `$title = 'Dashboard do Portfólio'`
        - Definir `$navigationSort = 1` para posição no menu
        - Implementar `canAccess()` — acessível para PM e Director
        - Criar view Blade `resources/views/filament/pages/portfolio-dashboard.blade.php`
        - Montar widgets: `PortfolioStatsWidget`, `BullseyeChartWidget`, `ProjectComparisonWidget`
        - _Requirements: 4.1, 5.1, 8.2, 8.4, 8.5, 10.1_
    - [ ]\* 7.4 Escrever testes de autorização e renderização das páginas
        - Testar que PM acessa Dashboard EVM dos próprios projetos
        - Testar que Director acessa Dashboard EVM de todos os projetos
        - Testar que PM e Director acessam PortfolioDashboard
        - Testar renderização das páginas sem erros com dados válidos e sem dados
        - Testar sub-navegação inclui aba "Dashboard EVM"
        - Testar navegação principal inclui "Portfólio"
        - _Requirements: 8.1, 8.2, 8.3, 8.4, 8.5_

- [ ]   8. Final checkpoint — Validar integração completa
    - Ensure all tests pass, ask the user if questions arise.

## Notes

- Tasks marcadas com `*` são opcionais e podem ser puladas para um MVP mais rápido
- Cada task referencia requisitos específicos para rastreabilidade
- Checkpoints garantem validação incremental
- Property tests validam propriedades universais de corretude definidas no design
- Unit tests validam exemplos específicos e edge cases
- Todos os widgets usam `$pollingInterval = null` — sem polling automático
- UI inteiramente em pt-BR conforme convenções do projeto
- Valores monetários em BRL (R$), índices com 4 casas decimais
