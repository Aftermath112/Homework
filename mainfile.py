import shutil
import sys
import scan
import normalize
from pathlib import Path
from file_generator import file_generator



def hande_file(path, root_folder, dist):
    target_folder = root_folder / dist
    target_folder.mkdir(exist_ok=True)
    path.replace(target_folder/normalize.normalize(path.name))


def handle_archive(path, root_folder, dist):
    target_folder = root_folder / dist
    target_folder.mkdir(exist_ok=True)
    print(target_folder)
    new_name = normalize.normalize(path.name.replace(Path(path).suffix[1:], ''))
    print(new_name)
    archive_folder = target_folder / new_name
    archive_folder.mkdir(exist_ok=True)

    try:
        shutil.unpack_archive(str(path.resolve(path)), str(archive_folder))
    except shutil.ReadError:
        archive_folder.rmdir()
        return
    except FileNotFoundError:
        archive_folder.rmdir()
        return
    path.unlink()


def remove_empty_folders(path):
    for item in path.iterdir():
        if item.is_dir():
            remove_empty_folders(item)
            try:
                item.rmdir()
            except OSError:
                pass


def get_folder_objects(root_path):
    for folder in root_path.iterdir():
        if folder.is_dir():
            remove_empty_folders(folder)
            try:
                folder.rmdir()
            except OSError:
                pass

def main(folder_path):
    scan.scan(folder_path)

    for file in scan.Images:
        hande_file(file, folder_path, "images")

    for file in scan.Doc:
        hande_file(file, folder_path, "documents")

    for file in scan.Music:
        hande_file(file, folder_path, "audio")

    for file in scan.Videos:
        hande_file(file, folder_path, "video")

    for file in scan.archives:
        handle_archive(file, folder_path, "archives")

    for file in scan.others:
        hande_file(file, folder_path, "OTHERS")


    get_folder_objects(folder_path)

def process(path):
    print(f"Start in {path}")
    arg = Path(path)
    scan(arg)

if __name__ == '__main__':
    path = sys.argv[1]
    process(path)
