import os
from urllib.parse import urlparse
from dataclasses import dataclass
import requests
from typing import Optional, Dict

from cava_tiler.settings import api_config
from titiler.core.dependencies import DefaultDependency
from fastapi import HTTPException, Query

@dataclass
class MaskParams(DefaultDependency):

    force_binary_mask: bool = Query(
        False, description="Whether to force binary mask."
    )

    def __post_init__(self):
        self.options = {'force_binary_mask': self.force_binary_mask}
        # remove force_binary_mask after creation since it's not a valid kwarg
        delattr(self, 'force_binary_mask')


def CustomPathParams(
    url: str = Query(..., description="Path to dataset in bucket or full url to cogeo")
) -> str:
    if "https://" not in url:
        final_url = os.path.join(
            f"https://{api_config.cogeo_source}", url.strip('/')
        )
    else:
        purl = urlparse(url)
        cogeo_bucket = api_config.cogeo_source.split('.')[0]
        if cogeo_bucket not in purl.netloc:
            raise HTTPException(
                status_code=403,
                detail=f"URL Not Allowed: `{url}`",
            )
        final_url = url

    req = requests.head(final_url)
    if req.status_code == 200:
        return final_url
    else:
        raise HTTPException(
            status_code=404,
            detail=f"COGEO Not Found: {final_url}",
        )
