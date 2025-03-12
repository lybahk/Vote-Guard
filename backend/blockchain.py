import hashlib
import time

class Blockchain:
    def __init__(self):
        self.chain = []
        self.create_block(previous_hash="0")

    def create_block(self, vote=None, previous_hash=None):
        block = {
            "index": len(self.chain) + 1,
            "timestamp": time.time(),
            "vote": vote,
            "previous_hash": previous_hash or self.get_last_hash(),
            "hash": hashlib.sha256(str(vote).encode()).hexdigest()
        }
        self.chain.append(block)
        return block

    def get_last_hash(self):
        return self.chain[-1]["hash"] if self.chain else "0"
