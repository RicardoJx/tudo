import hashlib

def hashed(text):
    return hashlib.md5(text.encode()).hexdigest()


SIMPLE_USER_DATA={
    'name':'tudo',
    'password':hashed('pass')
}
print(SIMPLE_USER_DATA)



def authenticate(username,password):
    return (SIMPLE_USER_DATA['name']==username) and (SIMPLE_USER_DATA['password']==hashed(password))