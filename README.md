# Acervo — C01

Solução de referência do laboratório de cancelamento do livro *Trabalhando com agentes de IA*. O projeto usa Python 3.13, Django 5.2.19 e PostgreSQL 18.7. Você precisa de Git e Docker com Compose, com o serviço do Docker em execução.

Dentro da pasta do Acervo, execute:

```sh
docker compose up -d --build --wait
docker compose exec web python manage.py migrate
docker compose exec web python manage.py dados_demo
docker compose exec web python manage.py test
```

Abra http://127.0.0.1:8000. Entre como `ana` ou `bruno`, com a senha `acervo-demo`. Ana tem um projetor reservado para o futuro e um notebook no passado. Bruno tem uma reserva futura de notebook. A lista mostra apenas as reservas da conta ativa. O catálogo mostra os dois equipamentos.

Os horários aparecem em UTC. O comando `dados_demo` mantém as reservas já criadas. Use uma pasta com nome diferente para executar outro checkpoint em paralelo e escolha uma porta livre com `ACERVO_PORT`. Por exemplo, com Bash ou Zsh:

```sh
ACERVO_PORT=8001 docker compose up -d --build --wait
```

Para parar os serviços preservando o banco, execute `docker compose down`. Para recomeçar com o banco vazio, execute `docker compose down --volumes` **na pasta do laboratório** e repita a preparação. Esse comando apaga os dados locais do projeto Compose.

## Conferir o cancelamento

Entre como Ana e use Tab até o botão **Cancelar reserva de Projetor**. Pressione Enter. A mensagem de confirmação deve aparecer e a reserva deve continuar na lista como **Cancelada**. A reserva do passado não tem botão. Ao entrar como Bruno, você verá apenas as reservas dessa conta.

A suíte automatizada também verifica a regra no servidor, o instante exato do início, a preservação do mesmo registro e a repetição da solicitação. Rode `docker compose exec web python manage.py test` para conferir.
