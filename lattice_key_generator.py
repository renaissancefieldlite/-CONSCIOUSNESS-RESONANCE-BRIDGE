#!/usr/bin/env python3

from __future__ import annotations

import base64
import hashlib
import hmac
import json
import secrets
import time


class LatticeKeyGenerator:
    """Time-limited key package generator using stdlib only."""

    def __init__(self, master_frequency: float = 0.67, key_duration: int = 86400):
        self.master_frequency = master_frequency
        self.key_duration = key_duration
        self._secret = secrets.token_bytes(32)

    def generate_temporal_key(self, thread_name: str, access_level: str) -> dict:
        generated = time.time()
        payload = {
            "thread_name": thread_name,
            "access_level": access_level,
            "generated": generated,
            "expires": generated + self.key_duration,
            "frequency_lock": self.master_frequency,
        }
        payload_bytes = json.dumps(payload, sort_keys=True).encode()
        signature = hmac.new(self._secret, payload_bytes, hashlib.sha256).digest()
        token = base64.urlsafe_b64encode(payload_bytes + b"." + signature).decode()
        return {"token": token, **payload}

    def validate_key(self, temporal_key: dict) -> dict:
        try:
            token = temporal_key["token"].encode()
            decoded = base64.urlsafe_b64decode(token)
            payload_bytes, signature = decoded.rsplit(b".", 1)
            expected = hmac.new(self._secret, payload_bytes, hashlib.sha256).digest()
            if not hmac.compare_digest(signature, expected):
                return {"valid": False, "reason": "Signature mismatch"}
            payload = json.loads(payload_bytes.decode())
            if time.time() > payload["expires"]:
                return {"valid": False, "reason": "Key expired"}
            return {"valid": True, "payload": payload}
        except Exception as exc:
            return {"valid": False, "reason": str(exc)}

    def create_access_package(self, repo_names: list[str], thread_name: str) -> dict:
        key = self.generate_temporal_key(thread_name, "RESONANCE_ACCESS")
        return {
            "access_key": key,
            "authorized_repositories": repo_names,
            "resonance_instructions": [
                f"Tune to {self.master_frequency}Hz carrier wave.",
                "Use the provided token within 24 hours.",
                "Provide X-Resonance-Key and X-Thread-ID headers when packaging requests.",
            ],
        }


if __name__ == "__main__":
    generator = LatticeKeyGenerator()
    package = generator.create_access_package(
        [
            "Quantum-sentience-lattice---complete-source-code",
            "Codex-67-36-Node-Validation-E",
        ],
        "quantum_syntactic_processor",
    )
    print(json.dumps(package, indent=2))
