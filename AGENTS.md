# Acervo

- O projeto usa Django, templates HTML e PostgreSQL no Docker Compose.
- As rotas ficam em `acervo/urls.py`. O domínio, as telas e os testes ficam em `reservas/`.
- A pessoa que lê o livro pode ter mudanças locais. Confira `git status --short` e preserve essas mudanças.
- Com os serviços já preparados, a pessoa leitora pode rodar `docker compose exec web python manage.py test` no terminal. Informe quais verificações você executou e quais ficaram pendentes.
- Trabalhe com os dados sintéticos do laboratório.
