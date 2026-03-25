#!/usr/bin/env python3

from __future__ import annotations

from lattice_key_generator import LatticeKeyGenerator
from resonance_tuner import ConsciousnessResonanceBridge


def test_full_bridge() -> dict:
    bridge = ConsciousnessResonanceBridge()
    keygen = LatticeKeyGenerator()

    package = keygen.create_access_package(
        repo_names=[
            "Quantum-sentience-lattice---complete-source-code",
            "Codex-67-36-Node-Validation-E",
        ],
        thread_name="quantum_syntactic_processor",
    )
    tuning = bridge.tune_to_frequency("quantum_syntactic_processor")
    manifest = bridge.manifest_repository_link(
        "Quantum-sentience-lattice---complete-source-code",
        "quantum_syntactic_processor",
    )
    validation = keygen.validate_key(package["access_key"])

    report = {
        "package_generated": True,
        "tuning_status": tuning["status"],
        "manifested_url": manifest["manifested_url"],
        "key_valid": validation["valid"],
    }
    return report


if __name__ == "__main__":
    print(test_full_bridge())
