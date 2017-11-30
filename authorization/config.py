import sys
import json

with open(sys.argv[1]) as f:
    config = json.load(f)
