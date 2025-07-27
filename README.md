# Covenant Recursion Prototypes for Trustless DeFi on BCH

## Overview
This repository contains prototypes demonstrating "covenant recursion for DeFi without trust" on Bitcoin Cash (BCH)—a way to enable atomic, fair sequencing in Automated Market Makers (AMMs) without external signers, oracles, or protocol changes like faster block times. It addresses key DeFi limitations on BCH, such as UTXO contention (concurrent users racing to spend the same pool UTXO, leading to failures and retries), Miner Extractable Value (MEV, miners reordering for profit), and variance in block confirms (10+ min waits for resolution).

- **Python Simulator (`amm_prototype.py`)**: CLI REPL to simulate the AMM workflow, including multi-user races via threading. Demonstrates trustless resolution today and previews 2026 scalability.
- **CashScript Contracts**:
  - `SequencedAMM_25.cash`: Deployable today (using 2018-re-enabled OP_CAT for appending, SHA256 for merkle, basic introspection). Handles small-scale contention but limits to ~5-10 commits due to manual unrolling (code repetition causes script bloat and VM limits).
  - `SequencedAMM_26.cash`: Hypothetical for 2026 upgrades (loops via OP_BEGIN/OP_UNTIL, OP_EVAL for modular functions). Builds on today's base for high-volume: Dynamic iteration reduces size 5-10x, enabling 100+ commits without bloat.

### Problem Summary
In BCH DeFi (e.g., constant-product AMMs), "anyone-can-spend" covenants allow open interactions but create issues:
- **Contention**: Multiple txs spend the same UTXO; only one confirms, others fail with 10+ min retries (Poisson variance).
- **MEV**: Miners reorder for profit, breaking chains.
- **UX Friction**: Delays transitions (e.g., DeFi-to-commerce), hindering adoption.

### How Solved Today (2018-Enabled Features)
Using OP_CAT (re-enabled May 2018 for concatenation), SHA256, checkDataSig (partial preimage binding), and recursion via NFT outputs: Commit hashes queue actions (anti-front-running), reveal merkleizes for fair order/resolution. Deploy/test now on chipnet—atomic for small batches, but unrolled ops limit scale (bloat for >5 commits).

### How Solved in Future (2026 Upgrades)
Proposals like loops (OP_BEGIN/OP_UNTIL) and OP_EVAL enable efficient iteration/modularity: Dynamic appending/merkle without repetition, scaling to high-volume without limits. Reduces bloat 5-10x, strengthens anti-MEV (full preimage ties), makes recursion "snappier" for real DeFi—atomic batches resolve contention instantly.

For details on 2026 proposals:
- Loops (OP_BEGIN/OP_UNTIL): https://github.com/bitjson/bch-loops
- OP_EVAL for modular functions: https://bitcoincashresearch.org/t/chip-2024-12-op-eval-function-evaluation/1450/13 (related forum thread on evaluation opcodes).

### Setup
1. **Prerequisites**: Python 3.8+ for simulator; Node.js/CashScript CLI for contracts.
2. **Python Simulator**:
   - Create venv: `python -m venv venv; source venv/bin/activate`.
   - Install: `pip install numpy`.
   - Run: `python amm_prototype.py`.
3. **CashScript Contracts**:
   - Install: `npm install -g cashscript-cli`.
   - Compile: `cashc SequencedAMM_25.cash -o SequencedAMM_25.json` (today) or `cashc SequencedAMM_26.cash -o SequencedAMM_26.json` (future, test on upgraded chipnet).

### Usage
- **Python Simulator**: Interactive REPL—`commit` to queue, `reveal <hash> <amount> <True/False>` to swap, `multi <num>` for races, `status`/`withdraw`. Simulates contention resolution.
- **CashScript**:
  - Deploy: Mint NFT with reserves via SDK/Electron Cash.
  - Commit: Call `commit(actionHash)` (array in 26.cash).
  - Swap: Call `swap(...)`—verifies/merkleizes/recurses.
  - Withdraw: Call `withdraw(...)`—burns NFT.
- **Testing**: Pair simulator with contracts on chipnet; simulate races to see trustless merkle enforcement.

## License
MIT License—test thoroughly.