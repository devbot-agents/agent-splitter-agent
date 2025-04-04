from fastapi import FastAPI, HTTPException
from app.controllers.agent_controller import router as agent_router
import os

app = FastAPI(
    title="Agent Splitter Agent",
    description="Divide a funcionalidade de um agente principal em microagentes com responsabilidades únicas e comunicação clara entre eles",
    version="0.1.0"
)

# Incluir routers
app.include_router(agent_router)

@app.get("/health")
async def health_check():
    """
    Endpoint para verificação de saúde da API.
    """
    return {"status": "healthy"} 