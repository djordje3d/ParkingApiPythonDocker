import os
from pathlib import Path
from fastapi import FastAPI
from fastapi.staticfiles import StaticFiles
from fastapi.responses import FileResponse, HTMLResponse

from app.routers import router
from app.services import init_cache

app = FastAPI(title="Parking Dashboard API")

# --- Include backend API routes ---
app.include_router(router)

# --- Init cache on startup ---


@app.on_event("startup")
def on_startup():
    print("🚀 Startup event triggered")
    init_cache(app)

# --- Serve Vue frontend ---


FRONTEND_DIST = os.path.join(os.path.dirname(__file__), "frontend", "dist")

if os.path.exists(FRONTEND_DIST):
    print(f"✅ Serving frontend from: {FRONTEND_DIST}")

    # Serve static assets
    app.mount("/assets", StaticFiles(directory=os.path.join(FRONTEND_DIST, "assets")), name="assets")

    # Serve index.html for root
    @app.get("/", response_class=HTMLResponse)
    async def serve_vue_app():
        return FileResponse(os.path.join(FRONTEND_DIST, "index.html"))

    # Catch-all for Vue Router history mode
    @app.get("/{full_path:path}")
    async def serve_vue_history(full_path: str):
        target = os.path.join(FRONTEND_DIST, full_path)
        return FileResponse(target) if os.path.exists(target) else FileResponse(os.path.join(FRONTEND_DIST, "index.html"))

else:
    print("⚙️ Development mode: Vue frontend not built (use `npm run dev`).")

# --- Optional test endpoint ---


@app.get("/api/hello")
def get_hello():
    return {"message": "Hello from FastAPI backend!"}


@app.post("/api/simulate")
def simulate():
    return {"status": "ok"}
