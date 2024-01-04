import multiprocessing
import time
import psycopg2
from agent import Agent
from offer import Offer
from AgentService import createAgentList

conn_params = {
    "host": "localhost",
    "port": "5432",
    "user": "postgres",
    "password": "admin",
    "database": "bildiri"
}

conn = psycopg2.connect(**conn_params)
cursor = conn.cursor()

def add_agents_to_shared_list(shared_list, agents):
    shared_list.extend(agents)

def update_agents_in_shared_list(agent_id, shared_list):
    for index,item in enumerate(shared_list):
        if isinstance(item,Agent):
            if item.id == agent_id:
                # State güncelle
                item.state = f"Updated State {agent_id}"
                # Num değerini +1 artır
                item.num += 1
                shared_list[index] = item
                # Offer ekle
                offer = Offer(aid=agent_id)
                shared_list.append(offer)
                break


def sync_shared_list_to_postgresql(shared_list,N):
    for item in shared_list:
        if isinstance(item, Agent):
            # Agent nesnesini PostgreSQL'e ekle
            cursor.execute('UPDATE agent SET state = %s, num = %s WHERE id = %s', [item.state, item.num, item.id])
        elif isinstance(item, Offer):
            # Offer nesnesini PostgreSQL'e ekle
            cursor.execute('INSERT into offer(data,aid) VALUES (%s,%s)', [item.data, item.aid])

    # Paylaşılan listeyi temizle
    del shared_list[N:]
    conn.commit()

def paralel(agents, shared_list):
    with multiprocessing.Pool() as pool:
        pool.starmap(update_agents_in_shared_list, [(agent.id, shared_list) for agent in agents])
        pool.close()
        pool.join()

def create_and_update_agents(agents, num_updates_per_agent):
    with multiprocessing.Manager() as manager:
        # Paylaşılan bellek üzerinde list oluştur
        shared_list = manager.list()
        # Main process içinde paylaşılan listeye agent verilerini ekle
        add_agents_to_shared_list(shared_list, agents)


        # Subprocess içinde paylaşılan listeyi kullanarak agent'ları güncelle
        for _ in range(num_updates_per_agent):
            paralel(agents, shared_list)
            # Subprocess içinde yapılan güncellemeleri PostgreSQL'e eşle
            sync_shared_list_to_postgresql(shared_list,N=len(agents))



def run(agents: [Agent], period: int):
    create_and_update_agents(agents, period)
