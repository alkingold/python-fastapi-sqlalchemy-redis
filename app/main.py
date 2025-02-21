"""
This module contains API routes
"""

from fastapi import FastAPI

app = FastAPI()

@app.get("/")
def read_root():
    """
    Test doc

    Returns:
        object: Test Fast API.
    """
    return {"message": "Hello, FastAPI!"}
