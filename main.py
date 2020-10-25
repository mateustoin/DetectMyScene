from app.DetectScene import DetectScene
from app.DetectUtils import DetectUtils

from typing import List

from fastapi import FastAPI, File, UploadFile, BackgroundTasks
from fastapi.responses import HTMLResponse

app = FastAPI()

@app.get("/")
async def main():
    """
        Formulário para inserir uma imagem. Chama endpoint /process/ quando enviado.
    """
    content = """
                <body>
                <form action="/process/" enctype="multipart/form-data" method="post">
                <input name="file" type="file">
                <input type="submit">
                </form>
                </body>
            """
    return HTMLResponse(content=content)

def cria_audio(descricao_simples: str, descricao_localizada: str):
    """
        Task background que cria os áudios baseado nas descrições, enquanto
        as mesmas já foram retornadas para quem solicitou.
    """
    DetectUtils.criaAudio(descricao_simples, 'simples')
    DetectUtils.criaAudio(descricao_localizada, 'localizada')

@app.post("/process/")
async def root_post(file: UploadFile = File(...), background_tasks: BackgroundTasks = BackgroundTasks):
    """
        Processa imagem utilizando o DetectScene, com ImageAI.
    """
    detect = DetectScene(await file.read())
    detect.detectaObjetos()
    detect.marcaPonto()
    detect.criaMatrizDistancia()
    detect.marcaLinha()
    descricao_simples = detect.criaDescricaoSimples()
    descricao_localizada = detect.criaDescricaoLocalizada()  
    
    background_tasks.add_task(cria_audio, descricao_simples=descricao_simples, descricao_localizada=descricao_localizada)

    return {"message": "Processamento concluído!",
            "descricaoSimples": descricao_simples,
            "descricaoLocalizada": descricao_localizada}