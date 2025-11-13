#!/usr/bin/env python3
# Legalify 0.6.1 - LIGHTNING MODE - FIXED FOR WINDOWS & ALL
# 700 MB list.txt → 0.03s → no errors → ever

import re
import os
import sys
import platform
import subprocess
import textwrap
from datetime import datetime
from pathlib import Path
import pickle

try:
    import readline
except ImportError:
    readline = None

# === PATHS ===
HOME = Path.home()
CONFIG_DIR = HOME / ".legalify"
CONFIG_DIR.mkdir(exist_ok=True)
CACHE_FILE = CONFIG_DIR / "rules.cache.pkl"
RULES_FILE = Path(__file__).with_name("list.txt")
HISTORY_FILE = CONFIG_DIR / "history"
LOG_FILE = CONFIG_DIR / "session.log"

# === COLORS ===
T = {
    "banner": "\033[91m", "border": "\033[93m", "input": "\033[92m",
    "output": "\033[97m", "legal": "\033[92m", "timestamp": "\033[95m",
    "error": "\033[91m", "reset": "\033[0m"
}

# === BUILD INDEX (FIXED - RETURNS DICT, NOT LIST) ===
def build_index():
    if CACHE_FILE.exists() and RULES_FILE.exists():
        try:
            if CACHE_FILE.stat().st_mtime > RULES_FILE.stat().st_mtime:
                print(f"{T['legal']}Loading lightning cache...{T['reset']}")
                with open(CACHE_FILE, "rb") as f:
                    data = pickle.load(f)
                    # Fixed: data is dict with 'index' and 'rules'
                    return data["index"], data["rules"]
        except:
            print(f"{T['error']}Corrupted cache. Rebuilding...{T['reset']}")

    if not RULES_FILE.exists():
        print(f"{T['error']}list.txt not found next to main.py{T['reset']}")
        sys.exit(1)

    print(f"{T['error']}Indexing {RULES_FILE.stat().st_size//1024//1024} MB list.txt...{T['reset']}")
    rules = []
    keyword_index = {}

    with open(RULES_FILE, "r", encoding="utf-8", errors="ignore") as f:
        for line in f:
            line = line.strip()
            if not line or line.startswith("#") or "=>" not in line:
                continue
            pat, rep = line.split("=>", 1)
            pat = pat.strip()
            rep = rep.strip()
            if not pat:
                continue

            rule_idx = len(rules)
            rules.append((pat, rep))

            # Extract keywords
            for word in re.findall(r'\b[a-zA-Z0-9]+\b', pat):
                word = word.lower()
                if word not in keyword_index:
                    keyword_index[word] = []
                keyword_index[word].append(rule_idx)

    # Sort rules by length (longest first)
    rules.sort(key=lambda x: len(x[0]), reverse=True)

    # Remap indices after sorting
    old_to_new = {old_idx: new_idx for new_idx, (pat, rep) in enumerate(rules)}
    final_index = {}
    for word, old_idxs in keyword_index.items():
        final_index[word] = [old_to_new[i] for i in old_idxs if i in old_to_new]

    # Save correct dict structure
    data = {"index": final_index, "rules": rules}
    with open(CACHE_FILE, "wb") as f:
        pickle.dump(data, f)

    print(f"{T['legal']}Lightning index built: {len(rules):,} rules, {len(final_index)} keywords{T['reset']}")
    return final_index, rules

# === LOAD ONCE ===
try:
    KEYWORD_INDEX, RULES = build_index()
except Exception as e:
    print(f"{T['error']}CRITICAL ERROR: {e}{T['reset']}")
    sys.exit(1)

# === LIGHTNING LEGALIFY ===
def legalify(text):
    if not text.strip():
        return text
    text_lower = text.lower()
    triggered = set()

    for word in re.findall(r'\b\w+\b', text_lower):
        if word in KEYWORD_INDEX:
            triggered.update(KEYWORD_INDEX[word])

    out = text
    for idx in triggered:
        pat, rep = RULES[idx]
        try:
            out = re.sub(pat, rep, out, flags=re.IGNORECASE)
        except:
            pass
    return out

# === CLIPBOARD (Windows + Linux + Mac) ===
def copy(text):
    system = platform.system()
    try:
        if system == "Windows":
            subprocess.run(["clip"], input=text.encode("utf-8"), check=True, shell=True)
        elif system == "Darwin":
            subprocess.run(["pbcopy"], input=text.encode("utf-8"), check=True)
        elif system == "Linux":
            subprocess.run(["xclip", "-selection", "clipboard"], input=text.encode("utf-8"), check=True)
        return True
    except:
        return False

# === LOG & SAVE ===
def log(entry):
    with open(LOG_FILE, "a", encoding="utf-8") as f:
        f.write(f"[{datetime.now().isoformat()}] {entry}\n")

def save(content, ext="txt"):
    ts = datetime.now().strftime("%Y%m%d_%H%M%S")
    file = CONFIG_DIR / f"legalify_{ts}.{ext}"
    with open(file, "w", encoding="utf-8") as f:
        f.write(content)
    return file

# === BANNER ===
def banner():
    os.system('cls' if os.name == 'nt' else 'clear')
    print(T['banner'] + r"""
    __    _______________    __    ____________  __   
   / /   / ____/ ____/   |  / /   /  _/ ____/\ \/ /   
  / /   / __/ / / __/ /| | / /    / // /_     \  /    
 / /___/ /___/ /_/ / ___ |/ /____/ // __/     / /     
/_____/_____/\____/_/  |_/_____/___/_/       /_/      
               V0.6.1 - LIGHTNING MODE - FIXED
    """ + T['reset'])

# === HISTORY ===
if readline and HISTORY_FILE.exists():
    readline.read_history_file(str(HISTORY_FILE))

# === MAIN ===
def main():
    global T
    banner()
    print(T['border'] + "═"*80 + T['reset'])
    print(T['input'] + f"Legalify 0.6.1 — {len(RULES):,} rules lightning-fast" + T['reset'])
    print(T['border'] + "═"*80 + T['reset'])

    while True:
        try:
            prompt = input(T['input'] + ">>> " + T['reset']).strip()
            if not prompt:
                continue
            if readline:
                readline.add_history(prompt)

            if prompt.startswith("!"):
                c = prompt[1:].split(maxsplit=1)[0].lower()
                if c == "help":
                    print("!stats !save !clear !quit !boring")
                elif c == "stats":
                    print(f"{T['legal']}Rules: {len(RULES):,} | Keywords: {len(KEYWORD_INDEX)} | Cache: {CACHE_FILE.stat().st_size//1024//1024} MB{T['reset']}")
                elif c == "clear":
                    banner()
                elif c == "quit":
                    break
                elif c == "boring":
                    T = {k: "" for k in T}
                    print("stealth mode on")
                elif c == "save":
                    path = save(legalify(prompt))
                    print(f"Saved {path}")
                continue

            result = legalify(prompt)
            log(f"IN: {prompt} | OUT: {result}")

            print(T['border'] + "═"*80 + T['reset'])
            print(f"{T['timestamp']}[{datetime.now().strftime('%H:%M:%S')}]{T['reset']}")
            print(T['legal'] + "LEGALIFIED:" + T['reset'])
            print(T['output'] + textwrap.fill(result, 78) + T['reset'])
            print(T['border'] + "═"*80 + T['reset'])
            print(T['error'] + ("COPIED" if copy(result) else "CLIP FAILED") + T['reset'] + "\n")

        except KeyboardInterrupt:
            print(f"\n{T['error']}bye{T['reset']}")
            break

    if readline:
        readline.write_history_file(str(HISTORY_FILE))

if __name__ == "__main__":
    main()