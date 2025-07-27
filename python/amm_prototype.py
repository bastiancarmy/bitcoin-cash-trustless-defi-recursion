import hashlib
import numpy as np
import threading
import time
import random

# Mock pool state
initial_k = 1000000
pool_bch = 1000
pool_tokens = 1000
merkle_root = b'\x00' * 32
commitments = []  # List of (user_id, action_hash) for demo
state_lock = threading.Lock()  # Lock for shared state access

def sha256(data):
    return hashlib.sha256(data).digest()

def cat(*args):
    return b''.join([bytes(arg) if isinstance(arg, int) else arg for arg in args])

def simulate_tx(commit_hash=None, input_amount=0, is_bch_input=True, action='swap', user_id=''):
    global pool_bch, pool_tokens, merkle_root, commitments
    with state_lock:  # Ensure atomicity for multi-thread
        if action == 'commit':
            action_details = f"{user_id} {input('Enter action details: ')}"
            action_hash = sha256(action_details.encode())
            commitments.append((user_id, action_hash))
            new_commitment = cat(merkle_root, action_hash)
            merkle_root = sha256(new_commitment)
            print(f"{user_id} Committed: Hash {action_hash.hex()}. New Merkle Root: {merkle_root.hex()}")
            return action_hash.hex()  # Return hex for easy CLI paste

        elif action == 'swap':
            commit_hash_bytes = bytes.fromhex(commit_hash)
            matching_commit = next((c for c in commitments if c[1] == commit_hash_bytes and c[0] == user_id), None)
            if not matching_commit:
                raise ValueError("Invalid commit hash for this user!")
            commitments.remove(matching_commit)
            
            sequenced_inputs = cat(pool_bch.to_bytes(8, 'big'), pool_tokens.to_bytes(8, 'big'), input_amount.to_bytes(8, 'big'))
            new_merkle_root = sha256(sequenced_inputs)
            
            new_pool_bch = pool_bch + input_amount if is_bch_input else pool_bch - input_amount
            new_pool_tokens = initial_k // new_pool_bch
            output_amount = pool_tokens - new_pool_tokens if is_bch_input else new_pool_tokens - pool_tokens
            
            pool_bch = new_pool_bch
            pool_tokens = new_pool_tokens
            merkle_root = new_merkle_root
            
            fee = 2000
            wait_time = np.random.exponential(scale=10)
            print(f"{user_id} Swap executed: Output {output_amount}. New Pool: BCH={pool_bch}, Tokens={pool_tokens}")
            print(f"{user_id} Merkle Root Updated: {merkle_root.hex()}. Simulated Wait: {wait_time:.2f} min")
            return output_amount

        elif action == 'withdraw':
            withdrawn_bch = pool_bch
            withdrawn_tokens = pool_tokens
            pool_bch = 0
            pool_tokens = 0
            merkle_root = b'\x00' * 32
            print(f"{user_id} Withdrawn: BCH={withdrawn_bch}, Tokens={withdrawn_tokens}. Pool Reset.")
            return withdrawn_bch, withdrawn_tokens

def user_thread(user_id, commit_details, amount, is_bch_input):
    time.sleep(random.uniform(0.1, 1))  # Simulate network delay
    commit_hash = simulate_tx(action='commit', user_id=user_id)
    time.sleep(random.uniform(0.5, 2))  # Delay before reveal
    try:
        simulate_tx(commit_hash, amount, is_bch_input, user_id=user_id)
    except ValueError:
        print(f"{user_id} Reveal failed: Contention or mismatch!")

def simulate_multi_user(num_users):
    threads = []
    for i in range(num_users):
        user_id = f"User-{i+1}"
        commit_details = f"swap {50 * (i+1)} {'BCH' if i % 2 == 0 else 'Tokens'}"
        amount = 50 * (i+1)
        is_bch = i % 2 == 0
        t = threading.Thread(target=user_thread, args=(user_id, commit_details, amount, is_bch))
        threads.append(t)
        t.start()
    for t in threads:
        t.join()

# CLI REPL
print("SequencedAMM Simulator with Multi-User Threading")
print("Commands: commit, reveal <hash> <amount> <True/False>, withdraw, status, multi <num_users>, exit")

while True:
    cmd = input("> ").strip().split()
    if not cmd:
        continue
    action = cmd[0].lower()
    
    try:
        if action == 'commit':
            simulate_tx(action='commit')
        elif action == 'reveal':
            if len(cmd) < 4:
                print("Usage: reveal <hash> <amount> <True/False>")
                continue
            commit_hash = cmd[1]
            amount = int(cmd[2])
            is_bch = cmd[3].lower() == 'true'
            simulate_tx(commit_hash, amount, is_bch)
        elif action == 'withdraw':
            simulate_tx(action='withdraw')
        elif action == 'status':
            print(f"Pool: BCH={pool_bch}, Tokens={pool_tokens}, K={initial_k}")
            print(f"Merkle Root: {merkle_root.hex()}")
            print(f"Pending Commitments: {len(commitments)}")
        elif action == 'multi':
            if len(cmd) < 2:
                print("Usage: multi <num_users>")
                continue
            num_users = int(cmd[1])
            simulate_multi_user(num_users)
        elif action == 'exit':
            break
        else:
            print("Invalid command!")
    except Exception as e:
        print(f"Error: {e}")