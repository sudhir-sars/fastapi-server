from fastapi import FastAPI, Request
from fastapi.responses import JSONResponse
from clerk_backend_api import Clerk
from clerk_backend_api.jwks_helpers import AuthenticateRequestOptions
import os
from .transcript_service import fetch_transcript
from youtube_transcript_api import YouTubeTranscriptApi
from youtube_transcript_api.proxies import WebshareProxyConfig
from dotenv import load_dotenv
load_dotenv()

PROXY_USERNAME = os.getenv("PROXY_USERNAME")
PROXY_PASSWORD = os.getenv("PROXY_PASSWORD")
CLERK_API_KEY = os.getenv("CLERK_SECRET_KEY")

ytt_api = YouTubeTranscriptApi(
    proxy_config=WebshareProxyConfig(
        proxy_username=PROXY_USERNAME,
        proxy_password=PROXY_PASSWORD,
    )
)

app = FastAPI()
print(PROXY_USERNAME,PROXY_PASSWORD,CLERK_API_KEY)

clerk = Clerk(bearer_auth=CLERK_API_KEY)

def is_signed_in(request: Request) -> bool:
    """Check if the request is authenticated using Clerk."""
    try:
        auth_state = clerk.authenticate_request(
            request,
            AuthenticateRequestOptions(authorized_parties=['http://localhost:3000'])
        )
        return auth_state.is_signed_in
    except Exception as e:
        print(f"Auth error: {e}")
        return False

@app.get("/transcript")
async def get_transcript(video_id: str, request: Request):

    # if not is_signed_in(request):
    #     return JSONResponse(status_code=401, content={"error": "Unauthorized"})
    
    result = fetch_transcript(video_id, ytt_api)
    # print(result)
    return result

@app.get("/")
async def root():
    """Root endpoint to confirm API is running."""
    return {"message": "Transcript API is running"}

@app.get("/health")
async def health_check():
    """Check if the transcript service is healthy by testing with a sample video ID."""
    test_video_id = "AiGdwqdpPKE"
    try:
        result = fetch_transcript(test_video_id)
        if result["transcript"]:
            return {"status": "healthy"}
        else:
            return {"status": "unhealthy", "message": result["message"]}
    except Exception as e:
        return {"status": "unhealthy", "error": str(e)}