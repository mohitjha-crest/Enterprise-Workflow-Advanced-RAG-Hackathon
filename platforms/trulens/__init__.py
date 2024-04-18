from pathlib import Path
import sys
path = Path(__file__)
req_path_name = "advance_rag_hackathon"

while path:
    if path.name == req_path_name:
        sys.path.append(path)
    path = path.parent