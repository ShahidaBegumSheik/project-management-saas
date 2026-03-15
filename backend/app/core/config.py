from pydantic import Field
from pydantic_settings import BaseSettings, SettingsConfigDict


class Settings(BaseSettings):
    model_config = SettingsConfigDict(env_file=".env", extra="ignore")

    database_url: str = Field(
        default="mysql+pymysql://root:root@127.0.0.1:3306/pm_saas", alias="DATABASE_URL"
    )

    jwt_secret_key: str = Field(default="change_me", alias="JWT_SECRET_KEY")
    jwt_algorithm: str = Field(default="HS256", alias="JWT_ALGORITHM")
    access_token_expire_minutes: int = Field(
        default=60, alias="ACCESS_TOKEN_EXPIRE_MINUTES"
    )
    refresh_token_expire_minutes: int = Field(
        default=10080, alias="REFRESH_TOKEN_EXPIRE_MINUTES"
    )

    cors_origins: str = Field(
        default="http://localhost:5173,http://127.0.0.1:5173", alias="CORS_ORIGINS"
    )

    seed_admin: bool = Field(default=True, alias="SEED_ADMIN")
    admin_email: str = Field(default="admin@gmail.com", alias="ADMIN_EMAIL")
    admin_password: str = Field(default="admin1234", alias="ADMIN_PASSWORD")

    smtp_host: str = Field(default="", alias="SMTP_HOST")
    smtp_port: int = Field(default=587, alias="SMTP_PORT")
    smtp_username: str = Field(default="", alias="SMTP_USERNAME")
    smtp_password: str = Field(default="", alias="SMTP_PASSWORD")
    email_from: str = Field(default="", alias="EMAIL_FROM")

    frontend_verify_url: str = Field(
        default="http://localhost:5173/verify-email", alias="FRONTEND_VERIFY_URL"
    )

    frontend_success_url: str = Field(
        default="http://localhost:5173/app/billing?checkout=success",
        alias="FRONTEND_SUCCESS_URL",
    )
    frontend_failure_url: str = Field(
        default="http://localhost:5173/app/billing?checkout=failure",
        alias="FRONTEND_FAILURE_URL",
    )

    login_rate_limit_count: int = Field(default=5, alias="LOGIN_RATE_LIMIT_COUNT")
    login_rate_limit_window_seconds: int = Field(
        default=300, alias="LOGIN_RATE_LIMIT_WINDOW_SECONDS"
    )

    razorpay_key_id: str = Field(default="", alias="RAZORPAY_KEY_ID")
    razorpay_key_secret: str = Field(default="", alias="RAZORPAY_KEY_SECRET")
    razorpay_webhook_secret: str = Field(default="", alias="RAZORPAY_WEBHOOK_SECRET")
    razorpay_pro_amount: int = Field(default=499, alias="RAZORPAY_PRO_AMOUNT")
    razorpay_currency: str = Field(default="INR", alias="RAZORPAY_CURRENCY")
    razorpay_company_name: str = Field(
        default="VertexCore", alias="RAZORPAY_COMPANY_NAME"
    )
    razorpay_company_description: str = Field(
        default="Project Management SaaS Pro Plan", alias="RAZORPAY_COMPANY_DESCRIPTION"
    )

    cache_ttl_seconds: int = Field(default=60, alias="CACHE_TTL_SECONDS")

    @property
    def cors_origins_list(self) -> list[str]:
        return [o.strip() for o in self.cors_origins.split(",") if o.strip()]


settings = Settings()
