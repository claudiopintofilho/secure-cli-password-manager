# Secure CLI Password Manager

## Description
A secure, lightweight, and local Command-Line Interface (CLI) password manager written in Python. This project was developed to practice core cybersecurity concepts, such as symmetric encryption, cryptographic hashing, and secure key derivation, applied within a clean software architecture.

---

## Security Architecture

This project was designed with a strong focus on local credential protection, data integrity, and secure data handling.

### Cryptography Approach

Unlike naive storage solutions, this project combines both **hashing** and **reversible symmetric encryption** to achieve maximum local security without compromising usability:

1. **One-Way Hashing (SHA-256 + Salt):** Used exclusively to verify the Master Password. The actual password is never stored on disk. Instead, the application generates a unique cryptographic fingerprint (hash) combined with a random 16-byte `salt` to prevent rainbow table and dictionary attacks.
2. **Key Derivation Function (PBKDF2):** Upon a successful login, the application uses **PBKDF2HMAC** (with SHA-256 and 100,000 iterations) to securely derive a 32-byte encryption key from the user's Master Password. This key exists *only* within the volatile memory (RAM) while the program runs and is never written to disk.
3. **Reversible Symmetric Encryption (AES-256 / Fernet):** Used for the credentials repository. Since the application must recover the original plain-text passwords for the user, it encrypts them using the derived RAM key before writing to the local file, and decrypts them on the fly during runtime.

### Secure Local Storage

Credentials are stored inside a dedicated JSON file (`dados_criptografados.json`). Even in the event of local file leakage, unauthorized access, or physical theft of the machine, the encrypted content remains mathematically unreadable without the proper decryption key.

### Master Password Authentication

The application acts as a secure vault. It will strictly deny access and refuse to decrypt any stored data unless a valid master password is provided. For enhanced security, the application automatically terminates after 3 consecutive failed login attempts.

### Security Goals Met:
- **Confidentiality:** Zero plain-text password storage.
- **Data Protection:** Protection against local file exposure and leakage.
- **Secure Authentication:** Robust master password validation using standard cryptographic guidelines.

---

## Technologies Used

- **Python 3** (Core logic and CLI)
- **`cryptography` library** (Fernet implementation and PBKDF2HMAC)
- **`hashlib` & `os` modules** (SHA-256 hashing and cryptographically secure pseudo-random number generation for Salts)
- **JSON** (Structured local data management)

---

## How to Install and Run

### Prerequisites
Make sure you have Python 3 installed on your machine.

### 1. Clone the repository
```bash
git clone [https://github.com/YOUR-USERNAME/secure-cli-password-manager.git](https://github.com/YOUR-USERNAME/secure-cli-password-manager.git)
cd secure-cli-password-manager
```

---

### 2. Setup the Virtual Environment (Highly Recommended)

Create and activate a virtual environment to isolate the project dependencies.

#### Linux / macOS

```bash
python3 -m venv venv
source venv/bin/activate
```

#### Windows

```bash
python -m venv venv
venv\Scripts\activate
```

---

### 3. Install Dependencies

Install the required security libraries:

```bash
pip install cryptography
```

---

### 4. Run the Application

```bash
python main.py
```
venv\Scripts\activate
