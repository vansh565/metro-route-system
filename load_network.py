import csv

def load_network(file_path):
 
    graph = {}
   
    with open(file_path,'r') as file:
        reader = csv.reader(file)
        next(reader) 
        
      
        for row in reader:
            station1, station2, distance = row
            distance = float(distance)  
            
      
            if station1 not in graph:
                graph[station1] = {}
            if station2 not in graph:
                graph[station2] = {}
            
       
            graph[station1][station2] = distance
            graph[station2][station1] = distance
                
    return graph

