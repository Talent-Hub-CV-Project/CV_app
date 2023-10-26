from pydantic_settings import BaseSettings, SettingsConfigDict


class Settings(BaseSettings):
    postgres_user: str
    postgres_password: str
    postgres_db: str
    postgres_host: str = "localhost"
    model_path: str = "models/yolov8n.onnx"
    port: int = 7000
    config_path: str = "alembic.ini"
    is_docker: bool = False

    model_config = SettingsConfigDict(env_file=(".env", "../.env"))
    model_config["protected_namespaces"] = ("settings_",)

    @property
    def postgres_dsn(self) -> str:
        return f"postgresql+psycopg2://{self.postgres_user}:{self.postgres_password}@{self.postgres_host}/{self.postgres_db}"
