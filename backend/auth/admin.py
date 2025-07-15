from werkzeug.security import check_password_hash

# Usuario fijo
ADMIN_USERNAME = "Mauricio"
ADMIN_PASSWORD_HASH = "scrypt:32768:8:1$W2LPZY66HwGPK9Tn$3df9af09f8adf61be83addbd19a9b087aefb28a6b98ea4ced32dedfb1544deb40c5061dd43fb7e55fd558ed9ae3633353be909ed25afd04035cd884998cd915e"

def verify_credentials(username, password):
    return username == ADMIN_USERNAME and check_password_hash(ADMIN_PASSWORD_HASH, password)
