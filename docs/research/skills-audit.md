# Auditoria e evolução das skills

Data da revisão: 13 de julho de 2026.

Este documento registra a análise das três skills do repositório, as decisões
tomadas e as melhorias implementadas. O objetivo foi otimizar descoberta,
precisão, uso de contexto, segurança e capacidade de verificação por agentes de
código.

## Referencial

A revisão usou documentação e exemplos oficiais:

- [Cursor Agent Skills](https://cursor.com/docs/skills)
- [Filament 5](https://filamentphp.com/docs/5.x/)
- [Filament 5 LLM index](https://filamentphp.com/docs/llms.txt)
- [Laravel Nova 5](https://nova.laravel.com/docs/v5/)
- [Laravel Nova 5 LLM index](https://nova.laravel.com/docs/llms.txt)
- [Conventional Commits 1.0.0](https://www.conventionalcommits.org/en/v1.0.0/)
- [Keep a Changelog](https://keepachangelog.com/)

Os critérios principais foram:

- `description` específica, com poucos falsos positivos;
- `SKILL.md` focado no fluxo de decisão;
- referências de um nível carregadas apenas quando necessárias;
- APIs e exemplos compatíveis com a versão declarada;
- precedência explícita das instruções do usuário e do protocolo do host;
- ciclo completo de implementação e verificação;
- ausência de regras absolutas onde o framework admite mais de uma solução.

## Resultado inicial

### `laravel-filament-v5` — 8/10

Era a skill mais preparada para agentes de código. O gate de componentes
oficiais, o roteamento para referências e o protocolo de consulta à documentação
reduziam o risco de gerar Blade ou CSS desnecessário.

Principais problemas encontrados:

- requisitos mais restritivos que os oficiais;
- assinatura de `infolist()` sem distinguir Resource e View page customizada;
- orientações contraditórias para ícones e operação;
- dependência do `CodeEntry` ausente no exemplo principal;
- regras absolutas para `preload()` e callbacks de cor;
- testes existentes, mas pouco integrados ao workflow.

### `prepare-commit` — 7,5/10

Já tinha bom fluxo, baixo custo de contexto, proteção contra staging indevido,
Conventional Commits em português e atualização conservadora do changelog.

Principais problemas encontrados:

- regras de amend e validação podiam conflitar com protocolos nativos do host;
- ausência de regra explícita para push;
- staging atômico descrito como intenção, sem loop operacional;
- tipos de commit e categorias de changelog incompletos;
- regras portáveis e regras específicas do host não estavam separadas.

### `laravel-nova-5` — 6/10

Tinha boa cobertura funcional, mas estava estruturada como um manual carregado
por inteiro. Também havia exemplos incompatíveis com a documentação Nova 5.

Principais problemas encontrados:

- ordem incorreta dos argumentos de download de uma action;
- dashboard com `authorize()` e `static label()` em vez de autorização no
  registro e `name()`;
- ausência de protocolo para consultar a documentação oficial atual;
- `SKILL.md` longo e referências temáticas insuficientes;
- gatilhos genéricos que colidiam com Filament;
- ausência de gate por `composer.json` / `composer.lock`;
- policy defaults resumidos de forma imprecisa;
- ausência de estratégia de testes.

## Alterações implementadas

### Laravel Filament v5

A skill passou da versão `2.0.0` para `2.1.0`.

- Os requisitos foram alinhados ao fluxo oficial do Filament 5: PHP 8.2+,
  Laravel 11.28+, Livewire 4+ e Tailwind CSS 4.1+.
- O gatilho agora exige sinais Filament e não ativa por “admin panel”,
  “dashboard” ou “status badge” isolados.
- O gate considera primeiro a superfície correta. Quando não existe equivalente
  oficial, exige consulta às docs e permite o menor workaround documentado.
- `infolist()` agora diferencia a assinatura estática do Resource da assinatura
  de instância em uma View page customizada.
- O exemplo de `CodeEntry` inclui `composer require phiki/phiki`.
- Ícones seguem uma hierarquia consistente: enum `Heroicon` para Heroicons e
  strings para outros sets documentados.
- Operações preferem métodos dedicados, usam `Operation` onde aceito e preservam
  `string $operation` em utility callbacks documentados.
- `preload()` e callbacks locais de cor deixaram de ser tratados como proibidos
  ou obrigatórios.
- A referência de testes tornou-se parte explícita do workflow pós-alteração e
  ganhou cobertura para View pages e relation managers.
- Snippets passaram a declarar quando são fragmentos e quais imports precisam
  ser adicionados.

Arquivos revisados: `SKILL.md`, `README.md` e todas as referências existentes em
`skills/laravel-filament-v5/references/`.

### Prepare Commit

A skill passou da versão `1.0.0` para `1.1.0`.

- As instruções do usuário e os protocolos do host passaram a ter precedência
  explícita para amend, hooks, push, permissões e comandos.
- Push exige pedido separado e explícito.
- Amend segue as condições do host; sem protocolo do host, exige pedido
  explícito e commit local não publicado.
- Comandos Git interativos, incluindo `git add -p`, foram proibidos.
- O staging agora usa caminhos explícitos e um loop por concern:
  stage, revisão do cached diff, checks permitidos, commit e nova inspeção.
- Os tipos adicionais foram separados dos requisitos normativos de Conventional
  Commits: somente `feat` e `fix` têm semântica obrigatória na especificação.
- O changelog agora cobre Added, Changed, Deprecated, Removed, Fixed e Security,
  além de breaking changes e mudanças internas que normalmente não geram
  entrada.
- Testes e formatadores só são executados quando o protocolo do host permite.
- A skill continua com invocação automática. Não foi adicionado
  `disable-model-invocation: true`, pois “commitar” é um gatilho principal e
  intencional; a segurança fica nas regras de autorização e precedência.
- O idioma passou a seguir usuário, convenção do projeto e histórico, com
  português brasileiro como fallback.

Arquivos revisados: `skills/prepare-commit/SKILL.md` e `README.md`.

### Laravel Nova 5

A skill passou da versão `1.0.0` para `2.0.0`.

- O `SKILL.md` foi reduzido para um gate, protocolo oficial, constraints,
  roteamento e workflow de verificação.
- O agente deve confirmar `laravel/nova` 5.x em `composer.json` e
  `composer.lock` antes de gerar código.
- O gatilho exige sinais Nova e diferencia explicitamente projetos Filament.
- Foi adicionado o protocolo baseado em `https://nova.laravel.com/docs/llms.txt`
  e páginas `/docs/v5/`.
- O download de actions usa `ActionResponse::download($name, $url)`.
- Dashboards usam `name()`, são registrados com `::make()` e recebem
  `canSee()` / `canSeeWhen()` durante o registro.
- Policy defaults foram documentados por operação, sem a simplificação
  “permite tudo” ou “nega tudo”.
- `HasMany` deixou de ter pluralização tratada como regra absoluta.
- Eager loading, polling, preload e actions queued passaram a considerar custo,
  escala e limitações reais.
- Snippets centrais incluem imports ou são marcados como fragmentos.
- Foram criadas referências para resources, fields, relationships,
  authorization, files e testing.
- A estratégia de testes usa APIs públicas de Laravel e do projeto; não inventa
  uma DSL de testes Nova que a documentação não oferece.

Arquivos revisados:

- `skills/laravel-nova-5/SKILL.md`
- `skills/laravel-nova-5/README.md`
- referências existentes de actions, métricas e customização;
- novas referências `resources.md`, `fields.md`, `relationships.md`,
  `authorization.md`, `files.md` e `testing.md`.

## Decisões de design

- Regras do host não foram copiadas integralmente para as skills. As skills
  declaram precedência e mantêm apenas garantias portáveis ou comportamento de
  domínio.
- Referências permanecem a um nível de profundidade para favorecer progressive
  disclosure.
- Exemplos curtos são permitidos, mas precisam ser completos ou identificados
  como fragmentos.
- A documentação instalada e o lockfile prevalecem sobre conhecimento de
  memória do modelo.
- Testes são proporcionais ao risco e à superfície alterada; sucesso de parsing
  não é tratado como verificação funcional.

## Verificações realizadas

- frontmatter e estrutura das skills revisados;
- referências locais e links oficiais conferidos;
- snippets e regras cruzadas revisados para consistência;
- `git diff --check` executado sem erros de whitespace;
- diagnósticos do editor executados nos arquivos alterados;
- nenhum commit ou push foi criado durante esta revisão.

## Próximas revisões

As APIs de Filament e Nova podem mudar dentro das linhas 5.x. Ao atualizar uma
skill:

1. consultar o respectivo `llms.txt`;
2. conferir a versão instalada e o lockfile de um projeto real;
3. revisar exemplos copiados nas referências;
4. executar prompts positivos e negativos para testar descoberta;
5. atualizar este documento quando houver nova decisão estrutural.
