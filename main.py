
import timeit
from services import AgentService, ConnectionService
from methods import ReturnMethod, DbMethod, SharedMemMethod
from models import Agent,Offer
from decimal import Decimal, ROUND_DOWN

def runDbMethod(agents: [Agent], period:int):
    ts = timeit.default_timer()
    DbMethod.run(agents,period)
    tf = timeit.default_timer()
    return tf-ts

def runReturnMethod(agents: [Agent], period:int):
    ts = timeit.default_timer()
    ReturnMethod.run(agents,period)
    tf = timeit.default_timer()
    return tf-ts

def runSharedMemMethod(agents: [Agent], period:int):
    ts = timeit.default_timer()
    SharedMemMethod.run(agents,period)
    tf = timeit.default_timer()
    return tf-ts


def formatFloat(number, precision=4):
    return round(number, precision)

def showResults(method_times):
    print("\n\n------------------------")
    best_time = list(('method',float('inf')))
    for method1, time1 in method_times.items():
        if best_time[1] > time1:
            best_time[0],best_time[1] = method1,time1
        for method2, time2 in method_times.items():
            if method1 != method2:
                time_diff = formatFloat(time1 - time2)
                time_ratio = formatFloat(time1 / time2)

                print(f"{method1} - {method2} Time Difference: {time_diff}")
                print(f"{method1} / {method2} Time Ratio: {time_ratio}")
    print("\nBEST -----> ",best_time[0],best_time[1])


def run(period: int,N: int):

    agents = AgentService.createAgentList(N)
    dbTime = runDbMethod(agents,period)
    print("DB: " , dbTime)

    agents = AgentService.createAgentList(N)
    returnTime = runReturnMethod(agents,period)
    print("Return: " , returnTime)

    agents = AgentService.createAgentList(N)
    sharedTime = runDbMethod(agents,period)
    print("Shared: " , sharedTime)

    method_times = {
    "DB": dbTime,
    "Return": returnTime,
    "Shared": sharedTime
    }

    showResults(method_times)

    

# KB büyüyünce db daha iyi
# 100kb de ajan sayısı arttıkça db daha iyi , period neredeyse etkisiz
# 1kb da ajan sayısı azaldıkça db daha iyi , period neredeyse etkisiz
# Shared ajan sayısı arttıkça kötüleşiyor , her türlü R ve DB den daha kötü



def start(period: int, N: int):

    postgresConn,postgresCur = ConnectionService.connectPostgres()
    postgresCur.execute("TRUNCATE TABLE agent CASCADE;")
    postgresConn.commit()
    offer = Offer()

    print("\n-------- Period: " , period , "  N: " , N, "  Data Size: ",offer.dataSize , " --------\n")
    run(period,N)