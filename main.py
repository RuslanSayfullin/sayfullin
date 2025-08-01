from fastapi import FastAPI
from fastapi.responses import HTMLResponse

app = FastAPI(title="Auth", version="1.0.0")

@app.get("/")
def read_root():
    html_content = "<h2>Hello, World!</h2>"
    return HTMLResponse(content=html_content)
