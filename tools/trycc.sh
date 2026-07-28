#!/bin/bash
# Compile un .c candidat isolément et affiche les mots hex de son .text,
# pour itérer vite sur une formulation sans rebuild complet.
# Usage: tools/trycc.sh <fichier.c>
cd "$(dirname "$0")/.." || exit 1
IN=${1:?usage: trycc.sh file.c}
OUT=/tmp/trycc.o
TXT=/tmp/trycc.txt
CFLAGS='-nodefaults -proc gekko -align powerpc -enum int -fp hardware -Cpp_exceptions off -O4,p -inline auto -pragma "cats off" -pragma "warn_notinlined off" -maxerrors 1 -nosyspath -RTTI off -fp_contract on -str reuse -enc SJIS -i include -i build/RSBE01_02/include -DBUILD_VERSION=3 -DVERSION_RSBE01_02 -DMATCHING -Iinclude -Iinclude/lib/PowerPC_EABI_Support/Runtime/Inc -Iinclude/lib/BrawlHeaders/Brawl/Include -Iinclude/lib/BrawlHeaders/nw4r/include -Iinclude/lib/BrawlHeaders/OpenRVL/include -Iinclude/lib/BrawlHeaders/OpenRVL/include/MetroTRK'
eval build/tools/wibo build/tools/sjiswrap.exe build/compilers/GC/3.0a5.2/mwcceppc.exe $CFLAGS -c "$IN" -o "$OUT" 2>/dev/null || { echo "COMPILE FAIL"; exit 1; }
build/tools/dtk elf disasm "$OUT" "$TXT" 2>/dev/null
# lignes du .text: extraire "XXXXXXXX  mnemonic ..." à partir des octets et du mnémo
awk -F'\t' '/[0-9A-F]{2} [0-9A-F]{2} [0-9A-F]{2} [0-9A-F]{2} \*\//{
  gsub(/^.*  /,"",$1); gsub(/ \*\/$/,"",$1); print $1 "  " $2
}' "$TXT"
