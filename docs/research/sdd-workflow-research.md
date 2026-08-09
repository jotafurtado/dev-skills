# Pesquisa e decisões — sdd-workflow 2.0

Data: 13 de julho de 2026.

Este documento registra a pesquisa oficial usada para reformular a skill
`sdd-workflow` e separa comportamento do Kiro de extensões portáteis da skill.

## Fontes oficiais

### Kiro

- [Specs](https://kiro.dev/docs/specs/)
- [Feature Specs](https://kiro.dev/docs/specs/feature-specs/)
- [Requirements-First](https://kiro.dev/docs/specs/feature-specs/requirements-first/)
- [Design-First](https://kiro.dev/docs/specs/feature-specs/tech-design-first/)
- [Quick Plan](https://kiro.dev/docs/specs/quick-plan/)
- [Bugfix Specs](https://kiro.dev/docs/specs/bugfix-specs/)
- [Analyze Requirements](https://kiro.dev/docs/specs/analyze-requirements/)
- [Correctness with Property-Based Tests](https://kiro.dev/docs/specs/correctness/)
- [Specs in CLI](https://kiro.dev/docs/cli/v3/specs/)

### Cursor e GitHub

- [Cursor Agent Skills](https://cursor.com/docs/skills)
- [GitHub Spec Kit](https://github.com/github/spec-kit)
- [Spec Kit persistence models](https://github.github.com/spec-kit/concepts/spec-persistence.html)

## Fatos confirmados sobre o Kiro

Feature Specs produzem três artefatos:

- `requirements.md`
- `design.md`
- `tasks.md`

O Kiro oferece:

- Requirements-First;
- Design-First em HLD ou LLD;
- Quick Plan sem gates intermediários;
- Bugfix Specs usando `bugfix.md`, não `requirements.md`.

No fluxo padrão, há revisão humana entre as fases de requisitos/design. O Quick
Plan concentra esclarecimentos no início e gera os três artefatos sem gates
intermediários.

As tasks são discretas, rastreáveis, podem ser obrigatórias ou opcionais e
possuem dependências. A execução de todas as tasks considera apenas tasks
obrigatórias incompletas e pode paralelizar itens independentes.

EARS é usado para comportamento observável:

```text
WHEN [condição ou evento]
THE SYSTEM SHALL [comportamento esperado]
```

Property-based testing é opcional por padrão. Correctness properties são
invariantes; PBT é apenas uma técnica possível para exercitá-las.

O Kiro IDE armazena specs em `.kiro/specs/`. O estado de UI, Sync Files,
`#spec`, botões e comandos do Kiro não são portáveis diretamente para outros
agentes.

## Referência do Spec Kit

O GitHub Spec Kit separa:

- `.specify/` para configuração, templates e scripts;
- `specs/` para artefatos versionados.

Isso confirmou que artefatos de produto devem permanecer visíveis e separados
da infraestrutura da ferramenta.

## Decisões da skill

### Diretório e identificação

A skill usa:

```text
sdd-specs/001-nome-da-spec/
```

`sdd-specs/` foi escolhido para:

- manter artefatos visíveis e versionáveis;
- identificar explicitamente a metodologia;
- evitar colisão com `.kiro/specs/` e `specs/` do Spec Kit.

O prefixo é obrigatório, monotônico, formatado com no mínimo três dígitos e
nunca reutilizado ou renumerado.

### Ativação

A skill continua elegível para auto-invocação, mas somente quando o usuário
menciona explicitamente SDD, Kiro, spec-driven development, spec, evitar vibe
coding ou planejamento antes da implementação. Uma solicitação comum de feature,
refactor ou bug não deve ativá-la.

### Estado portátil

`spec.yaml` é uma extensão desta skill. Ele registra:

- identificador, tipo e modo;
- fase e status;
- revisões, dependências e hashes;
- aprovações;
- autorização e task ativa.

O arquivo resolve uma lacuna de agentes sem a UI do Kiro: a mera existência de
um Markdown não prova aprovação.

### Persistência

Durante trabalho ativo, a skill usa uma living spec:

- Requirements-First e Quick Plan seguem requirements → design → tasks;
- Design-First segue design → requirements → tasks;
- Bugfix segue bugfix → design → tasks;
- uma alteração invalida seus descendentes no grafo do modo;
- tasks alteradas exigem reconciliação com o progresso.

Artefatos aprovados nunca são sobrescritos silenciosamente.

### Execução

Cada task segue:

```text
implementar → verificar → registrar evidência → marcar concluída
```

“Run all” considera somente tasks obrigatórias incompletas, respeita
dependências e paraleliza apenas quando o host suporta e não há conflito.

A convergência final confirma critérios de aceite, comportamento preservado,
checks e riscos restantes.

## Diferenças intencionais para o Kiro

- `sdd-specs/` substitui `.kiro/specs/`.
- `spec.yaml` substitui parte do estado mantido pela UI.
- Os templates Markdown e IDs são schema da skill, não formato normativo do
  Kiro.
- A skill explicita precedência do host e autorização de execução.
- Hashes e regras de invalidação são mecanismos portáteis adicionados.
