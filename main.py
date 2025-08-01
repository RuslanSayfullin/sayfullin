from fastapi import FastAPI
from fastapi.responses import HTMLResponse

app = FastAPI()

@app.get("/")
def read_root():
    html_content = "<h2>Привет, Элина!</h2><h3>Как дела?</h3>"
    return HTMLResponse(content=html_content)
