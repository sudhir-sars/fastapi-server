# Simple FastAPI Transcript Server
A minimal FastAPI server to handle GET requests for transcripts using a `videoId` query parameter.

## Run
1. Activate virtual environment: `source venv/bin/activate`
2. Install dependencies: `pip install -r requirements.txt`
3. Run server: `uvicorn app.main:app --reload`
4. Access: `http://localhost:8000/transcript?videoId=wcwscws`