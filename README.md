# secure-cli-password-manager
## Security

This project was designed with a strong focus on local credential protection and secure data handling.

### Encryption

All stored credentials are protected using **AES-256 encryption** through Python's `cryptography` library. Before being written to disk, sensitive information is encrypted using a key derived from the user's master password.

This ensures that:

- Passwords are never stored in plain text;
- Sensitive data remains protected even if the local storage file is exposed;
- Unauthorized users cannot recover stored credentials without the correct master password.

### Secure Local Storage

Credentials are stored inside a modified and encrypted JSON file. Even in the event of file leakage or unauthorized access, the encrypted content remains unreadable without the decryption key.

### Master Password Authentication

The application only decrypts stored data after successful master password validation. Without the correct master password, the encrypted credentials cannot be accessed or restored.

### Cryptography Approach

Unlike simple hashing mechanisms, this project uses **reversible encryption** because the application must be capable of recovering the original credentials when authorized by the user.

The workflow follows this structure:

1. The user creates a master password;
2. A cryptographic key is derived securely from the master password;
3. Credentials are encrypted using AES-256;
4. Encrypted data is stored locally;
5. Data is decrypted only after successful authentication.

### Security Goals

The main security objectives of the project are:

- Confidentiality of stored credentials;
- Protection against local file exposure;
- Secure authentication using a master password;
- Prevention of plain-text password storage.

### Technologies Used

- Python
- `cryptography` library
- AES-256 encryption
- Secure key derivation mechanisms
