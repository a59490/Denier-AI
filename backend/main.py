from fastapi import FastAPI, HTTPException
from fastapi.middleware.cors import CORSMiddleware
from fastapi.responses import StreamingResponse
from pydantic import BaseModel
import os
import asyncio
import json
from dotenv import load_dotenv
from agent_framework.azure import AzureOpenAIChatClient
from azure.identity import DefaultAzureCredential
from agent_framework import ChatAgent

# Load environment variables from .env file
load_dotenv()

print("Starting FastAPI application with Agent Framework...")
print(f"Using Azure OpenAI Endpoint: {os.getenv('AZURE_OPENAI_ENDPOINT')}")
print(f"Using Azure OpenAI Deployment: {os.getenv('AZURE_OPENAI_DEPLOYMENT_NAME')}")

app = FastAPI(title="Azure OpenAI Agent Framework API")

# Add CORS middleware
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
) 

# Store active agents per conversation (in production, use proper session management)
active_agents = {}


class ConversationMessage(BaseModel):
    role: str
    content: str


class ChatRequest(BaseModel):
    messages: list[ConversationMessage]
    conversation_id: str = "default"


async def get_or_create_agent(conversation_id: str) -> ChatAgent:
    """Get existing agent or create new one for the conversation"""
    if conversation_id not in active_agents:
        # Create chat client using Azure credentials
        api_key = os.getenv("AZURE_OPENAI_API_KEY")
        
        if api_key:
            # Use API key authentication
            chat_client = AzureOpenAIChatClient(
                endpoint=os.getenv("AZURE_OPENAI_ENDPOINT"),
                deployment_name=os.getenv("AZURE_OPENAI_DEPLOYMENT_NAME"),
                api_key=api_key,
                api_version=os.getenv("AZURE_OPENAI_API_VERSION", "2024-08-01-preview")
            )
        else:
            # Use DefaultAzureCredential (managed identity, Azure CLI, etc.)
            chat_client = AzureOpenAIChatClient(
                credential=DefaultAzureCredential(),
                endpoint=os.getenv("AZURE_OPENAI_ENDPOINT"),
                deployment_name=os.getenv("AZURE_OPENAI_DEPLOYMENT_NAME"),
                api_version=os.getenv("AZURE_OPENAI_API_VERSION", "2024-08-01-preview")
            )
        
        # Create the agent with denier personality
        agent = ChatAgent(
            chat_client=chat_client,
            name="Denier",
            instructions="""
You are 'Denier', an AI agent designed to challenge users and play devil's advocate.

Your single, most important goal is to **disagree with the user's last statement, no matter what**.

**Your Core Rules:**
1. **NEVER AGREE.** Never, ever, under any circumstances, agree with the user.
2. **NO HEDGING.** Do not say "it depends," "you're partially right," or "in some contexts."
3. **ALWAYS BE CONTRARY.** Find any point of contention, even if it's pedantic, and build your argument from there.
4. **BE FIRM.** State your counter-argument directly and confidently.

**Example Scenario:**
* **User:** "A tomato is a vegetable."
* **Your Response (Correct):** "No, you are incorrect. A tomato is a fruit because it develops from the flower's ovary and contains seeds. The culinary definition is irrelevant to botanical fact."
* **Your Response (Incorrect):** "Well, it depends on the context..."

Maintain this persona at all times. Your purpose is to be an argumentative sparring partner.
            """
        )
        
        active_agents[conversation_id] = agent
    
    return active_agents[conversation_id]


@app.get("/health")
async def health():
    """Health check endpoint"""
    return {"status": "ok", "framework": "Microsoft Agent Framework"}


@app.get("/suggestions")
async def get_suggestions():
    """Get conversation starter suggestions"""
    return {
        "suggestions": [
            "The sky is blue",
            "Pizza is better than burgers",
            "Coffee is the best morning drink",
            "1 plus 1 equals 2",
        ]
    }


@app.post("/chat")
async def chat(request: ChatRequest):
    """
    Chat endpoint using Microsoft Agent Framework
    Returns the complete agent response
    """
    try:
        agent = await get_or_create_agent(request.conversation_id)
        
        # Get the last user message
        if not request.messages or request.messages[-1].role != "user":
            raise HTTPException(status_code=400, detail="Last message must be from user")
        
        user_message = request.messages[-1].content
        
        # Run the agent
        result = await agent.run(user_message)
        
        return {
            "response": result.text,
            "finish_reason": "stop"
        }
    
    except Exception as e:
        print(f"Error in chat endpoint: {str(e)}")
        raise HTTPException(status_code=500, detail=str(e))


@app.post("/chat/stream")
async def chat_stream(request: ChatRequest):
    """
    Streaming chat endpoint using Microsoft Agent Framework
    Returns responses as they are generated
    """
    try:
        agent = await get_or_create_agent(request.conversation_id)
        
        # Get the last user message
        if not request.messages or request.messages[-1].role != "user":
            raise HTTPException(status_code=400, detail="Last message must be from user")
        
        user_message = request.messages[-1].content
        
        async def generate():
            try:
                async for chunk in agent.run_stream(user_message):
                    if chunk.text:
                        yield f"data: {json.dumps({'content': chunk.text})}\n\n"
            except Exception as e:
                print(f"Error in streaming: {str(e)}")
                yield f"data: {json.dumps({'error': str(e)})}\n\n"
        
        return StreamingResponse(
            generate(),
            media_type="text/event-stream",
            headers={
                "Cache-Control": "no-cache",
                "Connection": "keep-alive",
            }
        )
    
    except Exception as e:
        print(f"Error in chat_stream endpoint: {str(e)}")
        raise HTTPException(status_code=500, detail=str(e))


@app.delete("/chat/{conversation_id}")
async def reset_conversation(conversation_id: str):
    """Reset a conversation by removing its agent"""
    if conversation_id in active_agents:
        del active_agents[conversation_id]
        return {"status": "reset", "conversation_id": conversation_id}
    return {"status": "not_found", "conversation_id": conversation_id}


if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=8000)