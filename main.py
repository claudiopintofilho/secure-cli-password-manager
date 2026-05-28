from gerenciador import (adicionar_senha, 
                         ler_dados,
                         buscar_e_descriptografar_senha,
                         verificar_senha_mestre, 
                         registrar_senha_mestre,
                         iniciar_sessao)

def exibir_menu():
    print("\n" + "=" * 30)
    print("Gerenciador de Senhas CLI")
    print("=" * 30)
    print("1. Adicionar nova senha")
    print("2. Listar Servicos Salvos")
    print("3. Sair")
    print("=" * 30)

def autenticar_usuario():
    dados = ler_dados()

    if "config" not in dados:
        print("Bem-Vindo ao Gerenciador de Senhas!")
        print("Defina uma SENHA MESTRE. Nao a perca, ela nao pode ser recuperada!")

        while True:
            senha = input("Digite sua nova SENHA MESTRE: ").strip()
            confirmar_senha = input("Confirme sua SENHA MESTRE: ").strip()

            if senha == confirmar_senha and senha != "":
                registrar_senha_mestre(senha)
                iniciar_sessao(senha)
                break
            else:
                print("As senhas nao coincidem ou estao vazias. Tente novamente.")
    else:
        print("🔒O cofre esta trancado.")
        tentativas = 3
        while tentativas > 0:
            senha_digitada = input("Digite sua SENHA MESTRE para acessar: ").strip()
            if verificar_senha_mestre(senha_digitada):
                print("Acesso concedido! Bem-vindo de volta.")
                iniciar_sessao(senha_digitada)
                return True
            else:
                tentativas -= 1
                print(f"⚠️Senha incorreta. Tentativas restantes: {tentativas}")
        print("⚠️Excesso de tentativas. Programa encerrado por segurança.")
        return False

def main():
    if not autenticar_usuario():
        return
    
    while True:
        exibir_menu()
        escolha = input("Escolha uma opção: ").strip()

        if escolha == "1":
            servico = input("Nome do Serviço (ex : GitHub, Netflix): ").strip()
            usuario = input("Usuario/E-mail: ").strip()
            senha = input("Senha: ").strip()

            if servico and usuario and senha:
                adicionar_senha(servico, usuario, senha)
            else:
                print("⚠️Todos os campos são obrigatórios. Tente novamente.")
        elif escolha == "2":
            dados = ler_dados()
            credenciais = buscar_e_descriptografar_senha()  # Agora retorna as senhas descriptografadas
            
            if not credenciais:
                print("\n📭 Nenhum serviço cadastrado ainda.")
            else:
                print("\n📋 Serviços cadastrados:")
                for servico, info in credenciais.items():
                    print(f"- {servico} (Usuário: {info['usuario']} | Senha: {info['senha']})")
        elif escolha == "3":
            print("\n Saindo... Mantenha-se Sseguro!")
            break
        else:
            print("⚠️Opção inválida. Tente novamente.")

if __name__ == "__main__":
    main()