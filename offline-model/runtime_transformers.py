"""Runtime for the real model run: Hugging Face transformers on CPU, float32, fixed thread count, no sampling.

score() returns the next-token logits for the first token of "YES" and of "NO" once the assistant turn opens. One forward
pass per item, no generation, so there is no sampling state to pin. The harness imports this only after its network
preflight passed and its socket audit hook is installed."""
import hashlib

THREADS = 2  # fixed so float reduction order does not depend on the machine's core count


class Runtime:
    def __init__(self, weights_dir: str):
        import torch
        from transformers import AutoModelForCausalLM, AutoTokenizer
        torch.set_num_threads(THREADS)
        torch.use_deterministic_algorithms(True)
        self.torch = torch
        self.tok = AutoTokenizer.from_pretrained(weights_dir, local_files_only=True)
        self.model = AutoModelForCausalLM.from_pretrained(weights_dir, local_files_only=True, dtype=torch.float32)
        self.model.eval()
        self.yes = self.tok.encode("YES", add_special_tokens=False)
        self.no = self.tok.encode("NO", add_special_tokens=False)
        if self.yes[0] == self.no[0]:
            raise RuntimeError("YES and NO share a first token; the decision rule cannot separate them")

    def info(self) -> dict:
        import transformers
        return {"runtime": "transformers", "torch": self.torch.__version__, "transformers": transformers.__version__,
                "dtype": "float32", "threads": self.torch.get_num_threads(), "deterministic_algorithms": True,
                "yes_tokens": self.yes, "no_tokens": self.no,
                "yes_first_token": self.tok.decode([self.yes[0]]), "no_first_token": self.tok.decode([self.no[0]])}

    def score(self, system: str, user: str):
        messages = [{"role": "system", "content": system}, {"role": "user", "content": user}]
        text = self.tok.apply_chat_template(messages, tokenize=False, add_generation_prompt=True)
        enc = self.tok(text, return_tensors="pt", add_special_tokens=False)
        with self.torch.inference_mode():
            logits = self.model(**enc).logits[0, -1]
        return (float(logits[self.yes[0]]), float(logits[self.no[0]]),
                hashlib.sha256(text.encode("utf-8")).hexdigest(), int(enc["input_ids"].shape[1]))
