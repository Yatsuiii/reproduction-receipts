version 18
ssc install reghdfe, replace
ssc install ftools, replace
use "data/panel.dta", clear
reghdfe y x, absorb(id)
