# Template de Design (Referência)

O artefato de Design (Implementation Plan - Fase 2) define *como* o código vai cumprir as especificidades do Requirements, sendo a planta de Arquitetura. Ele serve como o guia do qual as "Tasks" serão literalmente decalque.

## Estrutura Obrigatória

### 1. Overview & Decisões de Design
Resumo técnico do que será criado (ou o que não será criado - ex: "Não criaremos tabelas novas, apenas Models/DTOs"). E a justificativa em formato numérico.

### 2. Architecture
Uso obrigatório de diagramas **Mermaid** para expressar Fluxos de Dados (SequenceDiagrams) ou componentes (Graph).

### 3. Components and Interfaces
Tabelas e blocos de código com "esboços" rápidos das assinaturas (interfaces, assinaturas de construtores de services injetando instâncias, assinaturas DTO/Enums). 
> **Regra:** Não escreva a implementação do código, apenas as assinaturas, para o plano focar em abstrações.

### 4. Data Models (Modelagem de Banco de Dados)
Desenho de Tabelas (Migrações necessárias) ou se não for entidade de banco, mapeamento da estrutura JSON transitante.

### 5. Correctness Properties
O diferencial para Testes Baseados em Propriedade (Property-Based Tests). 
*Definição:* Uma propriedade que deve se manter imutavelmente correta durante toda execução do sistema independentemente dos inputs.
Exemplo: "Property 1: SV = EV - PV (Validates: Requirements 1.1)". Defina pelo menos as Propriedades chaves a serem testadas para a arquitetura.

### 6. Error Handling
Uma matriz (tabela) de quais anomalias podem ocorrer e como agir sem "crachar" o sistema ou poluir o Log.

### 7. Testing Strategy
Indique se usará Unit Tests, Integration Tests, ou Property-Based tests, mapeando quais requisitos serão checados em quais arquivos de Mock/Test.
