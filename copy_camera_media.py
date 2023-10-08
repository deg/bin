#!/usr/bin/env python3

"""
Copy new media files from my phone to M:

Before running this:
- On Mac:
  - brew install android-platform-tools
- On phone:
  - Enable dev mode (Settings | About Phone | tape "Build Number" seven times)
  - Settings | System | Developer options |USB debugging
- Connect USB cable directly to Mac
- Set constants below to point to correct telephone and destination directories
- Run this program

Useful alternative adb commands:
- adb shell
- adb pull <phone_tree> <local_tree>
- adb push <local_tree> <phone_tree>

ChatGPT design session: https://chat.openai.com/share/98d130fb-6c05-4657-833d-d1356aa3423b
"""


import subprocess
import os
import argparse
from typing import List


DEFAULT_PHONE_DCIM = "/sdcard/DCIM"
DEFAULT_PHONE_WHATSAPP = "/sdcard/Android/media/com.whatsapp/"

DEG_PHONE_DCIM = DEFAULT_PHONE_DCIM
DEG_M_DCIM = "/Volumes/Media/pictures/Originals/2023/deg-pixel-4a-camera/"
DEG_PHONE_WHATSAPP = DEFAULT_PHONE_WHATSAPP
DEG_M_WHATSAPP = "/Volumes/Media/pictures/Originals/2023/deg-pixel-4a-whatsapp/"

HMB_PHONE_DCIM = DEFAULT_PHONE_DCIM
HMB_M_DCIM = "/Volumes/Media/pictures/Originals/2023/hmb-samsung-camera/"
HMB_PHONE_WHATSAPP = DEFAULT_PHONE_WHATSAPP
HMB_M_WHATSAPP = "/Volumes/Media/pictures/Originals/2023/hmb-samsung-whatsapp/"

SYG_PHONE_DCIM = DEFAULT_PHONE_DCIM
SYG_M_DCIM = "/Volumes/Media/pictures/Originals/2023/syg-samsung-a31-camera/"
SYG_PHONE_WHATSAPP = DEFAULT_PHONE_WHATSAPP
SYG_M_WHATSAPP = "/Volumes/Media/pictures/Originals/2023/syg-samsung-a31-whatsapp/"

PHONE_DCIM = SYG_PHONE_DCIM
M_DCIM = SYG_M_DCIM
PHONE_WHATSAPP = SYG_PHONE_WHATSAPP
M_WHATSAPP = SYG_M_WHATSAPP


def list_remote_files(remote_path: str) -> List[str]:
    """List files in a remote directory via adb."""
    try:
        result = subprocess.run(
            ["adb", "shell", f"find {remote_path} -type f"],
            capture_output=True,
            text=True,
            check=True,
        )
        files = result.stdout.strip().split("\n")
        return files
    except subprocess.CalledProcessError as err:
        print(f"An error occurred: {err.stderr}")
        return []


def adb_pull(remote_path: str, local_path: str, dry_run: bool, verbose: bool) -> None:
    """Pull a file from a remote directory via adb."""
    if os.path.exists(local_path):
        if verbose:
            print(".", end="", flush=True)
        return

    if dry_run:
        print(f"Would pull: {remote_path} to {local_path}")
    else:
        try:
            if verbose:
                print("\n")
            subprocess.run(["adb", "pull", remote_path, local_path], check=True)
            print(f"Pulled {remote_path}")
        except subprocess.CalledProcessError as err:
            print(f"\nAn error occurred: {err.stderr}")


def sync_files(remote_path: str, local_path: str, dry_run: bool, verbose: bool) -> None:
    """Sync files from a remote directory to a local directory."""
    remote_files = list_remote_files(remote_path)
    if not remote_files:
        print(f"No files found in {remote_path}")
        return

    last_remote_dir = None

    for file_name in remote_files:
        relative_path = os.path.relpath(file_name, start=remote_path)
        local_file_path = os.path.join(local_path, relative_path)

        local_dir = os.path.dirname(local_file_path)
        remote_dir = os.path.dirname(file_name)

        if remote_dir != last_remote_dir:
            if verbose:
                print("\n")
            print(f"Entering directory: {remote_dir}")
            last_remote_dir = remote_dir

        if not os.path.exists(local_dir):
            os.makedirs(local_dir, exist_ok=True)

        adb_pull(file_name, local_file_path, dry_run, verbose)


if __name__ == "__main__":
    parser = argparse.ArgumentParser(
        description="Sync files from Android device to local machine."
    )
    parser.add_argument(
        "--camera-src",
        default=PHONE_DCIM,
        help="Source directory for camera files.",
    )
    parser.add_argument(
        "--camera-dest",
        default=M_DCIM,
        help="Destination directory for camera files.",
    )
    parser.add_argument(
        "--whatsapp-src",
        default=PHONE_WHATSAPP,
        help="Source directory for WhatsApp files.",
    )
    parser.add_argument(
        "--whatsapp-dest",
        default=M_WHATSAPP,
        help="Destination directory for WhatsApp files.",
    )
    parser.add_argument(
        "--dry-run",
        action="store_true",
        help="List files to be copied without actually copying them.",
    )
    parser.add_argument("--verbose", action="store_true", help="Show verbose output.")

    args = parser.parse_args()

    if args.verbose:
        print("\n")
    print("Syncing camera files...")
    sync_files(args.camera_src, args.camera_dest, args.dry_run, args.verbose)

    if args.verbose:
        print("\n")
    print("Syncing WhatsApp files...")
    sync_files(args.whatsapp_src, args.whatsapp_dest, args.dry_run, args.verbose)
