from fastapi import FastAPI

app = FastAPI()

@app.get('/')
def root():
    return { "message": "Welcome to our Twitter Clone!" }