from models import Agent,Offer
from services import ConnectionService
import numpy as np
import timeit


postgresConn,postgresCur = ConnectionService.connectPostgres()


def run(agents: [Agent])-> None:
    for agent in agents:
        agent = serialRunAgent(agent)


def serialRunAgent(agent: Agent) -> None:
    agent.state = "serial"
    agent.num += 1
    offer = Offer(aid=agent.id)
    postgresCur.execute('UPDATE agent SET state = %s, num = %s WHERE id = %s',[agent.state,agent.num,agent.id])
    postgresCur.execute('INSERT into offer(data,aid,datasize) VALUES (%s,%s,%s)',[offer.data,agent.id,offer.dataSize])
    postgresConn.commit()
    ss = timeit.default_timer()
    matrixMul()
    sf = timeit.default_timer()
    st = sf-ss
    print("Serial Matrix MUl: ",st)  
    


def matrixMul():
    for i in range(5000):
            array1 = np.array([[1, 2, 3], [4, 5, 6], [7, 8, 9], [7, 8, 9], [7, 8, 9], [7, 8, 9], [7, 8, 9]], ndmin=7)
            array2 = np.array([[9, 8, 7], [6, 5, 4], [3, 2, 1], [7, 8, 9], [7, 8, 9], [7, 8, 9], [7, 8, 9]], ndmin=7)
            result = np.multiply(array1, array2)