# Template de Tasks (Referência)

O artefato de Tasks (Fase 3) deve ser extremamente metódico e processual. É o trilho do trem da fase "Grounded Execution".

## Regras de Estruturação
- Checklists usando `- [ ]`.
- Ordem do desenvolvimento "incremental" — preferivelmente do centro do domínio (Enums/DTOs) -> Interfaces/Services -> Adapters -> Apresentação/Telas.

## Estrutura Tipo

```markdown
- [ ] 1. Base do Domínio 
    - [ ] 1.1 Criar [Enum/DTO] com atributos x, y, z (_Requirements: 1.1_)
    - [ ] 1.2 Escrever property/unit test para [Enum/DTO] (Property X)

- [ ] 2. Checkpoint — Validação da Base
    - Pare as execuções, rode testes se aplicável e garanta que a infra inicial existe adequadamente. Peça verificação.

- [ ] 3. Camada de Aplicação / Services
    - [ ] 3.1 Criar ServiceX com injeção de Y.
    - [ ] 3.2 Escrever Feature Tests correspondentes (Property Z).

- [ ] 4. Checkpoint — Validação da Lógica Core
    - Pare as execuções, teste o service, corrija bugs antes de mexer na UI.

- [ ] 5. Integração com Frontend / Telas
    - [ ] 5.1 Atualizar Controller ou Action Filament/Inertia
```

> **Aviso:** Cada sub-tarefa do código DEVE estar referenciada a um número de Requisito ou Correctness Property descritos no artefato de Requirements e Design.
