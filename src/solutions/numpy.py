from typing import Optional, Tuple
from models.station import Station
import numpy as np

def get_optimal_station(data: np.ndarray, x: float, y: float) -> Optional[Tuple[Station, float]]:
	distance = np.sqrt(np.sum(np.square(data[..., 0:2] - np.array([x, y])), axis=1))
	reach = data[..., 2:].T
	index = np.argmax(reach - distance)
	speed_sqrt = (reach - distance)[0][index]
	if (speed_sqrt <= 0):
		return None
	else:
		return Station(
			x = data[index][0],
			y = data[index][1],
			reach = data[index][2],
		), speed_sqrt * speed_sqrt
