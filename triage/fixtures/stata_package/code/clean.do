use "$root/data/survey", clear
keep if age >= 18
save "$root/data/survey_clean.dta", replace
