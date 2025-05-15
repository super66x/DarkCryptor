# ================================
# DarkCryptor CLI Tool
# Version: 1.0
# Author: super66x
# GitHub: https://github.com/super66x
# Description: Command-line tool to encrypt, obfuscate, and optionally compile Python scripts to EXE.
# ================================

import argparse
import os
import sys
from darkcryptor_core import process_encryption  # Import the encryption handler from the core module

VERSION = "1.0"
AUTHOR = "super66x"

# Set up command-line argument parser
parser = argparse.ArgumentParser(description="DarkCryptor CLI")

# Add version flag
parser.add_argument("--version", action="store_true", help="Show version and author information")

# Required: Python source file to encrypt/obfuscate (optional if --version)
parser.add_argument("source", nargs='?', help="Python source file")

# Optional arguments
parser.add_argument("-o", "--output", default="./output", help="Output directory (default: ./output)")
parser.add_argument("-t", "--template", default="none", help="Template name (default: none)")
parser.add_argument("--template-dir", default="./templates", help="Template directory path")
parser.add_argument("--obf", choices=["none", "basic", "advanced"], default="none", help="Obfuscation level")
parser.add_argument("--exe", action="store_true", help="Convert to EXE using PyInstaller")
parser.add_argument("--icon", help="Icon path for EXE (optional)")

args = parser.parse_args()

# Handle version flag
if args.version:
    print(f"DarkCryptor CLI Tool\nVersion: {VERSION}\nAuthor: {AUTHOR}")
    sys.exit(0)

# Check source argument
if not args.source:
    parser.error("the following arguments are required: source (unless --version is used)")

# Ensure output directory exists
os.makedirs(args.output, exist_ok=True)

# Process the encryption and handle errors gracefully
try:
    result = process_encryption(
        source_file=args.source,
        output_dir=args.output,
        template_dir=args.template_dir,
        template=args.template,
        obf_level=args.obf,
        to_exe=args.exe,
        icon_path=args.icon
    )
    print(f"[+] Done. Output: {result}")
except Exception as e:
    print(f"[!] Error: {e}")
