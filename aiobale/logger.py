import logging

logger = logging.getLogger("client")

logger.setLevel(logging.WARNING)

console = logging.StreamHandler()
console.setLevel(logging.WARNING)

formatter = logging.Formatter("[%(asctime)s] %(levelname)s - %(message)s", "%H:%M:%S")
console.setFormatter(formatter)

logger.addHandler(console)


def set_debug(enabled: bool):
    level = logging.DEBUG if enabled else logging.WARNING
    logger.setLevel(level)
    console.setLevel(level)
