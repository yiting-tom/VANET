cd $PWD
mkdir out
#read -p "input mob file name (default is mob.tcl) : " mobTcl; mobTcl=${mobTcl:-"../mob.tcl"}
#read -p "output mob file name (default is out.mob.tcl) : " outMobTcl; outMobTcl=${outMobTcl:-"../out/out.mob.tcl"}
#read -p "output nod file name (default is out.nod.tcl) : " outNodTcl; outNodTcl=${outNodTcl:-"../out/out.nod.tcl"}
#read -p "input mob file name (defalut is out.mob.sor.tcl): " outMobSorTcl; outMobSorTcl=${outMobSorTcl:-"../out/out.mob.sor.tcl"}
#read -p "output act file name (defalut is out.act.tcl): " outActTcl; outActTcl=${outActTcl:-"../out/out.act.tcl"}
#read -p "input tr.ana file name (defalute is main.tr.nam): " trAna; trAna=${trAna:-"../out/main.tr.ana"}
#read -p "input sumo file name (defalute is sumo.xml): " sumo; sumo=${sumo:-"../sumo.xml"}
#read -p "input tr+sumo file name (defalute is main.tr): " trSumo; trSumo=${trSumo:-"../out/main.trSumo"}

mobTcl="../mob.tcl"

outMobTcl="out/out.mob.tcl"
outNodTcl="out/out.nod.tcl"
outActTcl="out/out.act.tcl"

outMobSorTcl="out/out.mob.sor.tcl"
trAna="out/main.tr.ana"
trSumo="out/main.trSumo"
mainTrRM="out/main.tr.RM"

mainTr="out/main.tr"
mainNam="out/main.nam"

read -p "Begin node : " startNode;
read -p "End node : " endNode
read -p "start time: " startTime
read -p "end time: " endTime

#read -p "APPpro: " APPpro
#read -p "NLpro: " NLpro
APPpro="cbr"
NLpro="udp" nodeNum=`expr $endNode - $startNode + 1`

echo "\nexe mob_splitter ...\n"
python3 mob_splitter.py $mobTcl $outMobTcl $outNodTcl $startNode $endNode $startTime $endTime

echo "\nsorting $outMobTcl ...\n"
sort -k 4 $outMobTcl > $outMobSorTcl

echo "\nexe act_splitter.py ...\n"
python3 act_splitter.py $outMobSorTcl $outActTcl $startNode $endNode $startTime $endTime $APPpro $NLpro

echo "\nexe ns main.tcl $nodeNum $endTime...\n"
ns ../main.tcl $nodeNum $endTime #$outNodTcl $outMobTcl $outActTcl $mainTr $mainNam
sleep 1

echo "\nremove redundancy ...\n"
awk '{if ($1 != "M") print();}' $mainTr > $mainTrRM
awk '{if ($10 != $11) print();}' $mainTrRM > $trAna

sleep 1
echo "\nexe tr_sumo.py ...\n"
python3 tr_sumo.py $trAna $outMobSorTcl $trSumo $startTime $endTime $startNode $endNode

sleep 1
echo "\nsorting $trSumo ...\n"
sort -nk 2 $trSumo > "../trace.out"

exit 0
