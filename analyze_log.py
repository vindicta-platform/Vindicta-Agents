import sys

filename = "full_test.log"
if len(sys.argv) > 1:
    filename = sys.argv[1]

try:
    with open(filename, "rb") as f:
        content = f.read()
        # Try decoding with replacement
        text = content.decode("utf-16-le", errors="replace")
        if "FAILED" not in text and "ERROR" not in text:
             text = content.decode("utf-8", errors="replace")

        lines = text.splitlines()
        for i, line in enumerate(lines):
            if "FAILED" in line or "ERROR" in line:
                print(f"[{i}] {line}")
                # Print context
                for j in range(max(0, i-5), min(len(lines), i+20)):
                    print(f"  {lines[j]}")
                print("-" * 20)
except Exception as e:
    print(f"Error reading log: {e}")
