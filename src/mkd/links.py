import os
from pathlib import Path

from .logging import log


def create_links(target_dir, link_dir, hard=False):
    """
    Create symlinks to all files in `target_dir`. 
    Links will be located at `link_dir`.
    Example:
        target_directory = "submodules/blog-monorepo"
        link_directory = "src/blog"
        create_links(target_directory, link_directory)
    """
    log.info(f"Linking {target_dir} to {link_dir}")
    if not os.path.isdir(target_dir):
        log.error(f"target directory {target_dir} does not exist.")
        return
    if not os.path.isdir(link_dir):
        log.info(f"link directory {link_dir} does not exist, creating it.")
        os.makedirs(link_dir)
    for root, dirs, files in os.walk(target_dir):
        dirs[:] = [d for d in dirs if not d.startswith('.')]
        for file in files:
            if file.startswith('.'):
                log.debug(f"Skipping {file}, it starts with a dot.")
                continue
            target_file = Path(os.path.join(root, file))
            relative_path = os.path.relpath(target_file, target_dir)
            link_file = Path(os.path.join(link_dir, relative_path))
            link_dir_path = os.path.dirname(link_file)
            if not os.path.exists(link_dir_path):
                os.makedirs(link_dir_path)
            if os.path.isdir(link_file):
                log.debug(f"Skipping {link_file}, it is a directory.")
                continue
            if os.path.exists(link_file) or os.path.islink(link_file):
                log.debug(f"Replacing existing file or link: {link_file}")
                os.remove(link_file)
            # we should make this relative again...
            if hard:
                link_file.hardlink_to(target_file)
                log.info(f"Created HARD link: {link_file} -> {target_file}")
            else:
                link_file.symlink_to(target_file)
                log.info(f"Created link: {link_file} -> {target_file}")
