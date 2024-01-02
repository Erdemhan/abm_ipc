from agent import Agent
import DbMethod


def createAgentPostgres():
    agent = Agent()
    DbMethod.postgresCur.execute('INSERT into agent (state) VALUES (%s) RETURNING id;',[agent.state])
    agent.id =  DbMethod.postgresCur.fetchone()[0]
    DbMethod.postgresConn.commit()
    return agent


def createDataList(num: int, data: str):
    dataList = []
    for i in range(num):
        dataList.append(data)
    return dataList
    

def createAgentSqlite():
    agent = Agent()
    DbMethod.sqliteCur.execute('INSERT into agent (state) VALUES (?) RETURNING id;',[agent.state])
    agent.id =  DbMethod.sqliteCur.fetchone()[0]
    DbMethod.sqliteConn.commit()
    return agent



def createAgentList(num:int , post: bool) -> [Agent]:
    agents = []
    if post:
        for i in range(num):
            agents.append(createAgentPostgres())
    else:
        for i in range(num):
            agents.append(createAgentSqlite())
    return agents

