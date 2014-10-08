h1 = "#99ffff"; h2 = "#4671d5"; h3 = "#ff0000"
set auto x
set auto y
set auto fix
set style data histogram
set style histogram cluster gap 1
set style fill solid border -1
set boxwidth 0.9
set xtic scale 0
set yrange [ 0 : * ]
set terminal epslatex

set title "Results for puzzle 1"
set output "graph1.eps"
plot 'puzzleData/puzzle1.dat' using 2:xtic(1) ti col fc rgb h1, '' u 3 ti col fc rgb h2, '' u 4 ti col fc rgb h3

set title "Results for puzzle 2"
set output "graph2.eps"
plot 'puzzleData/puzzle2.dat' using 2:xtic(1) ti col fc rgb h1, '' u 3 ti col fc rgb h2, '' u 4 ti col fc rgb h3

set title "Results for puzzle 3"
set output "graph3.eps"
plot 'puzzleData/puzzle3.dat' using 2:xtic(1) ti col fc rgb h1, '' u 3 ti col fc rgb h2, '' u 4 ti col fc rgb h3

set title "Results for puzzle 4"
set output "graph4.eps"
plot 'puzzleData/puzzle4.dat' using 2:xtic(1) ti col fc rgb h1, '' u 3 ti col fc rgb h2, '' u 4 ti col fc rgb h3

set title "Results for puzzle 5"
set output "graph5.eps"
plot 'puzzleData/puzzle5.dat' using 2:xtic(1) ti col fc rgb h1, '' u 3 ti col fc rgb h2, '' u 4 ti col fc rgb h3

