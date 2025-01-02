import os


def find_xls_files(folder_path: str) -> list[str]:
    """Возвращает список файлов из папки downloads"""

    return [
        os.path.join(folder_path, file)
        for file in os.listdir(folder_path)
        if file.endswith(".xls")
    ]
