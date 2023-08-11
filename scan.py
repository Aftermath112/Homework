import sys
from pathlib import Path


Images = list()
Videos = list()
Doc = list()
Music = list()
archives = list()
others = list()
unknown = set()
extensions = set()


registered_extensions = {
    "JPEG": Images,
    "PNG": Images,
    "JPG": Images,
    "SVG": Images,
    "AVI": Videos,
    "MP4": Videos,
    "MOV": Videos,
    "MKV": Videos,
    "TXT": Doc,
    "DOCX": Doc,
    "DOC": Doc,
    "PDF": Doc,
    "XLSX": Doc,
    "PPTX": Doc,
    "MP3": Music,
    "OGG": Music,
    "WAV": Music,
    "AMR": Music,
    "ZIP": archives,
    "GZ": archives,
    "TAR": archives
}


def get_extensions(file_name):
    return Path(file_name).suffix[1:].upper()


def scan(folder):
    for item in folder.iterdir():
        if item.is_dir():
            if item.name not in ("archives", "video", "audio", "documents", "images"):
                # folders.append(item)
                scan(item)
            continue

        extension = get_extensions(file_name=item.name)
        new_name = folder/item.name
        if not extension:
            others.append(new_name)
        else:
            try:
                container = registered_extensions[extension]
                extensions.add(extension)
                container.append(new_name)
            except KeyError:
                unknown.add(extension)
                others.append(new_name)


if __name__ == '__main__':
    path = sys.argv[1]
    print(f"Start in {path}")

    arg = Path(path)
    scan(arg)

