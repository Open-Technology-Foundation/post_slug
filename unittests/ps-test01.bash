#!/bin/bash
set -e
source ../post_slug.bash

declare filename="${1:-/var/log/kern.log}"
declare line sep script
declare -a seps=( - _ + ' ' )
declare -i pres=0 maxlen=52
	echo "Demo Slugtest.$script start"
	echo "  - Using file '$filename'"
	echo "  - separators ( ${seps[*]} )"
	echo "  - preserve case ( 0 1 )"
	echo "  - maxlen $maxlen"
	while read -r line; do 
		[[ -n "$line" ]] || continue
		echo "##"; 
		echo "Orig|scrp|s|p: $line" 
		for sep in "${seps[@]}"; do
			for pres in 0 1; do
				for script in py bash php js; do
					scr="${script}   "
					echo -n "Slug|${scr:0:4}|$sep|$pres: " 
					../post_slug.${script} "$line" "$sep" "$pres" $maxlen
		 		done
		 	done
		done
		echo "##"; 
	done 	< <(cat -s "$filename")
	echo "Demo Slugtest.$script end"

