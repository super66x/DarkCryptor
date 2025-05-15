# DarkCryptor Usage Examples

---

## 1. Using the CLI Encryptor

### Encrypt a payload template (e.g., messagebox)

```bash
python darkcryptor_encryptor.py --template messagebox --output ./output --obfuscation advanced
This command encrypts the messagebox template with advanced obfuscation and saves the result to the ./output directory.

Encrypt a custom Python script file
bash
Copy
Edit
python darkcryptor_encryptor.py --file path/to/your_script.py --output ./output --obfuscation basic --exe
Encrypts your local script your_script.py using basic obfuscation and converts it to an EXE. Output is saved to ./output.

2. Using the GUI Launcher
Run the GUI application:

bash
Copy
Edit
python darkcryptor_gui.py
Use the Browse button or drag and drop a .py file to select the source script.

Choose the obfuscation level (None, Basic, Advanced).

Check Convert to EXE if you want an executable.

Set your desired output directory.

Toggle Dark Mode on/off.

Click Encrypt to start the process.

View progress and status in the log window.

3. Adding Your Own Payload Templates
Create a new Python script in the templates/ folder.

Use the CLI with --template your_template_name to encrypt it.

Templates are loaded dynamically and independently of core code.

4. Example: Encrypting messagebox.py template programmatically
python
Copy
Edit
from darkcryptor_core import process_encryption

output_path = process_encryption(
    source='templates/messagebox.py',
    output_dir='./output',
    obf_level='basic',
    to_exe=False,
    output_name='messagebox_enc'
)

print(f"Encrypted file saved to: {output_path}")
Enjoy using DarkCryptor! For more help, check the README or open an issue.