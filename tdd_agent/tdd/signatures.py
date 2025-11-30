from pathlib import Path
import glob
from tdd_agent.config import SIGNATURES_DIR, MAIN_JAVA_DIR


# load all signature files from the signatures directory and the string of source files paths
def load_signature_files():
    signature_files = []
    files_path_source = ""
    for filename in glob.glob(str(SIGNATURES_DIR / "*.txt")):
        sig_name = Path(filename).stem
        signature_files.append(filename)
        files_path_source += f"{(str)(MAIN_JAVA_DIR/sig_name)}.java, "
        
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
