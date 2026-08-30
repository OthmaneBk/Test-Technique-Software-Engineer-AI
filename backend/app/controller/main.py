import sys
from pathlib import Path
import pandas as pd 
from fastapi import FastAPI, File, HTTPException, UploadFile
from io import BytesIO
from fastapi.middleware.cors import CORSMiddleware
from typing import Callable
sys.path.insert(0, str(Path(__file__).resolve().parents[1] / "ai" / "services"))
from mcp_client import MCP_CLIENT
from intent import is_show_all_intent 

sys.path.insert(0, str(Path(__file__).resolve().parents[1] / "ai" / "model"))
from AskResponse import AskResponse
from AskRequest import AskRequest
import inspect

sys.path.insert(0, str(Path(__file__).resolve().parents[1] / "data" / "services"))
from loader import DatasetLoader
from generate_dataset import DatasetGenerator
datasetloader = DatasetLoader()
DATA = None
sys.path.insert(0, str(Path(__file__).resolve().parents[1] / "ai" / "services"))
from history import HistoryStore
HISTORY = HistoryStore()

from typing import Any

DATASET_PATH = Path(__file__).resolve().parents[1] / "data" / "storage" / "data.csv"

app = FastAPI(title="Predylics - Mini App d'analyse de données")

app.add_middleware(
    CORSMiddleware,
    allow_origins=["http://localhost:5173"],
    allow_methods=["GET", "POST"],
    allow_headers=["*"],
)

@app.on_event("startup")
async def on_startup() -> None:
    global DATA
     

@app.on_event("shutdown")
async def on_shutdown() -> None:
    HISTORY.clear()

async def refactor_body(func: Callable, erreur: str) -> any:
    try:
        result = func()
        if inspect.isawaitable(result):
            result = await result
        return result
    except Exception as e:
        raise HTTPException(status_code=400, detail=f"{erreur} : {e}")

@app.get("/data")
async def get_data() -> list[dict]:
    def _get_data():
        DATA = datasetloader.load()
        if DATA is None:
            raise ValueError("Données non chargées")
        return DATA.to_dict(orient="records")

    return await refactor_body(_get_data, erreur="Données chargées incorrectement")


@app.post("/ask", response_model=AskResponse)
async def ask(request: AskRequest) -> AskResponse:
    async def _ask():
        history = HISTORY.load()
        if is_show_all_intent(request.question):
            return AskResponse(action="SHOW_ALL_DATA")
        answer = await MCP_CLIENT().ask(request.question, history)
        HISTORY.append(request.question, answer)
        return AskResponse(answer=answer)
    return await refactor_body(_ask, erreur="Erreur lors de la question")


@app.post("/import/file")
async def import_file(file: UploadFile = File(...)) -> dict:
    content = await file.read()

    def _import_file():
        global DATA
        df = pd.read_csv(BytesIO(content),sep=r"[,;\t]", engine="python")
        df.to_csv(DATASET_PATH, index=False)
        return {"data": df.to_dict(orient="records")}
    HISTORY.clear()
    return await refactor_body(_import_file, erreur="Fichier CSV invalide")


@app.get("/generatefile")
async def generatefile() -> Any: 
    global DATA
    HISTORY.clear()
    response = await refactor_body(DatasetGenerator().run,erreur="Erreur lors de la génération du dataset :")
    return response