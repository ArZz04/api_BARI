from fastapi import FastAPI
from routers import users, jwt_auth_users, product, get_info, refreshtoken

from mangum import Mangum

app = FastAPI()
handler = Mangum(app)

app.include_router(users.router)
app.include_router(jwt_auth_users.router)
app.include_router(product.router)
app.include_router(get_info.router)
app.include_router(refreshtoken.router)


@app.get("/")
async def root():
    return "API works correctly"

@app.get("/info")
async def url():
    return {'INICIAR SERVIDOR' : "uvicorn main:app --reload"}

#pip3 install -t dep -r requirements.txt    
#(cd dep; zip ../lambda_artifact.zip -r .) 
#zip -r lambda_artifact.zip -u main.py routers db