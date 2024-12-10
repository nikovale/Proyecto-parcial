from http.client import HTTPException
from fastapi import FastAPI, Response # type: ignore
from starlette.status import HTTP_200_OK,HTTP_201_CREATED,HTTP_204_NO_CONTENT,HTTP_401_UNAUTHORIZED # type: ignore
from model.user_connection import UserConnection
from schema.users_schema import LoginRequest, UsersSchema
#(venv) docente@TUL-9D399114:~/Escritorio/Niko/Proyecto-parcial$ 
#source venv/bin/activate
#uvicorn main:app --reload
#from:source .venv/bin/activate 
#from:reflex run

app = FastAPI()
conn = UserConnection()

@app.get("/", status_code=HTTP_200_OK)
def root():
    items = []
    for data in conn.read_all():
       dictionary = {}
       dictionary["id"] = data[0]
       dictionary["full_name"] = data[2]
       dictionary["phone"] = data[3]
       items.append(dictionary)
    return items

@app.get("/api/users/{id}",status_code=HTTP_200_OK)
def get_one(id: str):
    dictionary = {}
    data = conn.read_one(id)
    dictionary["id"] = data[0]
    dictionary["full_name"] = data[2]
    dictionary["phone"] = data[3]
    return dictionary


@app.post("/api/insert_users",status_code=HTTP_201_CREATED)
def insert(users_data: UsersSchema):
    data= users_data.dict()
    conn.write(data)
    return Response(status_code=HTTP_201_CREATED)


@app.put("/api/update/{id}", status_code=HTTP_204_NO_CONTENT)
def update(users_data:UsersSchema, id:str):
    data = users_data.dict()
    data["id"] = id
    conn.update(data)
    return Response(status_code=HTTP_204_NO_CONTENT)

@app.delete("/api/delete/{id}",status_code=HTTP_204_NO_CONTENT)
def delete(id:str):
    conn.delete(id)
    return Response(status_code=HTTP_204_NO_CONTENT)

@app.post("/api/login", status_code=HTTP_200_OK)
def login(request: LoginRequest):
    try:
        # Buscar el usuario por correo y contraseña
        user = conn.read_by_email_and_password(request.correo, request.password)

        # Verificar si el usuario existe
        if user:
            # Imprimir la información del usuario
            print(f"Usuario encontrado: ID={user['id']}")

            # Devolver solo el ID del usuario en la respuesta
            return {
                "message": "Login successful",
                "user": {
                    "id": user['id']
                }
            }

        # Si no pasa la validación, lanzar excepción
        raise HTTPException(
            status_code=HTTP_401_UNAUTHORIZED,
            detail="Invalid correo or password"
        )
    except Exception as e:
        print(f"Error al intentar iniciar sesión: {e}")
        raise HTTPException(status_code=HTTP_401_UNAUTHORIZED, detail="Error during login process")