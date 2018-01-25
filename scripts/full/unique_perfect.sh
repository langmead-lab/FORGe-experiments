#!/bin/bash

awk -F '\t' 'BEGIN {unique=0;perfect=0;total=0;} {total+=1} {if (/AS:i:0/) perfect+=1}  {if ($5 == '60') unique+=1} END {print unique, perfect, total}' $1
#awk -F '\t' 'BEGIN {unique=0;perfect=0;total=0;} {total+=1} {if ($12 == "AS:i:0") perfect+=1}  {if ($5 == '60') unique+=1} END {print unique, perfect, total}' $1
