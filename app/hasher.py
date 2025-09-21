from streamlit_authenticator import Hasher

# List your plain-text passwords here
passwords = ["abc", "def"]

# Generate hashed passwords
hashed_passwords = Hasher(passwords).generate()

print("Hashed passwords:")
for pwd in hashed_passwords:
    print(pwd)
