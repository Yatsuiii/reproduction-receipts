program define csvmerge
    /* merges directly from a .csv file */
    syntax varlist using/ [, nokeep]
    tempfile mergefile
    preserve
    clear
    insheet using "`using'"
    save `mergefile', replace
    restore
    merge 1:1 `varlist' using `mergefile'
end
