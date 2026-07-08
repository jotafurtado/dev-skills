# Implementation Plan: Módulo de Apontamento e Medição (Execução)

## Overview

Implementação incremental do Módulo de Apontamento e Medição, que estende a arquitetura existente do Módulo de Estruturação e Baseline (`project-structuring-baseline`). O plano segue a ordem: migrations de alteração e novas tabelas → enum e models novos → service de cálculo EV → policies → extensões nos Filament Resources existentes → página customizada de medição → integração e wiring final. Cada tarefa constrói sobre as anteriores e sobre os componentes já implementados no primeiro spec.

## Tasks

- [x]   1. Criar migrations de alteração e novas tabelas
    - [x] 1.1 Criar migration para adicionar `status_date` na tabela `projects`
        - Adicionar coluna `status_date` (date, nullable) na tabela `projects`
        - Atualizar o model `Project`: adicionar `status_date` ao `$fillable`, cast para `date`
        - Adicionar validação no `booted()` do model: `status_date` >= `planned_start_date`, `status_date` <= `planned_end_date`, e `active_baseline_id` não pode ser null quando `status_date` é definida
        - Atualizar `ProjectFactory` com state method `withStatusDate()`
        - _Requirements: 1.1, 1.2, 1.3, 1.4_

    - [x] 1.2 Criar migration para adicionar `measurement_method` e `assigned_to` na tabela `wbs_nodes`
        - Adicionar coluna `measurement_method` (string, default 'physical_percent') na tabela `wbs_nodes`
        - Adicionar coluna `assigned_to` (bigint, FK users.id, nullable, set null on delete) na tabela `wbs_nodes`
        - Adicionar index em `assigned_to`
        - Criar enum `MeasurementMethod` com valores `zero_hundred`, `fifty_fifty`, `weighted_milestones`, `physical_percent` — implementar `HasLabel` (labels pt-BR: "0/100", "50/50", "Marcos Ponderados", "Percentual Físico"), `HasColor`, `HasIcon`
        - Atualizar o model `WbsNode`: adicionar colunas ao `$fillable`, cast `measurement_method` para enum, relationship `assignedTo()` (belongsTo User), relationship `measurements()`, `actualCosts()`, `weightedMilestones()`
        - Atualizar o model `User`: adicionar relationship `assignedWorkPackages()` (hasMany WbsNode where assigned_to)
        - Atualizar `WbsNodeFactory` com state method `withMeasurementMethod()` e `assignedTo(User $user)`
        - _Requirements: 2.1, 2.2, 2.6, 3.1, 3.2, 3.3_

    - [x] 1.3 Criar model `Measurement` com migration e factory
        - Executar `php artisan make:model Measurement -mf`
        - Migration: tabela `measurements` com `wbs_node_id` (FK cascade), `status_date` (date), `percent_complete` (decimal 5,2), `earned_value` (decimal 15,2), `measurement_method` (string), `completed_milestones` (json nullable)
        - Unique index em `(wbs_node_id, status_date)`
        - Index em `(wbs_node_id, status_date DESC)` para carry-forward queries
        - Model: fillable, casts (date, decimal, json, enum), relationships (`wbsNode`), `#[ObservedBy(AuditObserver::class)]`
        - Adicionar validação no `booted()`: `percent_complete` entre 0 e 100, validação por método de medição (0/100 aceita só 0 e 100; 50/50 aceita só 0, 50 e 100), progresso não pode regredir (monotonicity), bloquear edição de registros históricos (`status_date` < `project.status_date`)
        - Factory: gerar medições válidas com states por método
        - _Requirements: 4.1, 4.2, 4.3, 4.5, 4.6, 4.7, 4.8, 4.10, 6.2, 6.4_

    - [x] 1.4 Criar model `ActualCost` com migration e factory
        - Executar `php artisan make:model ActualCost -mf`
        - Migration: tabela `actual_costs` com `wbs_node_id` (FK cascade), `status_date` (date), `actual_cost` (decimal 15,2)
        - Unique index em `(wbs_node_id, status_date)`
        - Index em `(wbs_node_id, status_date DESC)` para carry-forward queries
        - Model: fillable, casts (date, decimal), relationships (`wbsNode`), `#[ObservedBy(AuditObserver::class)]`
        - Adicionar validação no `booted()`: `actual_cost` >= 0, bloquear edição de registros históricos
        - Factory: gerar custos reais válidos
        - _Requirements: 5.1, 5.2, 5.3, 5.4, 5.5, 5.6, 6.3, 6.4_

    - [x] 1.5 Criar model `WeightedMilestone` com migration e factory
        - Executar `php artisan make:model WeightedMilestone -mf`
        - Migration: tabela `weighted_milestones` com `wbs_node_id` (FK cascade), `description` (string 255), `weight` (decimal 5,2), `sort_order` (integer default 0)
        - Index em `(wbs_node_id, sort_order)`
        - Model: fillable, casts (decimal), relationships (`wbsNode`), `#[ObservedBy(AuditObserver::class)]`
        - Adicionar validação no `booted()`: `weight` > 0, soma dos pesos de todos os milestones do mesmo `wbs_node_id` deve ser <= 100 (validação na criação/atualização), bloquear remoção de marco já concluído em medição
        - Factory: gerar marcos válidos
        - _Requirements: 2.3, 2.4, 12.1, 12.2, 12.3, 12.4, 12.5, 12.6_

- [x]   2. Checkpoint — Verificar migrations e models
    - Executar `php artisan migrate` para validar todas as migrations
    - Executar `php artisan test --compact` para garantir que testes existentes continuam passando
    - Executar `vendor/bin/pint --dirty --format agent` para formatação
    - Perguntar ao usuário se há dúvidas

- [x]   3. Implementar EvCalculationService
    - [x] 3.1 Criar `EvCalculationService` com cálculo de EV, agregação e carry-forward
        - Criar `app/Services/EvCalculationService.php`
        - Método `calculateEv(WbsNode $wp, float $percentComplete): float` — calcula EV como BAC × (percentComplete / 100), usando BAC da Baseline ativa. Retorna 0 se BAC é null/zero
        - Método `recordMeasurement(WbsNode $wp, float $percentComplete, ?array $completedMilestones = null): Measurement` — valida, calcula EV, faz upsert via `updateOrCreate` na combinação (wbs_node_id, status_date), envolve em `DB::transaction()`
        - Método `recordActualCost(WbsNode $wp, float $actualCost): ActualCost` — valida, faz upsert via `updateOrCreate`
        - Método `calculateWeightedMilestonesPercent(WbsNode $wp, array $completedMilestoneIds): float` — soma os pesos dos marcos concluídos
        - Método `getCarryForwardMeasurement(WbsNode $wp, string $statusDate): ?Measurement` — busca último registro com `status_date <= ?` via subquery
        - Método `getCarryForwardActualCost(WbsNode $wp, string $statusDate): ?ActualCost` — busca último registro com `status_date <= ?`
        - Método `aggregateEv(Project $project, string $statusDate): float` — agrega EV bottom-up na árvore EAP, usando carry-forward para WPs sem registro na data
        - Método `getEvmMetrics(Project $project): array` — retorna PV, EV, AC sincronizados na mesma status_date do projeto
        - _Requirements: 4.4, 4.7, 4.8, 4.9, 4.10, 5.1, 5.4, 7.1, 7.2, 7.3, 7.4, 7.5, 7.6, 8.1, 8.2, 8.4, 8.5_

    - [x] 3.2 Escrever property test para validação de range da Data de Status
        - **Property 1: Status date range validation**
        - Gerar datas aleatórias relativas ao intervalo do projeto, verificar aceitação/rejeição
        - Usar `repeat(100)` com Faker
        - **Validates: Requirements 1.2, 1.3**

    - [x] 3.3 Escrever property test para precondição de baseline na Data de Status
        - **Property 2: Status date requires active frozen baseline**
        - Gerar projetos com/sem baseline ativa, verificar que status_date só é aceita com baseline frozen
        - Usar `repeat(100)` com Faker
        - **Validates: Requirements 1.4**

    - [x] 3.4 Escrever property test para restrições de método de medição
        - **Property 3: Measurement method constrains allowed percent complete values**
        - Gerar valores aleatórios de % complete para cada método, verificar regras (0/100 → só 0 e 100; 50/50 → só 0, 50, 100; physical_percent → [0, 100])
        - Usar `repeat(100)` com Faker
        - **Validates: Requirements 4.1, 4.2, 4.3, 4.5**

    - [x] 3.5 Escrever property test para cálculo de marcos ponderados
        - **Property 4: Weighted milestones percent complete calculation**
        - Gerar conjuntos de marcos com pesos somando 100, marcar subconjuntos aleatórios como concluídos, verificar que % = soma dos pesos concluídos
        - Usar `repeat(100)` com Faker
        - **Validates: Requirements 4.4**

    - [x] 3.6 Escrever property test para monotonicity de progresso
        - **Property 5: Progress monotonicity (non-regression)**
        - Gerar sequências de % complete, verificar que regressão é rejeitada
        - Usar `repeat(100)` com Faker
        - **Validates: Requirements 4.6**

    - [x] 3.7 Escrever property test para fórmula de cálculo do EV
        - **Property 6: EV calculation formula**
        - Gerar BAC e % complete aleatórios, verificar EV = BAC × (%/100). BAC zero/null → EV = 0. 100% → EV = BAC. 0% → EV = 0
        - Usar `repeat(100)` com Faker
        - **Validates: Requirements 4.7, 7.1, 7.4, 7.5, 7.6**

    - [x] 3.8 Escrever property test para comportamento de upsert
        - **Property 7: Measurement and actual cost upsert behavior**
        - Criar registros duplicados para mesmo WP + status_date, verificar que existe exatamente 1 registro após operação
        - Usar `repeat(100)` com Faker
        - **Validates: Requirements 4.10, 5.4**

    - [x] 3.9 Escrever property test para validação de AC não-negativo
        - **Property 8: Actual cost non-negative validation**
        - Gerar valores aleatórios (positivos e negativos), verificar que negativos são rejeitados
        - Usar `repeat(100)` com Faker
        - **Validates: Requirements 5.2**

- [x]   4. Checkpoint — Verificar EvCalculationService e property tests
    - Executar `php artisan test --compact` para garantir que todos os testes passam
    - Perguntar ao usuário se há dúvidas

- [x]   5. Implementar imutabilidade, carry-forward e policies
    - [x] 5.1 Implementar imutabilidade de registros históricos e carry-forward
        - Garantir que validações no `booted()` de `Measurement` e `ActualCost` bloqueiam edição quando `status_date` < `project.status_date`
        - Implementar carry-forward no `EvCalculationService`: buscar último registro anterior quando não há registro na data atual
        - Retornar 0% / zero AC quando não há nenhum registro anterior
        - _Requirements: 1.5, 6.1, 6.2, 6.3, 6.4, 6.5, 8.4, 8.5_

    - [x] 5.2 Escrever property test para imutabilidade de registros históricos
        - **Property 9: Historical record immutability**
        - Criar registros em datas anteriores, avançar status_date, tentar editar, verificar bloqueio. Registros na data atual devem ser editáveis
        - Usar `repeat(100)` com Faker
        - **Validates: Requirements 1.5, 6.1, 6.2, 6.3, 6.4**

    - [x] 5.3 Escrever property test para agregação bottom-up de EV
        - **Property 10: EV bottom-up aggregation**
        - Gerar árvores EAP com EVs aleatórios em work packages, verificar que EV de nós não-folha = soma dos EVs dos descendentes
        - Usar `repeat(100)` com Faker
        - **Validates: Requirements 7.2, 7.3**

    - [x] 5.4 Escrever property test para carry-forward
        - **Property 11: Carry-forward for missing records**
        - Gerar WPs com registros em datas variadas, consultar em data posterior sem registro, verificar que retorna valor da data anterior mais recente. Sem registro anterior → retorna zero
        - Usar `repeat(100)` com Faker
        - **Validates: Requirements 8.4, 8.5**

    - [x] 5.5 Escrever property test para sincronização de dados EVM
        - **Property 12: EVM data synchronization on single status date**
        - Gerar projetos com múltiplas datas de status e registros, verificar que queries de PV, EV e AC usam a mesma status_date do projeto
        - Usar `repeat(100)` com Faker
        - **Validates: Requirements 8.1**

    - [x] 5.6 Criar `MeasurementPolicy` e `ActualCostPolicy`
        - Criar `app/Policies/MeasurementPolicy.php`: PM → create/update em qualquer WP; Líder → create/update apenas nos WPs atribuídos; Director → viewAny/view; bloquear edição de registros históricos
        - Criar `app/Policies/ActualCostPolicy.php`: PM → create/update em qualquer WP; Líder → sem acesso a AC; Director → viewAny/view; bloquear edição de registros históricos
        - Registrar policies via auto-discovery ou no `AuthServiceProvider`
        - _Requirements: 10.1, 10.2, 10.3, 10.4, 10.5_

    - [x] 5.7 Escrever property test para auditoria de mutações
        - **Property 13: Mutations produce audit logs**
        - Realizar operações CRUD em Measurement, ActualCost, WeightedMilestone, alterar Project.status_date e WbsNode.measurement_method, verificar que audit logs são criados com user_id, timestamp, old/new values
        - Usar `repeat(100)` com Faker
        - **Validates: Requirements 9.1, 9.2, 9.3, 9.4**

    - [x] 5.8 Escrever property test para RBAC de medições e custos
        - **Property 14: RBAC enforcement for measurements and costs**
        - Gerar combinações de roles (PM, Líder, Director) × operações (create/update measurement, create/update AC, view) × WPs (atribuído/não atribuído), verificar permissões
        - Usar `repeat(100)` com Faker
        - **Validates: Requirements 10.1, 10.2, 10.3, 10.4, 10.5**

- [x]   6. Checkpoint — Verificar imutabilidade, carry-forward, policies e property tests
    - Executar `php artisan test --compact` para garantir que todos os testes passam
    - Perguntar ao usuário se há dúvidas

- [x]   7. Implementar WeightedMilestone e validações de marcos
    - [x] 7.1 Completar validações de WeightedMilestone e serialização
        - Garantir validação de soma de pesos = 100 no model (ou no service ao salvar conjunto de marcos)
        - Implementar lógica de bloqueio de remoção de marco já concluído (verificar se ID do marco aparece em `completed_milestones` de algum Measurement)
        - Implementar ordenação de marcos por `sort_order`
        - _Requirements: 2.4, 12.1, 12.2, 12.3, 12.4, 12.5, 12.6_

    - [x] 7.2 Escrever property test para validação de pesos de marcos
        - **Property 15: Milestone weight validation and sum invariant**
        - Gerar conjuntos de pesos aleatórios, verificar que só conjuntos com pesos positivos e soma = 100 são aceitos
        - Usar `repeat(100)` com Faker
        - **Validates: Requirements 2.4, 12.2, 12.3**

    - [x] 7.3 Escrever property test para round-trip de serialização de marcos
        - **Property 16: Completed milestone serialization round-trip**
        - Gerar arrays de IDs aleatórios, serializar para JSON e deserializar, verificar equivalência
        - Usar `repeat(100)` com Faker
        - **Validates: Requirements 13.1, 13.2, 13.3**

- [x]   8. Checkpoint — Verificar WeightedMilestone e property tests
    - Executar `php artisan test --compact` para garantir que todos os testes passam
    - Perguntar ao usuário se há dúvidas

- [x]   9. Estender Filament Resources existentes
    - [x] 9.1 Estender `ProjectResource` com campo `status_date`
        - Adicionar campo `status_date` (DatePicker) no formulário de edição do projeto
        - Adicionar validação no campo: `minDate` = `planned_start_date`, `maxDate` = `planned_end_date`
        - Desabilitar campo se projeto não tem baseline ativa (exibir helperText explicativo)
        - Capturar `InvalidArgumentException` no save com try/catch e exibir `Notification::make()->danger()`
        - Adicionar coluna `status_date` na tabela de listagem de projetos
        - Exibir Data de Status de forma destacada na interface
        - _Requirements: 1.1, 1.2, 1.3, 1.4, 1.6_

    - [x] 9.2 Estender `WbsNodeResource` com campos `measurement_method` e `assigned_to`
        - Adicionar campo `measurement_method` (Select com enum `MeasurementMethod`) no formulário de edição de work packages
        - Definir default `physical_percent` para novos pacotes
        - Adicionar confirmação ao alterar método quando já existem medições (modal de confirmação)
        - Adicionar campo `assigned_to` (Select com users) no formulário de edição de work packages
        - Mostrar campos `measurement_method` e `assigned_to` apenas para nós do tipo `work_package`
        - Adicionar relation manager para `WeightedMilestone` (visível apenas quando método = `weighted_milestones`)
        - Validar soma dos pesos dos marcos = 100 no relation manager
        - Capturar `InvalidArgumentException` com try/catch e exibir `Notification::make()->danger()`
        - _Requirements: 2.1, 2.2, 2.5, 2.6, 3.1, 3.2, 3.3, 3.4, 3.5, 12.1, 12.6_

    - [x] 9.3 Escrever testes das extensões de ProjectResource e WbsNodeResource
        - Testar renderização do campo status_date no formulário de edição
        - Testar que status_date é bloqueado sem baseline ativa
        - Testar renderização dos campos measurement_method e assigned_to
        - Testar default physical_percent para novos work packages
        - Testar confirmação ao alterar método com medições existentes
        - Testar relation manager de WeightedMilestone
        - _Requirements: 1.1, 1.4, 1.6, 2.1, 2.2, 3.1_

- [x]   10. Checkpoint — Verificar extensões de Filament Resources
    - Executar `php artisan test --compact` para garantir que todos os testes passam
    - Perguntar ao usuário se há dúvidas

- [x]   11. Criar MeasurementPage (página customizada de apontamento)
    - [x] 11.1 Criar `MeasurementPage` como Custom Page do Filament
        - Criar `app/Filament/Resources/Projects/Pages/MeasurementPage.php` como custom page vinculada ao `ProjectResource`
        - Exibir Data de Status atual do projeto de forma destacada no topo da página
        - Listar work packages do projeto com: nome, código, BAC (da Baseline ativa), método de medição, % Complete atual, EV calculado, AC registrado
        - Filtrar automaticamente por líder de pacote logado (exceto PM que vê todos)
        - Adaptar formulário de entrada conforme método de medição:
            - `physical_percent`: campo numérico 0–100 com 2 casas decimais
            - `zero_hundred`: toggle ou select com 0% e 100%
            - `fifty_fifty`: select com 0%, 50%, 100%
            - `weighted_milestones`: lista de marcos com checkboxes, cálculo automático do %
        - Campo de AC (custo real) com máscara BRL (R$, vírgula decimal, ponto milhares) — visível apenas para PM
        - Exibir histórico de medições anteriores por work package (timeline ou tabela)
        - Exibir registros históricos em modo somente leitura
        - Usar `EvCalculationService` para calcular EV e registrar medições/custos
        - Capturar `InvalidArgumentException` com try/catch e exibir `Notification::make()->danger()`
        - Bloquear registro se projeto não tem Data de Status definida (exibir notificação)
        - _Requirements: 4.1, 4.2, 4.3, 4.4, 4.8, 4.9, 5.1, 5.6, 5.7, 6.5, 7.1, 8.2, 11.1, 11.2, 11.3, 11.4, 11.5, 11.6_

    - [x] 11.2 Escrever testes da MeasurementPage
        - Testar renderização da página com work packages
        - Testar filtro automático por líder de pacote
        - Testar formulário adaptativo por método de medição
        - Testar registro de % Complete e cálculo de EV
        - Testar registro de AC com máscara BRL
        - Testar bloqueio sem Data de Status definida
        - Testar exibição de histórico em modo somente leitura
        - Testar que Director vê apenas leitura
        - _Requirements: 4.9, 5.6, 6.5, 10.4, 11.1, 11.2, 11.3, 11.4_

- [x]   12. Checkpoint — Verificar MeasurementPage
    - Executar `php artisan test --compact` para garantir que todos os testes passam
    - Perguntar ao usuário se há dúvidas

- [x]   13. Integração final e wiring
    - [x] 13.1 Integrar todos os componentes e verificar fluxo completo
        - Garantir que `AuditObserver` está registrado via `#[ObservedBy]` nos novos models (Measurement, ActualCost, WeightedMilestone)
        - Garantir que alterações em `Project.status_date` e `WbsNode.measurement_method` geram audit logs
        - Garantir que `MeasurementPolicy` e `ActualCostPolicy` estão registradas e funcionando no Filament
        - Garantir que `EvCalculationService` é chamado corretamente na MeasurementPage
        - Garantir que carry-forward funciona para WPs sem registro na data atual
        - Verificar navegação: ProjectResource → MeasurementPage → histórico de medições
        - Verificar que registros históricos são somente leitura em toda a interface
        - Verificar que AC é input independente do % Complete
        - _Requirements: 1.5, 4.9, 5.5, 6.1, 6.4, 7.2, 8.1, 8.4, 9.1, 9.5, 10.1_

    - [x] 13.2 Escrever testes de integração end-to-end
        - Testar fluxo completo: criar projeto → estruturar EAP → congelar baseline → definir status_date → configurar métodos de medição → atribuir líderes → registrar % Complete → registrar AC → verificar EV calculado → verificar agregação bottom-up
        - Testar fluxo de carry-forward: registrar medição em data X → avançar status_date para Y → verificar que valores de X são carregados
        - Testar fluxo de imutabilidade: registrar em data X → avançar para Y → tentar editar registro de X → verificar bloqueio
        - Testar acesso PM vs Líder vs Director em todo o fluxo
        - Testar que audit logs são gerados em todo o fluxo
        - _Requirements: 1.1, 4.1, 5.1, 6.1, 7.1, 8.1, 9.1, 10.1_

- [x]   14. Checkpoint final — Garantir que todos os testes passam
    - Executar `php artisan test --compact` para garantir que todos os testes passam
    - Executar `vendor/bin/pint --dirty --format agent` para garantir formatação
    - Perguntar ao usuário se há dúvidas

## Notes

- Tarefas marcadas com `*` são opcionais e podem ser puladas para um MVP mais rápido
- Cada tarefa referencia requisitos específicos para rastreabilidade
- Checkpoints garantem validação incremental
- Property tests validam propriedades universais de correção (16 propriedades definidas no design)
- Unit/feature tests validam exemplos específicos e edge cases
- Todas as 16 correctness properties do design estão mapeadas como sub-tarefas de property test
- O projeto usa Pest v4 com `repeat(100)` e datasets randomizados via Faker para simular PBT
- Este módulo estende a arquitetura do primeiro spec (`project-structuring-baseline`) — não recria models base
- Convenções: UI em pt-BR, código em inglês, campos monetários com máscara BRL, enums com HasLabel/HasColor/HasIcon
- Validações de domínio no model lançam `InvalidArgumentException`, capturadas no Filament com `Notification::make()->danger()`
