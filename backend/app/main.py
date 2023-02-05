from fastapi import FastAPI, Depends
import oauth2
import models
from database import engine
from fastapi.middleware.cors import CORSMiddleware

import uvicorn
from fastapi import FastAPI
import uvicorn
from superuser import create_superuser
from routers import login, schools,roles,users


app = FastAPI()

origins=["*"]

app.add_middleware(CORSMiddleware,
                    allow_origins=origins,
                    allow_credentials=True,
                    allow_methods=["*"],
                    allow_headers=["*"],
                    )

app.include_router(login.router)
app.include_router(schools.router)
app.include_router(roles.router)
app.include_router(users.router)

@app.get("/ping")
def read_root():
    return {"response": "Test complete and ping Sucessful"}

@app.get("/test")
async def test( current_user: str = Depends(oauth2.get_current_user)):
    print(current_user)
    return {"got": "details"}


if __name__ == "__main__":
    models.Base.metadata.create_all(bind=engine)
    # create_superuser()
    uvicorn.run("main:app", reload = True)
    
    
