from fastapi import FastAPI
import app.models
from app.db.database import engine

# Cria as tabelas do BD caso não existam
models.Base.metadata.create_all(bind=engine)

app = FastAPI()