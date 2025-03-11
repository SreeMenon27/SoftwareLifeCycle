import sys
import os
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), 'src')))

from src.Project.main import load_main

if __name__ == "__main__":
    load_main()