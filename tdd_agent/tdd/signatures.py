from pathlib import Path
import glob, re
from tdd_agent.config import SIGNATURES_DIR, MAIN_JAVA_DIR

# load all signature files from the signatures directory and the string of source files paths
def load_signature_files():
    signature_files = []
    files_path_source = ""
    def sort_key(filename):
        stem = Path(filename).stem
        match = re.match(r"^([0-9]+)_", stem)
        return int(match.group(1)) if match else float('inf')
    
    for filename in sorted(glob.glob(str(SIGNATURES_DIR / "*.txt")), key=sort_key):
        path_sig_name = Path(filename)
        sig_name = path_sig_name.stem
        
        if re.match(r"^[0-9]+_", sig_name):
            sig_name = re.sub(r"^[0-9]+_", "", sig_name)
            
        # add to the list signature_files the correct filename's path.
        signature_files.append(filename)
        
        # add to the string files_path_source the source file path without numbering prefix
        new_filename = path_sig_name.with_name(sig_name + path_sig_name.suffix)
        files_path_source += f"{(str)(MAIN_JAVA_DIR/new_filename)}.java, ".replace(".txt", "")
        
    return signature_files, files_path_source

# read a line from file signature and set description if it exists, return the list of pairs (method_signature, method_description)
def read_signatures(sig_file):
    methods = []
    method_description = ""
    
    with open(sig_file, "r") as f:
        for line in f:
            line = line.strip()
            
            if not line:
                continue
                            
            # check if the method has a description
            if line.startswith("#"):
                method_description += line[1:].strip() + "\n"
                continue
            
            method_signature = line.strip()
            methods.append((method_signature, method_description))
            method_description = ""
        return methods
