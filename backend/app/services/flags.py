import hashlib

class FlagService:
    def evaluate(self, user_id: str, flag: dict) -> bool:
        if not flag["enabled"]:
            return False
        bucket = int(hashlib.md5(f"{user_id}:{flag['name']}".encode()).hexdigest(), 16) % 100
        return bucket < flag["rollout_pct"]