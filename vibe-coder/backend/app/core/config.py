from pydantic_settings import BaseSettings

class Settings(BaseSettings):
    PROJECT_NAME: str = "Vibe Coder"
    API_V1_STR: str = "/api/v1"
    WORKSPACE_DIR: str = "../workspace"

    class Config:
        env_file = ".env"

settings = Settings()
