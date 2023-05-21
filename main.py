from fastapi import FastAPI

from users.router import router as router_users

app = FastAPI(
    debug=True,
    title='Bewise.ai v.1',
    description='API для тестового задания Bewise.ai'
)

app.include_router(
    router_users
)
