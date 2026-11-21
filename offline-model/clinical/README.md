# Offline model receipt 2: does a clinical note ask for an action?

**Outcome: the 4B model beat the keyword rule, 58 to 50 out of 60. The 1.5B model lost to it, 45 to 50. Both results repeated on a second machine.**

Same rules as the [first receipt](../README.md): task frozen before anything else, a cheap baseline computed before any model saw the task, weights pinned by SHA-256, CPU only, no network interface but `lo`, two fresh machines, every run re-verified from a clean checkout by a verifier that needs neither the model nor the network.

| | Correct of 60 | Errors |
|---|---|---|
| Qwen3-4B-Instruct-2507, bfloat16, offline | **58** | `c04` "Would benefit from a cardiology opinion before discharge" (said NO), `c45` "Safe for discharge today with a district nurse visit on Thursday" (said NO; one of the judgement calls flagged in the [task README](task/README.md) before any run) |
| Keyword rule ([`baseline_keywords.py`](baseline_keywords.py)) | **50** | Past tense and negation: "Amoxicillin was started yesterday", "No need to repeat the chest X-ray", "Bloods not needed today" all read as YES |
| Qwen2.5-1.5B-Instruct, float32, offline | **45** | 13 of its 15 errors are YES on a note that asks for nothing, mostly ones that describe a finished action |
| Always answer NO | 33 | |

This is the first task in this repo where a model beats the cheap baseline. Read it with the bias stated in the task README: I wrote the notes knowing that a keyword rule struggles with tense and negation, so the 8-line gap partly measures how I wrote them. A keyword rule tuned on these 60 lines could close it. The task is 60 lines and the labels are mine, not a clinician's.

## What ran

- **Task:** [`task/`](task/README.md), 60 notes, 27 YES and 33 NO, frozen in commit `6f5865e` before the keyword rule or any model run.
- **Qwen3-4B-Instruct-2507** at Hub commit `cdbee75f17c01a7cc42f958dc650907174af0554`, Apache-2.0, 11 files pinned in [`MODEL_qwen3_4b.json`](MODEL_qwen3_4b.json) (8.0 GB; the three weight shards and `tokenizer.json` matched the SHA-256 the Hub stores for them). Run in bfloat16 with 4 threads ([`runtime_transformers_bf16.py`](../runtime_transformers_bf16.py)), because float32 would need 16 GB and the machines have 16 GB.
- **Qwen2.5-1.5B-Instruct**, same pin and float32 runtime as the first receipt.
- Same hashed dependency lock, same harness, now taking `--task clinical/task --model-json ...` (logged in [`FROZEN_CHANGES.md`](../FROZEN_CHANGES.md); two new failure injections were written and failed before that change, 18 of 18 pass after).
- Code under test: commit `2416623`, clean checkout on all four machines. [Run 44907782766](https://github.com/Yatsuiii/reproduction-receipts/actions/runs/44907782766).

## Machines, wall clock, cost

| Model | Machine | CPU | Harness wall clock | Peak RSS | Result |
|---|---|---|---|---|---|
| Qwen3-4B, bf16 | a, Ubuntu 24.04 | Intel Xeon 6975P-C (AMX, AVX-512 BF16) | 101.8 s | 7.8 GiB | 58/60 |
| Qwen3-4B, bf16 | b, Ubuntu 22.04 | AMD EPYC 9V74 (AVX-512 BF16, no AMX) | 187.0 s | 8.1 GiB | 58/60 |
| Qwen2.5-1.5B, fp32 | a, Ubuntu 24.04 | AMD EPYC 9V74 | 171.8 s | 9.1 GiB | 45/60 |
| Qwen2.5-1.5B, fp32 | b, Ubuntu 22.04 | AMD EPYC 7763 | 191.5 s | 9.1 GiB | 45/60 |

Inside the namespace every run recorded interfaces `['lo']`, a failed probe to `1.1.1.1:443`, and zero network attempts. With the network up, all four refused with exit 3 before loading weights. Weights download took 17 to 83 s per machine.

**Cost:** $0 billed (public repository, 0 billable ms reported). The seven jobs come to 23 runner-minutes after GitHub's per-job rounding, about $0.14 at the published $0.006 per minute for a standard Linux 2-core runner.

## Reproduction across machines

- `predictions.csv` byte-identical between machines for both models (4B: `357beaa7…dfb1`, 1.5B: `24785e25…acd9`).
- **1.5B, float32:** logits differ by at most 3.1e-5. Its closest decision, `c54`, has a margin of 0.041, so it held, but that is the thinnest margin in this repo.
- **4B, bfloat16:** logits differ by up to **1.25** on `c46` (margin −1.25 on Intel, −0.5 on AMD). The decision held on every line, but a drift that size means the receipt cannot promise that a bfloat16 run will make the same call on another CPU. It promises only what it shows: on these two CPUs, these 60 calls matched. The smallest 4B margin on either machine was 0.5, the same size as the drift. Float32 is the setting that reproduces to five decimal places; it needs more memory than these machines have for a 4B model.

## Check it yourself

```sh
git clone https://github.com/Yatsuiii/reproduction-receipts && cd reproduction-receipts
python3 -I offline-model/check_frozen.py
for m in qwen3-4b qwen2.5-1.5b; do
  for x in a b; do python3 -I offline-model/verify.py run offline-model/runs/gha-44907782766-1-clinical-$m-$x; done
  python3 -I offline-model/verify.py compare offline-model/runs/gha-44907782766-1-clinical-$m-a offline-model/runs/gha-44907782766-1-clinical-$m-b
done
python3 -I offline-model/clinical/baseline_keywords.py
```

## Every failed run

None failed in this round. The four network-up refusals are deliberate and listed in [`RUNS.json`](../RUNS.json). The label-triggered discover job that printed the 4B pin committed nothing.

## What this does not show

- That a 4B model is good at reading clinical notes. 60 short lines written by one non-clinician is not that test.
- That bfloat16 results reproduce across CPUs in general. See the drift above.
- Anything about a customer's own model or data. This is the harness that would sit around them.
