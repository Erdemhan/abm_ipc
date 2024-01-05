from . import MatrixMul
from services import ConnectionService
from models import Agent, Offer
import multiprocessing

postgresConn,postgresCur = ConnectionService.connectPostgres()


#DB Method

def runWithPostgres(agent: Agent) -> None:
    agent.state = "post"
    agent.num += 1
    offer = Offer(aid=agent.id)
    postgresCur.execute('UPDATE agent SET state = %s, num = %s WHERE id = %s',[agent.state,agent.num,agent.id])
    postgresCur.execute('INSERT into offer(data,aid,datasize) VALUES (%s,%s,%s)',[offer.data,agent.id,offer.dataSize])
    postgresConn.commit()

def run(agents: [Agent],period: int):
    for i in range(period):
        dbMethodPostgres(agents=agents)


def dbMethodPostgres(agents: [Agent]) -> [Agent]:
    with multiprocessing.Pool() as pool:
        pool.map(runWithPostgres,agents)
    pool.close()
    pool.join()
    pool.terminate()
    dbMethodUpdatePostgres(agents)


def dbMethodUpdatePostgres(agents: [Agent]) -> [Agent]:
    for agent in agents:
        postgresCur.execute('SELECT * from agent WHERE id= %s',[agent.id])
        agentData = postgresCur.fetchone()
        agent.id,agent.state,agent.num = agentData[0],agentData[1],agentData[2]






"""
def dbMethodSqlite(agents: [Agent]) -> [Agent]:
    with multiprocessing.Pool() as pool:
        pool.map(MatrixMul.runWithSqlite, agents)
    pool.close()
    pool.join()

    return dbMethodUpdateSqlite(agents)


def dbMethodUpdateSqlite(agents: [Agent]) -> [Agent]:
    for agent in agents:
        sqliteCur.execute('SELECT * from agent WHERE id= ?',[agent.id])
        agentData = sqliteCur.fetchone()
        agent.id,agent.state,agent.num = agentData[0],agentData[1],agentData[2]
    return agents
"""