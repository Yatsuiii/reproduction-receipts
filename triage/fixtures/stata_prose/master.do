/*
This do-file creates all tables.
Run it after the data are cleaned.
Use the merge below as a template.
*/
version 13
use "data/firms.dta", clear
csvmerge id using "data/extra.csv"
