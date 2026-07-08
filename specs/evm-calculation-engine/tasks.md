# Implementation Plan: Motor de Cálculo EVM (Monitoramento)

## Overview

Este plano implementa o Motor de Cálculo EVM como uma camada de cálculo pura sobre os services e models existentes. Não há migrações — apenas DTO, Enum, Service e testes. A ordem é incremental: tipos de dados → lógica de cálculo pura → agregação → portfólio → auditoria → integração.

## Tasks

- [x]   1. Criar o HealthStatus Enum
    - [x] 1.1 Criar `app/Enums/HealthStatus.php` com valores `Green`, `Yellow`, `Red`, `Gray`
        - Implementar `HasLabel` com labels pt-BR: "Saudável", "Atenção", "Crítico", "Sem Dados"
        - Implementar `HasColor` com cores Filament: "success", "warning", "danger", "gray"
        - Implementar `HasIcon` com Heroicons apropriados
        - Definir constantes `GREEN_THRESHOLD = 1.0` e `YELLOW_THRESHOLD = 0.9`
        - Implementar `fromIndex(?float $index): self` — Green se >= 1.0, Yellow se >= 0.9, Red se < 0.9, Gray se null
        - Implementar `worst(self $a, self $b): self` — retorna o pior status (Red > Gray > Yellow > Green, com Gray tratado como pior que Yellow mas igual a Red)
        - _Requirements: 7.1, 7.2, 7.3, 7.4, 7.5_

    - [x] 1.2 Escrever property test para classificação de saúde (Property 8)
        - **Property 8: Health classification follows threshold rules**
        - Gerar 100+ valores float (incluindo null, 0, 0.89, 0.9, 0.99, 1.0, 1.5) com `repeat(100)`
        - Verificar: Green quando >= 1.0, Yellow quando >= 0.9 e < 1.0, Red quando < 0.9, Gray quando null
        - Arquivo: `tests/Unit/HealthStatusTest.php`
        - **Validates: Requirements 7.1, 7.2, 7.3, 7.4**

    - [x] 1.3 Escrever property test para worst() do HealthStatus (Property 9)
        - **Property 9: Overall health equals worst of schedule and cost health**
        - Gerar 100+ pares de HealthStatus com `repeat(100)`
        - Verificar que worst() retorna o pior entre os dois, com ordenação Green < Yellow < Red, Gray tratado como pior que Yellow mas igual a Red
        - Arquivo: `tests/Unit/HealthStatusTest.php`
        - **Validates: Requirements 7.5**

- [x]   2. Criar o EvmSnapshot DTO
    - [x] 2.1 Criar `app/DTOs/EvmSnapshot.php` como `final readonly class`
        - Propriedades: pv, ev, ac, bac (float), sv, cv (float), spi, cpi (nullable float), eac, etc, vac (float), tcpi (nullable float), scheduleHealth, costHealth, overallHealth (HealthStatus), statusDate (nullable string)
        - Implementar `toArray(): array` — serializa para JSON com chaves snake_case, `etc` serializado como `etc_value`, HealthStatus como string value, nulls preservados
        - Implementar `static fromArray(array $data): self` — reconstrói EvmSnapshot a partir de array, converte strings de HealthStatus de volta para enum
        - _Requirements: 10.1, 10.2, 10.3, 10.4_

    - [x] 2.2 Escrever property test para serialização round-trip (Property 10)
        - **Property 10: EvmSnapshot serialization round-trip**
        - Gerar 100+ EvmSnapshots com valores aleatórios (incluindo nulls para SPI, CPI, TCPI) com `repeat(100)`
        - Serializar via `toArray()` e deserializar via `fromArray()`, verificar equivalência com tolerância de ponto flutuante
        - Arquivo: `tests/Unit/EvmSnapshotTest.php`
        - **Validates: Requirements 10.1, 10.2, 10.3, 10.4**

- [x]   3. Checkpoint — Verificar HealthStatus e EvmSnapshot
    - Ensure all tests pass, ask the user if questions arise.

- [x]   4. Implementar o EvmCalculationEngine — Cálculo de métricas derivadas
    - [x] 4.1 Criar `app/Services/EvmCalculationEngine.php` com injeção de dependências
        - Injetar `EvCalculationService`, `AggregationService`, `PvDistributionService` via constructor
        - Implementar `calculateDerivedMetrics(float $pv, float $ev, float $ac, float $bac): array` como método puro
        - Fórmulas: SV = EV - PV, CV = EV - AC, SPI = EV/PV (null se PV=0), CPI = EV/AC (null se AC=0)
        - EAC: se EV=BAC → AC; se CPI=null → BAC - EV; senão → AC + (BAC - EV) / CPI. Caso especial: CPI=0 (EV=0, AC>0) → EAC = BAC
        - ETC = EAC - AC, VAC = BAC - EAC
        - TCPI = (BAC - EV) / (BAC - AC), null se BAC=AC ou EV=BAC
        - Arredondar: SV, CV, EAC, ETC, VAC com 2 casas decimais; SPI, CPI, TCPI com 4 casas decimais
        - Implementar `classifyHealth(?float $index): HealthStatus` delegando para `HealthStatus::fromIndex()`
        - _Requirements: 1.1, 1.2, 1.3, 1.6, 1.7, 2.1, 2.2, 2.3, 2.4, 2.5, 2.6, 2.7, 3.1, 3.2, 3.3, 3.4, 3.5, 3.6, 4.1, 4.2, 4.3, 4.4, 4.5_

    - [x] 4.2 Escrever property test para fórmulas de métricas derivadas (Property 1)
        - **Property 1: Derived metrics formula correctness**
        - Gerar 100+ tuplas (pv, ev, ac, bac) com valores float >= 0 (incluindo zeros, ev=bac, bac=ac) com `repeat(100)`
        - Verificar cada fórmula: SV, CV, SPI, CPI, EAC, ETC, VAC, TCPI conforme regras de divisão por zero e caso especial EV=BAC
        - Arquivo: `tests/Unit/EvmCalculationEngineTest.php`
        - **Validates: Requirements 1.1, 1.2, 1.6, 1.7, 2.1, 2.2, 2.3, 2.4, 2.5, 2.6, 3.1, 3.2, 3.3, 3.4, 3.5, 4.1, 4.2, 4.3, 4.4**

    - [x] 4.3 Escrever property test para precisão decimal (Property 2)
        - **Property 2: Decimal precision of computed metrics**
        - Gerar 100+ tuplas (pv, ev, ac, bac) com `repeat(100)`
        - Verificar: SV, CV, EAC, ETC, VAC têm no máximo 2 casas decimais; SPI, CPI, TCPI (quando não null) têm no máximo 4 casas decimais
        - Arquivo: `tests/Unit/EvmCalculationEngineTest.php`
        - **Validates: Requirements 1.3, 2.7, 3.6, 4.5**

    - [x] 4.4 Escrever property test para consistência matemática (Property 11)
        - **Property 11: Mathematical consistency between related metrics**
        - Gerar 100+ tuplas com PV > 0 e AC > 0 com `repeat(100)`
        - Verificar: SV == SPI × PV - PV (tolerância float) e CV == CPI × AC - AC (tolerância float)
        - Arquivo: `tests/Unit/EvmCalculationEngineTest.php`
        - **Validates: Requirements 13.1, 13.2, 13.7**

    - [x] 4.5 Escrever property test para confluência (Property 6)
        - **Property 6: Aggregation confluence**
        - Gerar conjuntos de work packages com PV, EV, AC, BAC aleatórios, processar em ordens diferentes com `repeat(100)`
        - Verificar que o resultado agregado é idêntico independente da ordem de processamento
        - Arquivo: `tests/Unit/EvmCalculationEngineTest.php`
        - **Validates: Requirements 5.5**

- [x]   5. Implementar getProjectSnapshot e getNodeSnapshot
    - [x] 5.1 Implementar `getProjectSnapshot(Project $project): EvmSnapshot`
        - Verificar se projeto tem status_date e baseline ativa; se não, retornar EvmSnapshot zerado com classificação Gray
        - Chamar `EvCalculationService::getEvmMetrics()` para obter PV, EV, AC
        - Chamar `AggregationService::aggregateProjectBac()` para obter BAC
        - Chamar `calculateDerivedMetrics()` para obter métricas derivadas
        - Classificar saúde via `classifyHealth()` para schedule (SPI), cost (CPI) e overall (worst)
        - Montar e retornar `EvmSnapshot`
        - _Requirements: 8.1, 8.2, 8.3, 8.4, 9.3, 9.4_

    - [x] 5.2 Implementar `getNodeSnapshot(WbsNode $node): EvmSnapshot`
        - Para work packages: obter PV via `PvDistributionService::getCumulativePv()`, EV via carry-forward measurement, AC via carry-forward actual cost, BAC da baseline
        - Para nós não-folha: agregar PV, EV, AC recursivamente dos descendentes work packages; BAC = soma dos BACs dos WPs descendentes; EAC = soma dos EACs dos WPs descendentes
        - Usar eager loading para evitar N+1
        - Classificar saúde e montar EvmSnapshot
        - _Requirements: 1.4, 1.5, 2.8, 5.1, 5.2, 5.3, 5.4, 9.1, 9.2_

    - [x] 5.3 Escrever property test para agregação bottom-up (Property 3)
        - **Property 3: Bottom-up aggregation invariant**
        - Gerar árvores EAP aleatórias (2-4 níveis, 2-5 filhos) com PV, EV, AC nos work packages com `repeat(100)`
        - Verificar: PV, EV, AC de nós não-folha = soma dos respectivos valores dos WPs descendentes
        - Arquivo: `tests/Feature/EvmAggregationTest.php`
        - **Validates: Requirements 1.4, 1.5, 5.1, 5.2, 5.6, 5.7, 5.8**

    - [x] 5.4 Escrever property test para índices agregados (Property 4)
        - **Property 4: Aggregated indices use summed values, not averaged children indices**
        - Gerar árvores com WPs de SPIs/CPIs diferentes com `repeat(100)`
        - Verificar: SPI do pai = EV_agregado / PV_agregado, diferente da média dos SPIs dos filhos
        - Arquivo: `tests/Feature/EvmAggregationTest.php`
        - **Validates: Requirements 2.8, 5.3**

    - [x] 5.5 Escrever property test para agregação de EAC (Property 5)
        - **Property 5: EAC aggregation equals sum of leaf EACs**
        - Gerar árvores EAP, verificar EAC do nó = soma dos EACs dos WPs descendentes com `repeat(100)`
        - Verificar também: ETC do nó = soma dos ETCs, VAC = BAC_nó - EAC_nó
        - Arquivo: `tests/Feature/EvmAggregationTest.php`
        - **Validates: Requirements 3.7, 3.8, 3.9, 5.4**

- [x]   6. Checkpoint — Verificar cálculos e agregação
    - Ensure all tests pass, ask the user if questions arise.

- [x]   7. Implementar getPortfolioSnapshot
    - [x] 7.1 Implementar `getPortfolioSnapshot(): EvmSnapshot`
        - Buscar todos os projetos com `status_date` definida (WHERE status_date IS NOT NULL)
        - Para cada projeto, chamar `getProjectSnapshot()` independentemente
        - Somar PV, EV, AC, EAC de todos os projetos
        - BAC = soma dos BACs de projetos com baseline ativa
        - Calcular SPI, CPI do portfólio a partir dos valores somados (mesmas regras de divisão por zero)
        - VAC = BAC_portfólio - EAC_portfólio
        - TCPI não calculado no nível de portfólio (null)
        - Classificar saúde e montar EvmSnapshot
        - _Requirements: 6.1, 6.2, 6.3, 6.4, 6.5, 6.6, 6.7, 6.8, 6.9_

    - [x] 7.2 Escrever property test para agregação de portfólio (Property 7)
        - **Property 7: Portfolio aggregation includes only projects with status date**
        - Gerar conjuntos de 1-10 projetos (com/sem status_date) com `repeat(100)`
        - Verificar: PV, EV, AC, EAC do portfólio = soma apenas dos projetos com status_date definida
        - Verificar: projetos sem status_date não contribuem
        - Arquivo: `tests/Feature/EvmPortfolioTest.php`
        - **Validates: Requirements 6.1, 6.2, 6.3, 6.4, 6.5, 6.6, 6.7, 6.8, 6.9**

- [x]   8. Implementar registro de auditoria no EvmCalculationEngine
    - [x] 8.1 Adicionar registro de `AuditLog` em `getProjectSnapshot()`
        - Após calcular métricas com sucesso, criar `AuditLog` com operação `evm_metrics_calculated`
        - Registrar no `new_values`: PV, EV, AC, SPI, CPI
        - Usar `auditable_type` = `App\Models\Project`, `auditable_id` = project ID
        - Não registrar auditoria se o cálculo falhar ou retornar snapshot zerado
        - _Requirements: 12.1, 12.2, 12.3_

    - [x] 8.2 Escrever testes de auditoria
        - Verificar que recálculo gera audit log com operação `evm_metrics_calculated`
        - Verificar formato do audit log (new_values contém pv, ev, ac, spi, cpi)
        - Verificar que falha/snapshot zerado não gera audit log
        - Arquivo: `tests/Feature/EvmAuditTest.php`
        - _Requirements: 12.1, 12.2, 12.3_

- [x]   9. Checkpoint — Verificar portfólio e auditoria
    - Ensure all tests pass, ask the user if questions arise.

- [x]   10. Testes de integração end-to-end
    - [x] 10.1 Escrever teste de integração completo
        - Cenário end-to-end: criar projeto → baseline → medições → custos → calcular métricas derivadas
        - Verificar que getProjectSnapshot retorna valores corretos para um cenário com valores conhecidos do PRD
        - Verificar edge cases: projeto sem status_date, projeto sem baseline, projeto sem WPs
        - Arquivo: `tests/Feature/EvmIntegrationTest.php`
        - _Requirements: 8.1, 8.2, 8.3, 8.4, 9.1, 9.2, 9.3, 9.4, 11.1, 11.2, 11.3, 11.4_

- [x]   11. Final checkpoint — Verificar todos os testes
    - Ensure all tests pass, ask the user if questions arise.

## Notes

- Tasks marcadas com `*` são opcionais e podem ser puladas para um MVP mais rápido
- Cada task referencia requisitos específicos para rastreabilidade
- Checkpoints garantem validação incremental
- Property tests validam propriedades universais de corretude com `repeat(100)` no Pest v4
- Unit tests validam exemplos específicos e edge cases
- Não há migrações neste módulo — é puramente camada de cálculo/serviço
- O `EvmCalculationEngine` é registrado automaticamente pelo container do Laravel via auto-wiring
