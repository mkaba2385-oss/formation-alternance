import logging
import os
import structlog

ENV = os.getenv("ENV", "dev").lower()
LOG_LEVEL = logging.DEBUG if ENV == "dev" else logging.INFO


def setup_logging():
    shared_processors = [
        structlog.contextvars.merge_contextvars,
        structlog.processors.add_log_level,
        structlog.processors.TimeStamper(fmt="iso"),
        structlog.processors.StackInfoRenderer(),
    ]

    if ENV == "prod":
        processors = shared_processors + [
            structlog.processors.format_exc_info,
            structlog.processors.JSONRenderer(),
        ]
    else:
        processors = shared_processors + [
            structlog.dev.ConsoleRenderer(colors=True),
        ]

    structlog.configure(
        processors=processors,
        wrapper_class=structlog.make_filtering_bound_logger(LOG_LEVEL),
        context_class=dict,
        logger_factory=structlog.PrintLoggerFactory(),
        cache_logger_on_first_use=True,
    )


setup_logging()
logger = structlog.get_logger()


def process_user_action(user_id: int, action: str):
    log = logger.bind(user_id=user_id, action=action)

    log.debug("Début de l'analyse du payload", payload_size_bytes=1024)
    log.info("Action utilisateur initiée")

    if action == "export_data":
        log.warning("Action gourmande en ressources détectée", threshold_mb=500)

    try:
        if action == "invalid_action":
            raise ValueError("Action non supportée dans le système")

        log.info("Action exécutée avec succès", status="success", execution_time_ms=42)

    except Exception as e:
        log.error("Échec du traitement de l'action", error=str(e), exc_info=True)


if __name__ == "__main__":
    logger.info("Démarrage de l'application", environment=ENV, log_level=logging.getLevelName(LOG_LEVEL))

    process_user_action(user_id=42, action="export_data")
    process_user_action(user_id=99, action="invalid_action")