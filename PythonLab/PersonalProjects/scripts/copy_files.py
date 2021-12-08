import argparse
import os
import shutil

from tqdm import tqdm, tqdm_notebook, notebook


def directories_to_copy_no_clobber(source_dir, target_dir):
    files_to_copy = []
    for root, dirs, files in tqdm(os.walk(source_dir),total=5671):
        if "$RECYCLE" in root:
            continue
        for file_name in files:
            if file_name.startswith("."):
                continue
            source_path = os.path.join(root, file_name)
            relative_path = source_path.replace(source_dir, "")
            if relative_path.startswith("."):
                continue
            target_path = os.path.join(target_dir, relative_path)
            if os.path.isfile(source_path) and not os.path.isfile(target_path):
                files_to_copy.append(relative_path)

    return files_to_copy

if __name__ == '__main__':
    parser = argparse.ArgumentParser(description='Process some data.')
    parser.add_argument('--source_dir')
    parser.add_argument('--target_dir')
    args = parser.parse_args()

    files_to_copy = directories_to_copy_no_clobber(args.source_dir, args.target_dir)
    for file_dir in tqdm(files_to_copy):
        original = os.path.join(args.source_dir, file_dir)
        target = os.path.join(args.target_dir, file_dir)
        target_dir = os.path.dirname(target)
        os.makedirs(target_dir, exist_ok=True)
        tqdm.write(f"Copy {file_dir}")
        shutil.copyfile(original, target)

    a=1



