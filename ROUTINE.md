# Rotina diária de posts · @uselexia.ai

Procedimento que cada execução diária segue, do início ao fim. Ler junto com `brand/BRAND.md`.

## Configuração

| Item | Valor |
|---|---|
| Repositório | `ArthurPimenta02/lexia-media` (público), branch `main` |
| Metricool blogId | `7297517` |
| Fuso | `America/Sao_Paulo` |
| Horários | post A às **08:00**, post B às **18:00** (mesmo dia da execução) |
| Link público das imagens | `https://raw.githubusercontent.com/ArthurPimenta02/lexia-media/main/<caminho>` |

## Passos

1. **Ler o contexto**: `brand/BRAND.md`, os templates em `templates/` e as últimas 20 linhas de `posts/LOG.md`.
2. **Escolher os 2 posts do dia**:
   - nichos diferentes entre si e diferentes dos 2 últimos dias;
   - formatos diferentes entre si e diferentes do post anterior;
   - pelo menos 1 imagem única por dia; carrossel no máximo 1 por dia;
   - nenhum gancho repetido do LOG.
3. **Criar as artes** em HTML, uma página por slide, em `posts/AAAA-MM-DD-am/src/01.html`, `02.html`… e `posts/AAAA-MM-DD-pm/src/…`, seguindo o estilo dos templates (logos via `ASSETS/…`).
4. **Exportar**: `python3 tools/render.py posts/AAAA-MM-DD-am/src posts/AAAA-MM-DD-am` (idem para `pm`).
5. **Revisar visualmente** o `_sheet.jpg` de cada post: texto cortado, sobreposição indesejada, elemento cobrindo texto, contraste. Corrigir e exportar de novo até ficar limpo.
6. **Publicar as imagens no GitHub**: `git add`, commit, `git push`. Conferir que cada link raw responde 200 com `image/jpeg`.
7. **Agendar no Metricool** com `createScheduledPost` (autoPublish true, provider instagram, type POST, `media` com os links raw na ordem dos slides, `mediaAltText`, legenda seguindo o BRAND.md).
8. **Confirmar** com `getScheduledPosts` que os 2 posts estão na fila com status pendente.
9. **Registrar** os 2 posts em `posts/LOG.md` (data, horário, formato, nicho, gancho) e fazer push.
10. **Resumo final**: os 2 ganchos, formato e nicho de cada um e os links do planner do Metricool.

## Se algo der errado

- Exportação falhou ou ficou feia e não dá pra corrigir: troca o post por outro mais simples (imagem única) em vez de publicar algo quebrado.
- Push ou Metricool falhou: não repetir em loop. Tentar uma vez de novo; se falhar, encerrar e dizer exatamente o que falhou no resumo.
- Horário já passou (execução atrasada): agendar o post da manhã para 1 hora depois do horário atual e manter o das 18:00.
