# Fase 0 — Pesquisa e decisões técnicas

Nenhum item do Technical Context ficou como NEEDS CLARIFICATION: o alvo é um pacote de skill já existente, com linguagem, suíte de testes e formatos conhecidos. As decisões abaixo resolvem *como* cumprir os requisitos, com as alternativas que foram descartadas.

---

## D1 — Formato do índice compacto: Markdown

**Decisão**: `references/visual-catalog-index.md` — uma tabela de patterns seguida das listas de vocabulário por dimensão.

**Justificativa**: o consumidor é um agente que já lê `references/*.md` como parte normal do fluxo. Markdown é o formato de menor atrito: não exige ferramenta, não exige parsing, e a tabela cabe no orçamento de 3–5 KB de SC-001. As demais referências da skill são Markdown; um formato diferente criaria uma exceção sem ganho.

**Alternativas descartadas**:
- *JSON compacto* — obrigaria o agente a parsear ou a ler estrutura serializada onde prosa serve melhor, e criaria um segundo artefato JSON a ser confundido com a fonte da verdade.
- *Seção dentro do `SKILL.md`* — contraria o Princípio III: o índice seria carregado sempre, inclusive em tarefas que não selecionam pattern.
- *Um arquivo por superfície* — 9 arquivos para 22 patterns; a fragmentação custa mais do que economiza nessa escala.

---

## D2 — O índice é gerado, nunca editado à mão

**Decisão**: `scripts/build_catalog_index.py` projeta o catálogo no índice. A detecção de deriva (FR-003) regenera o índice em memória e compara com o arquivo versionado, reprovando na diferença.

**Justificativa**: comparar o artefato com a projeção recém-gerada é a única checagem que não pode passar por engano — não há regra a manter em sincronia, só a projeção. É o mesmo padrão de "gerado e verificado" já usado para arquivos derivados. A deriva que essa checagem previne já ocorreu duas vezes neste repositório: a seção `## Structure` do README e o campo `scope` do catálogo (FR-022).

**Alternativas descartadas**:
- *Validar campo a campo com regras próprias* — duplica a lógica de projeção e apodrece junto com ela.
- *Gerar o índice em tempo de execução* — quebraria a via primária, que precisa funcionar por leitura de arquivo, sem executar nada.

**Onde a checagem entra**: `validate_visual_catalog.py`. Hoje esse script valida apenas o inventário de screenshots e não inspeciona campos de pattern — a checagem de índice é capacidade nova, não extensão de regra existente, e o `main()` passa a acumular erros das duas famílias.

---

## D3 — Falha fechada com sugestão via `difflib`

**Decisão**: cada dimensão valida seu termo contra o vocabulário extraído do catálogo. Termo inválido levanta erro nomeando a dimensão e listando as sugestões de `difflib.get_close_matches`, da biblioteca padrão.

**Justificativa**: `difflib` cobre exatamente o caso que motivou o defeito — variação ortográfica (`organise` / `organize`) e erro de digitação — sem dependência externa, o que preserva a restrição de operação offline. Quando não há sugestão próxima, a mensagem lista os termos válidos daquela dimensão.

**Alternativas descartadas**:
- *Só `choices=` do `argparse`* — resolve a interface de linha de comando, mas deixa a função de consulta aberta a chamadas programáticas inválidas, que é como os próprios testes a exercitam. A validação precisa viver na função; `choices=` entra como reforço na camada de linha de comando.
- *Aceitar e avisar* — é o comportamento atual em outra roupagem, e viola o Princípio IV.

---

## D4 — Superfície restringe; todo o resto ordena

**Decisão**: a superfície continua sendo filtro. Objetivo, fluxo de trabalho, contexto responsivo, forma de informação e relacionamento passam a somar peso positivo quando casam e zero quando não casam. O valor `-100` some do código.

**Justificativa**: o `-100` foi medido produzindo 40% de alcançabilidade em duas dimensões; com as cinco somadas a esparsidade é maior. E a recusa resultante emitia uma mensagem factualmente errada — dizia que a superfície não casava, quando casava. Um pattern parcialmente aderente, ranqueado com honestidade, é um resultado melhor do que uma instrução para abandonar o catálogo.

**Consequência**: o `ValueError` de "nenhum pattern corresponde" deixa de ser alcançável por combinação. Ele permanece apenas para o caso de superfície inválida, que agora é tratado como vocabulário inválido (D3) e ganha a mensagem correspondente. A mensagem antiga, que instruía a registrar lacuna de catálogo, é removida.

**Alternativas descartadas**:
- *Manter forma de informação e relacionamento duras* — reintroduziria o cenário "pergunta legítima, zero resultado" pelas duas dimensões mais esparsas do vocabulário (34 e 24 valores).
- *Limiar mínimo de pontuação* — recria o problema com um número arbitrário no lugar de `-100`.

---

## D5 — `available_width` sai da assinatura, permanece no dado

**Decisão**: o parâmetro sai de `query_catalog()` e da linha de comando. O campo permanece em cada pattern do catálogo como metadado descritivo, e não aparece no índice (FR-004).

**Justificativa**: manter o parâmetro aceito e ignorado deixaria no `--help` uma dimensão sem significado, e nada impediria um agente de continuar raciocinando com ela. Remover o campo do dado, por outro lado, apagaria informação verdadeira sobre a largura em que cada pattern foi projetado. Separar as duas coisas — dado preservado, eixo de consulta removido — é o que dissolve a ambiguidade em vez de reetiquetá-la.

**Custo conhecido**: 15 referências no arquivo de testes precisam ser atualizadas. É mudança de contrato, coberta pela versão 1.1.0 (FR-021).

---

## D6 — Pontuação como campo do registro, não como afirmação

**Decisão**: cada asserção no registro de execução deixa de ser texto e passa a ser um objeto com `assertion`, `verdict` (`pass` / `fail` / `unscored`) e `evidence` (trecho do transcript). O campo `review_required` do arquivo passa a ser derivado: verdadeiro enquanto existir qualquer `unscored`.

**Justificativa**: o Princípio IV diz que exit code não é veredito. Se a pontuação for uma afirmação em prosa no documento de release, ela é inverificável e o portão volta a ser encenação. Como campo derivado, o estado do arquivo prova a si mesmo, e a verificação automatizada pode reprovar um arquivo que se declare revisado com asserções pendentes.

**Reprovação é resultado válido**: a análise de origem prevê que o cenário #10 reprova no eixo de evidência de imagem. Um `fail` registrado com citação vale mais do que uma aprovação forçada, e nenhum critério de sucesso desta feature exige 15 de 15.

**Alternativas descartadas**:
- *Pontuação automática por correspondência de texto* — as asserções são julgamentos de composição em prosa ("a resposta identifica o formulário como grupos paralelos estáveis, e não como sequência"); casar palavra-chave produziria veredito falso, que é pior do que veredito nenhum.
- *Registrar o veredito só no documento de release* — inverificável, e é exatamente o que falhou na versão 1.0.0.

---

## D7 — Localização da skill resolvida a partir do próprio arquivo

**Decisão**: o `SKILL.md` deixa de mostrar um comando com caminho relativo. A via primária é a leitura do índice, referenciado pelo caminho do diretório instalado da skill; a alternativa por ferramenta aparece com a localização resolvida da mesma forma.

**Justificativa**: o comando atual, `python3 scripts/query_visual_catalog.py`, falha a partir de qualquer diretório real de trabalho — a skill instalada fica em `~/.claude/skills/<nome>/` e o agente está no projeto do usuário. Os scripts internos já resolvem seus próprios caminhos com `Path(__file__).resolve().parents[1]`; o `SKILL.md` era o único ponto que assumia diretório de trabalho.

---

## D8 — Retags responsivos com efeito de seleção assimétrico

**Decisão**: `responsive-identity-centred-table` e `operational-dashboard` passam a declarar `mobile-first`.

**Justificativa**: nos dois casos a etiqueta atual contradiz a evidência oficial que o próprio pattern carrega. Só o primeiro muda o resultado da seleção — `dashboard` tem um único pattern revisado, então a consulta retornaria o mesmo com ou sem a correção. O retag do dashboard se justifica por exatidão descritiva, e a spec já o registra assim (FR-010), para que a implementação não o confunda com um requisito comportamental.

**Não alterado**: `record-detail-infolist` já declara os dois contextos.
