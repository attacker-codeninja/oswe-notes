#!/usr/bin/python3


import zipfile
from io import BytesIO


def _build_zip():
    f = BytesIO()
    
    z = zipfile.ZipFile(f, "w", zipfile.ZIP_DEFLATED)
    z.writestr("poc/poc.txt", "poc")
    z.close()
    
    zip = open("poc.zip", "wb")
    zip.write(f.getvalue())
    zip.close()
    
    
_build_zip()
