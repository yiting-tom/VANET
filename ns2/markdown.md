# color
NODE
$node color red

FLOW
$udp set fid_ 1
# connect
$ns_ attach-agnet $n0 $udp
$ns_ connect $udp $null
$ns_ detach-agent $n0 $udp
$ns_ at 1.0 "$cbr stop"
