from fastapi import FastAPI

from users.router import router as routers_user
from audio.router import router as routers_audio

app = FastAPI(
    debug=True,
    title='Bewise.ai v.1',
    description='API для тестового задания Bewise.ai'
)

app.include_router(
    routers_user
)
app.include_router(
    routers_audio
)
