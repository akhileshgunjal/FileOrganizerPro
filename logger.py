from pathlib import Path
from datetime import datetime


LOG_FOLDER = Path("logs")
LOG_FILE = LOG_FOLDER / "log.txt"


def write_log(message):

    LOG_FOLDER.mkdir(exist_ok=True)

    current_time = datetime.now().strftime("%Y-%m-%d %H:%M:%S")

    with open(LOG_FILE, "a", encoding="utf-8") as file:

        file.write(
            f"[{current_time}] {message}\n"
        )