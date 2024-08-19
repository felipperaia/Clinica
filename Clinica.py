import datetime
import json
import os

class Paciente:
    def __init__(self, nome, telefone):
        self.nome = nome
        self.telefone = telefone

    def to_dict(self):
        return {'nome': self.nome, 'telefone': self.telefone}

class Agendamento:
    def __init__(self, paciente, dia, hora, especialidade):
        self.paciente = paciente
        self.dia = dia
        self.hora = hora
        self.especialidade = especialidade

    def to_dict(self):
        return {
            'paciente': self.paciente.to_dict(),
            'dia': self.dia,
            'hora': self.hora,
            'especialidade': self.especialidade
        }

def carregar_dados():
    if os.path.exists('pacientes.json'):
        with open('pacientes.json', 'r') as file:
            pacientes_data = json.load(file)
            for pd in pacientes_data:
                pacientes.append(Paciente(pd['nome'], pd['telefone']))
    if os.path.exists('agendamentos.json'):
        with open('agendamentos.json', 'r') as file:
            agendamentos_data = json.load(file)
            for ad in agendamentos_data:
                paciente = Paciente(ad['paciente']['nome'], ad['paciente']['telefone'])
                agendamentos.append(Agendamento(paciente, ad['dia'], ad['hora'], ad['especialidade']))
    if os.path.exists('historico.json'):
        with open('historico.json', 'r') as file:
            historico_data = json.load(file)
            for hd in historico_data:
                paciente = Paciente(hd['paciente']['nome'], hd['paciente']['telefone'])
                historico.append(Agendamento(paciente, hd['dia'], hd['hora'], hd['especialidade']))

def salvar_dados():
    with open('pacientes.json', 'w') as file:
        json.dump([p.to_dict() for p in pacientes], file)
    with open('agendamentos.json', 'w') as file:
        json.dump([a.to_dict() for a in agendamentos], file)
    with open('historico.json', 'w') as file:
        json.dump([h.to_dict() for h in historico], file)

pacientes = []
agendamentos = []
historico = []
carregar_dados()

def cadastrar_paciente():
    nome = input("Digite o nome do paciente: ")
    telefone = input("Digite o telefone do paciente: ")
    for paciente in pacientes:
        if paciente.telefone == telefone:
            print("Paciente já cadastrado!")
            return
    pacientes.append(Paciente(nome, telefone))
    salvar_dados()
    print("Paciente cadastrado com sucesso")

def listar_pacientes():
    for idx, paciente in enumerate(pacientes):
        print(f"{idx + 1} - {paciente.nome} (Telefone: {paciente.telefone})")

def marcar_consulta():
    if not pacientes:
        print("Nenhum paciente cadastrado")
        return
    listar_pacientes()
    paciente_idx = int(input("Selecione o número do paciente: ")) - 1
    if paciente_idx < 0 or paciente_idx >= len(pacientes):
        print("Paciente inválido!")
        return

    paciente = pacientes[paciente_idx]
    dia = input("Digite o dia da consulta (DD-MM-AAAA): ")
    hora = input("Digite a hora da consulta (HH:MM): ")
    especialidade = input("Digite a especialidade desejada: ")

    try:
        data_consulta = datetime.datetime.strptime(f"{dia} {hora}", "%d-%m-%Y %H:%M")
        if data_consulta < datetime.datetime.now():
            print("Não é possível marcar consultas retroativas!")
            return
    except ValueError as e:
        print("Formato de data ou hora inválido!")
        return

    for agendamento in agendamentos:
        if agendamento.dia == dia and agendamento.hora == hora:
            print("Horário já agendado!")
            return

    novo_agendamento = Agendamento(paciente, dia, hora, especialidade)
    agendamentos.append(novo_agendamento)
    historico.append(novo_agendamento)
    salvar_dados()
    print("Consulta marcada com sucesso")

def listar_agendamentos():
    for idx, agendamento in enumerate(agendamentos):
        print(f"{idx + 1} - {agendamento.paciente.nome}, {agendamento.dia} {agendamento.hora}, {agendamento.especialidade}")

def cancelar_consulta():
    if not agendamentos:
        print("Nenhuma consulta agendada")
        return
    listar_agendamentos()
    agendamento_idx = int(input("Selecione o número do agendamento: ")) - 1
    if agendamento_idx < 0 or agendamento_idx >= len(agendamentos):
        print("Agendamento inválido!")
        return

    agendamento = agendamentos[agendamento_idx]
    print(f"Consulta agendada: {agendamento.paciente.nome}, {agendamento.dia}, {agendamento.hora}, {agendamento.especialidade}")
    confirmar = input("Deseja cancelar esta consulta? (s/n): ").lower()
    if confirmar == 's':
        agendamentos.pop(agendamento_idx)
        salvar_dados()
        print("Consulta cancelada com sucesso")

def apagar_paciente():
    if not pacientes:
        print("Nenhum paciente cadastrado")
        return
    listar_pacientes()
    paciente_idx = int(input("Selecione o número do paciente a ser apagado: ")) - 1
    if paciente_idx < 0 or paciente_idx >= len(pacientes):
        print("Paciente inválido!")
        return

    paciente = pacientes[paciente_idx]
    global agendamentos
    agendamentos = [agendamento for agendamento in agendamentos if agendamento.paciente != paciente]
    pacientes.pop(paciente_idx)
    salvar_dados()
    print("Paciente apagado com sucesso e todos os agendamentos associados foram removidos")

def historico_consultas():
    if not pacientes:
        print("Nenhum paciente cadastrado")
        return
    listar_pacientes()
    paciente_idx = int(input("Selecione o número do paciente para ver o histórico: ")) - 1
    if paciente_idx < 0 or paciente_idx >= len(pacientes):
        print("Paciente inválido!")
        return

    paciente = pacientes[paciente_idx]
    consultas = [agendamento for agendamento in historico if agendamento.paciente == paciente]
    if not consultas:
        print("Nenhuma consulta encontrada para este paciente")
    else:
        for idx, consulta in enumerate(consultas):
            print(f"{idx + 1} - {consulta.dia} {consulta.hora}, {consulta.especialidade}")

def apagar_item_historico():
    if not historico:
        print("Nenhum histórico de consulta encontrado")
        return
    historico_consultas()
    consulta_idx = int(input("Selecione o número da consulta a ser apagada do histórico: ")) - 1
    if consulta_idx < 0 or consulta_idx >= len(historico):
        print("Consulta inválida!")
        return

    historico.pop(consulta_idx)
    salvar_dados()
    print("Consulta apagada do histórico com sucesso")

def menu():
    while True:
        print("\n--- Menu Principal ---")
        print("1. Cadastrar um paciente")
        print("2. Marcar uma consulta")
        print("3. Histórico de consultas")
        print("4. Cancelar uma consulta")
        print("5. Apagar um paciente")
        print("6. Apagar item do histórico de consultas")
        print("7. Sair")
        opcao = input("Selecione uma opção: ")

        if opcao == '1':
            cadastrar_paciente()
        elif opcao == '2':
            marcar_consulta()
        elif opcao == '3':
            historico_consultas()
        elif opcao == '4':
            cancelar_consulta()
        elif opcao == '5':
            apagar_paciente()
        elif opcao == '6':
            apagar_item_historico()
        elif opcao == '7':
            print("Encerrando o programa.")
            break
        else:
            print("Opção inválida!")

if __name__ == "__main__":
    menu()
