"""
Manage Samba mounts to backend RAID
Volume shares at the application
layer.
"""

import os
import subprocess

import constants
import tpl.vault

MAIN_LOG = constants.logging.getLogger(__name__)

def mount(smb_mount: str, vault_token: str):
    """
    Use token to access Samba credentials
    and create a non-persisted mount to
    authorized shares.
    """

    smb_auth = tpl.vault.get_secret(
        vault_token,
        constants.SMB_VAULT_PATH
    )

    smb_username = smb_auth["USERNAME"]
    smb_password = smb_auth["PASSWORD"]

    with open("/tmp/.smbcredentials", "w", encoding="utf-8") as creds_opened:
        creds_opened.write(
            "username=" + smb_username + "\n" + \
            "password=" + smb_password + "\n"
        )

    if not os.path.isdir(smb_mount):
        os.makedirs(smb_mount)

    subprocess.run(
        [
            "mount",
            "--type",
            "cifs",
            "//" + constants.SMB_SHARE_HOST + "/" + constants.SMB_SHARE_NAME,
            smb_mount,
            "--options",
            "credentials=/tmp/.smbcredentials," + \
                "uid=" + constants.SMB_SHARE_UID + ",gid=" + constants.SMB_SHARE_GID + \
                ",dir_mode=0700,file_mode=0600,vers=3.11,seal"
        ],
        capture_output=True,
        text=True,
        check=True,
        timeout=5
    )

    MAIN_LOG.info("Mounted RAID SMB share : %s", constants.SMB_SHARE_NAME)

def unmount(smb_mount: str):
    """
    Unmount temp mount location once
    all SMB tasks have completed.
    """

    if os.path.ismount(smb_mount):
        os.system("umount " + smb_mount)
        os.remove("/tmp/.smbcredentials")

        MAIN_LOG.info("Unmounted RAID SMB share : %s", constants.SMB_SHARE_NAME)
