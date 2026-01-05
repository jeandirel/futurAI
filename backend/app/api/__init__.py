from fastapi import APIRouter

from .health import router as health_router
from .jobs import router as jobs_router
from .exports import router as exports_router
from .rag import router as rag_router
from .metrics import router as metrics_router

router = APIRouter()
router.include_router(health_router, prefix="/health", tags=["health"])
router.include_router(jobs_router, prefix="/jobs", tags=["jobs"])
router.include_router(exports_router, prefix="", tags=["exports"])
router.include_router(rag_router, prefix="/rag", tags=["rag"])
router.include_router(metrics_router, prefix="/metrics", tags=["metrics"])
