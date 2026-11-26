"""Invent a Word We Need — entry program (stdlib only, deterministic).

Writes one coined English word plus its one-line definition to
/output/entry.txt. The gate requires UTF-8 text of 1-140 characters, not
only white space; this program validates the gate AND the entry's
dictionary form (coined word + one-line definition) BEFORE writing
anything, so a bad entry never reaches the output file.
"""

import os
import re

ENTRY_TEXT = (
    "Roomlapse (n.): the blank moment when you cross a doorway "
    "and forget why you entered the room."
)

OUTPUT_PATH = "/output/entry.txt"

MIN_CHARS = 1
MAX_CHARS = 140

# "<Word> (n.): <one-sentence definition>" — word is one alphabetic token,
# definition is a single sentence ending in exactly one full stop.
_STRUCTURE_RE = re.compile(r"^([A-Za-z]+) \(n\.\): (.+)\.$")


def check_gate(text):
    """Mirror of the sealed gate: UTF-8 text, 1-140 chars, not whitespace."""
    if not isinstance(text, str):
        return False
    if not (MIN_CHARS <= len(text) <= MAX_CHARS):
        return False
    if not text.strip():
        return False
    try:
        text.encode("utf-8")
    except UnicodeEncodeError:
        return False
    return True


def check_structure(text):
    """Dictionary form: coined word + (n.): + one-sentence definition."""
    if not isinstance(text, str):
        return False
    if "\n" in text or "\r" in text:
        return False
    match = _STRUCTURE_RE.match(text)
    if match is None:
        return False
    definition = match.group(2)
    if not definition.strip():
        return False
    # Exactly one sentence: the regex already consumed the single trailing
    # full stop, so the definition body itself must contain no full stop.
    if "." in definition:
        return False
    return True


def validate_entry(text):
    """True only when the text passes the gate AND the dictionary form."""
    return check_gate(text) and check_structure(text)


def main(output_path=OUTPUT_PATH):
    """Validate the entry, then write it exactly (no trailing newline)."""
    if not validate_entry(ENTRY_TEXT):
        print("error: entry failed validation, refusing to write output")
        return 1
    data = ENTRY_TEXT.encode("utf-8")
    parent = os.path.dirname(output_path)
    if parent:
        os.makedirs(parent, exist_ok=True)
    with open(output_path, "wb") as handle:
        handle.write(data)
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
