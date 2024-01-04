import numpy as np

def matrixMul():
    for i in range(5000):
            array1 = np.array([[1, 2, 3], [4, 5, 6], [7, 8, 9], [7, 8, 9], [7, 8, 9], [7, 8, 9], [7, 8, 9]], ndmin=7)
            array2 = np.array([[9, 8, 7], [6, 5, 4], [3, 2, 1], [7, 8, 9], [7, 8, 9], [7, 8, 9], [7, 8, 9]], ndmin=7)
            np.multiply(array1, array2)
    


"""
def runWithSqlite(agent: Agent) -> None:
    agent.state = "postlite"
    agent.num += 1
    offer = Offer(aid=agent.id,price=100)
    sqliteCur.execute('UPDATE agent SET state= ?, num= ? WHERE id = ?',(agent.state,agent.num,agent.id))
    sqliteCur.execute('INSERT into offer(aid,price) VALUES (? , ?)',(agent.id,offer.price))
    sqliteConn.commit()
"""


"""
def matrixMul() -> None:
    for i in range(500):
            array1 = np.array([[1, 2, 3], [4, 5, 6], [7, 8, 9], [7, 8, 9], [7, 8, 9]], ndmin=5)
            array2 = np.array([[9, 8, 7], [6, 5, 4], [3, 2, 1], [7, 8, 9], [7, 8, 9]], ndmin=5)
            np.multiply(array1, array2) """