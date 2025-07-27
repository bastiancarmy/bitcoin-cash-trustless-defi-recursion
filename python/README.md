# SequencedAMM Simulator: Covenant Recursion for DeFi Without Trust

## Overview

This Python script is a CLI-driven REPL simulator for a covenant-based Automated Market Maker (AMM) on Bitcoin Cash (BCH), demonstrating "covenant recursion for DeFi without trust." It models how BCH's scripting can enable atomic, fair sequencing of DeFi interactions (e.g., swaps in a constant-product pool) without external signers, oracles, or protocol changes like faster block times.

### What It Demonstrates

*   **Trustless Resolution of DeFi Problems**: Simulates UTXO contention (multiple users racing to spend the same pool UTXO) and Miner Extractable Value (MEV, reordering for profit). Uses merkleized commit-reveal: Users commit hashed actions (queuing without revealing), then reveal to process swaps atomically. The "covenant" (simulated logic) appends hashes to a merkle root for fair order, recurses state via updates (like NFT commitments), and binds to a tx preimage for anti-MEV—all on-chain-like, without trust.
*   **Key DeFi Scenario**: In a multi-user race (e.g., via threading), commits queue fairly; reveals enforce sequence and resolve contention without failures or long waits (mock Poisson variance shown, but atomic batching mitigates it). Mismatched reveals (tampering) fail trustlessly.
*   **Now vs. Future**: Based on today's BCH (2018-re-enabled OP\_CAT for appending, SHA256 for merkle, basic introspection). Previews 2026 upgrades (loops/OP\_EVAL for scale)—handles small contention now, but upgrades enable high-volume without bloat.
*   **Relevance**: Addresses real AMM limitations (e.g., accidental double-spends on public contracts, 10+ min retries) in a decentralized, non-custodial way—complements discussions on faster blocks or alternatives like Tailstorm.

### Setup

1.  **Prerequisites**: Python 3.8+ installed.
2.  **Create Virtual Environment** (recommended for isolation):
    
    ```
    python -m venv venv source venv/bin/activate # macOS/Linux # or venv\Scripts\activate on Windows 
    ```
    
3.  **Install Dependencies**:
    
    ```
    pip install numpy 
    ```
    
4.  **Run the Script**:
    
    ```
    python amm_prototype.py 
    ```
    

### How to Use (CLI Commands)

The script starts an interactive REPL. Commands simulate DeFi workflow: Commit actions (queue hashes), reveal to execute swaps (resolve atomically), withdraw liquidity, check status, or run multi-user races.

*   **status**: View current pool state (reserves, merkle root, pending commitments).
    *   Example: `status`
    *   Demonstrates: Initial/updated state after recursion.
*   **commit**: Queue a hashed action (enter details at prompt, e.g., "swap 50 BCH").
    *   Example: `commit` then enter "swap 50 BCH".
    *   Demonstrates: Commit phase—appends hash to merkle root without revealing, preventing front-running.
*   **reveal <True/False>**: Execute swap on committed hash (True for BCH input, False for Tokens).
    *   Example: `reveal ca9f145926c8e58d68cdb92f90d5b8a45da118b81925392f81b599e9f7374aab 50 True` (paste hash from commit).
    *   Demonstrates: Reveal phase—verifies commit, merkleizes sequence, recurses state, shows output/wait. Fails on mismatch (trustless enforcement).
*   **withdraw**: Reclaim liquidity (simplified: full pool reset).
    *   Example: `withdraw`
    *   Demonstrates: Trustless LP exit—burns NFT, ends recursion.
*   **multi <num\_users>**: Simulate concurrent users racing commits/reveals (threading for contention).
    *   Example: `multi 2`
    *   Demonstrates: Real-world races—merkle ensures fair order, resolves without failures. Try `multi 5` for higher contention.
*   **exit**: Quit the REPL.

**Example Full Run (Contention Demo)**:

1.  `status` (initial pool).
2.  `multi 2` (race 2 users: one adds BCH, one swaps Tokens—merkle sequences, resolves atomically with mock waits).
3.  Attempt invalid reveal (e.g., `reveal invalid_hash 10 True`)—fails trustlessly.
4.  `status` (updated state after recursion).

**Notes**:

*   Hashes vary per run—copy from commits for reveals.
*   Mock wait uses numpy exponential (Poisson for block variance)—shows mitigation via batching.
*   For real BCH: Pair with the CashScript contract (deploys today for basics).

## License

MIT License—feel free to fork and experiment.
