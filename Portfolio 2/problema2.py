<<<<<<< HEAD
from datetime import datetime


class Paciente:
    def __init__(self, id, nome, rg, data_nascimento, sexo):
        self.id = id
        self.nome = nome
        self.rg = rg
        self.data_nascimento = data_nascimento
        self.sexo = sexo
        self.atendimentos = []

    def adicionar_atendimento(self, data, tipo, descricao, peso, altura):
        data_formatada = datetime.strptime(data, "%d-%m-%Y %H:%M")
        if not any(data_formatada == datetime.strptime(a.data, "%d-%m-%Y %H:%M") for a in self.atendimentos):
            atendimento = Atendimento(data, tipo, descricao, peso, altura, self)  # Passando self como paciente
            self.atendimentos.append(atendimento)
        else:
            print(f"Atendimento já registrado para esta data: {data}")

    def listar_atendimentos(self):
        for atendimento in self.atendimentos:
            print(f"Data: {atendimento.data}, Tipo: {atendimento.tipo}, Descrição: {atendimento.descricao}")

    def idade(self):
        data_nasc = datetime.strptime(self.data_nascimento, "%Y-%m-%d")
        hoje = datetime.now()
        return hoje.year - data_nasc.year - ((hoje.month, hoje.day) < (data_nasc.month, data_nasc.day))

    def total_atendimentos(self):
        return len(self.atendimentos)


class Atendimento:
    def __init__(self, data, tipo, descricao, peso, altura, paciente):
        self.data = data
        self.tipo = tipo
        self.descricao = descricao
        self.peso = peso
        self.altura = altura
        self.paciente = paciente  # Referência ao paciente


def quantidade_pacientes_por_sexo(pacientes):
    contador_sexo = {"Masculino": 0, "Feminino": 0}
    for paciente in pacientes.values():
        contador_sexo[paciente.sexo] += 1
    print("Pacientes por sexo:", contador_sexo)


def media_idade_pacientes(pacientes):
    total_idade = sum(paciente.idade() for paciente in pacientes.values())
    print("Média de idade dos pacientes:", total_idade / len(pacientes))


def atendimentos_por_data(pacientes, data):
    data_formatada = datetime.strptime(data, "%d-%m-%Y").date()
    atendimentos_data = []
    for paciente in pacientes.values():
        for atendimento in paciente.atendimentos:
            if datetime.strptime(atendimento.data, "%d-%m-%Y %H:%M").date() == data_formatada:
                atendimentos_data.append(
                    (atendimento.paciente.nome, atendimento.paciente.idade(), atendimento.descricao))
    print(f"Atendimentos em {data}:", atendimentos_data)


def atendimentos_paciente(pacientes):
    for id, paciente in pacientes.items():
        atendimentos_data = {}
        for atendimento in paciente.atendimentos:
            data = atendimento.data.split(' ')[0]  # Obtendo apenas a parte da data
            if data in atendimentos_data:
                atendimentos_data[data] += 1
            else:
                atendimentos_data[data] = 1
        print(f"\nTotal de atendimentos para {paciente.nome}: {paciente.total_atendimentos()}")
        for data, count in atendimentos_data.items():
            print(f"  Data: {data}, Atendimentos: {count}")

pacientes = {}
pacientes[1] = Paciente(1, "Maria Silva", "MG123456", "1980-05-15", "Feminino")
pacientes[2] = Paciente(2, "João Santos", "SP987654", "1990-08-20", "Masculino")

pacientes[1].adicionar_atendimento("11-05-2024 11:12", "Consulta", "Exame de sangue", 70, 1.65)
pacientes[1].adicionar_atendimento("12-05-2024 15:33", "Consulta", "Consulta de rotina", 70, 1.65)
pacientes[2].adicionar_atendimento("12-05-2024 14:37", "Exame", "Exame de sangue", 80, 1.75)

print()
quantidade_pacientes_por_sexo(pacientes)
media_idade_pacientes(pacientes)
atendimentos_por_data(pacientes, "12-05-2024")
atendimentos_paciente(pacientes)
=======
from datetime import datetime


class Paciente:
    def __init__(self, id, nome, rg, data_nascimento, sexo):
        self.id = id
        self.nome = nome
        self.rg = rg
        self.data_nascimento = data_nascimento
        self.sexo = sexo
        self.atendimentos = []

    def adicionar_atendimento(self, data, tipo, descricao, peso, altura):
        data_formatada = datetime.strptime(data, "%d-%m-%Y %H:%M")
        if not any(data_formatada == datetime.strptime(a.data, "%d-%m-%Y %H:%M") for a in self.atendimentos):
            atendimento = Atendimento(data, tipo, descricao, peso, altura, self)  # Passando self como paciente
            self.atendimentos.append(atendimento)
        else:
            print(f"Atendimento já registrado para esta data: {data}")

    def listar_atendimentos(self):
        for atendimento in self.atendimentos:
            print(f"Data: {atendimento.data}, Tipo: {atendimento.tipo}, Descrição: {atendimento.descricao}")

    def idade(self):
        data_nasc = datetime.strptime(self.data_nascimento, "%Y-%m-%d")
        hoje = datetime.now()
        return hoje.year - data_nasc.year - ((hoje.month, hoje.day) < (data_nasc.month, data_nasc.day))

    def total_atendimentos(self):
        return len(self.atendimentos)


class Atendimento:
    def __init__(self, data, tipo, descricao, peso, altura, paciente):
        self.data = data
        self.tipo = tipo
        self.descricao = descricao
        self.peso = peso
        self.altura = altura
        self.paciente = paciente  # Referência ao paciente


def quantidade_pacientes_por_sexo(pacientes):
    contador_sexo = {"Masculino": 0, "Feminino": 0}
    for paciente in pacientes.values():
        contador_sexo[paciente.sexo] += 1
    print("Pacientes por sexo:", contador_sexo)


def media_idade_pacientes(pacientes):
    total_idade = sum(paciente.idade() for paciente in pacientes.values())
    print("Média de idade dos pacientes:", total_idade / len(pacientes))


def atendimentos_por_data(pacientes, data):
    data_formatada = datetime.strptime(data, "%d-%m-%Y").date()
    atendimentos_data = []
    for paciente in pacientes.values():
        for atendimento in paciente.atendimentos:
            if datetime.strptime(atendimento.data, "%d-%m-%Y %H:%M").date() == data_formatada:
                atendimentos_data.append(
                    (atendimento.paciente.nome, atendimento.paciente.idade(), atendimento.descricao))
    print(f"Atendimentos em {data}:", atendimentos_data)


def atendimentos_paciente(pacientes):
    for id, paciente in pacientes.items():
        atendimentos_data = {}
        for atendimento in paciente.atendimentos:
            data = atendimento.data.split(' ')[0]  # Obtendo apenas a parte da data
            if data in atendimentos_data:
                atendimentos_data[data] += 1
            else:
                atendimentos_data[data] = 1
        print(f"\nTotal de atendimentos para {paciente.nome}: {paciente.total_atendimentos()}")
        for data, count in atendimentos_data.items():
            print(f"  Data: {data}, Atendimentos: {count}")

pacientes = {}
pacientes[1] = Paciente(1, "Maria Silva", "MG123456", "1980-05-15", "Feminino")
pacientes[2] = Paciente(2, "João Santos", "SP987654", "1990-08-20", "Masculino")

pacientes[1].adicionar_atendimento("11-05-2024 11:12", "Consulta", "Exame de sangue", 70, 1.65)
pacientes[1].adicionar_atendimento("12-05-2024 15:33", "Consulta", "Consulta de rotina", 70, 1.65)
pacientes[2].adicionar_atendimento("12-05-2024 14:37", "Exame", "Exame de sangue", 80, 1.75)

print()
quantidade_pacientes_por_sexo(pacientes)
media_idade_pacientes(pacientes)
atendimentos_por_data(pacientes, "12-05-2024")
atendimentos_paciente(pacientes)
>>>>>>> 66df591460bbc2b0ed74e6b39f473d193ee07fdd
