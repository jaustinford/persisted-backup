"""
Copy all files and directories between
backup sources.
"""

import os
import traceback
import time

import constants
import gbackup
import tpl.smb
import tpl.vault

MAIN_LOG = constants.logging.getLogger(__name__)

def main():
    """
    Mount volume, open config and assign
    elements and iterate over 'backup_targets'.
    """

    if os.environ.get("BACKUP_OBJECT").startswith("raid"):
        vault_token = tpl.vault.approle_login(constants.VAULT_APPROLE)

        smb_mount = gbackup.get_smb_mount()

        tpl.smb.mount(smb_mount, vault_token)

    try:
        gbackup.iterate_objects()

        if os.environ.get("BACKUP_OBJECT").startswith("raid"):
            tpl.smb.unmount(smb_mount)

    except Exception as broad_exception: # pylint: disable=broad-exception-caught
        MAIN_LOG.error(broad_exception)
        traceback.print_exc()

        if os.environ.get("BACKUP_OBJECT").startswith("raid"):
            tpl.smb.unmount(smb_mount)

    time.sleep(50000)

if __name__ == "__main__":
    main()
