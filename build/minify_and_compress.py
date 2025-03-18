"""
Minifying source files to dist folder
as well making zip file of the latter
usefull especially if lots of comments and docstings for documentation
"""

import os, re, shutil, python_minifier

SRC_NAME = 'src' #name of source folder in root
DIST_NAME = 'dist' #name of distr folder in root
DIST_PY_NAME = 'py' #folder for distributing minified py files
ZIP_NAME = 'distro.zip' #name of the zip for distr
ZIP_FORMAT = 'zip'
CWD = os.path.dirname(os.path.abspath(__file__))
ROOT = os.path.dirname(CWD)
SRC = os.path.join(ROOT, SRC_NAME)
DIST = os.path.join(ROOT, DIST_NAME)
DIST_PY = os.path.join(DIST, DIST_PY_NAME)
DIST_ZIP = os.path.join(DIST, ZIP_NAME)
print('root', ROOT)
print('src', SRC)
print('dist', DIST)
print('zip', DIST_ZIP)


def minify(source_code:str) -> str:
    """cleans fron documentation strings and minifies with light options"""
    cleaned_code_doc = re.sub(r'^\s*(\'\'\'|"""|\'\'\'|""").*$', '', source_code, flags=re.MULTILINE)
    #cleans docstrings for documentation
    minified_code = python_minifier.minify(
                    cleaned_code_doc,
                    remove_annotations=True,
                    combine_imports=True,
                    constant_folding=True
                )
    
    return minified_code


def compress(source_folder=DIST_PY, destination_folder=DIST, zip_name='distro'):
    # Ensure the destination folder exists
    os.makedirs(destination_folder, exist_ok=True)
    # Full path for the ZIP file (with the .zip extension)
    zip_path = os.path.join(destination_folder, zip_name)
    # Compress the source folder to the zip file at the specified destination
    shutil.make_archive(zip_path, ZIP_FORMAT, source_folder)
    print('ZIP', zip_path, ZIP_FORMAT)

def main():
    """loop the code in `SRC` without the links/symlinks in it"""
    print('-'*30)
    src_len = len(SRC)
    for root, dirs, files in os.walk(SRC, followlinks=False):
       for file in files:
            if not file.endswith('.py'):
                continue
            file_path = os.path.join(root, file)
            dest_path = DIST_PY + file_path[src_len:]
            with open(file_path, 'r') as f:
                original_source = f.read()
            minified_source = minify(original_source)
            
            os.makedirs(os.path.dirname(dest_path), exist_ok=True)

            with open(dest_path, 'w') as f:
                f.write(minified_source)
            
            print(file_path, len(original_source), '->', dest_path, len(minified_source))

    compress()


main()
