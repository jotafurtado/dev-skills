# Plano: melhorias de prepare-commit

Status: executado e revisado em 2026-09-16; evidências e limites em [tasks.md](tasks.md).
Contrato: [spec.md](spec.md).
Controle de execução: [tasks.md](tasks.md).
Evidência de origem: [parecer](../../assessments/2026-09-16-prepare-commit.md).

## Organização

`spec.md` define comportamento e aceitação; este plano define sequência e locais de alteração; `tasks.md` registra progresso e evidências. Se a decisão de produto mudar, atualizar primeiro a especificação. O parecer permanece histórico.

Manter a alteração nos três arquivos da skill já existentes. Não adicionar referências ou abstrações apenas para acomodar os exemplos atuais. As edições compartilham `SKILL.md` e devem ter um responsável pela integração, sem escrita concorrente nesse arquivo.

## Etapas

### P1 — Tornar a precedência de idioma explícita

Requisito: R5. Tarefa: T01.

1. No Preflight de `SKILL.md`, separar os cinco degraus definidos na especificação.
2. Explicitar a precedência da documentação sobre o histórico e o escopo de instruções aplicáveis do usuário.
3. Manter a resolução independente para mensagem e entrada de changelog, sem traduzir tokens de máquina.

Saída: uma única regra de seleção de idioma, usada pelos dois destinos. C03–C05 têm resultado determinável sem regra concorrente.

### P2 — Restaurar a referência como autoridade do changelog

Requisitos: R1 e R3; depende de P1. Tarefa: T02.

1. Reduzir Step 4 à existência do arquivo e ao encaminhamento obrigatório quando aplicável.
2. Alinhar Reference routing à mesma condição; remover a descrição de referência opcional e a justificativa de autossuficiência.
3. Em `references/changelog.md`, manter as regras de relevância, estrutura e categorias, com a remissão de idioma para o Preflight.
4. Preservar os casos já cobertos: documentação pública relevante, reversões, segurança, formatos próprios e remoções incompatíveis.
5. Remover a cópia de regras do núcleo, em vez de manter duas versões sincronizadas manualmente.

Saída: C01–C03 e C05 encaminhados por uma única autoridade de changelog; nenhuma tradução ou reorganização histórica implícita.

### P3 — Simplificar a descoberta de checks

Requisito: R2. Tarefa: T03.

1. Substituir o catálogo imperativo de stacks no Step 5 pela descoberta dos comandos configurados no projeto.
2. Definir a seleção do menor conjunto suficiente, sem impor um limite de um comando.
3. Preservar o compartilhamento do conjunto entre Step 5 e o loop por assunto do Step 6.
4. Manter relato de limitações, proteção do escopo e protocolo do host para falhas, sem adicionar ferramentas ou flags de política.

Saída: C06–C08 cobertos sem inferir ferramentas apenas de um manifesto.

### P4 — Corrigir o transporte da mensagem

Requisito: R4. Tarefa: T04.

1. Na seção de execução multilinha, distinguir argumentos diretos de strings interpretadas pelo shell.
2. Tornar argumentos diretos a preferência quando a API do host permitir.
3. Definir arquivo temporário UTF-8 sem BOM como alternativa permitida pelo host, com quoting do caminho, exclusão do staging e remoção após sucesso ou falha.
4. Remover os exemplos que prometem segurança universal ou dependem de encoding implícito. Evitar multiplicar receitas específicas de shell; se alguma permanecer, declarar e verificar seu ambiente.
5. Preservar parágrafos e footers como partes da mensagem, não como fragmentos de código a interpolar.

Saída: procedimento que permita executar C09 e C10 sem expansão de conteúdo e sem deixar artefatos no commit.

### P5 — Alinhar a documentação humana

Requisitos: R1–R5; depende de P1–P4. Tarefa: T05.

1. Atualizar `skills/prepare-commit/README.md` para descrever roteamento condicional, checks derivados do projeto, idioma por destino e transporte seguro condicionado ao host.
2. Remover promessas de autossuficiência do changelog e universalidade do quoting incompatíveis com a implementação.
3. Manter install, triggers e gates sem mudanças não relacionadas.
4. Não escolher nova versão ou anunciar release como parte desta melhoria; manter os campos existentes coerentes entre si.

Saída: README descreve exatamente o contrato implementado, sem duplicar o manual de execução.

### P6 — Verificar o contrato e registrar evidências

Requisitos: R1–R5 e invariantes; depende de P1–P5. Tarefa: T06.

#### Instruções e decisões

Exercitar C01–C08 e C11–C12 com cenários controlados e a skill revisada. Registrar a configuração de cada cenário, a decisão ou ação observada e o resultado esperado. Para seleção de checks, usar configurações mínimas distintas; observar comandos escolhidos, sem depender de instalar todas as stacks listadas na versão antiga.

Uma revisão estática pode confirmar ausência de regras concorrentes, mas não deve ser registrada como execução de um agente. Quando o harness permitir, usar execuções isoladas para observar leitura da referência, seleção de idioma, checks e gates. Registrar o método de verificação empregado e qualquer limitação.

#### Transporte real

- Usar repositório Git descartável fora do projeto, sem remote, sem hooks herdados e com identidade/configuração isoladas. Não alterar a configuração Git do usuário.
- Executar C09 pela API de argumentos diretos disponível ao host.
- Executar C10 pelo método de arquivo, incluindo caminho com espaços e falha controlada do commit.
- Comparar a mensagem gravada com o assunto, corpo e footer esperados, incluindo caracteres especiais e parágrafos. Não confundir o terminador final normalizado pelo Git com corrupção.
- No ambiente Windows, verificar a alternativa pelos PowerShell disponíveis e registrar suas versões. Verificar qualquer outro shell para o qual tenha sido mantido um exemplo específico; caso não esteja disponível, restringir a alegação de compatibilidade.
- Observar que o arquivo temporário não entrou no commit e não permaneceu após sucesso ou falha. Remover o repositório descartável ao final.

A evidência original de perda de acentos e expansão de `$HOME` já está no parecer. Não é necessário reexecutar os comandos defeituosos para confirmar esse relato; o trabalho aqui é provar a alternativa implementada.

#### Encerramento

Registrar em `tasks.md` os ambientes, cenários, resultados e limitações antes de marcar T06 concluída. Rodar validações documentais existentes que sejam pertinentes e conferir links alterados. Evitar testes permanentes que apenas fixem o texto da skill; manter um teste de regressão somente se exercitar um comportamento observável e seguir a convenção existente.

Saída: C01–C12 com evidência; nenhuma alegação de shell não verificado; requisitos e README coerentes. Não criar commit ou push sem solicitação específica.

## Dependências e riscos

- P1 antecede P2 para que a referência use uma precedência já definida.
- P3 e P4 não dependem semanticamente de P2, mas alteram o mesmo arquivo; a ordem acima evita conflitos de edição.
- A alternativa por arquivo depende de escrita UTF-8 e execução permitidas pelo host. Restrições do host devem ser respeitadas, não contornadas.
- A disponibilidade de shells limita a prova de compatibilidade. Reduzir a promessa ao que foi verificado, sem relatar cenários pendentes como sucesso.
- Durante a implementação, reler os trechos atuais antes de editar: os números de linha do parecer são históricos.
