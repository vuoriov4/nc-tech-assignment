import random
from typing import Iterable
from models.station import Station

def read_station_data(file_name: str) -> Iterable[Station]:
    """
    Reads CSV-formatted station data to memory. 
    The CSV file is expected to have no header and three floats per line (x, y, and reach).
    Returns an iterator of Station objects.

    :param str filename: File path of the CSV file.
    """
    with open(file_name) as file:
        for line in file:
            values = line.replace('\n', '').split(',')
            yield Station(
                x = float(values[0]),
                y = float(values[1]),
                reach = float(values[2])
            )

def generate_station_data(num_lines: int) -> Iterable[str]:
    """
    Generate CSV-formatted station data. 
    Returns an iterator for each line containing randomized data (x, y and reach)

    :param int num_lines: Number of lines to generate.
    """
    bounds_x = [-100, 100]
    bounds_y = [-100, 100]
    for _ in range(0, num_lines):
        x = random.uniform(bounds_x[0], bounds_x[1])
        y = random.uniform(bounds_y[0], bounds_y[1])
        reach = random.uniform(1.0, 12.0)
        yield '%f,%f,%f\n' % (x, y, reach)

# You may use this file to generate new datasets
if (__name__ == '__main__'):
    num_lines = 500 * 10 ** 6
    file_name = 'data/500M.csv'
    with open(file_name, 'w') as file:
        file.writelines(generate_station_data(num_lines))