from load_network import load_network
from dijkstra import dijkstra
from visualization import visualize_graph

def main():
    graph = load_network(r'D:\metro routing system project daa\data\metro_network.csv')
    print("Available stations:", list(graph.keys()))
    start = input("Enter start station: ")
    end = input("Enter end station: ")

    if start not in graph or end not in graph:
        print("Invalid station!")
        return

    path, distance = dijkstra(graph, start, end)
    if path:
        print(f"Shortest path: {' -> '.join(path)}")
        print(f"Total distance: {distance} km")
    else:
        print("No path found!")
        return 
    
    visualize = input("do you want the map ?(yes or no)").lower()
    if visualize == 'yes':
        try:
            visualize_graph(graph,path)
        except Exception as e:
            print("error in showing map:",str(e))

if __name__ == "__main__":
    main()