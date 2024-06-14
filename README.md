# Avaliação

## Criar o ambiente virtual

Na raiz do serviço principal:

```
python -m venv venv
cd venv/Scripts
activate
cd ..
cd ..
pip freeze > requirements.txt
```

## Rodando o projeto

Para instalar as dependências e rodar os serviços só é necessário rodar o docker compose up no src:

```
docker compose up
```