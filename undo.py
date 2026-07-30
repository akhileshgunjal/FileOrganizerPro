import shutil
from pathlib import Path


last_operation = []


def save_operation(original_path, new_path):

    last_operation.append(
        (
            str(original_path),
            str(new_path)
        )
    )


def undo_last_operation():

    if not last_operation:
        return 0

    restored = 0

    for original, new in reversed(last_operation):

        original = Path(original)
        new = Path(new)

        if new.exists():

            original.parent.mkdir(
                parents=True,
                exist_ok=True
            )

            if not original.exists():

                shutil.move(
                    str(new),
                    str(original)
                )

                restored += 1

    last_operation.clear()

    return restored