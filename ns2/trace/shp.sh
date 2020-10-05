awk '{ if( ($1 == "D" && $4 == "MAC" && $7 == "cbr") \
|| ($1 == "r" && ($7 == "cbr" || $10 == "ffffffff")) \
|| ($1 == "M") ) print; }' main.tr > main.out

$py splitter.py
sort -nk 2 main.srDM > main.out
rm main.srDM
