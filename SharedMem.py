import multiprocessing
from agent import Agent
from offer import Offer
from MatrixMul import matrixMul
import ConnectionService

postgresConn,postgresCur = ConnectionService.connectPostgres()


def add_agents_to_shared_list(shared_list, agents):
    shared_list.extend(agents)

def update_agents_in_shared_list(agent_id, shared_list):
    for index,item in enumerate(shared_list):
        if isinstance(item,Agent):
            if item.id == agent_id:
                # State güncelle
                item.state = "shared"
                # Num değerini +1 artır
                item.num += 1
                shared_list[index] = item
                # Offer ekle
                offer = Offer(aid=agent_id)
                shared_list.append(offer)
                break


def sync_shared_list_to_postgresql(shared_list,N):
    if len(shared_list) <= 0:
        pass
    for item in shared_list:
        if isinstance(item, Agent):
            # Agent nesnesini PostgreSQL'e ekle
            postgresCur.execute('UPDATE agent SET state = %s, num = %s WHERE id = %s', [item.state, item.num, item.id])
        elif isinstance(item, Offer):
            # Offer nesnesini PostgreSQL'e ekle
            postgresCur.execute('INSERT into offer(data,aid) VALUES (%s,%s)', [item.data, item.aid])
    postgresConn.commit()
    # Paylaşılan listeyi temizle
    del shared_list[N:]
    

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
