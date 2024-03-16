import os
import shutil

from copystatic import copy_files_recursive
from gencontent import generate_page

script_dir = os.path.dirname(os.path.realpath(__file__))
project_dir = os.path.dirname(script_dir)

dir_path_static = f"{project_dir}/static"
dir_path_public = f"{project_dir}/public"


def main():
    print("Deleting public directory...")
    if os.path.exists(dir_path_public):
        shutil.rmtree(dir_path_public)

    print("Copying static files to public directory...")
    copy_files_recursive(dir_path_static, dir_path_public)

    print("Generating page...")
    generate_page(
        f"{project_dir}/content/index.md",
        f"{project_dir}/template.html",
        f"{project_dir}/public/index.html"
    )


if __name__ == "__main__":
    main()
