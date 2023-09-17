from typing import List, Optional
from fastapi import FastAPI, Response
from fastapi.middleware.cors import CORSMiddleware
from fastapi.responses import FileResponse
from pydantic import BaseModel
import sqlite3
from helpers.chatgpt_utils import pass_to_chatgpt

import threading

app = FastAPI()

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

db_name = "./user_data_storage.db"

class AnalysisRequest(BaseModel):
    website_url: str
    company_name: str
    product_name: str
    product_text: str

@app.post("/analyze/{username}")
def analyze_website(username: str, request: AnalysisRequest):
    # Calling the pass_to_chatgpt function from chatgpt_utils
    analysis_result = pass_to_chatgpt(
        website_content=request.website_url,
        company_name=request.company_name,
        product_name=request.product_name,
        product_text=request.product_text
    )
    
    # Storing the analysis request and result in the database
    with sqlite3.connect(db_name) as conn:
        cursor = conn.cursor()
        cursor.execute(
            "INSERT INTO user_data (username, website_url, company_name, product_name, product_text) VALUES (?, ?, ?, ?, ?)",
            (username, request.website_url, request.company_name, request.product_name, request.product_text)
        )
        conn.commit()
    
    return analysis_result

@app.get("/get_user_requests/{username}")
def get_user_requests(username: str):
    with sqlite3.connect(db_name) as conn:
        cursor = conn.cursor()
        cursor.execute("SELECT website_url, company_name, product_name, product_text FROM user_data WHERE username=?", (username,))
        user_requests = cursor.fetchall()
    return user_requests

@app.get("/logo.png")
async def plugin_logo():
    filename = "logo.png"
    return FileResponse(filename, media_type="image/png")

@app.get("/.well-known/ai-plugin.json")
async def plugin_manifest():
    with open("./.well-known/ai-plugin.json") as f:
        text = f.read()
        return Response(text, media_type="application/json")

@app.get("/openapi.yaml")
async def openapi_spec():
    with open("openapi.yaml") as f:
        text = f.read()
        return Response(text, media_type="text/yaml")
