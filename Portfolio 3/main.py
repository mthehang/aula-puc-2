from paciente import Paciente
from atendimento import Atendimento
from queries import contar_pacientes_por_sexo, contar_atendimentos_por_paciente, contar_atendimentos_por_cid, \
    calcular_media_idade_pacientes


def main_menu():
    while True:
        print("\nMenu Principal:")
        print("1. Adicionar um novo paciente")
        print("2. Adicionar um novo atendimento")
        print("3. Ver todos os pacientes")
        print("4. Ver todos os atendimentos")
        print("5. Ver quantidade de pacientes por sexo")
        print("6. Ver quantidade de atendimentos para um paciente")
        print("7. Ver quantidade de atendimentos para um CID-10")
        print("8. Ver idade média dos pacientes")
        print("9. Atualizar um cadastro de paciente")
        print("10. Deletar um cadastro de paciente")
        print("11. Deletar um atendimento")
        print("12. Sair")
        opcao = input("Escolha uma opção: ")

        if opcao == '1':
            rg = input("RG: ")
            nome = input("Nome: ").title()
            sexo = input("Sexo (M/F): ").upper()
            data_nasc = input("Data de nascimento (AAAA-MM-DD): ")
            peso = float(input("Peso (kg): "))
            altura = float(input("Altura (m): "))
            paciente = Paciente(rg, nome, sexo, data_nasc, peso, altura)
            paciente.salvar()
        elif opcao == '2':
            id_paciente = int(input("ID do paciente: "))
            cid_10 = input("CID-10 do atendimento: ").upper()
            atendimento = Atendimento(id_paciente, cid_10)
            atendimento.salvar()
        elif opcao == '3':
            Paciente.listar_todos()
        elif opcao == '4':
            Atendimento.listar_todos()
        elif opcao == '5':
            print("\nQuantidade de pacientes por sexo:", contar_pacientes_por_sexo())
        elif opcao == '6':
            id_paciente = int(input("\nDigite o ID do paciente: "))
            print("Quantidade de atendimentos para o paciente:", contar_atendimentos_por_paciente(id_paciente))
        elif opcao == '7':
            cid = input("\nDigite o CID-10: ").upper()
            print("Quantidade de atendimentos para CID-10:", contar_atendimentos_por_cid(cid))
        elif opcao == '8':
            print("\nIdade média dos pacientes:", calcular_media_idade_pacientes())
        elif opcao == '9':
            id_paciente = int(input("\nDigite o ID do paciente a ser atualizado: "))
            Paciente.atualizar(id_paciente)
        elif opcao == '10':
            id_paciente = int(input("\nDigite o ID do paciente a ser deletado: "))
            Paciente.deletar(id_paciente)
        elif opcao == '11':
            id_atend = int(input("\nDigite o ID do atendimento a ser deletado: "))
            Atendimento.deletar(id_atend)
        elif opcao == '12':
            print("Saindo...")
            break
        else:
            print("\nOpção inválida. Tente novamente.")


if __name__ == "__main__":
    main_menu()
