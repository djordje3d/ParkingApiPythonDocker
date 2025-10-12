from fastapi import FastAPI
from fastapi.staticfiles import StaticFiles
from pathlib import Path

from app.routers import router
from app.services import init_cache
from fastapi.responses import HTMLResponse

app = FastAPI()

# Uključi API rute
app.include_router(router)

# Proveri da li postoji statički folder pre montiranja
static_path = Path("app/static")

if static_path.exists() and static_path.is_dir():  # Provera da li je folder pronađen
    print("📁 Static folder found — mounting at /static")
    app.mount("/static", StaticFiles(directory=static_path, html=True), name="static")

else:
    print("⚠️ Static folder not found — skipping mount")

# Inicijalizacija keša pri pokretanju


@app.on_event("startup")
def on_startup():
    print("🚀 Startup event triggered")
    init_cache(app)


@app.get("/", response_class=HTMLResponse)
def serve_index():
    index_file = static_path / "index.html"
    if index_file.exists():
        return index_file.read_text()
    return "<h1>Index file not found</h1>"
