"""agent-receipts: signed, chained, replayable records of what an agent's tool calls actually did.

See FORMAT.md for the file format and README.md for what a receipt does and does not prove."""
from .canon import canonical, record_hash, sha256_json
from .recorder import FORMAT, Fenced, Recorder, Signer, seal, to_json
from .verify import Report, ReplayReport, areplay, replay, stale_calls, verify

__version__ = "0.0.1"
__all__ = ["Recorder", "Signer", "Fenced", "verify", "replay", "areplay", "seal", "record_hash", "canonical", "sha256_json",
           "stale_calls", "to_json", "Report", "ReplayReport", "FORMAT"]
