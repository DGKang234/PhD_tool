#!/bin/bash

tango=$1

noa=$( sed -n 1p $tango )

sta="2"
end=$( echo "$noa + 1" | bc )
echo $end

for(( j=$sta; j<=$end; j++ ));     do
        rl=$( sed -n "$j"p $tango )
        spl=( $rl )
        printf "%3s%6.10s%20.6f%12.6f%12.6f\n" ${spl[0]} "core" ${spl[1]} ${spl[2]} ${spl[3]} >> gulp_tmp.xyz
        printf "%3s%6.10s%20.6f%12.6f%12.6f\n" ${spl[0]} "shel" ${spl[1]} ${spl[2]} ${spl[3]} >> gulp_tmp.xyz
done
