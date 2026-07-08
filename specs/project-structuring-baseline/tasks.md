# Implementation Plan: Módulo de Estruturação e Baseline

## Overview

Implementação incremental do módulo de Estruturação e Baseline da plataforma EVM. O plano segue a ordem: migrations e models base → services de domínio → policies e observer → Filament resources → integração e wiring final. Cada tarefa constrói sobre as anteriores, garantindo que não haja código órfão.

## Tasks

- [x]   1. Criar migrations e models base
    - [x] 1.1 Criar migration para adicionar coluna `role` na tabela `users`
        - Adicionar coluna `role` enum (`project_manager`, `portfolio_director`) com default `project_manager`
        - Atualizar o model `User` com cast para enum, fillable e relationship `projects()`
        - Atualizar `UserFactory` com state methods `projectManager()` e `portfolioDirector()`
        - _Requirements: 9.1, 9.5_

    - [x] 1.2 Criar model `Project` com migration e factory
        - Executar `php artisan make:model Project -mf`
        - Migration: tabela `projects` com `name`, `description`, `planned_start_date`, `planned_end_date`, `created_by_id` (FK users), `active_baseline_id` (FK baselines, nullable)
        - Model: fillable, casts (dates), relationships (`createdBy`, `wbsNodes`, `baselines`, `activeBaseline`)
        - Factory: gerar dados válidos com Faker, states para projeto com/sem datas
        - _Requirements: 1.1, 1.2, 1.3_

    - [x] 1.3 Criar model `WbsNode` com migration e factory
        - Executar `php artisan make:model WbsNode -mf`
        - Migration: tabela `wbs_nodes` com `project_id` (FK cascade), `parent_id` (FK self nullable cascade), `type` enum (phase/deliverable/work_package), `name`, `code`, `sort_order`, `bac` (decimal 15,2 nullable), `planned_start_date` (nullable), `planned_end_date` (nullable), `pv_distribution_method` (enum nullable), `pv_distribution` (json nullable)
        - Indexes: `(project_id, parent_id)`, `(project_id, type)`
        - Model: fillable, casts (type enum, dates, json, decimal), relationships (`project`, `parent`, `children`), scope `workPackages()`
        - Factory: gerar nós válidos com states `phase()`, `deliverable()`, `workPackage()`
        - _Requirements: 2.1, 2.2, 2.3, 3.1, 3.2, 4.1, 5.7_

    - [x] 1.4 Criar model `Baseline` com migration e factory
        - Executar `php artisan make:model Baseline -mf`
        - Migration: tabela `baselines` com `project_id` (FK cascade), `version_number`, `status` enum (draft/frozen), `snapshot` (json), `change_justification` (text nullable), `frozen_by_id` (FK users nullable), `frozen_at` (timestamp nullable)
        - Index: `(project_id, status)`
        - Model: fillable, casts (status enum, json, datetime), relationships (`project`, `frozenBy`)
        - Factory: gerar baselines com states `draft()`, `frozen()`
        - _Requirements: 6.3, 6.5, 6.6, 7.1_

    - [x] 1.5 Criar model `AuditLog` com migration e factory
        - Executar `php artisan make:model AuditLog -mf`
        - Migration: tabela `audit_logs` com `user_id` (FK users), `auditable_type`, `auditable_id`, `operation`, `old_values` (json nullable), `new_values` (json nullable), `created_at` (sem `updated_at`)
        - Indexes: `(auditable_type, auditable_id)`, `(user_id, created_at)`
        - Model: sem `updated_at`, sem soft deletes, fillable, casts (json), relationship `user()`, morph relationship `auditable()`
        - Factory: gerar logs de auditoria válidos
        - _Requirements: 8.1, 8.2, 8.3_

- [x]   2. Checkpoint — Verificar migrations e models
    - Executar `php artisan migrate` para validar todas as migrations
    - Executar `php artisan test --compact` para garantir que testes existentes continuam passando
    - Perguntar ao usuário se há dúvidas

- [x]   3. Implementar AggregationService
    - [x] 3.1 Criar `AggregationService` com lógica de agregação bottom-up
        - Criar `app/Services/AggregationService.php`
        - Método `aggregateBac(WbsNode $node): float` — calcula BAC somando filhos diretos recursivamente
        - Método `aggregateProjectBac(Project $project): float` — calcula BAC total do projeto
        - Método `aggregateStartDate(WbsNode $node): ?Carbon` — menor data de início dos descendentes
        - Método `aggregateEndDate(WbsNode $node): ?Carbon` — maior data de fim dos descendentes
        - Método `recalculate(Project $project): void` — recalcula todos os agregados do projeto
        - _Requirements: 3.1, 3.3, 3.4, 3.5, 3.6, 4.3, 4.4, 4.5, 4.6, 4.7, 10.1, 10.3_

    - [x] 3.2 Escrever property test para agregação de BAC
        - **Property 1: BAC aggregation invariant**
        - Gerar árvores EAP aleatórias com BACs em work packages, verificar soma bottom-up
        - Usar `repeat(100)` com Faker para gerar árvores variadas
        - **Validates: Requirements 3.1, 3.3, 3.4, 3.5, 3.6, 10.1, 10.3, 10.5**

    - [x] 3.3 Escrever property test para agregação de datas
        - **Property 2: Date aggregation invariant**
        - Gerar árvores com datas aleatórias em work packages, verificar min/max bottom-up
        - Usar `repeat(100)` com Faker
        - **Validates: Requirements 4.3, 4.4, 4.5, 4.6, 4.7**

    - [x] 3.4 Escrever property test para confluência de agregação
        - **Property 16: Aggregation confluence**
        - Processar work packages em ordens diferentes, comparar resultado
        - Usar `repeat(100)` com shuffle de arrays
        - **Validates: Requirements 10.4**

- [x]   4. Implementar PvDistributionService
    - [x] 4.1 Criar `PvDistributionService` com distribuição linear e personalizada
        - Criar `app/Services/PvDistributionService.php`
        - Método `distributeLinear(WbsNode $wp): array` — distribui BAC uniformemente entre datas
        - Método `validateCustomDistribution(WbsNode $wp, array $distribution): bool` — valida soma = BAC
        - Método `applyDistribution(WbsNode $wp, array $distribution): void` — salva distribuição no model
        - Método `getCumulativePv(WbsNode $node, string $period): float` — calcula PV cumulativo
        - Método `aggregatePv(Project $project): array` — agrega PV bottom-up por período
        - _Requirements: 5.1, 5.2, 5.3, 5.4, 5.5, 5.6_

    - [x] 4.2 Escrever property test para soma PV = BAC
        - **Property 7: PV distribution sum equals BAC**
        - Gerar BACs e ranges de datas aleatórios, verificar soma da distribuição linear
        - Usar `repeat(100)` com Faker
        - **Validates: Requirements 5.1, 5.3**

    - [x] 4.3 Escrever property test para round-trip de serialização PV
        - **Property 9: PV distribution serialization round-trip**
        - Gerar distribuições aleatórias, serializar/deserializar, comparar
        - Usar `repeat(100)` com Faker
        - **Validates: Requirements 5.7, 5.8, 5.9**

    - [x] 4.4 Escrever property test para agregação cumulativa de PV
        - **Property 8: PV cumulative aggregation**
        - Gerar árvores com PV em work packages, verificar agregação por período
        - Usar `repeat(100)` com Faker
        - **Validates: Requirements 5.4, 5.5, 10.2**

- [x]   5. Implementar BaselineService
    - [x] 5.1 Criar `BaselineService` com validação, freeze e controle de mudanças
        - Criar `app/Services/BaselineService.php`
        - Método `validateCompleteness(Project $project): array` — retorna lista de WPs incompletos
        - Método `freeze(Project $project, User $user, ?string $justification = null): Baseline` — valida, cria snapshot JSON, congela baseline, atualiza `active_baseline_id`
        - Método `createNewVersion(Project $project): Baseline` — cria rascunho copiando dados da baseline ativa
        - Método `buildSnapshot(Project $project): array` — constrói snapshot JSON completo da EAP
        - Usar `DB::transaction()` para operações de freeze
        - _Requirements: 6.1, 6.2, 6.3, 6.4, 6.5, 6.6, 7.1, 7.2, 7.3, 7.4, 7.5_

    - [x] 5.2 Escrever property test para validação de completude no freeze
        - **Property 10: Baseline freeze completeness validation**
        - Gerar projetos com WPs variados (completos e incompletos), verificar freeze
        - Usar `repeat(100)` com Faker
        - **Validates: Requirements 6.1, 6.2**

    - [x] 5.3 Escrever property test para bloqueio de modificações com baseline congelada
        - **Property 11: Frozen baseline blocks modifications**
        - Gerar modificações em projetos com baseline ativa, verificar rejeição
        - Usar `repeat(100)` com Faker
        - **Validates: Requirements 6.4**

    - [x] 5.4 Escrever property test para unicidade de baseline ativa
        - **Property 12: Single active baseline invariant**
        - Gerar sequências de freeze, verificar que apenas uma baseline é ativa por vez
        - Usar `repeat(100)` com Faker
        - **Validates: Requirements 6.6, 7.5**

- [x]   6. Checkpoint — Verificar services e property tests
    - Executar `php artisan test --compact` para garantir que todos os testes passam
    - Perguntar ao usuário se há dúvidas

- [x]   7. Implementar validações, policies e observer
    - [x] 7.1 Criar validações de domínio nos models
        - Adicionar validação de hierarquia no `WbsNode` (phase→deliverable→work_package)
        - Adicionar geração automática de código hierárquico no `WbsNode`
        - Adicionar validação de datas (end >= start, WP dentro do intervalo do projeto)
        - Adicionar validação de BAC (positivo, até 2 casas decimais)
        - _Requirements: 1.3, 2.2, 2.3, 2.4, 2.7, 3.2, 4.1, 4.2_

    - [x] 7.2 Escrever property test para validação de datas
        - **Property 3: Date validation rules**
        - Gerar pares de datas aleatórios, verificar regras de validação
        - Usar `repeat(100)` com Faker
        - **Validates: Requirements 1.3, 4.1, 4.2**

    - [x] 7.3 Escrever property test para hierarquia da EAP
        - **Property 4: WBS hierarchy enforcement**
        - Gerar combinações de tipos pai/filho, verificar validação
        - Usar `repeat(100)` com Faker
        - **Validates: Requirements 2.2, 2.7**

    - [x] 7.4 Escrever property test para consistência de códigos hierárquicos
        - **Property 5: Hierarchical code consistency**
        - Gerar árvores, inserir/reordenar, verificar códigos únicos e corretos
        - Usar `repeat(100)` com Faker
        - **Validates: Requirements 2.3, 2.4**

    - [x] 7.5 Escrever property test para deleção em cascata
        - **Property 6: Cascade deletion of descendants**
        - Gerar árvores, deletar nós, verificar contagem de remanescentes
        - Usar `repeat(100)` com Faker
        - **Validates: Requirements 2.5**

    - [x] 7.6 Criar policies de autorização
        - Criar `ProjectPolicy` — PM: full CRUD; Director: viewAny, view
        - Criar `WbsNodePolicy` — PM: full CRUD (bloqueado se baseline ativa); Director: viewAny, view
        - Criar `BaselinePolicy` — PM: create, freeze, change; Director: viewAny, view
        - Criar `AuditLogPolicy` — PM e Director: viewAny, view; ninguém: create, update, delete
        - Registrar policies no `AuthServiceProvider` ou via auto-discovery
        - _Requirements: 9.1, 9.2, 9.3, 9.4_

    - [x] 7.7 Escrever property test para RBAC
        - **Property 15: Role-based access control enforcement**
        - Gerar operações com diferentes roles, verificar permissões
        - Usar `repeat(100)` com Faker
        - **Validates: Requirements 9.2, 9.3, 9.4**

    - [x] 7.8 Criar `AuditObserver` para trilha de auditoria
        - Criar `app/Observers/AuditObserver.php`
        - Registrar observer para `Project`, `WbsNode` e `Baseline`
        - Capturar eventos `created`, `updated`, `deleted`
        - Registrar `user_id`, `operation`, `old_values`, `new_values` na tabela `audit_logs`
        - _Requirements: 8.1, 8.2_

    - [x] 7.9 Escrever property test para mutações gerarem audit logs
        - **Property 13: Mutations produce audit logs**
        - Realizar operações CRUD em Project, WbsNode, Baseline, verificar logs
        - Usar `repeat(100)` com Faker
        - **Validates: Requirements 8.1**

    - [x] 7.10 Escrever property test para imutabilidade de audit logs
        - **Property 14: Audit logs are immutable**
        - Tentar update/delete em audit logs, verificar falha
        - Usar `repeat(100)` com Faker
        - **Validates: Requirements 8.3**

- [x]   8. Checkpoint — Verificar validações, policies e observer
    - Executar `php artisan test --compact` para garantir que todos os testes passam
    - Perguntar ao usuário se há dúvidas

- [x]   9. Criar Filament Resources — ProjectResource
    - [x] 9.1 Criar `ProjectResource` com CRUD completo
        - Executar `php artisan make:filament-resource Project --generate`
        - Configurar form: campos `name`, `description`, `planned_start_date`, `planned_end_date`
        - Configurar table: colunas `name`, `planned_start_date`, `planned_end_date`, BAC agregado, status baseline
        - Integrar `ProjectPolicy` para autorização
        - Bloquear edição quando projeto tem baseline ativa (exibir notificação)
        - _Requirements: 1.1, 1.2, 1.3, 1.4, 1.5_

    - [x] 9.2 Escrever testes do ProjectResource
        - Testar renderização de list, create, edit pages
        - Testar criação de projeto com dados válidos
        - Testar bloqueio de edição com baseline ativa
        - Testar acesso PM vs Director
        - _Requirements: 1.1, 1.4, 1.5, 9.2, 9.3_

- [x]   10. Criar Filament Resources — WbsNodeResource
    - [x] 10.1 Criar `WbsNodeResource` como nested resource do Project
        - Criar resource para gerenciar nós EAP dentro de um projeto
        - Configurar form: campos `type`, `name`, `parent_id` (filtrado por hierarquia), `bac`, `planned_start_date`, `planned_end_date`
        - Configurar table: exibir hierarquia em árvore com código, tipo, nome, BAC, datas
        - Exibir BAC agregado e datas agregadas para nós não-folha via `AggregationService`
        - Implementar reordenação com atualização de códigos hierárquicos
        - Implementar confirmação de deleção em cascata
        - Integrar `WbsNodePolicy` para autorização (bloquear se baseline ativa)
        - _Requirements: 2.1, 2.2, 2.3, 2.4, 2.5, 2.6, 2.7, 3.1, 3.6, 3.7, 4.1, 4.2, 4.7_

    - [x] 10.2 Escrever testes do WbsNodeResource
        - Testar adição de nós respeitando hierarquia
        - Testar exibição de árvore hierárquica
        - Testar reordenação e atualização de códigos
        - Testar bloqueio com baseline ativa
        - _Requirements: 2.1, 2.2, 2.3, 2.4, 2.6_

- [x]   11. Criar Filament Resources — BaselineRelationManager e PV Distribution
    - [x] 11.1 Criar `BaselineRelationManager` no ProjectResource
        - Criar relation manager para listar baselines do projeto
        - Configurar table: colunas `version_number`, `status`, `frozen_at`, `change_justification`
        - Criar action `Freeze Baseline` que chama `BaselineService::freeze()`
        - Criar action `Create New Version` que chama `BaselineService::createNewVersion()`
        - Exibir notificação com WPs incompletos quando freeze falha
        - Integrar `BaselinePolicy` para autorização
        - _Requirements: 6.1, 6.2, 6.3, 6.4, 6.5, 6.6, 7.1, 7.3, 7.4, 7.5_

    - [x] 11.2 Criar página/action de distribuição de PV
        - Criar interface para selecionar método de distribuição (linear/custom) por work package
        - Para distribuição linear: botão que chama `PvDistributionService::distributeLinear()`
        - Para distribuição personalizada: formulário com campos por período para entrada manual
        - Validar soma PV = BAC e exibir erro se diferente
        - Solicitar redistribuição quando BAC ou datas mudam
        - _Requirements: 5.1, 5.2, 5.3, 5.6_

    - [x] 11.3 Escrever testes do BaselineRelationManager e PV Distribution
        - Testar ação de freeze com projeto completo e incompleto
        - Testar criação de nova versão
        - Testar distribuição linear e personalizada
        - Testar validação de soma PV = BAC
        - _Requirements: 6.1, 6.2, 7.1, 5.1, 5.3_

- [x]   12. Criar Filament Resources — AuditLogResource
    - [x] 12.1 Criar `AuditLogResource` como resource read-only
        - Executar `php artisan make:filament-resource AuditLog --generate`
        - Configurar como read-only (sem create, edit, delete)
        - Configurar table: colunas `user.name`, `auditable_type`, `operation`, `created_at`
        - Implementar filtros: por projeto, tipo de operação, usuário, intervalo de datas
        - Configurar view page para exibir `old_values` e `new_values` formatados
        - Integrar `AuditLogPolicy` para autorização
        - _Requirements: 8.1, 8.2, 8.3, 8.4_

    - [x] 12.2 Escrever testes do AuditLogResource
        - Testar renderização da listagem
        - Testar filtros por projeto, operação, usuário, datas
        - Testar que create/edit/delete não estão disponíveis
        - _Requirements: 8.3, 8.4_

- [x]   13. Checkpoint — Verificar Filament resources
    - Executar `php artisan test --compact` para garantir que todos os testes passam
    - Perguntar ao usuário se há dúvidas

- [x]   14. Integração final e wiring
    - [x] 14.1 Integrar todos os componentes e verificar fluxo completo
        - Garantir que `AuditObserver` está registrado para todos os models
        - Garantir que todas as policies estão registradas e funcionando no Filament
        - Garantir que `AggregationService` é chamado após mudanças em BAC/datas
        - Garantir que `PvDistributionService` é chamado quando necessário
        - Verificar que `BaselineService` bloqueia edições corretamente
        - Verificar navegação entre ProjectResource → WbsNodes → Baselines → AuditLog
        - _Requirements: 1.1, 2.6, 3.6, 5.6, 6.4, 8.1, 9.2, 9.3_

    - [x] 14.2 Escrever testes de integração end-to-end
        - Testar fluxo completo: criar projeto → adicionar EAP → definir BAC → distribuir PV → congelar baseline
        - Testar fluxo de mudança: criar nova versão → editar → recongelar
        - Testar que audit logs são gerados em todo o fluxo
        - Testar acesso PM vs Director em todo o fluxo
        - _Requirements: 1.1, 2.1, 3.1, 5.1, 6.1, 7.1, 8.1, 9.2, 9.3_

- [x]   15. Checkpoint final — Garantir que todos os testes passam
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
