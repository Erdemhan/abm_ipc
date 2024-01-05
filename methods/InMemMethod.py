"""
import psycopg2
import redis
import multiprocessing
from services import AgentService

# PostgreSQL bağlantı bilgileri
pg_conn_params = {
    "host": "localhost",
    "port": "5432",
    "user": "postgres",
    "password": "admin",
    "database": "bildiri"
}

# Redis bağlantı bilgileri
redis_conn_params = {
    "host": "127.0.0.1",
    "port": "6379",
    "db": 0,
}

def add_agents_to_redis(agents):
    r = redis.Redis(**redis_conn_params)
    for agent in agents:
        agent_data = {"state": agent.state, "num": agent.num}
        r.hset(f"agent:{agent.id}", mapping=agent_data)
        r.sadd("agent_ids", agent.id)
    return [agent.id for agent in agents]

def update_agents_in_redis(agent_id):
    r = redis.Redis(**redis_conn_params)

    # State güncelle
    new_state = f"Updated State {agent_id}"
    r.hset(f"agent:{agent_id}", "state", new_state)

    # Num değerini +1 artır
    r.hincrby(f"agent:{agent_id}", "num", 1)

    # Offer ekle
    offer_data = ONEKB # String olarak değiştirildi
    r.rpush(f"agent:{agent_id}:offers", offer_data)

def sync_redis_to_postgresql(agent_ids):
    r = redis.Redis(**redis_conn_params)

    for agent_id in agent_ids:
        state = r.hget(f"agent:{agent_id}", "state").decode("utf-8")
        num = int(r.hget(f"agent:{agent_id}", "num").decode("utf-8"))
        offers = r.lrange(f"agent:{agent_id}:offers", 0, -1)

        conn = psycopg2.connect(**pg_conn_params)
        cursor = conn.cursor()

        # State ve Num güncelle
        cursor.execute("UPDATE agent SET state = %s, num = %s WHERE id = %s", (state, num, agent_id))

        # Offer ekle
        for offer in offers:
            offer_data = {"aid": agent_id, "data": offer.decode("utf-8")}
            cursor.execute("INSERT INTO offer (aid, data) VALUES (%s, %s)", (agent_id, offer.decode("utf-8")))

        cursor.close()
        conn.commit()
        conn.close()

def save_redis_to_persistence():
    r = redis.Redis(**redis_conn_params)
    r.save()

def loop(agent_ids):
    with multiprocessing.Pool() as pool:
        pool.map(worker_function, agent_ids)
        pool.close()
        pool.join()

def worker_function(agent_ids):
    update_agents_in_redis(agent_ids)
    #sync_redis_to_postgresql(agent_ids)
    save_redis_to_persistence()




def run(agents, num_updates_per_agent):
    # Redis'e agent verilerini ekleyerek ve id'yi döndürerek
    agent_ids = add_agents_to_redis(agents)
    for _ in range(num_updates_per_agent):
        loop(agent_ids)

if __name__ == "__main__":
    run(AgentService.createAgentList(30),50)



"""