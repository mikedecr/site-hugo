import os


def create_links(source_dir, target_dir):
    """
    Create symlinks to all files in `source_dir`. Links will be located at `target_dir`.
    Example:
        source_directory = "submodules/blog-monorepo"
        target_directory = "src/blog"
        create_links(source_directory, target_directory)
    """
    if not os.path.isdir(source_dir):
        print(f"Source directory {source_dir} does not exist.")
        return
    if not os.path.isdir(target_dir):
        print(f"Target directory {target_dir} does not exist, creating it.")
        os.makedirs(target_dir)
    for root, dirs, files in os.walk(source_dir):
        dirs[:] = [d for d in dirs if not d.startswith('.')]
        for file in files:
            if file.startswith('.'):
                print(f"Skipping {file}, it starts with a dot.")
                continue
            source_file = os.path.join(root, file)
            relative_path = os.path.relpath(source_file, source_dir)
            target_file = os.path.join(target_dir, relative_path)
            target_dir_path = os.path.dirname(target_file)
            if not os.path.exists(target_dir_path):
                os.makedirs(target_dir_path)
            if os.path.isdir(target_file):
                print(f"Skipping {target_file}, it is a directory.")
                continue
            if os.path.exists(target_file) or os.path.islink(target_file):
                print(f"Replacing existing file or link: {target_file}")
                os.remove(target_file)
            os.link(source_file, target_file)
            print(f"Created link: {target_file} -> {source_file}")
