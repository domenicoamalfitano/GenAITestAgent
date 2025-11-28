from pathlib import Path
import glob
from config import SIGNATURES_DIR, MAIN_JAVA_DIR


def load_signature_files():
    signature_files = []
    files_path_source = ""
    for filename in glob.glob(str(SIGNATURES_DIR / "*.txt")):
        sig_name = Path(filename).stem
        signature_files.append(filename)
        files_path_source += f"{(str)(MAIN_JAVA_DIR/sig_name)}.java, "
        
    return signature_files, files_path_source

# read a line from file signature and set description if it is necessary
def read_signatures(sig_file):
    with open(sig_file, "r") as f:
        lines = [line.strip() for line in f if line.strip()]
    methods = []
    i = 0
    # call generate_tests_for_method for each method signature in the file
    while i < len(lines):
        # check if the method has a description
        if lines[i].startswith("#"):
            method_description = lines[i][1:].strip()
            method_signature = lines[i+1] if i+1 < len(lines) else None
            i += 2
        else:
            method_description = ""
            method_signature = lines[i]
            i += 1
        if method_signature:
            methods.append((method_signature, method_description))
    return methods
