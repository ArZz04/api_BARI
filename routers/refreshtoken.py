from fastapi import APIRouter, Depends, HTTPException, status
from pydantic import BaseModel
from fastapi.security import OAuth2PasswordBearer, OAuth2PasswordRequestForm
from jose import jwt, JWTError
from passlib.context import CryptContext
from datetime import datetime, timedelta
from fastapi.security import HTTPBearer

from db.client import db_client
from db.models.user import User, UserDB
from db.schemas.user import user_schema, users_schema

ACCESS_TOKEN_DURATION = 20
SECRET_KEY = "$2y$10$eDExHEG0GSWUvXhoxWovM./wsJS38BHu69l3qouX3zKNDGdqp7pve" #karlita 2 times
ALGORITHM = "HS256"

oauth2 = OAuth2PasswordBearer(tokenUrl='login')
crypt = CryptContext(schemes=["bcrypt"])

router = APIRouter()

async def auth_user(token: str):

    exception = HTTPException(
        status_code=status.HTTP_401_UNAUTHORIZED,
        detail="Credenciales de autenticación inválidas",
        headers={"WWW-Authenticate": "Bearer"})

    try:
        payload = jwt.decode(token, SECRET_KEY, algorithms=[ALGORITHM])
        if payload is None:
            raise exception

    except JWTError:
        raise exception

    return payload["sub"]



@router.get("/refresh", status_code=status.HTTP_200_OK)
async def refresh_token(token: str = Depends(oauth2)):
    # Verificar que el token de autorización es válido y ha sido firmado por el servidor de la aplicación.
    payload = await auth_user(token)

    # Buscar el usuario en la base de datos utilizando el ID almacenado en el token.
    user = search_user_(payload)

    # Generar un nuevo token de acceso utilizando la información del usuario y la clave secreta.
    access_token = generate_access_token(user)
    role_user = user.role

    # Devolver el nuevo token de acceso como respuesta.
    return {"access_token": access_token, "role": role_user}

def search_user_(username: str):
    user_dict = db_client.users.find_one({"username": username})
    if user_dict:
        return User(**user_dict)

def generate_access_token(user: User) -> str:
    # Definir el tiempo de expiración del token.
    expires_delta = 9

    # Definir los datos que se incluirán en el token.
    payload = {
        "sub": user.username,
        "exp": datetime.utcnow() + timedelta(seconds=expires_delta),
        "pass": "0000"
    }

    # Generar el token utilizando la clave secreta y el algoritmo especificado.
    access_token = jwt.encode(payload, SECRET_KEY, algorithm=ALGORITHM)

    # Devolver el token generado.
    return access_token

