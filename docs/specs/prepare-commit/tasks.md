# Tarefas: melhorias de prepare-commit

Status: implementação concluída e revisada em 2026-09-16. Limites de verificação registrados abaixo.
Contrato: [spec.md](spec.md).
Sequência e procedimento de verificação: [plan.md](plan.md).
Origem: [parecer A1–A5](../../assessments/2026-09-16-prepare-commit.md).

A criação destes documentos não conclui tarefas de implementação. Marcar uma tarefa somente após cumprir seu critério de saída. Registrar impedimentos no item correspondente, sem marcar como concluído. O parecer é histórico; evidência da implementação deve ser registrada aqui.

## Implementação

- [x] **T01 — Explicitar a precedência de idioma por destino.**
  - Origem: A5; requisito: R5; plano: P1.
  - Arquivo: `skills/prepare-commit/SKILL.md`, Preflight.
  - Dependências: nenhuma.
  - Saída: cinco degraus explícitos; documentação vence histórico; instruções conservam escopo; mensagem e changelog podem divergir conforme C03–C05.

- [x] **T02 — Restaurar roteamento e autoridade única do changelog.**
  - Origem: A1 e A3; requisitos: R1 e R3; plano: P2.
  - Arquivos: `skills/prepare-commit/SKILL.md` e `references/changelog.md` dentro da mesma skill.
  - Dependências: T01.
  - Saída: núcleo apenas verifica e encaminha; referência carregada quando o arquivo existe; nenhuma regra concorrente de idioma, relevância ou categoria; formatos próprios e casos existentes preservados conforme C01–C03 e C05.

- [x] **T03 — Derivar o conjunto de checks do projeto.**
  - Origem: A2; requisito: R2; plano: P3.
  - Arquivo: `skills/prepare-commit/SKILL.md`, Step 5 e sua integração com Step 6.
  - Dependências: nenhuma dependência funcional; executar após T02 para serializar edições no arquivo compartilhado.
  - Saída: descoberta baseada em configuração, menor conjunto suficiente, sem ferramentas ou flags impostas pela stack; indisponibilidade e falha distintas conforme C06–C08.

- [x] **T04 — Corrigir o transporte literal da mensagem.**
  - Origem: A4; requisito: R4; plano: P4.
  - Arquivo: `skills/prepare-commit/SKILL.md`, execução multilinha.
  - Dependências: nenhuma dependência funcional; executar após T03 para serializar edições no arquivo compartilhado.
  - Saída: argumentos diretos ou arquivo UTF-8 sem BOM conforme permissões do host; caminho protegido; temporário fora do staging e removido em sucesso/falha; exemplos inseguros removidos. Prova executável em T06.

- [x] **T05 — Alinhar o README ao comportamento implementado.**
  - Origem: A1–A5; requisitos: R1–R5; plano: P5.
  - Arquivo: `skills/prepare-commit/README.md`.
  - Dependências: T01–T04.
  - Saída: idioma, referências, checks e transporte descritos sem promessas excedentes; instalação, triggers e salvaguardas preservados; nenhuma release anunciada por este trabalho.

## Verificação

- [x] **T06 — Exercitar os cenários e registrar as evidências.**
  - Origem: A1–A5; requisitos: R1–R5 e invariantes; plano: P6.
  - Dependências: T01–T05.
  - Saída: C01–C12 atendidos e registrados abaixo, incluindo transporte real; links válidos; skill e referências em inglês; nenhuma alteração de autorização, nenhuma evidência simulada apresentada como execução real.
  - Os ambientes alegados devem corresponder aos exercitados. Se um ambiente não puder ser verificado, registrar a limitação e restringir a promessa antes de concluir.
  - A evidência de A4 no parecer descreve a revisão anterior e não conclui esta tarefa.

## Registro de evidências

Verificação em 2026-09-16: Main revisou os três arquivos implementados por dois subagents. C01–C08 e C11–C12 foram exercitados em simulação textual por modelo, com a skill e a referência implementadas como instruções e os cenários como fixtures. As decisões retornadas foram comparadas por Main com a especificação. Isso verifica interpretação, não execução de ferramentas ou leitura condicional real de arquivos. C09–C10 foram executados em Git real, em repositórios temporários isolados e removidos ao final.

| Cenário | Método, ambiente e evidência | Resultado |
| --- | --- | --- |
| C01 | Simulação textual: não carregar referência nem criar changelog ausente. | Decisão conforme. |
| C02 | Simulação textual: carregar referência; omitir whitespace-only; registrar API pública em Added. | Decisão conforme. |
| C03 | Simulação textual: entrada portuguesa, histórico inglês e estrutura preservados. | Decisão conforme. |
| C04 | Simulação textual: português documentado vence histórico inglês; espanhol da conversa sem artefatos; inglês sem sinais. | Decisão conforme. |
| C05 | Simulação textual: mensagem portuguesa, entrada inglesa em Removed APIs existente, com quebra e migração explícitas. | Decisão conforme. |
| C06 | Simulação textual: selecionar test e typecheck configurados; não inventar lint. | Decisão conforme. |
| C07 | Simulação textual: usar cargo test configurado na CI; não acrescentar deny-warnings. | Decisão conforme. |
| C08 | Simulação textual: executável ausente é indisponível; exit 1 é falha; host bloqueia commit quando falha. | Decisão conforme. |
| C09 | Git 2.53.0.windows.1; subprocesso sem shell; comparação dos bytes da mensagem armazenada via cat-file. Unicode, aspas, dólar, substituição literal, backticks, comentário literal, espaços e parágrafos preservados com `--cleanup=verbatim`. | Execução aprovada. |
| C10 | Arquivo UTF-8 sem BOM, caminho com espaços, `-F` e `--cleanup=verbatim`; PowerShell 7.6.6 e Windows PowerShell 5.1.26100.9444. Sucesso comparado byte a byte; falha controlada por ausência de alterações. Temporário removido em ambos os caminhos; índice limpo. | Execução aprovada nos dois shells. |
| C11 | Simulação textual: preview não cria commit; autorização de commit não autoriza push. | Decisão conforme. |
| C12 | Simulação textual: parar e perguntar diante de trabalho alheio stageado e bloqueio do host; não remover nem incorporar silenciosamente. | Decisão conforme. |

### Revisão e limites

- O transporte final acrescenta `--cleanup=verbatim` para não depender de defaults de cleanup do Git; o método foi exercitado, inclusive com linhas iniciadas por `#` e espaços intencionais.
- Gates de autorização, amend, hooks, staging e push foram preservados na revisão de Main. Nenhum commit ou push foi feito no repositório do projeto.
- Bash, Zsh e CMD não foram exercitados. A implementação removeu receitas específicas e a promessa universal de quoting; exige transporte permitido pelo host e interrupção quando não houver método seguro.
- Simulação textual não prova execução ponta a ponta de um agente com ferramentas. Essa limitação permanece explícita; não houve instalação ou execução de stacks Rust/Node para os cenários de seleção.
- Não foram criados testes permanentes de texto nem wrappers Git. Os experimentos foram descartáveis; a referência de changelog e o parecer histórico foram preservados como autoridades de seus respectivos conteúdos.

## Rastreabilidade

| Achado | Requisito | Implementação | Verificação |
| --- | --- | --- | --- |
| A1 | R1 | T02, T05 | T06: C01, C02 |
| A2 | R2 | T03, T05 | T06: C06–C08 |
| A3 | R3, R5 | T01, T02, T05 | T06: C02, C03, C05 |
| A4 | R4 | T04, T05 | T06: C09, C10 |
| A5 | R5 | T01, T05 | T06: C03–C05 |
| Salvaguardas preservadas | Invariantes | T01–T05 | T06: C11, C12 |
