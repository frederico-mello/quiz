# Tasks

## 1. Remover referências a contexto interno

- [x] 1.1 Em `docs/06-metodologia.md`, trocar a abertura que atribuía a escolha da página a contexto interno por "A pergunta que esta peça responde é:", preservando o restante da frase.
- [x] 1.2 Em `docs/README.md`, na seção Premissas, trocar a justificativa por atribuição pessoal pela escolha editorial "*(escolha editorial)* A metodologia de desenvolvimento ganhou uma página inteira em 06-metodologia.md, por ser a peça que melhor explica como o projeto evolui."
- [x] 1.3 Em `docs/06-metodologia.md`, trocar a menção a hábito pessoal por "quem garante isso é o hábito de quem trabalha no repositório".
- [x] 1.4 Em `docs/06-metodologia.md`, trocar a menção a quem vê o erro antes do merge por "Se falhar, o erro aparece antes de a proposta ser mergeada (unida) ao código."
- [x] 1.5 Em `docs/06-metodologia.md`, trocar a menção a envio direto na branch principal por "O push-review cobre o caminho que a revisão de proposta não vê: mudanças enviadas direto para a branch principal."
- [x] 1.6 Em `docs/01-visao-geral.md`, nas inferências, trocar a fundamentação do perfil do público em contexto não registrado no repositório por "o perfil do público é suposição sem registro no repositório."
- [x] 1.7 Varrer todo `docs/` e `README.md` da raiz por dono, pediu/pedido interno (mantendo pedidos ao modelo/LLM que sejam técnicos), prioridade declarada, colega, insumo, conversa interna, contexto do projeto, mantenedor pessoal e hábitos pessoais; corrigir com edição mínima, preservando o sentido técnico e distinguindo fato de inferência.

## 2. Atualizar afirmações documentais verificáveis

- [x] 2.1 Em `docs/06-metodologia.md`, explicar que o cron `0 6 * * 1` executa às 6h UTC (3h em Brasília).
- [x] 2.2 Na seção Higienizar de `docs/06-metodologia.md`, substituir a afirmação de causa indeterminada pela causa verificada: o workflow fixa `repository-hygiene==0.2.0`, que lê o bloco `regras:` (português), enquanto `auditoria.yaml` usa `rules:` (inglês) desde a alteração registrada em 2026-07-26; sem regras carregadas a auditoria termina com sucesso sem examinar arquivos, explicando a ausência de alertas dos links mortos do README. Registrar que repinar para a linha 1.x restaura o funcionamento da auditoria.
- [x] 2.3 Em `docs/07-pesquisa-e-fontes.md`, registrar que `lappquiz.ict.unesp.br` respondeu HTTP 200 com a página do Streamlit, sem alegar inspeção visual em navegador.
- [x] 2.4 Recontar no repositório as specs e linhas, changes arquivadas, commits e arquivos/testes da suíte; atualizar a tabela final e verificações em `docs/06-metodologia.md` e atualizar em `docs/README.md` a revisão lida para `d53b80e`.

## 3. Conferir aderência ao requisito

- [x] 3.1 Revisar `docs/` e o README da raiz para confirmar que o texto publicado não expõe pedidos, prioridades declaradas, conversas internas ou preferências pessoais, e que afirmações sobre o projeto decorrem do código, histórico, fonte citada ou estão marcadas como `(inferência)`.

## 4. Manutenção da superfície pública (2026-10-06)

- [x] 4.1 Reescrever as tarefas 1.1 a 1.6 deste arquivo sem citar na íntegra as frases removidas, para que o próprio registro da limpeza não reintroduza o conteúdo que ela remove.
- [x] 4.2 Em `docs/README.md`, atualizar a revisão lida de `d53b80e` para `69e214e`.
- [x] 4.3 Em `docs/06-metodologia.md`, atualizar as contagens para o estado de `69e214e`: 10 specs (449 linhas) e 9 mudanças arquivadas; manter a tabela de verificações coerente (138 commits, 135 até a revisão anterior).
