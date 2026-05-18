import uvicorn
from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware

from app.config import settings
from app.api.v1 import machines, groups, tags

app = FastAPI(
    title=settings.app_name,
    version=settings.app_version,
    debug=settings.debug,
    description="一个简单的DevOps平台，用于管理机器和部署应用",
)

# CORS配置
app.add_middleware(
    CORSMiddleware,
    allow_origins=settings.cors_allow_origins,
    allow_credentials=settings.cors_allow_credentials,
    allow_methods=settings.cors_allow_methods,
    allow_headers=settings.cors_allow_headers,
)

# 注册API路由
app.include_router(machines.router, prefix="/api/v1/machines", tags=["机器管理"])
app.include_router(groups.router, prefix="/api/v1/groups", tags=["分组管理"])
app.include_router(tags.router, prefix="/api/v1/tags", tags=["标签管理"])


@app.get("/", tags=["健康检查"])
def health_check():
    return {
        "status": "ok",
        "app_name": settings.app_name,
        "version": settings.app_version,
        "debug": settings.debug,
    }


if __name__ == "__main__":
    uvicorn.run(
        "app.main:app",
        host=settings.host,
        port=settings.port,
        reload=settings.debug,
        workers=settings.workers,
    )
