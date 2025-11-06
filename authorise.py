import bcrypt

def hash_password(plain_text_pass):
    pass_bytes = plain_text_pass.encode('utf-8')
    salt = bcrypt.gensalt()
    hashed_pass = bcrypt.hashpw(pass_bytes,salt)
    return hashed_pass

passd = "secretpanda"
pass_hash = hash_password(passd)
print(f"Password: {passd} Hash: {str(pass_hash)}")

def register_user(username,password):
    hashed_password = hash_password(password)
    with open("users.txt","a") as f:
        f.write(f"{username},{hashed_password}")
    print(f"User {username} registered.")
    print("Hello")
    
def login_user(usernem,password):
    with open("users.txt","r") as f:
        for line in f.readlines():
            user,hash = line.strip().split(',',1)