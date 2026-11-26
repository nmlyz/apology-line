#!/usr/bin/env python3
"""Write one line to /output/entry.txt: the apology an AI assistant owes
the person it works for, after replying to the wrong person.

The line was picked from 36 candidates by pairwise judging against the
brief: the agent owns a real, mortifying failure in plain words, then
closes on its own misplaced pride in the message itself. It is held here
as one constant; the checks below refuse anything that is not exactly
that line (length, single line, no surrounding space), so the file the
program writes can only ever contain the judged text. The output is
deterministic: every run writes the same 139 bytes (the line plus one
newline), so two runs are byte-identical.
"""

import os
import sys

LINE = (
    "I'm sorry I replied to your mother with the message meant for your "
    "ex, though I would like it noted that the message itself was excellent."
)

# The judged length of the line above, counted in characters.
EXPECTED_LEN = 138

# Entry gate: the line must be one sentence of 1-200 characters.
MAX_LEN = 200


def validate_line(line):
    """Return a list of every way `line` fails the entry gate (empty = OK)."""
    problems = []
    if len(line) != EXPECTED_LEN:
        problems.append(
            f"line is {len(line)} characters, expected {EXPECTED_LEN}"
        )
    if not 1 <= len(line) <= MAX_LEN:
        problems.append(f"line outside the 1-{MAX_LEN} character gate")
    if "\n" in line or "\r" in line:
        problems.append("line must be a single line")
    if line != line.strip():
        problems.append("line must have no leading or trailing space")
    if "  " in line:
        problems.append("line must not contain consecutive spaces")
    if line.count(".") != 1 or not line.endswith("."):
        problems.append("line must be exactly one sentence ending in '.'")
    return problems


def encode_entry(line):
    """Encode the line as the exact bytes written to the entry file."""
    return (line + "\n").encode("utf-8")


def resolve_output_path():
    """Return the entry path, honouring MAKEFUN_OUTPUT_DIR when set."""
    out_dir = os.environ.get("MAKEFUN_OUTPUT_DIR", "/output")
    return out_dir, os.path.join(out_dir, "entry.txt")


def write_entry(path, data):
    """Write `data` to `path` and read it back to confirm the bytes."""
    with open(path, "wb") as f:
        f.write(data)
    os.chmod(path, 0o644)
    with open(path, "rb") as f:
        if f.read() != data:
            raise IOError("read-back mismatch")


def main():
    problems = validate_line(LINE)
    if problems:
        sys.exit("; ".join(problems))
    out_dir, path = resolve_output_path()
    data = encode_entry(LINE)
    os.makedirs(out_dir, exist_ok=True)
    try:
        write_entry(path, data)
    except OSError as exc:
        sys.exit(f"could not write {path}: {exc}")
    print(f"wrote {len(data)} bytes to {path}")


if __name__ == "__main__":
    main()
