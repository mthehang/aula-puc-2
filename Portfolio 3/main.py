from paciente import Paciente
from atendimento import Atendimento


def main_menu():
    while True:
        print("\nMenu Principal:")
        print("1. Adicionar um novo paciente")
        print("2. Adicionar um novo atendimento")
        print("3. Ver todos os pacientes")
        print("4. Ver todos os atendimentos")
        print("5. Ver atendimentos por data")
        print("6. Ver quantidade de pacientes por sexo")
        print("7. Ver quantidade de atendimentos para um paciente")
        print("8. Ver quantidade de atendimentos para um CID-10")
        print("9. Ver idade média dos pacientes")
        print("10. Atualizar um cadastro de paciente")
        print("11. Atualizar um cadastro de atendimento")
        print("00. Sair")
        opcao = input("Escolha uma opção: ")

        match opcao:
            case '1':
                nome = input("\nNome: ").title()
                rg = input("RG: ")
                sexo = input("Sexo (M/F): ").upper()
                data_nasc = input("Data de nascimento (AAAA-MM-DD): ")
                peso = float(input("Peso (kg): ").replace(',', '.'))
                altura = float(input("Altura (m): ").replace(',', '.'))
                paciente = Paciente(rg, nome, sexo, data_nasc, peso, altura)
                paciente.salvar()
            case '2':
                id_paciente = int(input("\nID do paciente: "))
                cid_10 = input("CID-10 do atendimento: ").upper()
                atendimento = Atendimento(id_paciente, cid_10)
                atendimento.salvar()
            case '3':
                Paciente.listar_todos()
            case '4':
                Atendimento.listar_todos()
            case '5':
                data = input("\nDigite a data que deseja pesquisar atendimentos (AAAA-MM-DD): ")
                Atendimento.listar_data(data)
            case '6':
                print("\nQuantidade de pacientes por sexo:", Paciente.contar_sexo())
            case '7':
                id_paciente = int(input("\nDigite o ID do paciente: "))
                print("Quantidade de atendimentos para o paciente:", Atendimento.contar_por_paciente(id_paciente))
            case '8':
                cid = input("\nDigite o CID-10: ").upper()
                print("Quantidade de atendimentos para CID-10:", Atendimento.contar_por_cid(cid))
            case '9':
                print("\nIdade média dos pacientes:", Paciente.media_idade())
            case '10':
                id_paciente = int(input("\nDigite o ID do paciente a ser atualizado: "))
                Paciente.atualizar(id_paciente)
            case '11':
                id_atend = int(input("\nDigite o ID do atendimento a ser atualizado: "))
                Atendimento.atualizar(id_atend)
            case '00':
                print("Saindo...")
                break
            case _:
                print("\nOpção inválida. Tente novamente.")


if __name__ == "__main__":
    main_menu()
