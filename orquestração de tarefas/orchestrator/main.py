import sys
import os
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))
from protos import sistema_pb2, sistema_pb2_grpc
import grpc
from concurrent import futures
import time
import threading
import socket
from common.lamport import LamportClock

class OrquestradorServicer(sistema_pb2_grpc.OrquestradorServicer):
    def __init__(self):
        self.clock = LamportClock()
        self.workers = {} 
        self.tarefas = {} 
        self.proximo_worker_idx = 0

    def Login(self, request, context):
        if request.usuario == "admin" and request.senha == "123":
            return sistema_pb2.TokenResponse(token="token_valido", sucesso=True)
        return sistema_pb2.TokenResponse(token="", sucesso=False)

    def SubmeterTarefa(self, request, context):
        self.clock.update(request.tempo_logico)
        id_t = f"T-{int(time.time())}"
        
        active_workers = list(self.workers.keys())
        if not active_workers:
            return sistema_pb2.TarefaResponse(id_tarefa=id_t, mensagem="Erro: Nenhum worker ativo")

        worker_escolhido = active_workers[self.proximo_worker_idx % len(active_workers)]
        self.proximo_worker_idx += 1
        
        self.tarefas[id_t] = {"status": "Processando", "worker": worker_escolhido}
        
        print(f"[{self.clock.value}] Tarefa {id_t} distribuída para {worker_escolhido} (Round Robin)")
        
        return sistema_pb2.TarefaResponse(id_tarefa=id_t, mensagem=f"Enviada para {worker_escolhido}")

def sync_backup():
    MCAST_GRP = '224.1.1.1'
    MCAST_PORT = 5007
    sock = socket.socket(socket.AF_INET, socket.SOCK_DGRAM, socket.IPPROTO_UDP)
    while True:
        try:
            sock.sendto(b"HEARTBEAT_PRIMARY", (MCAST_GRP, MCAST_PORT))
        except:
            pass
        time.sleep(2)

def monitorar_workers(orquestrador_instance):
    sock = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
    sock.bind(('0.0.0.0', 5008))
    while True:
        data, addr = sock.recvfrom(1024)
        msg = data.decode()
        if "HEARTBEAT" in msg:
            worker_id = msg.split("|")[1]
            orquestrador_instance.workers[worker_id] = time.time()

        now = time.time()
        for wid, last_seen in list(orquestrador_instance.workers.items()):
            if now - last_seen > 10:
                print(f"[!] FALHA DETECTADA: Worker {wid} parou de enviar heartbeats.")
                del orquestrador_instance.workers[wid]
                print(f"[*] Reatribuindo tarefas do {wid} para o próximo nó ativo...")

if __name__ == "__main__":
    inst = OrquestradorServicer()
    threading.Thread(target=monitorar_workers, args=(inst,), daemon=True).start()
    threading.Thread(target=sync_backup, daemon=True).start()
    
    server = grpc.server(futures.ThreadPoolExecutor(max_workers=10))
    sistema_pb2_grpc.add_OrquestradorServicer_to_server(inst, server)
    server.add_insecure_port('[::]:50051')
    
    print("Orquestrador Principal rodando na porta 50051...")
    server.start()
    server.wait_for_termination()