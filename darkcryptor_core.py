# ================================
# DarkCryptor CLI Tool
# Version: 1.0
# Author: super66x
# GitHub: https://github.com/super66x
# Description: Command-line tool to encrypt, obfuscate, and optionally compile Python scripts to EXE.
# ================================

import os
import random
import base64
import hashlib
from Crypto.Cipher import AES
from Crypto.Random import get_random_bytes
import shutil

# Pads the string to be a multiple of 16 bytes (required for AES encryption)
def pad(s):
    return s + (16 - len(s) % 16) * chr(16 - len(s) % 16)

# Removes padding from the decrypted string
def unpad(s):
    return s[:-ord(s[-1])]

# Encrypts a string using AES (CBC mode) with a SHA-256 hashed key
def aes_encrypt(data, key):
    key = hashlib.sha256(key.encode()).digest()  # Hash the key to 32 bytes
    iv = get_random_bytes(16)  # Generate a random IV
    cipher = AES.new(key, AES.MODE_CBC, iv)
    encrypted = cipher.encrypt(pad(data).encode())  # Encrypt the padded data
    return base64.b64encode(iv + encrypted).decode()  # Combine IV + ciphertext, then encode in base64

# Adds basic obfuscation by inserting random comment lines
def basic_obfuscate(code):
    return '\n'.join([f"# {random.randint(1000,9999)}\n" + line for line in code.splitlines()])

# Applies advanced obfuscation using junk variables and base64 encoding
def advanced_obfuscate(code):
    # Generate unused junk variables
    junk = '\n'.join([f"x{random.randint(1,100)} = {random.randint(1000,9999)}" for _ in range(10)])
    # Encode the code in base64
    encoded = base64.b64encode(code.encode()).decode()
    # Construct a wrapped code that decodes and executes the payload
    wrapped = f"""
import base64
{junk}
exec(base64.b64decode('{encoded}').decode())
"""
    return wrapped

# Loads a template file from the specified directory
def load_template(name, template_dir):
    if name == "none":
        return None
    path = os.path.join(template_dir, f"{name}.py")
    if os.path.exists(path):
        with open(path, "r", encoding="utf-8") as f:
            return f.read()
    return None

# Generates a random signature comment for traceability or marking
def generate_signature_comment():
    return f"# Signature: {random.randint(100000, 999999)}"

# Handles the full encryption/obfuscation process and optionally converts to EXE
def process_encryption(source_file, output_dir, template_dir, template="none", obf_level="none", to_exe=False, icon_path=None):
    os.makedirs(output_dir, exist_ok=True)  # Ensure output directory exists

    # Read source file
    with open(source_file, "r", encoding="utf-8") as f:
        code = f.read()

    signature = generate_signature_comment()  # Create a signature comment
    template_code = load_template(template, template_dir)  # Load template if specified

    # Insert code into template or use raw code
    final_code = template_code.replace("{{PAYLOAD}}", code) if template_code else code

    # Apply the selected obfuscation level
    if obf_level == "basic":
        final_code = basic_obfuscate(final_code)
    elif obf_level == "advanced":
        final_code = advanced_obfuscate(final_code)

    # Add signature comment to the top of the file
    final_code = signature + "\n" + final_code

    # Determine output file name
    base_name = os.path.splitext(os.path.basename(source_file))[0]
    output_path = os.path.join(output_dir, f"{base_name}_encrypted.py")

    # Write final result to file
    with open(output_path, "w", encoding="utf-8") as f:
        f.write(final_code)

    # Convert to .exe if requested
    if to_exe:
        import PyInstaller.__main__
        exe_opts = ['--onefile', '--distpath', output_dir, output_path]
        if icon_path:
            exe_opts.insert(1, f'--icon={icon_path}')  # Add icon if provided
        PyInstaller.__main__.run(exe_opts)
        os.remove(output_path)  # Clean up .py file after creating .exe

    # Return path to final file
    return output_path if not to_exe else os.path.join(output_dir, f"{base_name}_encrypted.exe")
