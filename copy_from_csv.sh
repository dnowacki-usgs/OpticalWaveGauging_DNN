#!/usr/bin/env bash

CSV="$1"
SRC="$2"
DST="$3"

mkdir -p "$DST"

# Skip header, read first column, copy each file
tail -n +2 "$CSV" | cut -d',' -f1 | while read -r fname; do
    # skip empty lines
    [ -z "$fname" ] && continue
    cp "$SRC/$fname" "$DST/"
done


