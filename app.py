from flask import Flask, render_template, request
from load_network import load_network
from dijkstra import dijkstra
from visualization import visualize_graph
import os
import logging


logging.basicConfig(level=logging.DEBUG)
logger = logging.getLogger(__name__)

template_dir = os.path.abspath(os.path.join(os.path.dirname(__file__), '..', 'templates'))
static_dir = os.path.abspath(os.path.join(os.path.dirname(__file__), '..', 'static'))
app = Flask(__name__, template_folder=template_dir, static_folder=static_dir)

try:
    graph = load_network('D:\metro routing system project daa\data\metro_network.csv')
    stations = list(graph.keys())
    if not stations:
        raise ValueError("No stations loaded from CSV")
    logger.info(f"Stations loaded: {stations}")
except Exception as e:
    graph = {}
    stations = []
    logger.error(f"Error loading graph: {str(e)}")

@app.route('/', methods=['GET', 'POST'])
def index():
    result = None
    path = None
    distance = None
    image_path = None

    if not stations:
        result = "Error: Failed to load metro network. Check CSV file."
        logger.error("No stations available")
        return render_template('index.html', stations=stations, result=result, image_path=image_path)

    if request.method == 'POST':
        start = request.form.get('start')
        end = request.form.get('end')
        logger.debug(f"Received form data: start={start}, end={end}")

        if start and end and start in graph and end in graph:
            logger.debug(f"Processing Dijkstra for {start} to {end}")
            path, distance = dijkstra(graph, start, end)
            if path:
                # Fare calculation based on distance
                if distance <= 5:
                    fare = 10
                elif distance <= 10:
                    fare = 20
                elif distance <= 15:
                    fare = 30
                else:
                    fare = 40

                result = f"Shortest path: {' -> '.join(path)}<br>Total distance: {distance} km<br>Fare: ₹{fare}"

                try:
                    visualize_graph(graph, path, start, end, output_path='D:\metro routing system project daa\static\graph.png')
                    image_path = 'graph.png'
                    logger.info("Graph image generated successfully")
                    with open('D:\metro routing system project daa\output\results.txt', 'a') as f:
                        f.write(f"{start} to {end}: {' -> '.join(path)}, {distance} km\n")
                except Exception as e:
                    logger.error(f"Error generating graph: {str(e)}")
                    result += "<br>Error generating map. Check server logs."
            else:
                result = f"No path found between {start} and {end}"
                logger.warning(f"No path found from {start} to {end}")
        else:
            result = "Invalid stations selected!"
            logger.error(f"Invalid stations: start={start}, end={end}")

    return render_template('index.html', stations=stations, result=result, image_path=image_path)

if __name__ == '__main__':
    app.run(debug=True, port=5001)