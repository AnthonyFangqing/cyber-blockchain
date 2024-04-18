import hashlib
import time
from dataclasses import dataclass
import copy
from dacite import from_dict

@dataclass
class Transaction:
    sender: str
    recipient: str
    amount: float


@dataclass
class Block:
    index: int
    transactions: list[Transaction]
    proof: int
    previous_hash: str


class Blockchain:
    def __init__(self, address, difficulty_number, mining_reward):
        self.address = address
        self.difficulty_number = difficulty_number
        self.mining_reward = mining_reward
        self.chain = []
        self.current_transactions = []
        self.players = set()

        
        genesis_block = self.create_block(0, [Transaction("GOD", self.address, 100)], 0, 0)
        while not self.check_proof(genesis_block):
            genesis_block.proof += 1
        self.add_block(genesis_block)

    def create_block(self, index, transactions, proof, previous_hash):
        return Block(index, copy.copy(transactions), proof, previous_hash)

    def create_transaction(self, sender, recipient, amount):
        return Transaction(sender, recipient, amount)

    def get_transactions(self):
        return self.current_transactions

    def current_block(self):
        return self.chain[-1]

    def add_transaction(self, sender, recipient, amount):
        self.current_transactions.append(Transaction(sender, recipient, amount))

    def next_index(self):
        return len(self.chain) + 1

    def get_length(self):
        return len(self.chain)

    def add_block(self, block):
        if self.check_proof(block):
            self.chain.append(block)

    def add_player(self, address):
        self.players.add(address)

    def hash_block(self, block):
        return hashlib.sha256(str(block).encode()).hexdigest()

    def check_proof(self, block):
        # Check that the hash of the block ends in difficulty_number many zeros
        return self.hash_block(block)[:self.difficulty_number] == '0' * self.difficulty_number

    def mine(self):
        # Give yourself a reward at the beginning of the transactions
        self.add_transaction("GOD", self.address, self.mining_reward)
        
        last_block = self.current_block()
        new_block = self.create_block(last_block.index + 1, self.current_transactions, 0, self.hash_block(last_block))
        
        # Find the right value for proof
        while not self.check_proof(new_block):
            new_block.proof += 1
        
        # Add the block to the chain
        self.add_block(new_block)
        
        # Clear your current transactions
        self.current_transactions = []

    def validate_chain(self, chain):
        # Check that the chain is valid
        # The chain is an array of blocks
        # You should check that the hashes chain together
        # The proofs of work should be valid
        return True

    def receive_chain(self, chain_raw_json):
        chain = [from_dict(Block, b) for b in chain_raw_json]
        if self.validate_chain(chain) and len(chain) > self.get_length():
            self.chain = chain
            return True
        return False
