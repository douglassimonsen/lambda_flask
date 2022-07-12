import zipfile
import os


def get_files():
    all_paths = []
    for directory, subdirs, paths in os.walk('.'):
        if any(p in directory for p in ('.\\.git', '__pycache__')):
            continue
        all_paths.extend([
            os.path.join(directory, p) 
            for p in paths 
            if all(p != x for x in ('.gitignore', 'deploy.zip', 'zipper.py', 'test.py'))])
    return all_paths


with open('deploy.zip', 'wb') as f:
    with zipfile.ZipFile(f, 'w') as zf:
        for path in get_files():
            zf.write(path)
