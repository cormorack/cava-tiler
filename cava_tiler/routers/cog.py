from rio_cogeo.cogeo import cog_info as rio_cogeo_info
from rio_cogeo.models import Info
from rio_tiler.io import COGReader

from titiler.core.factory import TilerFactory

from cava_tiler.dependencies import MaskParams, CustomPathParams

from fastapi import Depends, Query


cog = TilerFactory(
    reader=COGReader,
    router_prefix="cog",
    additional_dependency=MaskParams,
    path_dependency=CustomPathParams,
)


@cog.router.get("/validate", response_model=Info)
def cog_validate(
    src_path: str = Depends(CustomPathParams),
    strict: bool = Query(False, description="Treat warnings as errors"),
):
    """Validate a COG"""
    return rio_cogeo_info(src_path, strict=strict)


router = cog.router
