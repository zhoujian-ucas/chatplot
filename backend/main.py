from fastapi import FastAPI, HTTPException, WebSocket, UploadFile, File
from fastapi.middleware.cors import CORSMiddleware
import uvicorn
import json
import asyncio
import logging
from typing import Dict, List, Optional
import requests
from services.ollama_service import OllamaService
from services.data_service import DataService
from services.visualization_service import VisualizationService
from utils.helpers import parse_data_request, validate_data, suggest_visualizations
from models.database import init_db
import tempfile
from pathlib import Path

# Configure logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

app = FastAPI(title="ChatPlot API")

# Initialize services
ollama_service = OllamaService()
data_service = DataService()
visualization_service = VisualizationService()

# Initialize database
engine = init_db()

# Configure CORS
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],  # In production, replace with specific origins
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

class ChatManager:
    def __init__(self):
        self.active_connections: Dict[str, WebSocket] = {}

    async def connect(self, websocket: WebSocket, client_id: str):
        await websocket.accept()
        self.active_connections[client_id] = websocket
        logger.info(f"Client {client_id} connected")

    def disconnect(self, client_id: str):
        self.active_connections.pop(client_id, None)
        logger.info(f"Client {client_id} disconnected")

    async def send_message(self, client_id: str, message: str):
        if client_id in self.active_connections:
            await self.active_connections[client_id].send_text(message)

chat_manager = ChatManager()

@app.get("/")
async def root():
    return {"message": "ChatPlot API is running"}

@app.websocket("/ws/{client_id}")
async def websocket_endpoint(websocket: WebSocket, client_id: str):
    await chat_manager.connect(websocket, client_id)
    try:
        while True:
            data = await websocket.receive_text()
            try:
                # Parse the data request
                request = parse_data_request(data)
                
                # Get response from Ollama
                response = await ollama_service.generate_response(
                    prompt=data,
                    system_prompt="You are a helpful data analysis assistant. Help users analyze their data and provide insights."
                )
                
                await chat_manager.send_message(client_id, response["response"])
            except Exception as e:
                logger.error(f"Error processing message: {str(e)}")
                await chat_manager.send_message(
                    client_id,
                    f"Error processing message: {str(e)}"
                )
    except Exception as e:
        logger.error(f"WebSocket error: {str(e)}")
    finally:
        chat_manager.disconnect(client_id)

@app.post("/api/analyze")
async def analyze_data(file: UploadFile = File(...)):
    try:
        # Create a temporary file to store the uploaded data
        with tempfile.NamedTemporaryFile(delete=False, suffix=Path(file.filename).suffix) as temp_file:
            content = await file.read()
            temp_file.write(content)
            temp_file_path = temp_file.name

        # Load and validate the data
        data = data_service.load_data(temp_file_path)
        validation_result = validate_data(data)
        
        if not validation_result["is_valid"]:
            raise HTTPException(
                status_code=400,
                detail=f"Invalid data: {validation_result['issues']}"
            )

        # Get data summary
        data_summary = data_service.get_data_summary(data)

        # Get visualization suggestions
        viz_suggestions = suggest_visualizations(data)

        # Generate analysis with Ollama
        analysis_prompt = f"""
        Analyze the following data:
        Summary: {json.dumps(data_summary)}
        Suggested visualizations: {json.dumps(viz_suggestions)}
        
        Provide insights and recommendations.
        """
        
        analysis_result = await ollama_service.analyze_data(analysis_prompt)

        # Create visualization
        viz_result = visualization_service.analyze_and_visualize(data, analysis_result)

        return viz_result

    except Exception as e:
        logger.error(f"Error analyzing data: {str(e)}")
        raise HTTPException(status_code=500, detail=str(e))
    finally:
        # Clean up temporary file
        if 'temp_file_path' in locals():
            Path(temp_file_path).unlink(missing_ok=True)

if __name__ == "__main__":
    uvicorn.run("main:app", host="0.0.0.0", port=8000, reload=True) 