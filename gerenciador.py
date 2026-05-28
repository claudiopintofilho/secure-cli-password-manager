import json
import os
import hashlib
import base64 
from cryptography.fernet import Fernet
from cryptography.hazmat.primitives import hashes
from cryptography.hazmat.primitives.kdf.pbkdf2 import PBKDF2HMAC

_CHAVE_CRIPTOGRAFICA = None

ARQUIVOS_DADOS = "dados_criptografados.json"

def ler_dados():
    if not os.path.exists(ARQUIVOS_DADOS):
        return {}
    try:
        with open(ARQUIVOS_DADOS, "r", encoding="utf-8") as arquivo:
            return json.load(arquivo)
    except json.JSONDecodeError:
        return {}
    
def salvar_dados(dados):
    with open(ARQUIVOS_DADOS, "w", encoding="utf-8") as arquivo:
        json.dump(dados, arquivo, indent=4)

def adicionar_senha(servico, usuario, senha_pura):
    global _CHAVE_CRIPTOGRAFICA
    if _CHAVE_CRIPTOGRAFICA is None:
        print("⚠️Erro: Sessão não iniciada. Autentique-se primeiro.")
        return
    
    dados = ler_dados()
    if "credenciais" not in dados:
        dados["credenciais"] = {}
    
    #inicializa o motor de criptografia com a nossa chave da memoria RAM
    f = Fernet(_CHAVE_CRIPTOGRAFICA)
    senha_bytes = senha_pura.encode('utf-8')
    senha_criptografada_bytes = f.encrypt(senha_bytes)

    senha_criptografada_str = senha_criptografada_bytes.decode('utf-8')


    dados["credenciais"][servico] ={
        "usuario": usuario,
        "senha": senha_criptografada_str
    }
    salvar_dados(dados)
    print(f"Credencial para '{servico}' adicionada com sucesso.")

def gerar_hash_senha(senha_mestre, salt=None):
    if salt is None:
        salt = os.urandom(16)
    
    validador = hashlib.sha256(salt + senha_mestre.encode('utf-8')).hexdigest()
    return validador, salt.hex()

def verificar_senha_mestre(senha_digitada):
    dados = ler_dados()
    if "config" not in dados:
        return False
    hash_salvo = dados["config"]["master_hash"]
    salt_salvo = dados["config"]["salt"]

    salt_bytes = bytes.fromhex(salt_salvo)
    novo_hash,_ = gerar_hash_senha(senha_digitada, salt_bytes)

    return novo_hash == hash_salvo

def registrar_senha_mestre(senha_mestre):
    dados = ler_dados()
    hash_validador, salt_hex = gerar_hash_senha(senha_mestre)

    dados["config"] = {
        "master_hash": hash_validador,
        "salt": salt_hex
    }

    if "credenciais" not in dados:
        dados["credenciais"] = {}

    salvar_dados(dados)
    print("Senha mestre registrada com sucesso! Seu cofre de senhas está protegido.")


def derivar_char(senha_mestre, salt_hex):
    #deriva uma chave de 32 bytes
    salt_bytes = bytes.fromhex(salt_hex)
    kdf = PBKDF2HMAC(
        algorithm=hashes.SHA256(),
        length=32,
        salt=salt_bytes,
        iterations=100_000, # Rodar 100 mil vezes para aumentar a segurança contra ataques de força bruta
    )

    #Gera a chave e codifica em Base64 para uso com Fernet  
    chave = base64.urlsafe_b64encode(kdf.derive(senha_mestre.encode('utf-8')))
    return chave

def iniciar_sessao(senha_mestre):
    global _CHAVE_CRIPTOGRAFICA
    dados = ler_dados()
    salt_hex = dados["config"]["salt"]
    _CHAVE_CRIPTOGRAFICA = derivar_char(senha_mestre, salt_hex)

def buscar_e_descriptografar_senha():
    global _CHAVE_CRIPTOGRAFICA
    dados = ler_dados()
    credenciais = dados.get("credenciais", {})

    if not credenciais or _CHAVE_CRIPTOGRAFICA is None:
        return credenciais
    
    f = Fernet(_CHAVE_CRIPTOGRAFICA)
    credenciais_descriptografadas = {}

    for servico, info in credenciais.items():
        try:
            senha_criptografada_bytes = info["senha"].encode('utf-8')
            senha_descriptografada_bytes = f.decrypt(senha_criptografada_bytes)
            senha_descriptografada = senha_descriptografada_bytes.decode('utf-8')
            credenciais_descriptografadas[servico] = {
                "usuario": info["usuario"],
                "senha": senha_descriptografada
            }
        except Exception:
            credenciais_descriptografadas[servico] = {
                "usuario": info["usuario"],
                "senha": "⚠️Erro ao descriptografar"
            }

    return credenciais_descriptografadas