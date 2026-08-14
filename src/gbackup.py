"""
Perform backups against
iterated targets.
"""

import os

import constants
import resolve
import clone

MAIN_LOG = constants.logging.getLogger(__name__)

def get_smb_mount():
    """
    Select SMB mountpoint based on
    value for 'BACKUP_DISK_MOUNTPOINT'.
    """

    if os.environ.get("BACKUP_DISK_MOUNTPOINT") == "/persisted-backup-dst":
        smb_mount = "/persisted-backup-src"

    elif os.environ.get("BACKUP_DISK_MOUNTPOINT") == "/persisted-backup-src":
        smb_mount = "/persisted-backup-dst"

    return smb_mount

def process_backup(backup_direction: str, backup_target: str):
    """
    Direct the flow along whether
    'backup_target_src_fq' has a wildcard.
    """

    if backup_direction == "forward":
        src_root = "/persisted-backup-src/"
        dst_root = "/persisted-backup-dst/"

    elif backup_direction == "reverse":
        src_root = "/persisted-backup-dst/"
        dst_root = "/persisted-backup-src/"

    backup_target_src_fq = src_root + backup_target
    backup_target_dst_fq = dst_root + backup_target

    if "*" in backup_target_src_fq:
        backup_target_fqs = resolve.manage_wildcards(
            src_root,
            dst_root,
            backup_target_src_fq
        )

    else:
        backup_target_fqs = [
            (
                backup_target_src_fq,
                backup_target_dst_fq
            )
        ]

    for backup_target_fq in backup_target_fqs:
        if os.path.isfile(backup_target_fq[0]) or os.path.islink(backup_target_fq[0]):
            clone.manage_file(
                backup_direction,
                dst_root,
                backup_target_fq[0],
                backup_target_fq[1]
            )

        elif os.path.isdir(backup_target_fq[0]):
            resolve.manage_dirs(
                backup_direction,
                src_root,
                dst_root,
                backup_target_fq[0]
            )

def iterate_objects():
    """
    Create symlink then iterate of each
    'backup_target' in both forward and
    reverse direction.
    """

    if not os.path.islink(os.environ.get("BACKUP_DISK_MOUNTPOINT")):
        os.symlink(
            "/persisted-backup-disk/" + os.environ.get("BACKUP_OBJECT").split("-")[0],
            os.environ.get("BACKUP_DISK_MOUNTPOINT")
        )

    for backup_object in constants.CONFIG_OBJECTS:
        if backup_object["name"] == os.environ.get("BACKUP_OBJECT"):
            MAIN_LOG.info("Processing backup : %s", backup_object["name"])

            backup_targets = backup_object["targets"]
            break

    for backup_target in backup_targets:
        process_backup("forward", backup_target)
        process_backup("reverse", backup_target)
