import paralel
from agent import Agent
import multiprocessing
import ConnectionService
from psycopg2.extras import execute_values
from functools import partial

postgresConn,postgresCur = ConnectionService.connectPostgres()
sqliteConn,sqliteCur = ConnectionService.connectSqlite()

def run(agents: [Agent]):
    return returny(agents)

def returny(agents: [Agent]):
    with multiprocessing.Pool() as pool:
        results = pool.starmap(paralel.runWithReturn,agents)
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
        postgresCur.execute('INSERT into offer(data) VALUES (%s) RETURNING id;',[offer.data])
    postgresConn.commit()