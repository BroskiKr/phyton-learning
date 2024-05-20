from fastapi import FastAPI
import psycopg2
from .database import engine
from .routers import user,post,auth,googleAuth
from fastapi.middleware.cors import CORSMiddleware


app = FastAPI() 

origins=["*"]
app.add_middleware(
    CORSMiddleware,
    allow_origins=origins,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# models.Base.metadata.create_all(bind=engine)

app.include_router(post.router)
app.include_router(user.router)
app.include_router(auth.router)
app.include_router(googleAuth.router)


@app.get('/') 
def read_root(): 
  return 'Home' 

