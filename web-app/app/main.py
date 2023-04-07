import uvicorn

from configs.app_configs import AppSettings

if __name__ == "__main__":
    app_settings = AppSettings()

    uvicorn.run(
        "app:app",
        host="0.0.0.0",
        port=app_settings.port,
        reload=False,
        log_level=app_settings.log_level,
        workers=app_settings.workers
    )
