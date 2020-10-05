set val(chan)           Channel/WirelessChannel    ;# channel type
set val(prop)           Propagation/TwoRayGround   ;# radio-propagation model
set val(netif)          Phy/WirelessPhy            ;# network interface type 
set val(mac)            Mac/802_11                 ;# MAC type 
set val(ifq)            Queue/DropTail/PriQueue    ;# interface queue type 
set val(ll)             LL                         ;# link layer type 
set val(ant)            Antenna/OmniAntenna        ;# antenna model
set val(ifqlen)         32768                      ;# max packet in ifq

set val(nn) [lindex $argv 0]
set endTime [lindex $argv 1]

set val(rp) DumbAgent 
set val(cbr_packet_size) 10Kb
set val(cbr_rate) 20Mb

set val(cbr_interval) 0.005
set val(udp_interval) 0.005

set ns_ [new Simulator]
#Antenna/OmniAntenna set X_ 0
#Antenna/OmniAntenna set Y_ 0
#Antenna/OmniAntenna set Z_ 1.5
#Antenna/OmniAntenna set Gt_ 1.0
#Antenna/OmniAntenna set Gr_ 1.0
 
#Phy/WirelessPhy set CPThresh_ 10.0
#Phy/WirelessPhy set CSThresh_ 2.13643e-11
Phy/WirelessPhy set RXThresh_ 1.7614884e-10
Phy/WirelessPhy set bandwidth_ 2e6
Phy/WirelessPhy set Pt_ 0.28183815
Phy/WirelessPhy set freq_ 914e+6
Phy/WirelessPhy set L_ 1.0 


set f [open ../main.tr w]
$ns_ trace-all $f
set nf [open ../main.nam w]
$ns_ namtrace-all-wireless $nf 3200 3200
 
# set up topography object
set topo       [new Topography]
 
$topo load_flatgrid 3200 3200
$ns_ color 0 Gray
$ns_ color 1 Red
$ns_ color 2 Green
$ns_ color 3 Blue
 
# Create God
create-god 32
 
# create channel
set chan [new $val(chan)]
 
$ns_ node-config -adhocRouting $val(rp) \
                -llType $val(ll) \
                -macType $val(mac) \
                -ifqType $val(ifq) \
                -ifqLen $val(ifqlen) \
                -antType $val(ant) \
                -propType $val(prop) \
                -phyType $val(netif) \
                -channel $chan \
                -topoInstance $topo \
                -agentTrace OFF \
                -routerTrace OFF \
                -macTrace ON \
                -movementTrace OFF
 
for {set i 0} {$i < $val(nn)} {incr i} {
#        puts "new node_($i)"
        set node_($i) [$ns_ node]
        $node_($i) color white
#        $ns_ at 0.0 "$node_($i) color white"
        $node_($i) random-motion 0
        $ns_ initial_node_pos $node_($i) 80
}
 
source "out/out.nod.tcl"
source "out/out.mob.tcl"

for {set i 0} {$i < $val(nn) } {incr i} {
  for {set j 0} {$j < $val(nn)} {incr j} {
    if {$i != $j } {

      set udp_($i-$j) [new Agent/UDP] 
      set interval_ $val(udp_interval)
      set null_($i-$j) [new Agent/Null]
      $ns_ at 0.0 "$ns_ attach-agent $node_($i) $udp_($i-$j)"
      $ns_ at 0.0 "$ns_ attach-agent $node_($j) $null_($i-$j)"
      $ns_ at 0.0 "$ns_ connect $udp_($i-$j) $null_($i-$j)"

      $udp_($i-$j) set fid_ 0

      set cbr_($i-$j) [new Application/Traffic/CBR]
      $cbr_($i-$j) set type_ CBR
      $cbr_($i-$j) set packet_size_ $val(cbr_packet_size)
      $cbr_($i-$j) set rate_ $val(cbr_rate)
      $cbr_($i-$j) set random_ false
      $cbr_($i-$j) set interval_ $val(cbr_interval)

      $ns_ at 0.0 "$cbr_($i-$j) attach-agent $udp_($i-$j)"
      $ns_ at 0.0 "$cbr_($i-$j) start"

    }
  } 
}
#source "out/out.act.tcl"

$ns_ at $endTime "finish"
 
#INSERT ANNOTATIONS HERE
proc finish {} {
        puts "finishing ..."
        global ns_ f nf val
        $ns_ flush-trace
        close $f
        close $nf
        exit 0
}
puts "Starting Simulation..."
$ns_ run
