import json
import os
import hashlib

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
    dados = ler_dados()
    if "credenciais" not in dados:
        dados["credenciais"] = {}
    
    dados["credenciais"][servico] ={
        "usuario": usuario,
        "senha": senha_pura
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

