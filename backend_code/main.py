from fastapi import FastAPI, HTTPException
from fastapi.middleware.cors import CORSMiddleware
import uvicorn
from app.routers import zones, simulation, chatops, analytics, chat
from app.core.config import settings

app = FastAPI(
    title="PlantOps Digital Twin API",
    description="Backend API for Digital Twin Dashboard with watsonx Orchestrate",
    version="2.0.0"
)

# CORS middleware
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Include routers
app.include_router(zones.router, prefix="/api", tags=["zones"])
app.include_router(simulation.router, prefix="/api", tags=["simulation"])
app.include_router(chatops.router, prefix="/api", tags=["chatops"])
app.include_router(analytics.router, prefix="/api", tags=["analytics"])
app.include_router(chat.router, prefix="/api", tags=["chat"])

@app.get("/")
async def root():
    return {
        "message": "PlantOps Digital Twin API",
        "version": "2.0.0",
        "docs": "/docs"
    }

@app.get("/health")
async def health_check():
    return {"status": "healthy", "service": "PlantOps Digital Twin API"}

if __name__ == "__main__":
    uvicorn.run(
        "main:app",
        host="0.0.0.0",
        port=8000,
        reload=True
    )
