import asyncio
from contextlib import asynccontextmanager
from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from app.services.click_flush import flush_clicks_to_db
from app.routers import auth, links

async def periodic_flush():
    while True:
        try:
            # Offload blocking database/redis I/O to a worker thread
            await asyncio.to_thread(flush_clicks_to_db)
        except Exception as e:
            print("Flush error:", e)
        await asyncio.sleep(60)

@asynccontextmanager
async def lifespan(app: FastAPI):
    # Start periodic flush task in background
    task = asyncio.create_task(periodic_flush())
    yield
    task.cancel()
    try:
        await task
    except asyncio.CancelledError:
        pass

app = FastAPI(lifespan=lifespan)

origins = [
    "http://localhost:3000",      # React dev server
    "http://127.0.0.1:5173",      # Vite dev server
    "https://url-shortener-frontend-steel.vercel.app"
]

app.add_middleware(
    CORSMiddleware,
    allow_origins=origins,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

@app.get('/')
def root():
    return {"hello": "fast"}

# Mount routers in correct order of precedence
app.include_router(auth.router)
app.include_router(links.router)
