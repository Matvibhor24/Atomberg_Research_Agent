from fastapi import FastAPI, HTTPException
from fastapi.responses import StreamingResponse
from pydantic import BaseModel
from typing import List, Optional
from main import run_pipeline, run_pipeline_server, run_pipeline_server_with_progress
from config import get_keywords, API_TITLE
import json
import asyncio

from dotenv import load_dotenv
import os

load_dotenv()

from fastapi.middleware.cors import CORSMiddleware

app = FastAPI(title=API_TITLE)
app.add_middleware(
    CORSMiddleware,
    allow_origins=["http://localhost:3000"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)


class AgentRequest(BaseModel):
    keywords: List[str] = get_keywords()
    n: Optional[int] = 20

@app.post("/run-agent")
async def run_agent(req: AgentRequest):
    try:
        initial_state = {
            "keywords": req.keywords,
            "top_n_per_platform": req.n,
        }
        final_state = run_pipeline_server(initial_state)

        response = {
            "sources": final_state.get("raw_data", []),
            "metrics": final_state.get("metrics", {}),
            "insights": final_state.get("insights", {}),
        }

        return response
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))


@app.post("/run-agent-stream")
async def run_agent_stream(req: AgentRequest):
    print(f"Received request at /run-agent-stream [POST]: {req.json()}")
    async def generate_progress():
        try:
            initial_state = {
                "keywords": req.keywords,
                "top_n_per_platform": req.n,
            }
            
            # Stream progress updates
            async for progress_data in run_pipeline_server_with_progress(initial_state):
                yield f"data: {json.dumps(progress_data)}\n\n"
                await asyncio.sleep(0.1) 
                
        except Exception as e:
            error_data = {"type": "error", "message": str(e)}
            yield f"data: {json.dumps(error_data)}\n\n"
    
    return StreamingResponse(
        generate_progress(),
        media_type="text/plain",
        headers={
            "Cache-Control": "no-cache",
            "Connection": "keep-alive",
            "Access-Control-Allow-Origin": "*",
        }
    )


if __name__ == "__main__":
    import uvicorn
    uvicorn.run("server:app", host="0.0.0.0", port=8000, reload=True)
