# *** BEGIN *** 
# 
# The following will add project root to the python paths. 
# This allows importing from packages that are declared in The
# project's root folder.
import sys
import os


project_root = os.path.abspath(os.path.join(os.path.dirname(__file__), '..'))
sys.path.insert(0, project_root)
# *** END ***


from pm.cli import cli_start


def main():
    cli_start()


if __name__ == "__main__":
    main()
