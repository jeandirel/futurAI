from typing import List

from pydantic import BaseModel, Field


class RAGQuery(BaseModel):
    query: str = Field(..., description="Texte de la requete ou du sujet")
    k: int = Field(3, ge=1, le=10, description="Nombre de passages a retourner")
    level: str | None = Field(None, description="Niveau scolaire cible (ex: Master)")
    language: str = Field("fr", description="Langue de generation (fr/en)")


class RAGChunk(BaseModel):
    source: str
    position: int
    text: str


class RAGResponse(BaseModel):
    chunks: List[RAGChunk]
