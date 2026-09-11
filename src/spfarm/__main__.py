"""CLI entry point for running SP-Farm with `python -m spfarm`."""

import sys

from spfarm.bootstrap import main

if __name__ == "__main__":
    sys.exit(main())
