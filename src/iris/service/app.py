from contextlib import asynccontextmanager
import time
from typing import List, Literal
import uuid

from fastapi import BackgroundTasks, FastAPI, HTTPException
import joblib
import pandas as pd
from pydantic import BaseModel, Field
from ..config import settings
from iris import db


class Features(BaseModel):
    model_config = {"extra": "forbid"}

    sepal_length: float = Field(gt=0)
    sepal_width: float = Field(gt=0)
    petal_length: float = Field(gt=0)
    petal_width: float = Field(gt=0)


class BatchFeatures(BaseModel):
    rows: list[Features] = Field(min_length=1, max_length=1000)


class Prediction(BaseModel):
    # 0 is setosa, 1 is versicolor, 2 is virginica.
    class_predict: Literal[0, 1, 2]

    model_version: str
    request_id: str
    latency_ms: float


@asynccontextmanager
async def lifespan(app: FastAPI):
    bundle = joblib.load(settings.model_path)
    app.state.pipeline = bundle["pipeline"]
    app.state.metadata = bundle["metadata"]
    app.state.version = bundle["metadata"]["model_version"]

    db.init()
    yield
    app.state.pipeline = None


app = FastAPI(title='IRIS', lifespan=lifespan)


@app.get("/health")
def health():
    return {"status": "ok", "model_version": getattr(app.state, "version", "unknown")}


@app.get("/ready")
def ready():
    if getattr(app.state, "pipeline", "None") is None:
        raise HTTPException(status_code=503, detail="Model not loaded")

    return {"status": "ready"}


@app.post('/v1/predict')
def predict(x: Features, bg: BackgroundTasks) -> Prediction:
    t0 = time.perf_counter()
    request_id = str(uuid.uuid4())
    payload = x.model_dump()

    class_predict = app.state.pipeline.predict([list(payload.values())])[0]

    latency_ms = round((time.perf_counter() - t0) * 1000, 2)

    bg.add_task(
        db.save_prediction,
        request_id, payload, class_predict, app.state.version, latency_ms
    )

    return Prediction(
        class_predict=class_predict,
        model_version=app.state.version,
        request_id=request_id,
        latency_ms=latency_ms,
    )


@app.post('/v1/predict/batch')
def batch_predict(x: BatchFeatures, bg: BackgroundTasks) -> List[Prediction]:
    t0 = time.perf_counter()
    payloads = [row.model_dump() for row in x.rows]
    df = pd.DataFrame(payloads)

    classes = app.state.pipeline.predict(df).tolist()

    latency_ms = round((time.perf_counter() - t0) * 1000, 2)

    results = []
    for payload, class_predict in zip(payloads, classes, strict=True):
        request_id = str(uuid.uuid4())
        bg.add_task(
            db.save_prediction, request_id, payload, class_predict, app.state.version, latency_ms,
        )

        results.append(
            Prediction(
                class_predict=class_predict,
                model_version=app.state.version,
                request_id=request_id,
                latency_ms=latency_ms,
            )
        )

    return results
