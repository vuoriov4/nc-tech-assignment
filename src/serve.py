from flask import Flask, request 
from functools import partial
import pandas as pd
from solutions.simple import get_optimal_station as get_optimal_station_simple
from solutions.numpy import get_optimal_station as get_optimal_station_numpy
from data import read_station_data

# Load datasets to memory. See README.md on the limitations.
datasets = {
    '5.txt':  list(read_station_data('./data/5.txt')),
    '5M.txt': list(read_station_data('./data/5M.txt')),
}

# Transform to dataframes for numpy.
dataframes = {
    key: pd.DataFrame.from_dict(value).to_numpy() 
    for (key, value) in datasets.items() 
}

# Solutions and their respective imports.
# Example usage: solutions['simple']('5.txt')(x, y)
solutions = {
    'simple': lambda dataset: partial(get_optimal_station_simple, datasets[dataset]),
    'numpy': lambda dataset: partial(get_optimal_station_numpy, dataframes[dataset])
}

# Spin up the HTTP server for client use.
app = Flask(__name__)

@app.route('/')
def api():
    if (not validate(request.args)):
        return "Invalid parameters", 400
    x = float(request.args['x'])
    y = float(request.args['y'])
    dataset = request.args.get('dataset', '5.txt')
    solution = request.args.get('solution', 'numpy')
    result = solutions[solution](dataset)(x, y)
    if (result == None):
        return "No network station within reach for point x=%.1f, y=%.1f" % (x, y), 200
    else:
        station, speed = result
        return "Best network station for point x=%.1f, y=%.1f is x=%.1f, y=%.1f with speed %.1f" % (
            x, y, station['x'], station['y'], speed
        ), 200
        
def validate(args: dict):
    for num in ['x', 'y']:
        if (not num in args): 
            return False
        try:
            float(args[num])
        except ValueError:
            return False
    if ('solution' in args):
        if (not args['solution'] in ['simple', 'numpy']):
            return False
    if ('dataset' in args):
        if (not args['dataset'] in datasets.keys()):
            return False
    return True