"""Starting point and sub-paths are defined here"""
from fastapi import FastAPI
from app.routers import users, login, tweets, likes, comments

app = FastAPI()
app.include_router(users.router)
app.include_router(login.router)
app.include_router(follows.router)
app.include_router(tweets.router)
app.include_router(likes.router)
app.include_router(comments.router)



@app.get('/')
def root():
    """Root path"""
    return { "message": "Welcome to our Twitter Clone! Go to '/docs' for the API documentation." }
