#!/bin/bash
# Safe REL grind: for each module, bank small verified batches of trivial functions.
# On a batch build failure, BISECT: revert, then retry the same functions one at a time
# (batch=1) so only the truly-bad function is blacklisted and the good ones are recovered.
cd /private/tmp/claude-501/-Users-romt/acb283f2-d321-48f9-955d-3b2312329564/scratchpad/brawl || exit 1
BAD=/private/tmp/claude-501/-Users-romt/acb283f2-d321-48f9-955d-3b2312329564/scratchpad/bad_rel.txt
LAST=/private/tmp/claude-501/-Users-romt/acb283f2-d321-48f9-955d-3b2312329564/scratchpad/last_rel.txt
BATCHES=${1:-6}; START=${2:-0}; COUNT=${3:-15}
MODLIST=$(ls config/RSBE01_02/rels/ | tail -n +$((START+1)) | head -n "$COUNT")
ok=0; skip=0

revert_mod() {  # $1 = module
  git checkout HEAD -- "config/RSBE01_02/rels/$1/splits.txt" configure.py >/dev/null 2>&1
  git clean -fq src/mo_stub/ >/dev/null 2>&1
  python3 configure.py >/dev/null 2>&1
}

for mod in $MODLIST; do
  [ -d "config/RSBE01_02/rels/$mod" ] || continue
  for i in $(seq 1 "$BATCHES"); do
    RES=$(python3 tools/bank_rel.py "$mod" 5 2>/dev/null)
    n=$(echo "$RES" | sed -n 's/.*\/ \([0-9]*\) functions/\1/p')
    if [ -z "$n" ] || [ "$n" = "0" ]; then break; fi
    python3 configure.py >/dev/null 2>&1
    OUT=$(ninja 2>&1)
    if echo "$OUT" | grep -qE 'FAILED|error:'; then
      # bisect: revert the batch, then re-attempt each function individually
      revert_mod "$mod"
      for j in $(seq 1 "$n"); do
        R1=$(python3 tools/bank_rel.py "$mod" 1 2>/dev/null)
        n1=$(echo "$R1" | sed -n 's/.*\/ \([0-9]*\) functions/\1/p')
        if [ -z "$n1" ] || [ "$n1" = "0" ]; then break; fi
        python3 configure.py >/dev/null 2>&1
        if ninja 2>&1 | grep -qE 'FAILED|error:'; then
          cat "$LAST" >> "$BAD"          # blacklist just this one bad function
          revert_mod "$mod"
          skip=$((skip+1))
        else
          git add -A src/mo_stub config/RSBE01_02/rels configure.py >/dev/null 2>&1
          git -c user.name="RomThpt" -c user.email="romain@xrpl-commons.org" commit -q -m "Match $mod trivial functions" >/dev/null 2>&1
          ok=$((ok+1))
        fi
      done
    else
      git add -A src/mo_stub config/RSBE01_02/rels configure.py >/dev/null 2>&1
      git -c user.name="RomThpt" -c user.email="romain@xrpl-commons.org" commit -q -m "Match $mod trivial functions" >/dev/null 2>&1
      ok=$((ok+1))
    fi
  done
  echo "module $mod done"
done
python3 configure.py >/dev/null 2>&1; ninja >/dev/null 2>&1
git push -q fork match/getfacetexptr-changetaskprio 2>&1 | tail -1
echo "=== grind_rel fini: $ok batchs OK, $skip skippés ==="
build/tools/objdiff-cli report generate -o /tmp/gr.json 2>/dev/null
python3 -c "import json;d=json.load(open('/tmp/gr.json'));m=d['measures'];print('Global: %.4f%% | %d fonctions'%(float(m['matched_code_percent']), int(float(m.get('matched_functions',0)))))"
