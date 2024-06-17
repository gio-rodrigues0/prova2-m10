from fastapi import FastAPI, HTTPException
from logging_config import LoggerSetup
import logging
from typing import List
from schema import User

# Cria um logger raiz
logger_setup = LoggerSetup()

# Adiciona o logger para o módulo
LOGGER = logging.getLogger(__name__)

app = FastAPI()

users: List[User] = []

@app.post("/users/", response_model=User)
def create_user(user: User):
    users.append(user)
    LOGGER.info("Usuário adicionado com sucesso")
    return user

@app.get("/users/", response_model=List[User])
def read_users():
    LOGGER.info("Retornando lista de usuários")
    return users

@app.get("/users/{user_id}", response_model=User)
def read_user(user_id: int):
    for user in users:
        if user.id == user_id:
            LOGGER.info(f"Usuário de id {user_id} encontrado")
            return user
    LOGGER.error(f"Usuário de id {user_id} não encontrado")
    raise HTTPException(status_code=404, detail="User not found")

@app.put("/users/{user_id}", response_model=User)
def update_user(user_id: int, updated_user: User):
    for index, user in enumerate(users):
        if user.id == user_id:
            users[index] = updated_user
            LOGGER.info(f"Usuário de id {user_id} atualizado")
            return updated_user
    LOGGER.error(f"Não foi possível atualizar o usuário de id {user_id}")
    raise HTTPException(status_code=404, detail="User not found")

@app.delete("/users/{user_id}", response_model=User)
def delete_user(user_id: int):
    for index, user in enumerate(users):
        if user.id == user_id:
            deleted_user = users.pop(index)
            LOGGER.info(f"Usuário de id {user_id} deletado com sucesso")
            return deleted_user
    LOGGER.error(f"Não foi possível deletar o usuário de id {user_id}")
    raise HTTPException(status_code=404, detail="User not found")
