import os
import requests
from fastapi import APIRouter, HTTPException
from pydantic import BaseModel
from dotenv import load_dotenv

load_dotenv()

router = APIRouter()

class ChatRequest(BaseModel):
    message: str

class ChatResponse(BaseModel):
    response: str
    status: str = "success"

# Watson Orchestrate configuration
AGENT_ID = os.getenv("AGENT_ID")
TOKEN_ENDPOINT = os.getenv("TOKEN_ENDPOINT")
API_KEY = os.getenv("API_KEY")
YOUR_INSTANCE_URL = os.getenv("YOUR_INSTANCE_URL")

def get_access_token():
    """Get IBM Cloud IAM access token"""
    headers = {
        "Content-Type": "application/x-www-form-urlencoded",
    }
    data = {
        "grant_type": "urn:ibm:params:oauth:grant-type:apikey",
        "apikey": API_KEY,
    }
    
    response = requests.post(TOKEN_ENDPOINT, headers=headers, data=data)
    if response.status_code == 200:
        return response.json()["access_token"]
    else:
        raise Exception(f"Failed to get access token: {response.text}")

@router.post("/chat", response_model=ChatResponse)
async def chat_with_agent(request: ChatRequest):
    """
    Chat with Watson Orchestrate agent
    Agent ID is fixed in environment variables
    """
    try:
        # Get access token
        access_token = get_access_token()
        
        # Prepare the request to Watson Orchestrate
        endpoint = f"{YOUR_INSTANCE_URL}/v1/agents/{AGENT_ID}/runs"
        
        headers = {
            "Authorization": f"Bearer {access_token}",
            "Content-Type": "application/json",
        }
        
        payload = {
            "input": {
                "message": request.message
            }
        }
        
        # Call Watson Orchestrate agent
        response = requests.post(endpoint, headers=headers, json=payload)
        
        if response.status_code == 200 or response.status_code == 201:
            result = response.json()
            
            # Extract the agent's response
            agent_response = result.get("output", {}).get("message", "I received your message but couldn't generate a response.")
            
            # Alternative paths for response extraction
            if not agent_response or agent_response == "I received your message but couldn't generate a response.":
                # Try different response structures
                if "result" in result:
                    agent_response = result["result"]
                elif "response" in result:
                    agent_response = result["response"]
                elif "output" in result and isinstance(result["output"], str):
                    agent_response = result["output"]
            
            return ChatResponse(
                response=agent_response,
                status="success"
            )
        else:
            raise HTTPException(
                status_code=response.status_code,
                detail=f"Watson Orchestrate API error: {response.text}"
            )
            
    except Exception as e:
        raise HTTPException(
            status_code=500,
            detail=f"Error communicating with Watson Orchestrate: {str(e)}"
        )
