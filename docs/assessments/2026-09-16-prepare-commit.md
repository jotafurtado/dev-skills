# Parecer sobre as alterações de prepare-commit

Data: 2026-09-16.
Status: avaliação registrada; melhorias ainda não implementadas.

## Escopo e conclusão

Revisão das alterações locais de `skills/prepare-commit/` contra o `HEAD` da sessão original. A versão declarada passou de `1.4.1` para `1.5.0`; o último commit da skill identificado naquela revisão foi `cc663f8c506f054a7a6bd0ba9f998b569dea5e25`. Esse commit é contexto histórico, não um snapshot das alterações locais. As linhas abaixo identificam a versão revisada e podem mudar após a implementação.

A direção é boa: a skill ficou mais genérica e preservou suas salvaguardas. Antes de considerar a revisão pronta, é necessário corrigir o transporte da mensagem, eliminar regras duplicadas e explicitar a precedência de idioma.

Este parecer é um registro do momento da revisão. O comportamento desejado está na [especificação](../specs/prepare-commit/spec.md); a execução futura está no [plano](../specs/prepare-commit/plan.md) e nas [tarefas](../specs/prepare-commit/tasks.md).

## Pontos positivos

- Escopos e exemplos menos acoplados a Laravel.
- Idioma da conversa considerado antes do fallback, em vez de assumir pt-BR para qualquer projeto.
- Exemplos em inglês, alinhados à convenção de autoria de skills do repositório.
- Preservação da autorização explícita para commit/push, da proteção do trabalho alheio e do staging por assunto.

## Standards: estrutura e manutenção

### A1 — Detalhes de changelog retornaram ao núcleo

Evidência: [SKILL.md](../../skills/prepare-commit/SKILL.md), Reference routing e Step 4, linhas 47–51 e 156–173 na revisão.

Relevância, categorias e organização foram incorporadas ao fluxo, enquanto a referência passou a ser opcional. Isso contraria a convenção do repositório de manter o núcleo comportamental em `SKILL.md` e carregar referências sob demanda. Mesmo execuções sem changelog carregam esse detalhamento.

Recomendação: deixar no núcleo a verificação da existência do arquivo e o roteamento obrigatório quando aplicável; manter o detalhamento em `references/changelog.md`. Uma referência distribuída com a skill não é uma dependência externa de execução.

### A2 — Descoberta de checks excessivamente prescritiva

Evidência: [SKILL.md](../../skills/prepare-commit/SKILL.md), Step 5, linhas 179–190 na revisão.

O texto mistura descoberta com receitas como `cargo clippy -- -D warnings`, Pest e Ruff. Os imperativos podem ser interpretados como política do projeto, embora a presença de um manifesto não estabeleça essas ferramentas ou flags. `-D warnings` acrescenta uma exigência que o repositório pode não adotar.

Este é um risco de interpretação das instruções, não uma execução defeituosa observada.

Recomendação: descobrir comandos nos scripts, configurações e CI existentes e executar o menor conjunto suficiente. Evitar a formulação no singular que pode sugerir escolher entre testes e typecheck quando ambos são necessários.

### A3 — Duplicação com regras divergentes

Evidência: [SKILL.md](../../skills/prepare-commit/SKILL.md), Preflight e Step 4, especialmente linha 165; [references/changelog.md](../../skills/prepare-commit/references/changelog.md), linhas 3 e 21 na revisão.

O Step 4 manda preservar o idioma do arquivo, enquanto o Preflight permite que uma instrução explícita escolha outro idioma. Cenário: changelog em inglês e pedido explícito de entrada em português. As passagens apontam para decisões diferentes.

A referência também admite preservar estruturas personalizadas, enquanto o núcleo prescreve headings específicos. A decisão passa a depender de a referência opcional ter sido carregada.

Recomendação: uma única autoridade para idioma no Preflight e uma única autoridade para relevância, estrutura e categorias na referência de changelog.

## Comportamento: riscos de execução

### A4 — A garantia de transporte multiplataforma não se sustenta

Evidência: [SKILL.md](../../skills/prepare-commit/SKILL.md), Cross-Platform Multiline Commit Execution, linhas 206–233 na revisão.

Múltiplos argumentos `-m` são aceitos pelo Git, mas não neutralizam a interpretação do texto pelo shell. A alternativa por pipeline também depende do encoding do PowerShell.

Experimento realizado durante a revisão anterior, em repositório temporário isolado:

| Cenário | Resultado observado |
| --- | --- |
| `-m "docs: explain $HOME expansion"`, PowerShell 7.6.6 | `$HOME` substituído pelo diretório do usuário. |
| Mesmo comando, Windows PowerShell 5.1.26100.9444 | Mesma expansão de `$HOME`. |
| Here-string enviado a `git commit -F -`, PowerShell 7.6.6 | Acentos preservados. |
| Mesmo pipeline, Windows PowerShell 5.1.26100.9444 | `configuração e ação` virou `configura??o e a??o`; também foi observado BOM no início da mensagem. |
| Argumentos diretos, sem shell, via subprocesso | `$HOME` literal e acentos preservados, com assunto e corpo separados por linha em branco. |

Foram criados commits vazios apenas no repositório temporário para observar a mensagem gravada. O diretório temporário foi removido; o repositório do projeto não foi alterado pelo experimento. Bash, Zsh e CMD não foram exercitados. Este registro preserva o resultado da sessão anterior; não afirma uma nova execução nem prova que todas as entradas possíveis são seguras.

Recomendação: preferir argumentos diretos quando o host permitir; caso contrário, transportar a mensagem em arquivo temporário UTF-8 sem BOM com `git commit -F`. O caminho ainda exige quoting adequado ao host. Essa alternativa por arquivo deverá ser exercitada na implementação; o experimento anterior comprovou apenas a alternativa com argumentos diretos. Exemplos específicos de shell devem declarar suas condições de quoting e encoding.

### A5 — Precedência de idioma com desempate implícito

Evidência: [SKILL.md](../../skills/prepare-commit/SKILL.md), Preflight, linhas 22–29 na revisão.

Documentação do projeto e histórico passaram a ser subitens do mesmo degrau. Antes, a documentação ficava explicitamente acima do artefato existente. Quando a documentação pede português e o histórico está em inglês, a precedência fica menos clara.

Recomendação: instrução explícita aplicável → convenção documentada → artefato daquele destino → idioma da conversa → inglês. Preservar a distinção entre idioma da mensagem e idioma da entrada de changelog.

## Spec: aderência ao pedido original

Não havia issue ou especificação identificada para as alterações locais durante a revisão. A mudança de fallback e a ampliação da compatibilidade não foram classificadas como desvio de escopo. A especificação vinculada acima nasce deste parecer e não deve ser apresentada como requisito histórico da alteração revisada.

## Fontes e limites

- Convenções de autoria do repositório, fornecidas no contexto da revisão.
- [Git: git-commit](https://git-scm.com/docs/git-commit): `-m` aceita parágrafos separados; `-F` lê arquivo ou stdin.
- [PowerShell: about_Character_Encoding](https://learn.microsoft.com/en-us/powershell/module/microsoft.powershell.core/about/about_character_encoding): diferenças de encoding entre versões e papel de `$OutputEncoding` na comunicação com programas externos.
- [Conventional Commits 1.0.0](https://www.conventionalcommits.org/en/v1.0.0/).
- [Keep a Changelog 1.1.0](https://keepachangelog.com/en/1.1.0/).

Balanço: três achados de estrutura/manutenção e dois de execução. A divergência de regras é o principal problema estrutural; a corrupção da mensagem é o problema de execução reproduzido. A redação da skill deve ser validada por cenários além dos testes mecânicos de transporte: um exemplo Git correto, isoladamente, não prova que o agente seguirá todo o fluxo.
