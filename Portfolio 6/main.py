from datetime import datetime
from atendimento import Atendimento
from paciente import Paciente
from servico import Servico
from medicos import Medico


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
                          f"Data de Nascimento: {paciente.data_nasc}, "
                          f"Peso: {paciente.peso} kg, Altura: {paciente.altura} m")
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
                    if novo_sexo in [None, "", 'M', 'F']:
                        break
                    else:
                        print("Digite apenas M ou F.")

                while True:
                    nova_data_nasc = input(
                        "Nova data de nascimento (DD/MM/AAAA, deixe em branco para não alterar): ").strip()
                    if Paciente.validar_data(nova_data_nasc) or nova_data_nasc in [None, ""]:
                        break
                    else:
                        print("\nData inválida. Por favor, insira a nova data no formato AAAA-MM-DD.")

                while True:
                    try:
                        novo_peso = input("Novo peso (kg, deixe em branco para não alterar): ").strip().replace(',',
                                                                                                                '.')
                        break
                    except ValueError:
                        print("\nPor favor, insira um peso válido.")

                while True:
                    try:
                        nova_altura = input("Nova altura (m, deixe em branco para não alterar): ").strip().replace(
                            ',', '.')
                        if nova_altura.isdigit() or nova_altura in [None, ""]:
                            break
                        else:
                            print("\nPor favor, insira uma altura válida.")
                    except ValueError:
                        print("\nPor favor, insira uma altura válida.")

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
        print("5. Excluir atendimento")
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
                if atendimento.carregar_dados():
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

            case 5:
                while True:
                    try:
                        id_atend = int(input("Digite o ID do atendimento que deseja excluir: "))
                        break
                    except ValueError:
                        print("ID inválido. Digite novamente: ")
                atendimento = Atendimento(id_atend=id_atend)
                if atendimento.carregar_dados():
                    print(f"\nDados Atuais — ID paciente: {atendimento.id_paciente}, CID-10: {atendimento.cid_10}, "
                          f"Código Manchester: {atendimento.cod_manchester}, Data: {atendimento.data_atend}")
                    while True:
                        resposta = input("\nDeseja excluir este atendimento? (S / N): ")
                        match resposta.upper():
                            case 'S':
                                if atendimento.excluir_atendimento():
                                    print(f"\nAtendimento com ID {atendimento.id_atend} excluído com sucesso.\n")
                                    break
                                else:
                                    print(atendimento.erro)
                                    break
                            case 'N':
                                print("\nOperação cancelada!")
                                break
                            case __:
                                print("Opção inválida. Digite novamente: ")
                else:
                    print(atendimento.erro)

                input("Pressione ENTER para retornar ao Menu Pacientes")

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


def menu_servico():
    while True:
        print("\nMenu Serviço")
        print("1. Cadastrar novo serviço")
        print("2. Ver todos os serviços")
        print("3. Atualizar um serviço de atendimento")
        print("4. Listar serviços de um código TUSS")
        print("5. Listar serviços em data específica")
        print("6. Excluir serviço")
        print("00. Voltar ao menu principal")
        while True:
            try:
                opcao = int(input("\nEscolha uma opção: ").strip())
                break
            except ValueError:
                print("\nOpção inválida. Digite novamente: ")

        match opcao:
            case 1:
                while True:
                    try:
                        id_atend = int(input("Digite ID do atendimento: ").strip())
                        id_tuss = input("Digite o código TUSS do serviço: ")
                        medicos_id = int(input("Digite o ID do médico: ").strip())
                        break
                    except ValueError:
                        print("\nDados inválidos. Digite novamente: ")

                servico = Servico(id_atend=id_atend, id_tuss=id_tuss, medicos_id=medicos_id)
                result = servico.salvar()

                if result:
                    print("\nServiço cadastrado com sucesso.")
                else:
                    print(servico.erro)

                input("\nDigite ENTER para voltar ao Menu Serviços")

            case 2:
                servico = Servico()
                valor = servico.listar_todos()
                if valor:
                    for servicos in valor:
                        print(f"\nID serviço: {servicos[0]}"
                              f"\nID atendimento: {servicos[1]}"
                              f"\nCódigo TUSS: {servicos[2]}"
                              f"\nID Médico: {servicos[3]}"
                              f"\nData serviço: {servicos[4]}")

                input("\nPressione ENTER para retornar ao Menu Serviços")

            case 3:
                while True:
                    try:
                        id_atend_serv = int(input("Digite ID de serviço que deseja atualizar: "))
                        servico = Servico(id_atend_serv=id_atend_serv)
                        if not servico.carregar_dados():
                            print(servico.erro)
                            break

                        print(f"\nID serviço: {servico.id_atend_serv}"
                              f"\nID atendimento: {servico.id_atend}"
                              f"\nCódigo TUSS: {servico.id_tuss}"
                              f"\nID Médico: {servico.medicos_id}"
                              f"\nData serviço: {servico.data_serv}")

                        novo_id_atend = input(
                            "\nDigite o novo ID de atendimento (deixe em branco para não alterar): ").strip()
                        novo_id_tuss = input("Digite o novo Código TUSS (deixe em branco para não alterar): ").strip()
                        novo_medicos_id = input("Digite o novo ID do médico (deixe em branco para não alterar): "
                                                "").strip()

                        if servico.atualizar(novo_id_atend, novo_id_tuss, novo_medicos_id):
                            print("\nServiço atualizado com sucesso.")
                            break
                        else:
                            print(servico.erro)
                    except ValueError:
                        print("\nID inválido. Por favor, insira um número.")

                input("\nPressione ENTER para voltar ao Menu Serviços")

            case 4:
                while True:
                    try:
                        id_tuss = input("\nDigite o Código TUSS: ").strip()
                        if not id_tuss:
                            print("\nCódigo TUSS não pode ser vazio.")
                            continue

                        servico = Servico(id_tuss=id_tuss)
                        resultados = servico.servicos_id_tuss()

                        if resultados:
                            print("\nServiços prestados para o Código TUSS específico:")
                            for resultado in resultados:
                                nome_paciente = resultado[0]
                                data_atendimento = resultado[1]
                                valor_total = f"{resultado[2]:.2f}".replace(".", ",")

                                print(f"\nPaciente: {nome_paciente}")
                                print(f"Data do Atendimento: {data_atendimento}")
                                print(f"Valor Total: R$ {valor_total}")
                        else:
                            print(servico.erro)
                        break
                    except ValueError:
                        print("\nErro ao processar o código TUSS. Por favor, insira um valor válido.")
                    except Exception as e:
                        print(f"\nErro: {str(e)}")
                        break

                input("\nPressione ENTER para voltar ao Menu Serviços.")

            case 5:
                while True:
                    try:
                        data = input("\nDigite a data que deseja pesquisar serviços (DD/MM/AAAA): ").strip()
                        if not Paciente.validar_data(data):
                            print("\nData inválida. Por favor, insira a data no formato DD/MM/AAAA.")
                            continue
                        servico = Servico(data_serv=datetime.strptime(data, "%d/%m/%Y").strftime("%Y-%m-%d"))
                        resultados = servico.servico_data()

                        if resultados:
                            print(f"\nServiços prestados em {data}:")
                            for resultado in resultados:
                                cod_tuss = resultado[0]
                                sexo = resultado[1]
                                quantidade = resultado[2]
                                valor_total = f"{resultado[3]:.2f}".replace(".", ",")

                                print(f"\nCódigo TUSS: {cod_tuss}")
                                print(f"Sexo: {sexo}")
                                print(f"Quantidade de Serviços: {quantidade}")
                                print(f"Valor Total: R$ {valor_total}")
                        else:
                            print(servico.erro)
                        break
                    except ValueError:
                        print("\nErro ao processar a data. Por favor, insira um valor válido.")
                    except Exception as e:
                        print(f"\nErro: {str(e)}")
                        break

                input("\nPressione ENTER para voltar ao Menu Serviços.")

            case 6:
                while True:
                    try:
                        id_serv = int(input("Digite ID do serviço a ser excluído: "))
                        break
                    except ValueError:
                        print("ID inválido.")
                servico = Servico(id_atend_serv=id_serv)
                servico.carregar_dados()
                print(f"\nID serviço: {servico.id_atend_serv}"
                      f"\nID atendimento: {servico.id_atend}"
                      f"\nCódigo TUSS: {servico.id_tuss}"
                      f"\nID Médico: {servico.medicos_id}"
                      f"\nData serviço: {servico.data_serv}")

                while True:
                    resposta = input("\nDeseja mesmo excluir este serviço? (S / N): ")

                    if resposta.upper() == "S":
                        if servico.excluir():
                            print(f"\nServiço com ID {servico.id_atend_serv} excluído com sucesso.")
                            break
                        else:
                            print(servico.erro)
                            break
                    elif resposta.upper() == "N":
                        print("\nOperação cancelada!")
                        break
                    else:
                        print("\nOpção inválida. Digite novamente: ")

                input("Pressione ENTER para voltar ao Menu Serviços.")

            case 00:
                break
            case __:
                print("\nOpção inválida. Digite novamente: ")


def menu_medico():
    while True:
        print("\nMenu Médicos")
        print("1. Cadastrar novo médico")
        print("2. Ver todos os médicos")
        print("3. Atualizar um cadastro de médico")
        print("4. Excluir médico")
        print("00. Voltar ao menu principal")

        opcao = input("Escolha uma opção: ").strip()

        if opcao == "1":
            nome = input("Digite o nome do médico: ").strip()
            medico = Medico()
            especialidades = medico.listar_especialidades()
            if especialidades:
                for resultado in especialidades:
                    print(f"ID: {resultado[0]}, Descrição: {resultado[1]}")
                especialidade = int(input("Digite o ID da especialidade: ").strip())
                medico = Medico(nome=nome, id_especialidade=especialidade)
                if medico.salvar():
                    print(f"Médico {nome} cadastrado com sucesso.")
                else:
                    print(medico.erro)
            else:
                print(medico.erro)
            input("\nPressione ENTER para retornar ao Menu Médicos")

        elif opcao == "2":
            medico = Medico()
            medicos = medico.listar_todos()
            if medicos:
                print("\nLista de Médicos:")
                for med in medicos:
                    print(f"ID: {med[0]}, Nome: {med[1]}, Especialidade: {med[2]}")
            else:
                print(medico.erro)
            input("\nPressione ENTER para retornar ao Menu Médicos")

        elif opcao == "3":
            try:
                id_medico = int(input("Digite o ID do médico a ser atualizado: ").strip())
                medico = Medico(id_medico=id_medico)
                if medico.carregar_dados():
                    print(f"Dados Atuais — Nome: {medico.nome}")
                    novo_nome = input("Novo nome (deixe em branco para não alterar): ").strip()

                    especialidades = medico.listar_especialidades()
                    if especialidades:
                        for resultado in especialidades:
                            print(f"ID: {resultado[0]}, Descrição: {resultado[1]}")
                        nova_especialidade = input("Digite o ID da nova especialidade "
                                                   "(deixe em branco para não alterar): ").strip()
                        nova_especialidade = int(nova_especialidade) if nova_especialidade else None

                        if medico.atualizar(novo_nome=novo_nome, nova_especialidade=nova_especialidade):
                            print(f"Médico ID: {medico.id_medico} atualizado com sucesso.")
                        else:
                            print(f"Erro ao atualizar médico: {medico.erro}")
                else:
                    print(medico.erro)
            except ValueError:
                print("ID inválido. Por favor, insira um número inteiro.")
            input("\nPressione ENTER para retornar ao Menu Médicos")

        elif opcao == "4":
            try:
                id_medico = int(input("Digite o ID do médico a ser excluído: ").strip())
                medico = Medico(id_medico=id_medico)
                if medico.excluir():
                    print(f"Médico ID: {id_medico} excluído com sucesso.")
                else:
                    print(medico.erro)
            except ValueError:
                print("ID inválido. Por favor, insira um número inteiro.")
            input("\nPressione ENTER para retornar ao Menu Médicos")

        elif opcao == "00" or "0":
            break

        else:
            print("Opção inválida! Tente novamente.")


def menu_compliance():
    while True:
        print("\nMenu Relatórios de Compliance")
        print("1. Serviços fora da relação de Especialidades X Serviços")
        print("2. Quantidade de serviços prestados por tipo de serviço")
        print("3. Pacientes que utilizaram serviço mais de uma vez")
        print("4. Serviços incompatíveis com o sexo do paciente")
        print("5. Serviços solicitados por médicos fora da especialidade")
        print("00. Voltar ao menu principal")

        opcao = input("Escolha uma opção: ").strip()

        if opcao == "1":
            servico = Servico()
            resultados = servico.servicos_fora_especialidade()
            if resultados:
                for resultado in resultados:
                    print(f"ID Atendimento Serviço: {resultado[0]}")
                    print(f"ID Atendimento: {resultado[1]}")
                    print(f"ID TUSS: {resultado[2]}")
                    print(f"Data Serviço: {resultado[3]}")
                    print(f"Especialidade: {resultado[4]}\n")
            else:
                print(servico.erro)
            input("\nPressione ENTER para retornar ao Menu Relatórios de Compliance")

        elif opcao == "2":
            servico = Servico()
            resultados = servico.quantidade_servicos_por_tipo()
            if resultados:
                for resultado in resultados:
                    print(f"Tipo de Serviço: {resultado[0]}")
                    print(f"Quantidade: {resultado[1]}\n")
            else:
                print("Nenhum dado encontrado.")
            input("\nPressione ENTER para retornar ao Menu Relatórios de Compliance")

        elif opcao == "3":
            servico = Servico()
            resultados = servico.servico_mais_uma_vez()
            if resultados:
                for resultado in resultados:
                    print(f"Nome do Paciente: {resultado[0]}")
                    print(f"ID Paciente: {resultado[1]}")
                    print(f"Descrição do Serviço: {resultado[2]}")
                    print(f"Quantidade de Serviços: {resultado[3]}\n")
            else:
                print("Nenhum paciente encontrado.")
            input("\nPressione ENTER para retornar ao Menu Relatórios de Compliance")

        elif opcao == "4":
            servico = Servico()
            resultados = servico.servicos_incompativeis_sexo()
            if resultados:
                for resultado in resultados:
                    print(f"ID Atendimento Serviço: {resultado[0]}")
                    print(f"ID Atendimento: {resultado[1]}")
                    print(f"ID TUSS: {resultado[2]}")
                    print(f"Data Serviço: {resultado[3]}")
                    print(f"Nome do Paciente: {resultado[4]}")
                    print(f"Sexo do Paciente: {resultado[5]}")
                    print(f"Descrição do Serviço: {resultado[6]}\n")
            else:
                print(servico.erro)
            input("\nPressione ENTER para retornar ao Menu Relatórios de Compliance")

        elif opcao == "5":
            servico = Servico()
            resultados = servico.servicos_fora_especialidade_medico()
            if resultados:
                for resultado in resultados:
                    print(f"ID Atendimento Serviço: {resultado[0]}")
                    print(f"ID Atendimento: {resultado[1]}")
                    print(f"ID TUSS: {resultado[2]}")
                    print(f"Data Serviço: {resultado[3]}")
                    print(f"Nome do Médico: {resultado[4]}")
                    print(f"Especialidade: {resultado[5]}\n")
            else:
                print(servico.erro)
            input("\nPressione ENTER para retornar ao Menu Relatórios de Compliance")

        elif opcao == "00":
            break

        else:
            print("Opção inválida! Tente novamente.")



def main_menu():
    while True:
        print("\nMenu Principal:")
        print("1. Pacientes")
        print("2. Atendimentos")
        print("3. Serviços")
        print("4. Médicos")
        print("5. Relatórios de Compliance")
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
                menu_servico()
            case 4:
                menu_medico()
            case 5:
                menu_compliance()
            case 00:
                print("Saindo...")
                break
            case _:
                print("\nOpção inválida. Tente novamente.")


if __name__ == "__main__":
    main_menu()
