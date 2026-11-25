This run tested the wrong version, and that was the spec's fault, not the package's. The setup step picked `ramchoice` 1.1:
the newest file in the CRAN archive dated on or before 2021-10-20. The dates in that archive index are the dates a file was
archived, which is when the next release replaced it, not when it was published. So 1.1 had already been replaced before
the script was written. It has no `logitSimu`, and the script stops on its first call. Nothing here speaks to the
package. Run 3 corrects the rule (see the protocol).
