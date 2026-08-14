"""
Fully-qualified paths, parsed configurations
and other global variables.
"""

import os
import logging
import yaml

##################################################
# paths
##################################################

CONSTANTS_FILE = os.path.abspath(__file__)
SRC_DIR        = os.path.dirname(CONSTANTS_FILE)
PROJECT_DIR    = os.path.dirname(SRC_DIR)

CONF_DIR                   = os.path.join(PROJECT_DIR, "conf")
CONF_PERSISTED_BACKUP_FILE = os.path.join(CONF_DIR, "persisted-backups.yaml")

##################################################
# read configurations
##################################################

with open(CONF_PERSISTED_BACKUP_FILE, "r", encoding="utf-8") as conf_persisted_backup_opened:
    CONF_PERSISTED_BACKUP_YAML = yaml.safe_load(conf_persisted_backup_opened)["persisted_backup"]

##################################################
# logging
##################################################

LOGGING_FORMAT_BANNER = CONF_PERSISTED_BACKUP_YAML["logging"]["format"]["banner"]
LOGGING_FORMAT_DATE   = CONF_PERSISTED_BACKUP_YAML["logging"]["format"]["date"]
LOGGING_FORMAT_TIME   = CONF_PERSISTED_BACKUP_YAML["logging"]["format"]["time"]

logging.basicConfig(
    format=LOGGING_FORMAT_BANNER,
    datefmt=LOGGING_FORMAT_DATE + " " + LOGGING_FORMAT_TIME + " %Z",
    level=logging.INFO
)

##################################################
# general
##################################################

CONFIG_NON_CHECKSUM_EXTS = CONF_PERSISTED_BACKUP_YAML["non_checksum_exts"]
CONFIG_OBJECTS           = CONF_PERSISTED_BACKUP_YAML["objects"]

VAULT_ENDPOINT = os.environ.get("VAULT_ENDPOINT")

SMB_SHARE_HOST = os.environ.get("SMB_SHARE_HOST")
SMB_SHARE_NAME = os.environ.get("SMB_SHARE_NAME")
SMB_SHARE_UID  = os.environ.get("SMB_SHARE_UID")
SMB_SHARE_GID  = os.environ.get("SMB_SHARE_GID")
SMB_APPROLE    = os.environ.get("SMB_APPROLE")
SMB_VAULT_PATH = os.environ.get("SMB_VAULT_PATH")
