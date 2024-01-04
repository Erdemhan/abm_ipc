from agent import Agent
from offer import Offer
import multiprocessing
import ConnectionService


postgresConn,postgresCur = ConnectionService.connectPostgres()
sqliteConn,sqliteCur = ConnectionService.connectSqlite()

def runWithReturn(agent: Agent) -> (Agent,bool):
    agent.state = "returned"
    agent.num += 1
    offer = offer = Offer(aid=agent.id)
    return (agent,offer)

def run(agents: [Agent], period: int):
    for i in range(period):
        results = returny(agents)
        agents = [result[0] for result in results]
        updateReturny(results)

def returny(agents: [Agent]):
    with multiprocessing.Pool() as pool:
        results = pool.map(runWithReturn,agents)
    pool.close()
    pool.join()
    #DbMethod.updateReturny(results)
    return results



# Return Method
def updateReturny(results):
    for result in results:
        agent = result[0]
        offer = result[1]
        postgresCur.execute('UPDATE agent SET state = %s, num = %s WHERE id = %s',[agent.state,agent.num,agent.id])
        postgresCur.execute('INSERT into offer(data,aid) VALUES (%s,%s) RETURNING id;',[offer.data,agent.id])
    postgresConn.commit()