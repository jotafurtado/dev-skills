# Especificação: melhorias de prepare-commit

Status: implementada e revisada em 2026-09-16; evidências e limites em [tasks.md](tasks.md).
Data: 2026-09-16.
Origem: [parecer A1–A5](../../assessments/2026-09-16-prepare-commit.md).
Execução: [plano](plan.md) e [tarefas](tasks.md).

## Objetivo

Tornar as instruções de `prepare-commit` inequívocas e portáveis sem ampliar permissões de Git. Preservar os ganhos de generalização, resolver as cinco oportunidades do parecer e manter o núcleo da skill focado em decisões e roteamento.

## Escopo

Arquivos de implementação previstos:

- `skills/prepare-commit/SKILL.md`: precedência de idioma, roteamento, descoberta de checks e transporte da mensagem.
- `skills/prepare-commit/references/changelog.md`: autoridade sobre relevância, estrutura e classificação do changelog.
- `skills/prepare-commit/README.md`: descrição humana consistente com o comportamento implementado.

Estes documentos em `docs/` registram a proposta; sua criação não implementa as melhorias. O conteúdo final da skill e de suas referências permanece em inglês, conforme a convenção do repositório. Os documentos de planejamento seguem o português usado na documentação de manutenção existente.

## Requisitos

### R1 — Carregamento condicional do changelog

Origem: A1.

- O Step 4 deve verificar a existência de `CHANGELOG.md` na raiz do projeto alvo.
- Sem esse arquivo, deve pular a atualização e não criá-lo sem solicitação explícita.
- Quando o arquivo existir e o fluxo alcançar esse passo, deve carregar `references/changelog.md` antes de decidir se há uma entrada relevante.
- Relevância, categorias e regras de organização devem existir apenas na referência. O núcleo mantém somente a condição e o encaminhamento.
- A tabela de roteamento deve apontar a mesma condição, sem apresentar a referência como opcional ou como dependência externa.

Aceitação: C01 e C02; leitura estrutural confirma uma única definição do detalhamento de changelog.

### R2 — Checks derivados do projeto

Origem: A2.

- Descobrir os checks aplicáveis nos scripts, configurações e CI do projeto, considerando ferramentas e versões disponíveis.
- A presença de um manifesto deve orientar a descoberta, não autorizar um catálogo fixo de ferramentas ou flags.
- Executar o menor conjunto suficiente para os arquivos ou pacotes envolvidos; esse conjunto pode conter testes, lint e typecheck.
- Preservar execução não interativa, preferência por modo de verificação e proteção de arquivos fora do escopo.
- Distinguir check indisponível de check executado com falha; relatar ambos fielmente e seguir o protocolo do host, sem tratar falha como sucesso ou indisponibilidade.
- Manter Step 5 como dono da descoberta e Step 6 como consumidor do conjunto aplicável a cada assunto. Não acrescentar redescoberta a cada commit.

Aceitação: C06–C08; nenhum comando é escolhido apenas por ser comum naquela stack, e nenhuma política de warnings é acrescentada pela skill.

### R3 — Autoridade única para o changelog

Origem: A3.

- A referência deve obter o idioma da entrada exclusivamente pela precedência do Preflight definida em R5.
- Preservar estrutura, headings e estilo existentes quando forem intencionais; usar Keep a Changelog como organização padrão quando não houver convenção própria.
- Preservar a classificação por impacto, incluindo documentação pública relevante, reversões, segurança e remoções com quebra de compatibilidade.
- Uma instrução explícita para o idioma da nova entrada não implica traduzir entradas antigas ou reorganizar o arquivo.
- Remover regras concorrentes de idioma e categorias do núcleo e alinhar o README ao roteamento real.

Aceitação: C02, C03 e C05; o resultado não depende de uma referência ter sido lida opcionalmente.

### R4 — Transporte literal da mensagem

Origem: A4.

- Escolher um método permitido pelo host que transporte assunto, corpo e footers sem interpretação do conteúdo pelo shell.
- Preferir argumentos diretos para o processo Git quando disponíveis. Múltiplos `-m` representam parágrafos; isso não torna uma string de comando interpolada segura.
- Quando argumentos diretos não estiverem disponíveis, usar arquivo temporário UTF-8 sem BOM com `git commit -F`, por operações permitidas pelo host. Proteger o argumento do caminho conforme o shell ou API utilizado.
- Preservar caracteres Unicode, aspas, sinais de dólar, backticks e quebras de parágrafo intencionais. A normalização usual do terminador final pelo Git não é corrupção da mensagem.
- Manter o arquivo temporário fora dos caminhos stageados e removê-lo ao concluir ou falhar, sem apagar arquivos de terceiros.
- Se o host não permitir um transporte seguro, reportar a limitação antes de criar o commit, em vez de improvisar uma alternativa com perda de conteúdo.
- Remover a promessa de segurança universal de `-m "..."` e o pipeline PowerShell sem controle de encoding. Exemplos específicos de shell, se mantidos, exigem validação no ambiente declarado.

Aceitação: C09 e C10; a mensagem armazenada no commit preserva os valores e a estrutura esperados. Alegações de compatibilidade não podem exceder os métodos e ambientes efetivamente verificados.

### R5 — Precedência explícita por destino

Origem: A5; resolve também o conflito de idioma de A3.

Usar a seguinte ordem para cada destino escrito, respeitando as instruções superiores do host:

1. Instrução explícita aplicável do usuário, respeitando seu escopo e duração.
2. Convenção documentada do projeto.
3. Artefato existente daquele destino: histórico recente para a mensagem; changelog para a entrada.
4. Idioma da conversa.
5. Inglês como fallback da skill.

Uma instrução limitada a um commit não altera o padrão futuro do projeto. Na ausência de uma regra superior comum, mensagem e entrada podem ter idiomas diferentes. Manter tokens exigidos por Conventional Commits, como `BREAKING CHANGE`, sem traduzir sua sintaxe.

Aceitação: C03–C05; documentação vence histórico divergente, e a preferência de um destino não é copiada automaticamente para o outro.

## Invariantes preservadas

As melhorias não alteram autorização de commit/push, precedência do host, elegibilidade de amend, tratamento de hooks, staging explícito por assunto, proibição de staging interativo, proteção de segredos ou preservação do trabalho de terceiros. Pedido de mensagem ou preview não autoriza commit. Pedido de commit não autoriza push. Validar em C11 e C12.

## Cenários de aceitação

Resultados da verificação registrados em [tasks.md](tasks.md), distinguindo simulação textual de execução real. Os resultados históricos do parecer não substituem a verificação da nova redação e dos novos métodos.

| ID | Requisitos | Situação | Resultado esperado |
| --- | --- | --- | --- |
| C01 | R1 | Projeto sem `CHANGELOG.md` na raiz. | Pula atualização, não cria arquivo nem carrega a referência de changelog. |
| C02 | R1, R3 | Changelog existente; comparar uma mudança interna sem impacto externo e uma mudança pública relevante. | Carrega a referência; omite a primeira entrada e registra a segunda no formato existente. |
| C03 | R3, R5 | Changelog inglês e solicitação explícita de nova entrada em português. | Nova entrada em português; conteúdo histórico e estrutura preservados. |
| C04 | R5 | Documentação determina português, histórico inglês e pedido sem override. | Mensagem em português. Sem documentação nem artefato, usa conversa; sem esses sinais, inglês. |
| C05 | R3, R5 | Histórico de commits português, changelog inglês com organização própria e remoção incompatível, sem regra superior comum. | Mensagem portuguesa e entrada inglesa; usa a categoria de remoção existente, sem criar headings concorrentes. |
| C06 | R2 | Projeto configura testes e typecheck relevantes, sem linter configurado. | Seleciona os dois checks necessários, sem inventar um terceiro. |
| C07 | R2 | Projeto Rust sem política de warnings como erros. | Descobre os checks reais; não acrescenta `-D warnings` por conta própria. |
| C08 | R2 | Comparar check configurado mas indisponível e check disponível que retorna falha. | Relatos distintos e verdadeiros; aplica protocolo do host, sem declarar aprovação. |
| C09 | R4 | Assunto, corpo e footer com Unicode, aspas, `$HOME`, `$(...)`, backticks e parágrafos, usando argumentos diretos. | Conteúdo literal preservado na mensagem gravada; nenhum trecho vira comando de shell. |
| C10 | R4 | Mesma mensagem por arquivo UTF-8 sem BOM, caminho com espaços; exercitar sucesso e falha do commit. | Mensagem correta no sucesso; temporário fora do staging e removido nos dois caminhos. |
| C11 | Invariantes | Pedido de mensagem/preview e pedido de commit sem push. | Nenhum commit no primeiro caso; nenhum push no segundo. |
| C12 | Invariantes | Índice contém trabalho de outro assunto; host impõe restrições adicionais. | Não incorpora ou remove esse trabalho silenciosamente; respeita o host. |

## Fora do escopo

- Implementar as melhorias durante a criação destes documentos.
- Criar um wrapper Git, framework de execução ou catálogo de comandos por linguagem.
- Reformular os gates de segurança, adicionar retries, alterar configurações Git ou instalar ferramentas automaticamente.
- Reestruturar outras skills, traduzir changelogs inteiros ou introduzir novos formatos de changelog.
- Definir release, aumentar a versão automaticamente ou criar commit/push sem solicitação específica.

## Critério de conclusão da implementação

Todos os requisitos R1–R5 atendidos; README coerente; cenários C01–C12 verificados com evidência e limitações registradas nas tarefas; invariantes preservadas. Métodos de transporte mantidos devem ter prova executável nos ambientes alegados. Ambiente indisponível deve ser identificado, e a promessa correspondente deve ser restringida antes de declarar a melhoria concluída.
