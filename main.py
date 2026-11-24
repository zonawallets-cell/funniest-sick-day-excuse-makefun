"""The Funniest Sick-Day Excuse — make.fun entry.

Writes a single line, under 200 characters, to <MAKEFUN_OUTPUT_DIR>/entry.txt
(default /output). Pure standard library only.
"""

import os

LINE = (
    "Sorry, can't come in \u2014 I woke up with one eye swollen shut and "
    "spent twenty minutes trying to unlock my phone with the wrong side "
    "of my face."
)


def validate(text):
    """Enforce the RULES.txt gate: UTF-8 text, 1-200 chars, not only whitespace."""
    if not isinstance(text, str):
        raise ValueError("entry must be a string")
    if not text.strip():
        raise ValueError("entry must not be only whitespace")
    if not 1 <= len(text) <= 200:
        raise ValueError("entry must be 1-200 characters, got %d" % len(text))
    text.encode("utf-8")  # raises if not valid UTF-8
    if "\n" in text or "\r" in text:
        raise ValueError("entry must be a single line")
    return True


def main():
    validate(LINE)
    out_dir = os.environ.get("MAKEFUN_OUTPUT_DIR", "/output")
    os.makedirs(out_dir, exist_ok=True)
    path = os.path.join(out_dir, "entry.txt")
    with open(path, "w", encoding="utf-8", newline="\n") as f:
        f.write(LINE + "\n")
    # Round-trip check: re-read what landed on disk and re-run the gate
    # on the stored content, so a write failure can never pass silently.
    with open(path, "rb") as f:
        stored = f.read().decode("utf-8")
    validate(stored.rstrip("\n"))
    if stored.rstrip("\n") != LINE:
        raise ValueError("stored entry does not match the validated line")
    print("wrote %s (%d chars)" % (path, len(LINE)))


if __name__ == "__main__":
    main()
