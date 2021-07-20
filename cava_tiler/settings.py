"""CAVA Tiler API settings."""

import pydantic


class ApiSettings(pydantic.BaseSettings):
    """FASTAPI application settings."""

    name: str = "CAVA Tiler"
    cors_origins: str = "*"
    cachecontrol: str = "public, max-age=3600"
    debug: bool = False

    lower_case_query_parameters: bool = False

    cogeo_source: str = "rca-map-layers"

    @pydantic.validator("cogeo_source")
    def parse_cogeo_source(cls, v):
        if "s3.us-west-2.amazonaws.com" not in v:
            return f"{v}.s3.us-west-2.amazonaws.com"
        return v

    @pydantic.validator("cors_origins")
    def parse_cors_origin(cls, v):
        """Parse CORS origins."""
        return [origin.strip() for origin in v.split(",")]

    class Config:
        """model config"""

        env_file = ".env"
        env_prefix = "TITILER_API_"


api_config = ApiSettings()
