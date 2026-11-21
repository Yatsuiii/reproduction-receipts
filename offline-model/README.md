# Offline model receipt

**Outcome: the run reproduced on a second machine. The model lost to a regular expression.**

An open-weight model scored a frozen 60-line task on CPU, inside a network namespace whose only interface was `lo`, on two fresh GitHub-hosted machines with different Ubuntu images and different CPU vendors. Both produced byte-identical predictions (`predictions.csv` SHA-256 `2ebf4b2e3b6072bf0f0a48483ebe6497a10162fccbd83888221c2f1ed5c9aba4`). A third clean checkout re-verified both runs without trusting either.

| | Correct of 60 | Notes |
|---|---|---|
| Qwen2.5-1.5B-Instruct, offline, CPU | **42** | Same on both machines. 17 of its 18 errors are a missed identifier: it answered NO to a phone number, an email, an IBAN. |
| Regular-expression rule ([`baseline.py`](baseline.py)) | **53** | Written before any model output existed. Misses bare names. |
| Always answer NO | 32 | |

The model is not the product, and this task is not a benchmark: I wrote both the lines and the labels. What the receipt shows is that the claim "this output came from these exact weights, this code and this prompt, on a machine that could not reach the network" can be checked by someone who was not there. The accuracy is reported because a receipt that hid a losing number would be worth nothing.

## What ran

- **Model:** [`Qwen/Qwen2.5-1.5B-Instruct`](https://huggingface.co/Qwen/Qwen2.5-1.5B-Instruct/tree/989aa7980e4cf806f80c7fef2b1adb7bc71aa306) at commit `989aa7980e4cf806f80c7fef2b1adb7bc71aa306`, Apache-2.0 (model card declaration; the `LICENSE` file is pinned and its first line reads "Apache License, Version 2.0"). Eight files pinned in [`MODEL.json`](MODEL.json); `model.safetensors` is `dd924a11…d3ee`, 3,087,467,144 bytes, and matched the SHA-256 the Hub stores for that LFS object. The other seven are not LFS files, so the Hub has no hash to compare them with; their pin is trust-on-first-download from the [discover run](https://github.com/Yatsuiii/reproduction-receipts/actions/runs/44905523493).
- **Task:** [`task/`](task/README.md), 60 lines, does each contain a personal identifier, YES or NO. Frozen in the first commit, before any code.
- **Decision rule:** one forward pass per line, compare the next-token logit of `YES` (token 14004) against `NO` (token 8996) after the assistant turn opens. No sampling, no generation.
- **Runtime:** torch `2.14.1+cpu`, transformers `5.22.2`, float32, 2 threads, `torch.use_deterministic_algorithms(True)`, Python 3.12.10. Every package installed with `--require-hashes` from [`requirements.lock`](requirements.lock) (SHA-256 `c3646b01…78d3`).
- **Code under test:** commit [`7c1d878`](https://github.com/Yatsuiii/reproduction-receipts/commit/7c1d8782cb122915cd5291317b1fec6fc928e970), clean checkout on both machines. `harness.py` `b82d9056…383a`, `runtime_transformers.py` `de6b99d9…aeb`, both pinned in [`FROZEN.json`](FROZEN.json) before the first scored run.

## Commands

Each machine ran these from a fresh checkout ([workflow](../.github/workflows/offline-model.yml), [run 44906039993](https://github.com/Yatsuiii/reproduction-receipts/actions/runs/44906039993)):

```sh
python -m venv /tmp/venv
/tmp/venv/bin/python -m pip install --require-hashes --no-deps \
  --extra-index-url https://download.pytorch.org/whl/cpu -r offline-model/requirements.lock
/tmp/venv/bin/python -I offline-model/fetch_weights.py --fetch --model offline-model/MODEL.json --dest /tmp/weights

# must refuse: network is up (exit 3)
/tmp/venv/bin/python -I offline-model/harness.py --weights /tmp/weights --out offline-model/runs/$RUN_ID-network-up

# the scored run: new network namespace, then drop back to the runner user
sudo unshare -n setpriv --reuid="$(id -u)" --regid="$(id -g)" --clear-groups \
  env HOME="$HOME" PATH="/tmp/venv/bin:/usr/bin:/bin" \
  /tmp/venv/bin/python -I offline-model/harness.py --weights /tmp/weights --out /tmp/out
```

Inside the namespace the harness recorded interfaces `['lo']` and a probe to `1.1.1.1:443` failing with `[Errno 101] Network is unreachable`. Its socket audit hook logged zero connect, DNS or send attempts during inference. With the network up, the same harness refused on both machines (machine a saw `docker0, enp39s0, lo`) and exited 3 before loading anything.

## Environment, hardware, wall clock, cost

| | Machine a | Machine b |
|---|---|---|
| Image | Ubuntu 24.04.5, image 20261116.133.1 | Ubuntu 22.04.5, image 20261116.365.1 |
| CPU | Intel Xeon 6975P-C, 4 vCPU, AVX-512 and AMX | AMD EPYC 7763, 4 vCPU, AVX2, no AVX-512 |
| Memory | 16 GB, peak RSS 9.1 GiB | 16 GB, peak RSS 9.1 GiB |
| Install / fetch weights | 33 s / 25 s | 51 s / 20 s |
| Harness wall clock (load + score 60) | 89.3 s (3.8 s + 83.5 s) | 206.1 s (6.8 s + 197.0 s) |
| Whole job | 2 min 52 s | 4 min 57 s |
| Result | 42/60 | 42/60 |

**Cost:** $0 billed. GitHub reported 0 billable ms for the run because the repository is public. At GitHub's published rate for a standard Linux 2-core runner, $0.006 per minute ([pricing](https://docs.github.com/en/billing/reference/actions-runner-pricing)), with each job rounded up to whole minutes, the four jobs come to 10 minutes, about $0.06. Model download is free at this size. On a customer's own CPU box the cost is the 1.5 to 3.5 minutes of machine time above.

## Re-check from a clean checkout

A third job checked out the branch after both machines had pushed, and ran [`verify.py`](verify.py), which uses only the standard library and needs neither the model nor the network:

```text
run …-a: 42/60 correct recomputed from this checkout's labels   PASS
run …-b: 42/60 correct recomputed from this checkout's labels   PASS
predictions.csv byte-identical: True
logits.csv byte-identical: False
largest margin difference: 0.000102996826171875 on p52
```

The logits are not byte-identical across the two CPUs, and the receipt does not claim they are. The largest difference in any YES-minus-NO margin was 1.03e-4; the smallest margin in either run was 0.281, so no decision was near enough to the line to flip. You can repeat this check yourself on any machine with Python 3:

```sh
git clone https://github.com/Yatsuiii/reproduction-receipts && cd reproduction-receipts
python3 -I offline-model/check_frozen.py
python3 -I offline-model/verify.py run offline-model/runs/gha-44906039993-1-a
python3 -I offline-model/verify.py run offline-model/runs/gha-44906039993-1-b
python3 -I offline-model/verify.py compare offline-model/runs/gha-44906039993-1-a offline-model/runs/gha-44906039993-1-b
python3 -I offline-model/verify.py ledger offline-model/RUNS.json
```

To rerun the model rather than check the record, run the commands above on your own Linux machine (about 3 GB download, 10 GB RAM).

## Failure injections

[`injections/EXPECTED.json`](injections/EXPECTED.json) lists 14 ways the run could cheat or the receipt could lie, committed before any harness code. Each has a test in [`tests/test_injections.py`](tests/test_injections.py) that builds the case in a throwaway checkout with fake weights and a stub model, and runs the real harness and verifier. All 14 are caught, on this sandbox and on GitHub. They include: a network interface present, a connect or DNS call during inference, one flipped byte in the weights, a missing or extra weights file, an edited task, a dirty checkout, an edited prediction, a misreported accuracy, an edited label, two runs that disagree, and a failed run deleted from the ledger.

## Every failed run

All listed in [`RUNS.json`](RUNS.json), which `verify.py ledger` checks.

1. [Run 44905916825](https://github.com/Yatsuiii/reproduction-receipts/actions/runs/44905916825), the first scoring attempt, failed on both machines before loading weights. A one-off workflow that resolved the dependency lock ran again on the same push and committed a different lock: nine packages came out at older versions from the same command four minutes later (details in [`FROZEN_CHANGES.md`](FROZEN_CHANGES.md)). The branch moved, the run's commit check refused, and the frozen-file check flagged the changed lock. I reverted the second lock and deleted that workflow. The commit message of `7c1d878` says it switched the checkout to the exact commit; that edit did not land, and the run used the original branch checkout guarded by the commit check, which passed.
2. [Run 44905951637](https://github.com/Yatsuiii/reproduction-receipts/actions/runs/44905951637) never ran: GitHub held the bot's commit for approval.
3. The two network-up refusals above are deliberate and kept as runs.

## What this does not show

- That the model is good at this. It is not: a regex beats it by 11 lines.
- That the network namespace is the only possible path out. The audit hook sees Python-level socket calls only. The namespace is the guarantee; the hook is the record.
- That the runs happened. The run directories were committed by `github-actions[bot]` from the job that produced them, and the job logs are public, but bytes in a repository do not prove execution by themselves. Rerunning is the only proof that does not trust GitHub or me.
- Independence from GitHub. Both machines are GitHub-hosted. The second differs in image, CPU vendor and instruction set, not in operator.
- A real customer task, a licensed model the customer already runs, or an air-gapped machine. This is the harness that would sit around one.
