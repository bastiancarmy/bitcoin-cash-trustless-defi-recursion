# SequencedAMM: Covenant-Based AMM for BCH DeFi

## Overview
This folder contains two CashScript contract versions for a constant-product Automated Market Maker (AMM) with commit-reveal sequencing and covenant recursion on Bitcoin Cash (BCH). They demonstrate atomic resolution of UTXO contention and MEV without signers or block time changes—using merkleized state for fair ordering and recursion via NFT commitments. The contracts address DeFi limitations like concurrent double-spends on public pools.

- **SequencedAMM_25.cash**: Deployable today (post-2018 fork with OP_CAT for appending, SHA256 for merkle, basic introspection). Handles small-scale contention (2-5 commits) but uses manual unrolling for sequences, limiting efficiency due to script bloat.
- **SequencedAMM_26.cash**: Hypothetical for 2026 upgrades (loops via OP_BEGIN/OP_UNTIL, OP_EVAL for modular functions). Builds on today's base for scalability—dynamic batches (100+ commits) without bloat, 5-10x size reduction, reusable logic for complex state/extraction.

### What It Demonstrates
- **Trustless DeFi Recursion**: Commit hashes to queue actions (anti-front-running), reveal to swap atomically. Merkle roots enforce sequence; outputs recurse state (updated reserves/merkle in NFT).
- **DeFi Limitations Addressed**: Handles concurrent double-spends on public UTXOs (e.g., AMM pools)—resolves in one tx without waits. Anti-MEV via preimage binding.
- **Now (25.cash) vs. Future (26.cash)**: Today's version enables proofs-of-concept (deploy/test now for basics). 2026 optimizes: Loops iterate for appending/sequencing (no unrolling bloat); OP_EVAL modularizes extraction/math (faster, scalable for high-volume without VM limits).

### Setup
1. **Install CashScript**: `npm install -g cashscript-cli` (requires Node.js).
2. **Compile**:
   - For today: `cashc SequencedAMM_25.cash -o SequencedAMM_25.json`.
   - For future (hypothetical—test on upgraded chipnet): `cashc SequencedAMM_26.cash -o SequencedAMM_26.json`.

### How to Use
- **Deployment**: Use CashScript SDK or Electron Cash—mint initial NFT with reserves (e.g., 1000 BCH, 1000 Tokens).
- **Commit**: Build tx calling `commit(actionHash)` (or array in 26.cash)—queues hash(es) in NFT.
- **Reveal/Swap**: Call `swap(inputAmount, isBCHInput, commitHash)`—verifies, swaps, recurses.
- **Withdraw**: Call `withdraw(lpPk, lpSig)`—burns NFT, reclaims funds.
- **Testing**: On chipnet—simulate contention with concurrent txs; merkle enforces order. For 25.cash, limit to small batches; 26.cash scales via loops.
- **Advantages of 26.cash**: Dynamic loops/OP_EVAL enable high-volume (e.g., iterate 100 commits without code repetition vs. today's unrolled bloat); modular functions reduce size 5-10x, improve UX for complex DeFi.

## License
MIT License—test on testnet before mainnet.