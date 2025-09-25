from fastapi import FastAPI
from fastapi.staticfiles import StaticFiles
from pathlib import Path

from app.routers import router
from app.services import init_cache

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
