from itsdangerous import URLSafeTimedSerializer
from config import Config

def generate_token(email):
    serializer = URLSafeTimedSerializer(Config.SECRET_KEY)
    return serializer.dumps(email, salt='email-verification-salt')

def verify_token(token, expiration=1800):
    serializer = URLSafeTimedSerializer(Config.SECRET_KEY)
    try:
        email = serializer.loads(token, salt='email-verification-salt', max_age=expiration)
        return email
    except Exception:
        return None
