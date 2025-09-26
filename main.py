import os
from pathlib import Path
from fastapi import FastAPI, Request
from fastapi.middleware.cors import CORSMiddleware
from fastapi.templating import Jinja2Templates
from fastapi.staticfiles import StaticFiles
from fastapi.responses import HTMLResponse, RedirectResponse
from app.routers import auth, github, user
from app.db.mongo import connect_db

app = FastAPI()

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],  # tighten in prod
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Get the absolute path to the project root
current_file = Path(__file__).resolve()
project_root = current_file.parent.parent.parent  # Go up 3 levels
static_dir = project_root / "static"
templates_dir = project_root / "templates"

print(f"Current file: {current_file}")
print(f"Project root: {project_root}")
print(f"Static dir: {static_dir}")
print(f"Templates dir: {templates_dir}")
print(f"Static exists: {static_dir.exists()}")
print(f"Templates exists: {templates_dir.exists()}")

# Use absolute paths to avoid any confusion
app.mount("/static", StaticFiles(directory=str(static_dir)), name="static")
templates = Jinja2Templates(directory=str(templates_dir))

# Include existing routers
app.include_router(auth.router, prefix="/auth", tags=["auth"])
app.include_router(user.router, prefix="/user", tags=["user"])
app.include_router(github.router, prefix="/github", tags=["github"])

# Frontend routes
@app.get("/", response_class=HTMLResponse)
async def root():
    return RedirectResponse(url="/login")

@app.get("/login", response_class=HTMLResponse)
async def login_page(request: Request):
    return templates.TemplateResponse("login.html", {"request": request})

@app.get("/register", response_class=HTMLResponse)
async def register_page(request: Request):
    return templates.TemplateResponse("register.html", {"request": request})

@app.get("/dashboard", response_class=HTMLResponse)
async def dashboard_page(request: Request):
    return templates.TemplateResponse("dashboard.html", {"request": request})

@app.get("/repo", response_class=HTMLResponse)
async def repo_page(request: Request):
    return templates.TemplateResponse("repo_analysis.html", {"request": request})

@app.get("/bulk", response_class=HTMLResponse)
async def bulk_page(request: Request):
    return templates.TemplateResponse("bulk_analysis.html", {"request": request})

@app.on_event("startup")
async def startup_db():
    await connect_db()

if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=8000)