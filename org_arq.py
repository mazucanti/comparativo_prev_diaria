from zipfile import ZipFile
import shutil, os
from pathlib import Path




def extrai():
    diretorios = Path('downloads/full').glob('**/*')
    files = [diretorio for diretorio in diretorios if diretorio.is_file()]
    for file in files:
        if file.suffix == ".zip":
            try:
                with ZipFile(file) as zp:
                    zp.extractall('downloads/full')
            except:
                continue


