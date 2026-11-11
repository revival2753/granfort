from pwdlib import PasswordHash

password_hash = PasswordHash.recommended()

# хеширует пароль для сохр в бд
def get_password_hash(password: str) -> str:
    return password_hash.hash(password)

# сверка данных пароля
def verify_password(plain_password: str, hashed_password: str) -> bool:
    return password_hash.verify(plain_password, hashed_password)