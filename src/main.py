import os
import shutil

from copystatic import copy_files_recursive

script_dir = os.path.dirname(os.path.realpath(__file__))
parent_dir = os.path.dirname(script_dir)

dir_path_static = f"{parent_dir}/static"
dir_path_public = f"{parent_dir}/public"


def main():
    print("Deleting public directory...")
    if os.path.exists(dir_path_public):
        shutil.rmtree(dir_path_public)

    print("Copying static files to public directory...")
    copy_files_recursive(dir_path_static, dir_path_public)


if __name__ == "__main__":
    main()
