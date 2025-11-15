from cryptography.fernet import Fernet
import os
import json

VAULT_FILE = "vault.json"
KEY_FILE = "vault.key"

# Generate encryption key (only once)
def generate_key():
    if not os.path.exists(KEY_FILE):
        key = Fernet.generate_key()
        with open(KEY_FILE, "wb") as f:
            f.write(key)

def load_key():
    with open(KEY_FILE, "rb") as f:
        return f.read()

def encrypt_data(data, key):
    fernet = Fernet(key)
    return fernet.encrypt(data.encode()).decode()

def decrypt_data(data, key):
    fernet = Fernet(key)
    return fernet.decrypt(data.encode()).decode()

def load_vault():
    if not os.path.exists(VAULT_FILE):
        return {}
    with open(VAULT_FILE, "r") as f:
        return json.load(f)

def save_vault(vault):
    with open(VAULT_FILE, "w") as f:
        json.dump(vault, f, indent=2)

def add_password():
    site = input("Enter website/app name: ").strip()
    username = input("Enter username/email: ").strip()
    password = input("Enter password: ").strip()

    key = load_key()
    vault = load_vault()

    encrypted_pw = encrypt_data(password, key)
    vault[site] = {"username": username, "password": encrypted_pw}

    save_vault(vault)
    print(f"✅ Password saved securely for {site}!")

def view_passwords():
    key = load_key()
    vault = load_vault()

    if not vault:
        print("⚠️ No saved passwords yet.")
        return

    for site, creds in vault.items():
        decrypted_pw = decrypt_data(creds["password"], key)
        print(f"\n🔹 {site}")
        print(f"   👤 {creds['username']}")
        print(f"   🔑 {decrypted_pw}")

def main():
    generate_key()
    print("\n🔐 Encrypted Password Vault")
    print("------------------------------")

    while True:
        print("\n1️⃣ Add New Password")
        print("2️⃣ View Saved Passwords")
        print("3️⃣ Exit")

        choice = input("\nSelect an option: ")

        if choice == "1":
            add_password()
        elif choice == "2":
            view_passwords()
        elif choice == "3":
            print("👋 Goodbye — Stay secure!")
            break
        else:
            print("❌ Invalid choice. Please try again.")

if __name__ == "__main__":
    main()
