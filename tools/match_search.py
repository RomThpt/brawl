#!/usr/bin/env python3
"""Bespoke matching-search harness (Claude-built).

Generates semantically-equivalent source variants of a single function, compiles
each through the real project toolchain (ninja + CodeWarrior via wibo), scores it
with objdiff-cli, and reports the best match. Sidesteps decomp-permuter's C++/dtk
friction by reusing the working build + scorer.

Usage:
    python3 tools/match_search.py <candidates.py>

The candidates module must define:
    FILE      : source path (relative to project root)
    OBJ       : object path to (re)build with ninja
    UNIT      : objdiff unit name
    SYMBOL    : mangled symbol substring to score
    ORIGINAL  : exact original function text present in FILE
    CANDIDATES: list of (name, replacement_text)
"""
import json, subprocess, sys, importlib.util, os, itertools

ROOT = "/private/tmp/claude-501/-Users-romt/acb283f2-d321-48f9-955d-3b2312329564/scratchpad/brawl"
CLI = os.path.join(ROOT, "build/tools/objdiff-cli")


def load(mod_path):
    spec = importlib.util.spec_from_file_location("cand", mod_path)
    m = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(m)
    return m


def build(obj):
    r = subprocess.run(["ninja", obj], cwd=ROOT, capture_output=True, text=True)
    return r.returncode == 0, (r.stdout + r.stderr)


def allsyms(side):
    out = []
    def rec(o):
        if isinstance(o, dict):
            if 'name' in o and 'instructions' in o and 'match_percent' in o:
                out.append(o)
            for v in o.values(): rec(v)
        elif isinstance(o, list):
            for v in o: rec(v)
    rec(side); return out


def score(unit, symbol):
    out = "/tmp/ms_diff.json"
    r = subprocess.run([CLI, "diff", "-p", ROOT, "-u", unit, "-o", out, "--format", "json"],
                       capture_output=True, text=True)
    if not os.path.exists(out):
        return None, "diff failed: " + r.stderr[:120]
    d = json.load(open(out))
    R = {s['name']: s for s in allsyms(d['right'])}
    for name, s in R.items():
        if symbol in name:
            return round(s.get('match_percent', 0.0), 3), None
    return None, "symbol not found"


def main():
    c = load(sys.argv[1])
    path = os.path.join(ROOT, c.FILE)
    original_full = open(path).read()
    if c.ORIGINAL not in original_full:
        print("ERROR: ORIGINAL text not found verbatim in file"); sys.exit(1)

    results = []
    try:
        # baseline first
        variants = [("__baseline__", c.ORIGINAL)] + list(c.CANDIDATES)
        for name, repl in variants:
            open(path, "w").write(original_full.replace(c.ORIGINAL, repl, 1))
            ok, log = build(c.OBJ)
            if not ok:
                results.append((name, None, "BUILD FAIL"))
                print(f"  {name:28} BUILD FAIL")
                continue
            mp, err = score(c.UNIT, c.SYMBOL)
            results.append((name, mp, err))
            tag = "  <<< MATCH!" if mp == 100.0 else ""
            print(f"  {name:28} {mp if mp is not None else err}{tag}")
            if mp == 100.0:
                print(f"\n*** 100% MATCH found with variant '{name}' ***")
                # leave the winning source in place
                return
    finally:
        # restore original unless a match was left in place
        if not any(r[1] == 100.0 for r in results):
            open(path, "w").write(original_full)
            build(c.OBJ)  # rebuild baseline to keep tree consistent

    ranked = sorted([r for r in results if isinstance(r[1], float)], key=lambda x: -x[1])
    print("\n=== classement ===")
    for name, mp, _ in ranked[:10]:
        print(f"  {mp:7.3f}%  {name}")


if __name__ == "__main__":
    main()
