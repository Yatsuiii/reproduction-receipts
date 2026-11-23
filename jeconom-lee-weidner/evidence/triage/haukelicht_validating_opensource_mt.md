# Triage verdict: BLOCKED

- Package: `pk/haukelicht_validating_opensource_mt` at commit `74a1d6b40d413cf511e1ffbc2c6a0fd85e429e8d`
- Triaged: 2026-11-23T17:48:00Z on Linux-6.18.44-fc-v726-x86_64-with-glibc2.39, Python 3.13.18, 0.162 s of analysis
- Triage script: `triage.py` SHA-256 `c2ddd83b920c4425cd0a0de65ad0939cbd2fcd483f8eed518b115216c43138ca`; options: defaults
- 5 blockers, 5 deviations, 3 notes

Triage reads the package and never executes it. This verdict says whether the committed materials can be run on this desk and what a rerun would have to change. It says nothing about whether the paper's results are correct.

## Blockers

- **MISSING_INPUT_UNDOCUMENTED**: `cmp_translations.tsv` is read by the code and named in the documentation (data/datasets/classifier_finetuning/README.md), but it is not in the package and no source for it is given.
  Evidence: `code/05-analyses/02-describe_finetuning_datasets.R:300`
- **MISSING_INPUT_RESTRICTED**: `dupont_and_rachuj_2022_coded_manifesto_sentences.rds` is read by the code but is not in the package. The documentation does not name it, but does describe restricted data ("not publicly available"), so it is most likely one of those.
  Evidence: `code/01-data_preparation/classifier_finetuning/prepare_dupont_and_rachuj_2022_manifesto_data.R:32`
- **MISSING_INPUT_UNDOCUMENTED**: `lda90.rds` is read by the code and named in the documentation (data/results/topic_modeling/README.md), but it is not in the package and no source for it is given.
  Evidence: `code/05-analyses/01-analyze_topic_modeling_results.R:246`
- **MISSING_INPUT_RESTRICTED**: `PImPo_qsl_wo_verbatim.csv` is read by the code but is not in the package. The documentation does not name it, but does describe restricted data ("not publicly available"), so it is most likely one of those.
  Evidence: `code/01-data_preparation/classifier_finetuning/prepare_lehmann_and_zobel_2018_manifesto_data.R:45`
- **MISSING_INPUT_UNDOCUMENTED**: `poljak_2022_attack_data_translated.tsv` is read by the code and named in the documentation (data/datasets/classifier_finetuning/README.md), but it is not in the package and no source for it is given.
  Evidence: `code/05-analyses/02-describe_finetuning_datasets.R:507`

## Deviations a rerun would have to log

- **UNPINNED_DEPENDENCIES**: Python requirements without an exact version: scikit-learn=1.3.2; imbalanced-learn=0.11.0. A rerun installs whatever is current and must log the versions it got.
  Evidence: `code/02-machine_translation/requirements.txt`, `code/04-classifier_finetuning/requirements.txt`
- **UNDECLARED_DEPENDENCIES**: Python code imports google, imblearn, torch, tqdm, which no dependency file names.
  Evidence: `code/02-machine_translation/translate.py`, `code/04-classifier_finetuning/finetune_classifier.py`, `code/05-analyses/translation_discrepancy/02-compute_translation_similiarities_for_label_disagreement_cases.py`, `code/05-analyses/translation_similarity/01-sample_examples_for_similarity_analysis.py`, `code/05-analyses/translation_similarity/02-compute_translation_similiarities.py`
- **UNDECLARED_DEPENDENCIES**: R code loads ISOcodes, cld2, countrycode, dataverse, devtools, lubridate, manifestoR, proxy, psych, quanteda, quanteda.textstats, readtext, readxl, which renv.lock does not pin.
  Evidence: `renv.lock`
- **RUNTIME_DOWNLOAD**: Code fetches data over the network when it runs (download.file). What the server returns today may differ from what the authors got; a receipt must record each file fetched and its SHA-256.
  Evidence: `code/01-data_preparation/classifier_finetuning/prepare_dupont_and_rachuj_2022_manifesto_data.R:28`, `code/01-data_preparation/classifier_finetuning/prepare_lehmann_and_zobel_2018_manifesto_data.R:42`
- **GPU_REQUIRED**: The package refers to GPUs or CUDA. A CPU rerun may be slower or numerically different and must say so.

## Notes

- **UNRESOLVED_PATHS**: 2 file reads use paths built at run time (macros, globs, variables), so triage could not check that those inputs exist.
  Evidence: `code/03-topic_modeling/01-fit_tipic_models.R:49`, `code/05-analyses/02-describe_finetuning_datasets.R:410`
- **CLUSTER_MENTIONED**: The package mentions a cluster or batch scheduler; scripts may assume one.
- **NO_LICENCE**: No licence file and no licence named in the documentation. Running it for a check is unaffected, but a receipt should quote and hash files rather than redistribute them.

## What triage looked at

- 338 files, 402,865,214 bytes. Languages: python (5), r (20), shell (11).
- Documentation read: README.md, data/datasets/classifier_finetuning/README.md, data/datasets/topic_modeling/texts/README.md, data/exdata/poljak_2022/README.md, data/exdata/theocharis_et_al_2016/README.md, data/results/topic_modeling/README.md, replication_r_requirements.txt. Licences named: none.
- Master scripts: none.
- File reads traced: 44; writes: 3; unresolved paths: 2; missing: cmp_translations.tsv, dupont_and_rachuj_2022_coded_manifesto_sentences.rds, lda90.rds, pimpo_qsl_wo_verbatim.csv, poljak_2022_attack_data_translated.tsv.
- Links found: 7; checked: no.
