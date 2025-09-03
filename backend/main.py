from fastapi import FastAPI
from fastapi.staticfiles import StaticFiles
from fastapi.responses import FileResponse
from pathlib import Path
import os
# from api.endpoints import api_router


app = FastAPI()

from fastapi.middleware.cors import CORSMiddleware

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)


@app.get('/api/health')
async def health():
    return { 'status': 'healthy' }


frontend_build_path = Path(__file__).parent / "dist"
# allow overriding where the frontend build is placed
frontend_build_path = Path(os.getenv("FRONTEND_DIST_PATH", str(frontend_build_path)))

# Only mount the full dist folder (Vite puts index.html + assets inside dist).
if frontend_build_path.exists():
    app.mount("/", StaticFiles(directory=str(frontend_build_path), html=True), name="frontend")

@app.get("/{full_path:path}")
async def serve_react_app(full_path: str):
    # Serve requested file if it exists in the dist folder, otherwise return index.html
    requested = frontend_build_path / full_path
    if requested.exists() and requested.is_file():
        return FileResponse(requested)
    return FileResponse(frontend_build_path / "index.html")