import traceback

print("🚀 Starting app...")

try:
    from fastapi import FastAPI
    from backend.routes.chat import router
    from fastapi.middleware.cors import CORSMiddleware
    from dotenv import load_dotenv

    load_dotenv()

    app = FastAPI()

    app.add_middleware(
        CORSMiddleware,
        allow_origins=["*"],
        allow_credentials=True,
        allow_methods=["*"],
        allow_headers=["*"],
    )

    app.include_router(router, prefix="/chat")

    @app.get("/")
    def home():
        return {"message": "AI Assistant Running"}

    print("✅ App initialized")

except Exception:
    print("❌ FULL ERROR BELOW:")
    traceback.print_exc()