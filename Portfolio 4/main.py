from datetime import datetime

from paciente import Paciente
from atendimento import Atendimento
from servico import Servico


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
                opcao = int(input("\nDigite uma opção: ").strip())
                break
            except ValueError:
                print("\nOpção inválida! Tente novamente.")

        match opcao:
            case 1:
                nome = input("\nNome: ").strip().title()
                while True:
                    try:
                        rg = int(input("RG: ").strip())
                        if len(str(rg)) == 9:
                            break
                        else:
                            print("\nPor favor, insira um número RG válido.")
                    except ValueError:
                        print("\nPor favor, insira um número RG válido.")

                while True:
                    sexo = input("Sexo (M/F): ").strip().upper()
                    if sexo == 'M' or 'F':
                        break
                    else:
                        print("\nDigite apenas M ou F.")

                while True:
                    data_nasc = input("Data de nascimento (DD/MM/AAAA): ").strip()
                    if Paciente.validar_data(data_nasc):
                        break
                    else:
                        print("\nData inválida. Por favor, insira a data no formato DD/MM/AAAA.")

                while True:
                    try:
                        peso = float(input("Peso (kg): ").strip().replace(',', '.'))
                        break
                    except ValueError:
                        print("\nPor favor, insira um peso válido.")

                while True:
                    try:
                        altura = float(input("Altura (m): ").strip().replace(',', '.'))
                        break
                    except ValueError:
                        print("\nPor favor, insira um peso válido.")

                paciente = Paciente(nome=nome, rg=rg, sexo=sexo,
                                    data_nasc=datetime.strptime(data_nasc, "%d/%m/%Y").strftime('%Y-%m-%d'),
                                    peso=peso, altura=altura)
                if paciente.salvar():
                    print(F"\nPaciente ID: {paciente.id_paciente} cadastrado com sucesso.")
                else:
                    print(paciente.erro)
                input("\nPressione ENTER para retornar ao Menu Pacientes")

            case 2:
                paciente = Paciente()
                dados = paciente.listar_todos()
                if dados:
                    print()
                    for dado in dados:
                        print(
                            f"ID: {dado[0]}, Nome: {dado[1]}, RG: {dado[2]}, "
                            f"Sexo: {dado[3]}, Data de Nascimento: {dado[4]}, "
                            f"Peso: {dado[5]} kg, Altura: {dado[6]} m")
                else:
                    print(paciente.erro)
                input("\nPressione ENTER para retornar ao Menu Pacientes")
            case 3:
                # ERRO, precise corridor
                while True:
                    try:
                        id_paciente = int(input("\nDigite o ID do paciente a ser atualizado: ").strip())
                        break
                    except ValueError:
                        print("\nDigite um ID válido.")

                paciente = Paciente(id_paciente=id_paciente)
                dados = paciente.carregar_dados()
                if dados:
                    print(f"Dados Atuais — Nome: {paciente.nome}, RG: {paciente.rg}, Sexo: {paciente.sexo}, "
                          f"Data de Nascimento: {paciente.data_nasc}, Peso: {paciente.peso} kg, Altura: {paciente.altura} m")
                else:
                    print(paciente.erro)
                    input("\nPressione ENTER para retornar ao Menu Pacientes")
                    break

                novo_nome = input("Novo nome (deixe em branco para não alterar): ").strip().title()
                while True:
                    try:
                        novo_rg = input("Novo RG (deixe em branco para não alterar): ").strip()
                        if novo_rg in [None, ""] or (novo_rg.isdigit() and len(novo_rg) == 9):
                            break
                        else:
                            print("\nPor favor, insira um número novo RG válido.")
                    except ValueError:
                        print("\nPor favor, insira um número novo RG válido.")

                while True:
                    novo_sexo = input("Novo sexo (M/F, deixe em branco para não alterar): ").strip().upper()
                    if novo_sexo == 'M' or 'F':
                        break
                    else:
                        print("Digite apenas M ou F.")

                while True:
                    nova_data_nasc = input(
                        "Nova data de nascimento (DD/MM/AAAA, deixe em branco para não alterar): ").strip()
                    if Paciente.validar_data(nova_data_nasc):
                        break
                    else:
                        print("Data inválida. Por favor, insira a nova data no formato AAAA-MM-DD.")

                while True:
                    try:
                        novo_peso = input("Novo peso (kg, deixe em branco para não alterar): ").strip().replace(',',
                                                                                                                '.')
                        break
                    except ValueError:
                        print("\nPor favor, insira um peso válido.")

                while True:
                    try:
                        nova_altura = float(
                            input("Nova altura (m, deixe em branco para não alterar): ").strip().replace(
                                ',', '.'))
                        break
                    except ValueError:
                        print("\nPor favor, insira um peso válido.")

                if paciente.atualizar(novo_nome=novo_nome, novo_rg=novo_rg, novo_sexo=novo_sexo,
                                      nova_data_nasc=nova_data_nasc, novo_peso=novo_peso, nova_altura=nova_altura):

                    print(F"\nPaciente ID: {paciente.id_paciente} atualizado com sucesso.")
                else:
                    print(f"Erro ao atualizar cadastro de paciente: {paciente.erro}")

                input("\nPressione ENTER para retornar ao Menu Pacientes")
            case 4:
                paciente = Paciente()
                valor = paciente.contar_sexo()
                if valor:
                    print(valor)
                else:
                    print(paciente.erro)

                input("\nPressione ENTER para retornar ao Menu Pacientes")

            case 5:
                paciente = Paciente()
                media = paciente.media_idade()
                if media:
                    print("\nIdade média dos pacientes: ", media)
                else:
                    print(paciente.erro)
                input("\nPressione ENTER para retornar ao Menu Pacientes")

            case 00:
                break

            case _:
                print("Opção inválida! Tente novamente.")


def menu_atendimento():
    while True:
        print("\nMenu Atendimentos")
        print("1. Cadastrar novo atendimento")
        print("2. Ver todos os atendimentos")
        print("3. Atualizar um atendimento de um paciente")
        print("4. Pesquisar atendimentos")
        print("00. Retornar ao Menu Principal")

        while True:
            try:
                opcao = int(input("\nDigite uma opção: ").strip())
                break
            except ValueError:
                print("\nDigite uma opção válida.")

        match opcao:
            case 1:
                while True:
                    try:
                        id_paciente = int(input("\nID do paciente: ").strip())
                        break
                    except ValueError:
                        print("\nPor favor, insira um número válido para o ID do paciente.")

                cid_10 = input("CID-10 do atendimento: ").strip().upper()
                cod_manchester = input("Código Manchester do atendimento: ").strip().title()

                atendimento = Atendimento(id_paciente=id_paciente, cid_10=cid_10, cod_manchester=cod_manchester)
                if atendimento.salvar():
                    print(f"\nAtendimento ID {atendimento.id_atend} para o(a) paciente {atendimento.id_paciente} "
                          f"cadastrado com sucesso na data e hora: {atendimento.data_atend}")
                else:
                    print(atendimento.erro)

                input("\nPressione ENTER para retornar ao Menu Atendimentos")

            case 2:
                atend = Atendimento()
                atendimentos = atend.listar_todos()
                if atendimentos:
                    print()
                    for atendimento in atendimentos:
                        print(
                            f"ID Atendimento: {atendimento[0]}, "
                            f"ID Paciente: {atendimento[1]}, CID-10: {atendimento[2]}, "
                            f"Código Manchester: {atendimento[3]}, Data: {atendimento[4]}")
                else:
                    print(atend.erro)

                input("\nPressione ENTER para retornar ao Menu Atendimentos")
            case 3:
                while True:
                    try:
                        id_atend = int(input("\nDigite o ID do atendimento a ser atualizado: ").strip())
                        break
                    except ValueError:
                        print("\nDigite um ID válido.")

                atendimento = Atendimento(id_atend=id_atend)
                dados = atendimento.carregar_dados()
                if dados:
                    print(f"\nDados Atuais — ID paciente: {atendimento.id_paciente}, CID-10: {atendimento.cid_10}, "
                          f"Código Manchester: {atendimento.cod_manchester}, Data: {atendimento.data_atend}")
                else:
                    print(atendimento.erro)
                    input("\nPressione ENTER para retornar ao Menu Pacientes")
                    break

                novo_cid_10 = input("Novo CID-10 (deixe em branco para não alterar): ").strip().upper()
                novo_cod_manchester = input("Novo código Manchester "
                                            "(deixe em branco para não alterar): ").strip().title()

                if atendimento.atualizar(novo_cid_10, novo_cod_manchester):
                    print(F"\nAtendimento ID: {atendimento.id_atend} atualizado com sucesso.")
                else:
                    print(atendimento.erro)

                input("\nPressione ENTER para retornar ao Menu Atendimentos")

            case 4:
                submenu_atendimento()

            case 00:
                break
            case _:
                print("\nDigite uma opção válida.")


def submenu_atendimento():
    while True:
        print("\nMenu Pesquisar Atendimentos")
        print("1. Pesquisar atendimentos por data")
        print("2. Quantidade de atendimentos para um paciente")
        print("3. Quantidade de atendimentos para um CID-10")
        print("4. Pesquisar valor total de um atendimento específico")
        print("5. Pesquisar valor total de atendimentos de um paciente específico")
        print("00. Retornar ao Menu Atendimentos")
        try:
            opcao = int(input("\nDigite uma opção: ").strip())
            match opcao:
                case 1:
                    while True:
                        data = input("\nDigite a data que deseja pesquisar atendimentos (DD/MM/AAAA): ").strip()
                        if Paciente.validar_data(data):
                            break
                        else:
                            print("\nData inválida. Por favor, insira a data no formato DD/MM/AAAA.")

                    atendimento = Atendimento(data_atend=datetime.strptime(data, "%d/%m/%Y").strftime('%Y-%m-%d'))
                    listar_data = atendimento.listar_data()
                    if listar_data:
                        for data in listar_data:
                            print(f"ID Atendimento: {data[0]}, ID Paciente: {data[1]}, CID-10: {data[3]}, "
                                  f"Código Manchester: {data[4]}, "
                                  f"Data Atendimento: {data[2]}")
                    else:
                        print(atendimento.erro)

                    input("\nPressione ENTER para retornar ao Menu Pesquisar Atendimentos")

                case 2:
                    while True:
                        try:
                            id_paciente = int(input("\nDigite o ID do paciente: ").strip())
                            break
                        except ValueError:
                            print("\nDigite um número válido.")
                    atendimento = Atendimento(id_paciente=id_paciente)
                    contar = atendimento.contar_por_paciente()
                    if contar:
                        print("\nQuantidade de atendimentos para o paciente: ", contar)
                    else:
                        print(atendimento.erro)

                    input("\nPressione ENTER para retornar ao Menu Pesquisar Atendimentos")
                case 3:
                    cid = input("\nDigite o CID-10: ").strip().upper()
                    atendimento = Atendimento(cid_10=cid)
                    contar = atendimento.contar_por_cid()
                    if contar:
                        print("\nQuantidade de atendimentos para CID-10: ", contar)
                    else:
                        print(atendimento.erro)

                    input("\nPressione ENTER para retornar ao Menu Pesquisar Atendimentos")
                case 4:
                    while True:
                        try:
                            id_atendimento = int(
                                input("\nDigite o ID do atendimento que deseja ver o valor total: ").strip())
                            break
                        except ValueError:
                            print("\nDigite um ID válido")
                    atendimento = Atendimento(id_atend=id_atendimento)
                    valor = atendimento.valor_total_tuss()
                    if valor:
                        print(valor)
                    else:
                        print(atendimento.erro)
                    input("\nPressione ENTER para retornar ao Menu Pesquisar Atendimentos")
                case 5:
                    while True:
                        try:
                            id_paciente = int(
                                input(
                                    "\nDigite o ID do paciente que deseja ver o valor total de atendimentos: ").strip())
                            break
                        except ValueError:
                            print("\nDigite um ID válido")
                    atendimento = Atendimento(id_paciente=id_paciente)
                    valor = atendimento.valor_paciente()
                    if valor:
                        if valor[0] is None:
                            valor[0] = 0
                        print(f"\nPaciente ID: {atendimento.id_paciente}"
                              f"\nNome: {valor[1]}"
                              f"\nValor total gasto: R${valor[0]}")
                    else:
                        print(atendimento.erro)

                    input("\nPressione ENTER para retornar ao Menu Pesquisar Atendimentos")
                case 00:
                    break
                case _:
                    print("\nDigite uma opção válida")
        except ValueError:
            print("\nDigite uma opção válida")


def main_menu():
    while True:
        print("\nMenu Principal:")
        print("1. Pacientes")
        print("2. Atendimentos")
        print("3. Serviços")
        print("00. Sair")

        while True:
            try:
                opcao = int(input("\nEscolha uma opção: ").strip())
                break
            except ValueError:
                print("Opção inválida. Digite novamente: ")

        match opcao:
            case 1:
                menu_paciente()
            case 2:
                menu_atendimento()
            case 3:
                pass
            case 00:
                print("Saindo...")
                break
            case _:
                print("\nOpção inválida. Tente novamente.")


if __name__ == "__main__":
    main_menu()
