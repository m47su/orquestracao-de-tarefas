# Plataforma Distribuída de Processamento Colaborativo de Tarefas

## 📋 Sobre o Projeto
Este sistema é uma plataforma de orquestração de tarefas distribuídas desenvolvida como projeto final para a disciplina de **Sistemas Distribuídos** no **IFBA - Campus Santo Antônio de Jesus**. 

O objetivo é simular um ambiente real de processamento colaborativo, onde múltiplos clientes submetem tarefas a um orquestrador que as distribui entre diversos nós de processamento (*Workers*), garantindo tolerância a falhas, balanceamento de carga e consistência de estado.

**Discentes:** Lara Gabriela Barreto Costa e Yasmin Neves Siqueira.  
**Docente:** Felipe Silva.

## 🏗️ Arquitetura do Sistema
O sistema é composto por quatro papéis principais:
* **Orquestrador Principal:** Ponto central que autentica usuários, mantém o estado global e coordena os Workers.
* **Orquestrador Secundário (Backup):** Monitora o principal via UDP Multicast e assume as operações em caso de falha (*failover*).
* **Workers:** Executam as tarefas e enviam sinais de vida (*heartbeats*) periodicamente.
* **Clientes:** Interface para submissão de tarefas e consulta de status em tempo real.

### Tecnologias Utilizadas
* **Linguagem:** Python 3.13+.
* **Comunicação Cliente-Orquestrador:** gRPC sobre TCP.
* **Sincronização Orquestradores:** UDP Multicast (IP: `224.1.1.1`, Porta: `5007`).
* **Monitoramento de Workers:** Heartbeats via UDP (Porta: `5008`).
* **Ordenação de Eventos:** Relógios Lógicos de Lamport.

## 📁 Estrutura do Repositório
A estrutura foi organizada de forma modular para facilitar a manutenção e escalabilidade:

```text
orquestracao-de-tarefas/
├── client/
│   └── client.py          # Implementação do cliente gRPC
├── common/
│   └── lamport.py         # Lógica do Relógio de Lamport
├── orchestrator/
│   ├── main.py            # Orquestrador Principal
│   └── backup.py          # Orquestrador de Backup (Failover)
├── protos/
│   ├── sistema.proto      # Definição do contrato gRPC
│   ├── sistema_pb2.py     # Arquivos gerados pelo Protocol Buffers
│   └── sistema_pb2_grpc.py
└── worker/
    └── worker.py          # Nó de processamento (Worker)
```

## 🚀 Como Executar

### 1. Pré-requisitos
Certifique-se de ter o Python instalado e as dependências do gRPC:
```bash
pip install grpcio grpcio-tools
```

### 2. Execução (Ordem Recomendada)
Para o funcionamento correto, abra terminais separados e execute os componentes na seguinte ordem:

1.  **Orquestrador Principal:**
    ```bash
    python orchestrator/main.py
    ```
2.  **Orquestrador de Backup:**
    ```bash
    python orchestrator/backup.py
    ```
3.  **Workers (Mínimo de 3 recomendados):**
    ```bash
    python worker/worker.py
    ```
4.  **Cliente:**
    ```bash
    python client/client.py
    ```

## 🛠️ Funcionalidades Implementadas

* **Autenticação:** O sistema utiliza um token simples. Credenciais padrão: Usuário `admin` / Senha `123`.
* **Balanceamento de Carga:** Implementado algoritmo **Round Robin** para distribuição equitativa das tarefas entre os Workers ativos.
* **Tolerância a Falhas:**
    * **Worker:** Se um Worker parar de enviar heartbeats por mais de 10 segundos, o orquestrador reatribui suas tarefas pendentes.
    * **Orquestrador:** O Backup assume a posição de Principal se não receber o sinal multicast em 5 segundos.
* **Consistência:** Uso de **Relógios de Lamport** para garantir a ordenação parcial de eventos em todo o sistema distribuído.

## 📊 Exemplos de Uso
Ao executar o cliente, o seguinte fluxo ocorre:
1.  O cliente realiza login e recebe um token.
2.  O cliente submete uma tarefa (ex: "Processar Relatório Financeiro").
3.  O orquestrador incrementa o relógio de Lamport, registra o evento e envia a tarefa para um Worker disponível seguindo a ordem circular.
4.  O status pode ser acompanhado pelos logs detalhados em cada terminal.

---
