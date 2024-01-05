import argparse
import sys
from main import start
from models import DataSize

def launch(num_of_agents, periods):
    if num_of_agents <= 0 or periods <= 0:
        print("Error: num_of_agents and periods values must be positive integers.")
        sys.exit(1)
    elif num_of_agents > 1000 or periods > 1000:
        print("Error: num_of_agents and periods values must be lower than 1000.")
        sys.exit(1)
    
    start(N=num_of_agents, period=periods)

if __name__ == '__main__':
    parser = argparse.ArgumentParser(description='Specify the required arguments to launch the program.')
    parser.add_argument('--num_of_agents', type=int, required=True, help='Number of agents')
    parser.add_argument('--periods', type=int, required=True, help='Number of periods')
    parser.add_argument('--datasize', type=DataSize, required=True, help='Number of periods')

    args = parser.parse_args()
    
    launch(args.num_of_agents, args.periods)
