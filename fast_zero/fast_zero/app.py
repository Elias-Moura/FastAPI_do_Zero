from fastapi import FastAPI
from starlette.responses import HTMLResponse

from fast_zero.schemas import Message

app = FastAPI()


@app.get('/', status_code=200, response_model=Message)
def read_root():
    return {'message': 'Olá Mundo!'}


@app.get('/html', status_code=200, response_class=HTMLResponse)
def hw_html():
    return '<h1>Hello World!</h1>'
