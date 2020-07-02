from zipfile import ZipFile
import shutil, os
from pathlib import Path




def extrai():
    diretorios = Path('full').glob('**/*')
    files = [diretorio for diretorio in diretorios if diretorio.is_file()]
    for file in files:
        if file.suffix == ".zip":
            try:
                with ZipFile(file) as zp:
                    zp.extractall('full')
            except:
                continue

def main():
    extrai()
    diretorios = Path('full').glob('**/*')
    files = [diretorio for diretorio in diretorios if diretorio.is_file()]
    for file in files:
        if file.suffix == ".xls":
            print(file._str)
            shutil.copy(file._str, 'entradas')
        
        os.unlink(file)


main()