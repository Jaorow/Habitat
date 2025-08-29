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



frontend_build_path = Path(__file__).parent / "frontend_build"

app.mount("/static", StaticFiles(directory=frontend_build_path / "static"), name="static")
app.mount("/", StaticFiles(directory=frontend_build_path, html=True), name="frontend")

# app.include_router(api_router, prefix="/api")


@app.get('/api/health')
async def health():
    return { 'status': 'healthy' }

# @app.get("/")
# async def serve_react_index():
#     return FileResponse(frontend_build_path / "index.html")

# # Catch-all route for React
# @app.get("/{full_path:path}")
# async def serve_react_routes(full_path: str):
#     file_path = frontend_build_path / full_path
#     if file_path.exists() and file_path.is_file():
#         return FileResponse(file_path)
#     return FileResponse(frontend_build_path / "index.html")

@app.get("/{full_path:path}")
async def serve_react_app(full_path: str):
    file_path = os.path.join("build", "index.html")
    return FileResponse(file_path)