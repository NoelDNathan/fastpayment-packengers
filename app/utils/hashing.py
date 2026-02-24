import bcrypt

class PasswordSecurity:
    @staticmethod
    def hash(p: str) -> str:
        return bcrypt.hashpw(p.encode("utf-8")[:72], bcrypt.gensalt()).decode("utf-8")

    @staticmethod
    def verify(p: str, h: str) -> bool:
        return bcrypt.checkpw(p.encode("utf-8")[:72], h.encode("utf-8"))
