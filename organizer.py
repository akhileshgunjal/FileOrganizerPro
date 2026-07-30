import shutil
from pathlib import Path

from file_types import FILE_TYPES
from undo import save_operation


def get_category(extension):

    extension = extension.lower()

    for category, extensions in FILE_TYPES.items():

        if extension in extensions:
            return category

    return "Others"


def organize_folder(folder_path, enabled_categories=None):

    folder = Path(folder_path)

    if not folder.exists():
        raise FileNotFoundError(
            "Selected folder does not exist."
        )

    stats = {
        "Images": 0,
        "Documents": 0,
        "PDFs": 0,
        "Videos": 0,
        "Audio": 0,
        "Archives": 0,
        "Programs": 0,
        "Others": 0
    }

    moved_files = []

    for item in folder.iterdir():

        if item.is_dir():
            continue

        category = get_category(item.suffix)

        # ------------------------------------------
        # CHECK SETTINGS
        # ------------------------------------------

        if enabled_categories is not None:

            if not enabled_categories.get(category, True):

                continue

        destination = folder / category

        destination.mkdir(
            exist_ok=True
        )

        new_location = destination / item.name

        # ------------------------------------------
        # PREVENT OVERWRITING
        # ------------------------------------------

        if new_location.exists():

            counter = 1

            while True:

                new_name = (
                    f"{item.stem}_{counter}{item.suffix}"
                )

                new_location = (
                    destination / new_name
                )

                if not new_location.exists():
                    break

                counter += 1

        # ------------------------------------------
        # MOVE FILE
        # ------------------------------------------

        shutil.move(
            str(item),
            str(new_location)
        )

        # ------------------------------------------
        # SAVE FOR UNDO
        # ------------------------------------------

        save_operation(
            item,
            new_location
        )

        stats[category] += 1

        moved_files.append(
            (item.name, category)
        )

    total = sum(
        stats.values()
    )

    return total, stats, moved_files