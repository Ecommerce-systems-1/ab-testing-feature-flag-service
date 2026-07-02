import hashlib
import json

class AssignmentService:
    def assign(self, user_id: str, experiment: dict) -> str | None:
        key = f"{user_id}:{experiment['id']}"
        bucket = int(hashlib.md5(key.encode()).hexdigest(), 16) % 100
        variants = experiment["variants"]
        splits = experiment["traffic_split"]
        cumulative = 0
        for variant, split in zip(variants, splits):
            cumulative += split
            if bucket < cumulative:
                return variant
        return None  # user not in experiment