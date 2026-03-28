import sys
import os
import time
import uuid
import socket
import threading

sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))
from protos import sistema_pb2, sistema_pb2_grpc

# Configurações do Worker
WORKER_ID = f"Worker-{str(uuid.uuid4())[:4]}"
ORCHESTRATOR_IP = 'localhost'
HEARTBEAT_PORT = 5008 

def send_heartbeat():
    """Envia sinal de vida para o Orquestrador """
    sock = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
    print(f"[*] {WORKER_ID} iniciado. Enviando heartbeats para porta {HEARTBEAT_PORT}...")
    while True:
        try:
            message = f"HEARTBEAT|{WORKER_ID}"
            sock.sendto(message.encode(), (ORCHESTRATOR_IP, HEARTBEAT_PORT))
        except Exception as e:
            print(f"[!] Erro ao enviar heartbeat: {e}")
        time.sleep(3) # Intervalo de 3 segundos

if __name__ == "__main__":
    # Inicia o envio de batimentos em segundo plano
    threading.Thread(target=send_heartbeat, daemon=True).start()
    
    print(f"[v] {WORKER_ID} online e aguardando comandos...")
    
    # Mantém o processo vivo
    try:
        while True:
            time.sleep(1)
    except KeyboardInterrupt:
        print(f"\n[!] {WORKER_ID} encerrado.")