from pathlib import Path
from os import remove as rm
import io
from zipfile import ZipFile
from bs4 import BeautifulSoup

from PIL import Image

from PIL import ImageFile
ImageFile.LOAD_TRUNCATED_IMAGES = True


def main():
    print("Enter path to .epub file:")
    path = Path(input())

    print('Please enter path to converted epub file:')
    spath = Path(input())

    print(f'{path.resolve().absolute()}')
    print('will parsed and saved to')
    print(f'{spath.resolve().absolute()}')

    q = input("Is everything right? [Y/n] ")

    if not (q == "Y" or q == "y" or q == ""):
        return

    with ZipFile(path, 'r') as rzip:
        with ZipFile(spath, 'w') as wzip:
            files = rzip.namelist()

            for file in files:
                print(f"Processing {file}")
                if file.endswith('.png'):
                    img = Image.open(io.BytesIO(rzip.read(file)))
                    jpg_img = img.convert('RGB')
                    filename = file.replace('.png', '.jpg')

                    b = io.BytesIO()
                    jpg_img.save(b, 'jpeg')
                    im_bytes = b.getvalue()

                    wzip.writestr(filename, im_bytes)
                elif file.endswith('.xhtml') or file.endswith('.html') or file.endswith('.ncx') or file.endswith('.opf') or file.endswith('.xml'):
                    rfile = rzip.read(file)

                    soup = BeautifulSoup(rfile, 'lxml')

                    for elem in soup.find_all():
                        for attr in elem.attrs.items():
                            try:
                                elem[attr[0]] = attr[1].replace(
                                    '.png', '.jpg') if not attr[0] == 'media-type' else attr[1].replace('image/png', 'image/jpeg')
                            except:
                                pass

                    wzip.writestr(file, soup.__str__())
                elif not file.endswith('/'):
                    wzip.writestr(file, rzip.read(file))


if __name__ == "__main__":
    main()
