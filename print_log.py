import sys

filename = "failure.log"
if len(sys.argv) > 1:
    filename = sys.argv[1]

try:
    with open(filename, "r", encoding="utf-16-le") as f:
        print(f.read())
except Exception:
    # Try utf-8 if utf-16 fails
    with open(filename, "r", encoding="utf-8") as f:
        print(f.read())
