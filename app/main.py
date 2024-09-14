from fastapi import FastAPI
from app.routers import user, post, auth, googleAuth, generating_posts
from fastapi.middleware.cors import CORSMiddleware


app = FastAPI()

origins = ["*"]
app.add_middleware(
    CORSMiddleware,
    allow_origins=origins,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
    expose_headers=["x-total-count"],
)


app.include_router(post.router)
app.include_router(user.router)
app.include_router(auth.router)
app.include_router(googleAuth.router)
app.include_router(generating_posts.router)


@app.get("/")
def read_root():
    return "Home"
