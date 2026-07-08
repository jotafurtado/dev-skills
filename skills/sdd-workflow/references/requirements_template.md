# Template BDD/Requirements (Referência)

O artefato de Requisitos (Fase 1) deve seguir uma estrutura formal, limitando o escopo a regras de negócio tangíveis. Ele deve adotar a Linguagem Ubíqua e Critérios de Aceitação baseados em "SHALL/WHEN/IF".

## Estrutura Obrigatória

### 1. Introdução
Breve resumo do propósito do módulo ou feature, suas integrações vitais e escopo macro.

### 2. Glossário
Definição dos termos-chave do domínio para abolir ambiguidades.

### 3. Requisitos de Negócio (Épicos / Detais)
Para cada grande função, crie um bloco contendo a História do Usuário e seus Critérios.

#### Exemplo de Estrutura:
### Requisito 1: [Nome do Requisito]

**User Story:** Como [Ator], eu quero [Ação / Funcionalidade], para que [Objetivo de Negócio - Valor].

#### Critérios de Aceitação
Use gramática formal e sentenças afirmativas vinculativas. Sublinhe as condições sistêmicas para garantir precisão e testabilidade (com foco em Property-Based Testing quando possível).
1. **WHEN** [contexto/ação], **THE** [Sistema/Serviço] **SHALL** [ação devida / cálculo].
2. **IF** [situação de borda/exceção], **THEN THE** [Sistema/Serviço] **SHALL** [caminho alternativo].
3. **FOR ALL** [elementos de uma de lista/árvore], o [resultado] **SHALL** [comportamento garantido universal].

> **Dica SDD:** Cada critério de aceitação de um requisito deverá estar vinculado diretamente a uma Tarefa de execução de Teste posteriormente.
