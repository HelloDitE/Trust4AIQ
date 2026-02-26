#Ce module servira à rendre illisibles les données des patients avant de les stocker.

from cryptography.fernet import Fernet
from config.settings import SECRET_KEY

# On initialise le "chiffreur" avec la clé du .env
cipher_suite = Fernet(SECRET_KEY)

def encrypt_data(data: str) -> str:
    """
    Transforme un texte clair en texte chiffré illisible.
    Ex: "Asthme" -> "gAAAAABk..."
    """
    if data is None:
        return None
    # On doit convertir le texte (str) en bytes, puis chiffrer, puis revenir en string
    return cipher_suite.encrypt(data.encode('utf-8')).decode('utf-8')

def decrypt_data(token: str) -> str:
    """
    Transforme un texte chiffré en texte clair.
    Ex: "gAAAAABk..." -> "Asthme"
    """
    if token is None:
        return None
    try:
        return cipher_suite.decrypt(token.encode('utf-8')).decode('utf-8')
    except Exception as e:
        print(f"Erreur de déchiffrement : {e}")
        return "ERROR_DECRYPT"