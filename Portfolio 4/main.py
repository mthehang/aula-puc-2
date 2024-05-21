from paciente import Paciente
from atendimento import Atendimento


def menu_paciente():
    while True:
        print("\nMenu Pacientes")
        print("1. Cadastrar novo paciente")
        print("2. Ver todos os pacientes")
        print("3. Atualizar um cadastro de paciente")
        print("4. Ver quantidade de pacientes por sexo")
        print("5. Ver idade média dos pacientes")
        print("00. Voltar ao menu principal")

        while True:
            try:
                opcao = int(input("Digite uma opção: "))
                break
            except ValueError:
                print("Opção inválida! Tente novamente.")

        match opcao:
            case '1':
                nome = input("\nNome: ").title()
                while True:
                    try:
                        rg = int(input("RG: "))
                        if len(str(rg)) == 9:
                            break
                        else:
                            print("Por favor, insira um número RG válido.")
                    except ValueError:
                        print("Por favor, insira um número RG válido.")

                while True:
                    sexo = input("Sexo (M/F): ").upper()
                    if len(sexo) == 1 and sexo.upper() == 'M' or 'F':
                        break
                    else:
                        print("Digite apenas M ou F.")

                while True:
                    data_nasc = input("Data de nascimento (AAAA-MM-DD): ")
                    if Paciente.validar_data(data_nasc):
                        break
                    else:
                        print("Data inválida. Por favor, insira a data no formato AAAA-MM-DD.")

                while True:
                    try:
                        peso = float(input("Peso (kg): ").replace(',', '.'))
                        break
                    except ValueError:
                        print("Por favor, insira um peso válido.")

                while True:
                    try:
                        altura = float(input("Altura (m): ").replace(',', '.'))
                        break
                    except ValueError:
                        print("Por favor, insira um peso válido.")

                paciente = Paciente(rg, nome, sexo, data_nasc, peso, altura)
                paciente.salvar()
                input("\nPressione ENTER para voltar ao Menu Principal")
                break

            case '2':
                Paciente.listar_todos()
                input("\nPressione ENTER para voltar ao Menu Principal")
                break
            case '3':
                while True:
                    try:
                        id_paciente = int(input("\nDigite o ID do paciente a ser atualizado: "))
                        break
                    except ValueError:
                        print("Digite um ID válido.")

                Paciente.atualizar(id_paciente)
                input("\nPressione ENTER para voltar ao Menu Principal")
                break
            case '4':
                print("\nQuantidade de pacientes por sexo:", Paciente.contar_sexo())
                break
            case '5':
                print("\nIdade média dos pacientes:", Paciente.media_idade())
                break
            case '00':
                break
            case _:
                print("Opção inválida! Tente novamente.")


def menu_atendimento():
    print("\nMenu Atendimentos")
    print("1. Cadastrar novo atendimento")
    print("2. Ver todos os atendimentos")
    print("3. Atualizar um atendimento de um paciente")
    print("4. ")


def main_menu():
    while True:
        print("\nMenu Principal:")
        print("1. Pacientes")
        print("2. Atendimentos")
        print("3. Serviços")

        print("2. Adicionar um novo atendimento")
        print("4. Ver todos os atendimentos")
        print("5. Ver atendimentos por data")

        print("7. Ver quantidade de atendimentos para um paciente")
        print("8. Ver quantidade de atendimentos para um CID-10")

        print("11. Atualizar um cadastro de atendimento")
        print("00. Sair")

        while True:
            try:
                opcao = int(input("Escolha uma opção: "))
                break
            except ValueError:
                print("Opção inválida. Digite novamente: ")

        match opcao:
            case '1':
                menu_paciente()
            case '2':
                while True:
                    try:
                        id_paciente = int(input("\nID do paciente: "))
                        break
                    except ValueError:
                        print("Por favor, insira um número válido para o ID do paciente.")

                cid_10 = input("CID-10 do atendimento: ").upper()
                cod_manchester = input("Código Manchester do atendimento: ").upper()

                atendimento = Atendimento(id_paciente, cid_10, cod_manchester)
                atendimento.salvar()

            case '4':
                Atendimento.listar_todos()
            case '5':
                while True:
                    data = input("\nDigite a data que deseja pesquisar atendimentos (AAAA-MM-DD): ")
                    if Paciente.validar_data(data):
                        break
                    else:
                        print("Data inválida. Por favor, insira a data no formato AAAA-MM-DD.")

                Atendimento.listar_data(data)

            case '7':
                while True:
                    try:
                        id_paciente = int(input("\nDigite o ID do paciente: "))
                        break
                    except ValueError:
                        print("Digite um número válido.")

                print("Quantidade de atendimentos para o paciente:", Atendimento.contar_por_paciente(id_paciente))

            case '8':
                cid = input("\nDigite o CID-10: ").upper()
                print("Quantidade de atendimentos para CID-10:", Atendimento.contar_por_cid(cid))

            case '11':
                while True:
                    try:
                        id_atend = int(input("\nDigite o ID do atendimento a ser atualizado: "))
                        break
                    except ValueError:
                        print("Digite um ID válido.")

                Atendimento.atualizar(id_atend)

            case '00':
                print("Saindo...")
                break
            case _:
                print("\nOpção inválida. Tente novamente.")


if __name__ == "__main__":
    main_menu()
