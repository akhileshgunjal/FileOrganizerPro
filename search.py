
from pathlib import Path


def search_files(folder_path, search_text):

    results = []

    folder = Path(folder_path)

    if not folder.exists():
        return results

    search_text = search_text.lower().strip()

    if not search_text:
        return results

    for file_path in folder.rglob("*"):

        if file_path.is_file():

            file_name = file_path.name.lower()

            if search_text in file_name:

                results.append(file_path)

    return results

