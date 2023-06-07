"""Starting point and sub-paths are defined here"""
from fastapi import FastAPI
from app.routers import users, login, follows


app = FastAPI()
app.include_router(users.router)
app.include_router(login.router)
app.include_router(follows.router)


@app.get('/')
def root():
    """Root path"""
    return { "message": "Welcome to our Twitter Clone! Go to '/docs' for the API documentation." }
