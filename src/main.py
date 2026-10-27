from fastapi import FastAPI

app = FastAPI(
    title="CampusFlow API",
    description="School Management System API",
    version="1.0.0",
)

@app.get("/")
def root():
    return {
        "message": "Welcome to CampusFlow",
        "status": "running",
    }


@app.get("/health")
def health_check():
    return {"status": "healthy"}
