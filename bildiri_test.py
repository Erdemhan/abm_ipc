
import timeit
import AgentService
import ReturnService
import DbMethod
import RedisService


ISPOST = True


def main(period: int,N: int):

    agents = AgentService.createAgentList(N)

    dbs = timeit.default_timer()
    for i in range(period):  
        agents = DbMethod.run(agents)

    dbf = timeit.default_timer()
    dbt = dbf-dbs
    print("DB: ",dbt)

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


# KB büyüyünce db daha iyi
# 100kb de ajan sayısı arttıkça db daha iyi , period neredeyse etkisiz
# 1kb da ajan sayısı azaldıkça db daha iyi , period neredeyse etkisiz

if __name__ == "__main__":
    period=100
    N=50
    print("Period: " , period , "  N: " , N)
    main(period,N)