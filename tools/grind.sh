#!/bin/bash
# Safe autonomous grind: bank small batches of trivial functions, verify the DOL
# sha1 (127 files OK) before committing; on failure, blacklist the batch and revert.
cd /private/tmp/claude-501/-Users-romt/acb283f2-d321-48f9-955d-3b2312329564/scratchpad/brawl || exit 1
BAD=/private/tmp/claude-501/-Users-romt/acb283f2-d321-48f9-955d-3b2312329564/scratchpad/bad_funcs.txt
LAST=/private/tmp/claude-501/-Users-romt/acb283f2-d321-48f9-955d-3b2312329564/scratchpad/last_batch.txt
CYCLES=${1:-15}
ok=0; skipped=0
for i in $(seq 1 "$CYCLES"); do
  OUTB=$(python3 tools/bank_batch.py 5 2>/dev/null | grep -c 'unit stub')
  if [ "$OUTB" = "0" ]; then echo "cycle $i: rien à banker, stop"; break; fi
  python3 configure.py >/dev/null 2>&1
  OUT=$(ninja 2>&1)
  if echo "$OUT" | grep -q '127 files OK'; then
    git add -A src/stub config/RSBE01_02/splits.txt configure.py >/dev/null 2>&1
    git -c user.name="RomThpt" -c user.email="romain@xrpl-commons.org" commit -q -m "Match trivial stub functions" >/dev/null 2>&1
    ok=$((ok+1)); echo "cycle $i: OK (committed)"
  else
    cat "$LAST" >> "$BAD"
    git checkout HEAD -- config/RSBE01_02/splits.txt configure.py >/dev/null 2>&1
    git clean -fq src/stub/ >/dev/null 2>&1
    python3 configure.py >/dev/null 2>&1
    skipped=$((skipped+1)); echo "cycle $i: DOL cassé, $(wc -l < "$LAST" | tr -d ' ') fn blacklistées"
  fi
done
python3 configure.py >/dev/null 2>&1; ninja >/dev/null 2>&1
git push -q fork match/getfacetexptr-changetaskprio 2>&1 | tail -1
echo "=== grind fini: $ok cycles OK, $skipped skippés ==="
build/tools/objdiff-cli report generate -o /tmp/g.json 2>/dev/null
python3 -c "import json;d=json.load(open('/tmp/g.json'));m=d['measures'];print('Global: %.4f%% | %d fonctions'%(float(m['matched_code_percent']), int(float(m.get('matched_functions',0)))))"
