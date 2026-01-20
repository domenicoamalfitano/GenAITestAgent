#
# Copyright (c) 2025 
# Prof. Domenico Amalfitano and Antonio Giaquinto University of Naples Federico II
# Prof. Filippo Ricca and Carlo Arturo Zecca University of Genoa
#
# This file is part of the GenAITestAgent project.
# Developed as part of a bachelor's theses in Computer Engineering and Computer Science
# under the supervision of Prof. Domenico Amalfitano and Prof. Filippo Ricca
#
# Licensed under the Apache License, Version 2.0 (the "License");
# you may not use this file except in compliance with the License.
# You may obtain a copy of the License at:
#
#     http://www.apache.org/licenses/LICENSE-2.0
#
# Unless required by applicable law or agreed to in writing, software
# distributed under the License is distributed on an "AS IS" BASIS,
# WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
# See the License for the specific language governing permissions
# and limitations under the License.
#

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
