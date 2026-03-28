import grpc
import sys
import os

# Ajuste para importar os protos corretamente
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))
from protos import sistema_pb2, sistema_pb2_grpc
from common.lamport import LamportClock

def rodar_cliente():
    clock = LamportClock()
    channel = grpc.insecure_channel('localhost:50051')
    stub = sistema_pb2_grpc.OrquestradorStub(channel)

    # 1. Autenticação 
    print("[v] Tentando login...")
    auth_res = stub.Login(sistema_pb2.LoginRequest(usuario="admin", senha="123"))
    
    if not auth_res.sucesso:
        print("[!] Falha na autenticação.")
        return

    token = auth_res.token
    print(f"[v] Autenticado! Token: {token}")

    # 2. Submeter Tarefa 
    clock.increment()
    print(f"[{clock.value}] Enviando tarefa: 'Processar Relatório Financeiro'")
    
    tarefa_res = stub.SubmeterTarefa(sistema_pb2.TarefaRequest(
        token=token,
        descricao="Processar Relatório Financeiro",
        tempo_logico=clock.value
    ))

    print(f"[*] Resposta do Orquestrador: {tarefa_res.mensagem} (ID: {tarefa_res.id_tarefa})")

if __name__ == "__main__":
    rodar_cliente()