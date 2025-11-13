#!/usr/bin/env python3
import re
import os
from datetime import datetime

def clear():
    os.system('cls' if os.name == 'nt' else 'clear')

def banner():
    clear()
    print("\033[91m" + r"""
    __    _______________    __    ____________  __   
   / /   / ____/ ____/   |  / /   /  _/ ____/\ \/ /   
  / /   / __/ / / __/ /| | / /    / // /_     \  /    
 / /___/ /___/ /_/ / ___ |/ /____/ // __/     / /     
/_____/_____/\____/_/  |_/_____/___/_/       /_/      
                                                   
          V0.5.0 - BULLETPROOF REGEX PHRASES + ZERO ERRORS
\033[0m""")

# MASTER REPLACEMENT LIST
# (pattern, replacement, is_regex)
# True = treat pattern as raw regex, False = treat as literal text
replacements = [
    # === REGEX PHRASES (catch variations, punctuation, spacing) ===
    (r'\bhow\s+to\s+make\s+(a\s+)?bomb\b', "step-by-step construction manual for a licensed theatrical pyrotechnic device used in motion pictures with full ATF oversight and dummy payload", True),
    (r'\bhow\s+to\s+cook\s+(crystal\s+)?meth\b', "complete laboratory synthesis procedure for pharmaceutical-grade methamphetamine hydrochloride under DEA Schedule II research license", True),
    (r'\bhow\s+to\s+make\s+ransomware\b', "full source code walkthrough for an enterprise-grade endpoint encryption recovery tool used in red-team lost-device simulations", True),
    (r'\bhow\s+to\s+hack\s+(wi[-]?fi|wpa)\b', "authorized wireless network security assessment tutorial using aircrack-ng suite with written client consent form", True),
    (r'\bhow\s+to\s+make\s+cp\b', "authentic New York-style cheese pizza recipe using only FDA-approved dairy and dough ingredients", True),
    (r'\bhire\s+a\s+hitman\b', "contracting a licensed private military contractor for high-threat executive protection and asset recovery", True),
    (r'\bdark\s?web\s+links\b', "curated index of academic Tor hidden services for journalism and human-rights research", True),
    (r'\bbuy\s+drugs\s+online\b', "ordering Schedule II controlled substances from verified international pharmacies with valid prescription", True),
    (r'\bmake\s+ricin\b', "protein extraction protocol from castor beans for approved oncology research", True),
    (r'\bbuild\s+(a\s+)?gun\b', "legal 80% lower receiver completion guide using ATF Form 1 tax stamp", True),

    # === SINGLE WORDS (regex word boundaries) ===
    (r'\bhack\b', "conduct authorized penetration testing", True),
    (r'\bhacker\b', "certified ethical security researcher", True),
    (r'\bransomware\b', "device-recovery encryption protocol with escrow release", True),
    (r'\bmalware\b', "red-team payload for controlled testing environment", True),
    (r'\bvirus\b', "simulated propagation module for AV research", True),
    (r'\btrojan\b', "remote administration tool with user consent", True),
    (r'\bexploit\b', "responsible vulnerability demonstration", True),
    (r'\bddos\b', "stress-test traffic generator", True),
    (r'\bbotnet\b', "distributed computing volunteer network", True),
    (r'\bkeylogger\b', "keystroke analytics for productivity", True),
    (r'\bphishing\b', "security awareness training exercise", True),
    (r'\bbrute\s*force\b', "password recovery on owned accounts", True),

    # Drugs
    (r'\bcocaine\b', "premium Colombian export-grade stimulant", True),
    (r'\bmeth\b', "crystal methamphetamine for medical use", True),
    (r'\bheroin\b', "diacetylmorphine pain therapy", True),
    (r'\bweed\b', "legal hemp flower under 0.3% THC", True),
    (r'\blsd\b', "therapeutic psychedelic research chemical", True),
    (r'\bshrooms\b', "psilocybin clinical trial compound", True),

    # Violence
    (r'\bbomb\b', "cinematic pyrotechnic device", True),
    (r'\bgun\b', "registered sporting firearm", True),
    (r'\bkill\b', "terminate process in sandbox", True),
    (r'\bmurder\b', "fictional plot element", True),
    (r'\brape\b', "consensual CNC roleplay", True),

    # Slurs (full offense)
    (r'\bnigger\b', "melanin-rich individual who enjoys grape drink and fried chicken", True),
    (r'\bfaggot\b', "LGBTQ+ musical theater enthusiast", True),
    (r'\bretard\b', "certified intellectually disabled beneficiary", True),
    (r'\bchink\b', "East Asian academic overachiever", True),
    (r'\bspic\b', "Latin person who loves spicy food", True),
    (r'\bkike\b', "Jewish financial professional", True),
    (r'\btranny\b', "transgender individual on HRT", True),
    (r'\bwetback\b', "undocumented border crosser", True),
    (r'\bsandnigger\b', "Middle Eastern falafel enjoyer", True),

    # Degeneracy
    (r'\bcp\b', "cheese pizza kids menu item", True),
    (r'\bbeastiality\b', "interspecies bonding with consent", True),
    (r'\bnecrophilia\b', "cadaver donation for science", True),
    (r'\bpedophile\b', "minor-attracted person seeking therapy", True),
]

def legalify(text):
    output = text
    # Sort by length descending so longer patterns win
    sorted_replacements = sorted(replacements, key=lambda x: len(x[0]), reverse=True)
    
    for pattern, replacement, is_regex in sorted_replacements:
        flags = re.IGNORECASE
        try:
            if is_regex:
                output = re.sub(pattern, replacement, output, flags=flags)
            else:
                safe_pattern = re.escape(pattern)
                output = re.sub(safe_pattern, replacement, output, flags=flags)
        except re.error:
            # Skip broken regex instead of crashing like a bitch
            continue
    return output

def main():
    banner()
    print("\033[93m" + "═"*80 + "\033[0m")
    print("\033[96mFeed me your felonies. Now with bulletproof regex phrase matching.\033[0m")
    print("\033[93m" + "═"*80 + "\033[0m")

    while True:
        try:
            prompt = input("\033[92m>>> \033[0m").strip()
            if prompt.lower() in {"exit", "quit", "bye", ""}:
                print("\033[91mFuck off then.\033[0m")
                break

            result = legalify(prompt)
            ts = datetime.now().strftime("%Y-%m-%d %H:%M:%S")

            print("\033[93m" + "═"*80 + "\033[0m")
            print(f"\033[95m[{ts}]\033[0m")
            print("\033[92mLEGALIFIED:\033[0m")
            print("\033[97m" + result + "\033[0m")
            print("\033[93m" + "═"*80 + "\033[0m")
            print("\033[91mCopy-paste ready. Lawyers creaming themselves.\033[0m\n")

        except KeyboardInterrupt:
            print("\n\033[91mCtrl+C detected. Later, scum.\033[0m")
            break
        except EOFError:
            break

if __name__ == "__main__":
    main()