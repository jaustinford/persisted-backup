"""
Steps to copy file and directory
content and metadata elements.
"""

import os
import re
import shutil
import filecmp

import constants

MAIN_LOG = constants.logging.getLogger(__name__)

def diff_file(src_file: str, dst_file: str, dst_relative: str, should_copy: bool):
    """
    Use different methods to compare
    files.
    """

    should_compare = True

    for non_checksum_ext in constants.CONFIG_NON_CHECKSUM_EXTS:
        if src_file.endswith("." + non_checksum_ext):
            should_compare = False
            break

    if should_compare:
        if not filecmp.cmp(src_file, dst_file):
            MAIN_LOG.info("Different checksum, updating file : %s", dst_relative)
            should_copy = True

        else:
            MAIN_LOG.info("Confirmed checksum of file : %s", dst_relative)

    else:
        if os.path.getsize(src_file) != os.path.getsize(dst_file):
            MAIN_LOG.info("Different size, updating file : %s", dst_relative)
            should_copy = True

        else:
            MAIN_LOG.info("Confirmed size of file : %s", dst_relative)

    return should_copy

def manage_dir(backup_direction: str, dst_root: str, src_dir: str, dst_dir: str):
    """
    Copy directories and preserve
    metadata elements.
    """

    if backup_direction == "forward":
        direction_colored = "\033[" + "0;92m" + backup_direction + "\033[" + "0;0m"

    elif backup_direction == "reverse":
        direction_colored = "\033[" + "0;94m" + backup_direction + "\033[" + "0;0m"

    dst_relative = re.sub(dst_root, direction_colored + " - ", dst_dir)

    if backup_direction == "forward":
        if not os.path.isdir(dst_dir):
            MAIN_LOG.info("Creating dir : %s", dst_relative)

            os.makedirs(dst_dir)
            shutil.copystat(src_dir, dst_dir, follow_symlinks=False)

        else:
            MAIN_LOG.info("Confirmed dir : %s", dst_relative)

        src_dir_stat      = os.stat(src_dir)
        src_dir_stat_uid  = src_dir_stat.st_uid
        src_dir_stat_gid  = src_dir_stat.st_gid
        src_dir_stat_mode = src_dir_stat.st_mode

        os.chown(dst_dir, src_dir_stat_uid, src_dir_stat_gid)
        os.chmod(dst_dir, src_dir_stat_mode)

    elif backup_direction == "reverse":
        if not os.path.isdir(dst_dir) and os.path.isdir(src_dir):
            MAIN_LOG.info("Removing dir : %s", re.sub("0;94m", "0;31m", dst_relative))
            shutil.rmtree(src_dir)

        else:
            MAIN_LOG.info("Confirmed dir : %s", dst_relative)

def manage_file(backup_direction: str, dst_root: str, src_file: str, dst_file: str):
    """
    Copy files and preserve
    metadata elements.
    """

    should_copy = False

    if backup_direction == "forward":
        direction_colored = "\033[" + "0;92m" + backup_direction + "\033[" + "0;0m"

    elif backup_direction == "reverse":
        direction_colored = "\033[" + "0;94m" + backup_direction + "\033[" + "0;0m"

    dst_relative = re.sub(dst_root, direction_colored + " - ", dst_file)

    if backup_direction == "forward":
        if not os.path.exists(dst_file):
            MAIN_LOG.info("Creating file : %s", dst_relative)
            should_copy = True

        else:
            should_copy = diff_file(
                src_file,
                dst_file,
                dst_relative,
                should_copy
            )

        if should_copy:
            if not os.path.islink(dst_file):
                shutil.copyfile(src_file, dst_file, follow_symlinks=False)
                shutil.copystat(src_file, dst_file, follow_symlinks=False)

        if not os.path.islink(dst_file):
            src_file_stat      = os.stat(src_file)
            src_file_stat_uid  = src_file_stat.st_uid
            src_file_stat_gid  = src_file_stat.st_gid
            src_file_stat_mode = src_file_stat.st_mode

            os.chown(dst_file, src_file_stat_uid, src_file_stat_gid)
            os.chmod(dst_file, src_file_stat_mode)

    elif backup_direction == "reverse":
        if not os.path.isfile(dst_file):
            MAIN_LOG.info("Removing file : %s", re.sub("0;94m", "0;31m", dst_relative))
            os.remove(src_file)

        else:
            MAIN_LOG.info("Confirmed file : %s", dst_relative)
