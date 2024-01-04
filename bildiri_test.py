
import timeit
import AgentService
import ReturnService
import DbMethod
import SharedMem
import ConnectionService

postgresConn,postgresCur = ConnectionService.connectPostgres()

def main(period: int,N: int):

    postgresCur.execute("TRUNCATE TABLE agent CASCADE;")
    postgresConn.commit()

    ss = timeit.default_timer()

    agents = AgentService.createAgentList(N)
    SharedMem.run(agents,period)
    sf = timeit.default_timer()
    st = sf-ss
    print("Shared: ",st)  


    agents = AgentService.createAgentList(N)
    dbs = timeit.default_timer()
    DbMethod.run(agents,period)
    dbf = timeit.default_timer()
    dbt = dbf-dbs
    print("DB: ",dbt)

    agents = AgentService.createAgentList(N)
    rs = timeit.default_timer() 
    ReturnService.run(agents,period)
    rf = timeit.default_timer()
    rt = rf-rs
    print("R: ",rt)

    print("\n\n")
    print("DB - R : ", dbt - rt)
    print("DB / R : ", dbt/rt)
    print("\n")
    print("DB - S : ", dbt - st)
    print("DB / S : ", dbt/st)
    print("\n")
    print("R - S : ", rt - st)
    print("R / S : ", rt/st)
    

# KB büyüyünce db daha iyi
# 100kb de ajan sayısı arttıkça db daha iyi , period neredeyse etkisiz
# 1kb da ajan sayısı azaldıkça db daha iyi , period neredeyse etkisiz
# Shared ajan sayısı arttıkça kötüleşiyor , her türlü R ve DB den daha kötü

if __name__ == "__main__":
    period=10
    N=20
    print("Period: " , period , "  N: " , N, "\n")
    main(period,N)