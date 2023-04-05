#!/bin/bash

version=$(typst --version)
echo "Using version $version"

source_file="${1}"

readarray -t source_file <<< "$source_file"

for f in "${source_file[@]}"; do
	if [[ -z "$f" ]]; then
		continue
	fi

	echo "Building '$f'…"
	typst compile "$f"
done
