
import timeit
import AgentService
import ReturnService
import DbMethod


ISPOST = True


def main(period: int,N: int):

    agents = AgentService.createAgentList(N,ISPOST)

    dbs = timeit.default_timer()
    for i in range(period):  
        agents = DbMethod.run(agents)

    dbf = timeit.default_timer()
    dbt = dbf-dbs
    print("DB: ",dbt)

    agents = AgentService.createAgentList(N,ISPOST)
    rs = timeit.default_timer() 
    for i in range(period):
        results = ReturnService.returny(agents)
        agents = [result[0] for result in results]
        ReturnService.updateReturny(results)

    rf = timeit.default_timer()
    rt = rf-rs
    print("R: ",rt)
    print("DB - R : ", dbt - rt)
    print("DB / R : ", dbt/rt)




if __name__ == "__main__":
    period=30
    N=50
    print("Period: " , period , "  N: " , N)
    main(period,N)