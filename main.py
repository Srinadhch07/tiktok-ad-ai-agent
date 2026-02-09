from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from fastapi.responses import RedirectResponse
from dotenv import load_dotenv

from app.routes.users.user_auth import auth_router
from app.routes.users.user_routes.v1 import routes

load_dotenv()

app = FastAPI( title="TikTok Ads", version="1.0.0", docs_url="/docs", redoc_url="/redoc", Debug=False)

app.add_middleware( CORSMiddleware, allow_origins=["*"],  allow_credentials=True, allow_methods=["*"], allow_headers=["*"],)

app.include_router(auth_router.router,prefix="/user",tags=["User Authentication"])
app.include_router(routes.router,prefix="/user/api",tags=["User APIs"])

@app.get("/")
async def home():
    return RedirectResponse(url="/docs")