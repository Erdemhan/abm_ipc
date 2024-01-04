
import timeit
import AgentService
import ReturnService
import DbMethod
import RedisService
import SharedMem

ISPOST = True


def main(period: int,N: int):

    ss = timeit.default_timer()

    agents = AgentService.createAgentList(N)
    SharedMem.run(agents,period)

    sf = timeit.default_timer()
    st = sf-ss
    print("Shared: ",st)  


    
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
    print("\n")
    print("DB - S : ", dbt - st)
    print("DB / S : ", dbt/st)
    

# KB büyüyünce db daha iyi
# 100kb de ajan sayısı arttıkça db daha iyi , period neredeyse etkisiz
# 1kb da ajan sayısı azaldıkça db daha iyi , period neredeyse etkisiz

if __name__ == "__main__":
    period=10
    N=20
    print("Period: " , period , "  N: " , N)
    main(period,N)