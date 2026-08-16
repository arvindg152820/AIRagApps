from fastapi import FastAPI, HTTPException
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel
from .graph import app
import os

# Add by Arvind
api = FastAPI(
    title="Secure RAG API"
)

api.add_middleware(
    CORSMiddleware,
    allow_origins=[
        "http://localhost:5173",
        "http://127.0.0.1:5173",
        "https://secure-rag-frontend-d4ewdbeehjbkfrfq.southindia-01.azurewebsites.net",
        "https://secure-rag-frontend-qa-gsdbfehhama2frch.southindia-01.azurewebsites.net",
        "https://secure-rag-frontend-uat-bkf2f8fea2a8edf9.southindia-01.azurewebsites.net",
    ],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

class LoginRequest(BaseModel):
    username: str
    password: str

class QuestionRequest(BaseModel):
    user_id: str
    question: str

USERS = {

    "alice": {
        "password": "alice123",
        "groups": ["Employees"]
    },

    "bob": {
        "password": "bob123",
        "groups": [
            "Employees",
            "HR"
        ]
    },

    "carol": {
        "password": "carol123",
        "groups": [
            "Employees",
            "ProjectAlpha"
        ]
    },

    "david": {
        "password": "david123",
        "groups": [
            "Employees",
            "Finance"
        ]
    }
}

@api.get("/health")
def health():
    return {
        "status": "healthy",
        "environment": os.getenv("APP_ENV", "UNKNOWN")
    }

@api.post("/login")
def login(request: LoginRequest):
    user = USERS.get(
        request.username
    )
    if not user:
        raise HTTPException(
            status_code=401,
            detail="Invalid username or password"
        )

    if user["password"] != request.password:
        raise HTTPException(
            status_code=401,
            detail="Invalid username or password"
        )

    return {
        "user_id": request.username,
        "groups": user["groups"]
    }

@api.post("/ask")
def ask_question(request: QuestionRequest):
    user = USERS.get(
        request.user_id
    )

    if not user:
        raise HTTPException(
            status_code=401,
            detail="Invalid user"
        )

    groups = user["groups"]
    result = app.invoke({
        "query": request.question,
        "user_id": request.user_id,
        "user_groups": groups,
        "documents": [],
        "answer": ""
    })

    return {
        "question": request.question,
        "answer": result["answer"],
        "documents":
            [
                {
                    "file_name":
                        d["file_name"]
                }
                for d in result["documents"]
            ]
    }