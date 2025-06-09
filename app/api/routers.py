from fastapi import APIRouter

from app.api.endpoints import farm, health, plantation, productor, reports, season

router = APIRouter()

router.include_router(health.router, prefix="/health", tags=["health"])
router.include_router(
    productor.router,
    prefix="/productor",
    tags=["productor"])
router.include_router(farm.router, prefix="/farm", tags=["farm"])
router.include_router(
    plantation.router,
    prefix="/plantation",
    tags=["plantation"])
router.include_router(season.router, prefix="/season", tags=["season"])
router.include_router(reports.router, prefix="/reports", tags=["reports"])
