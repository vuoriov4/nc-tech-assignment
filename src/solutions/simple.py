from typing import Iterable, Optional, Tuple
from models.station import Station

def get_optimal_station(data: Iterable[Station], x: float, y: float) -> Optional[Tuple[Station, float]]:
	optimal_s = None
	max_speed = None
	for s in data:
		distance = ((x - s['x']) * (x - s['x']) + (y - s['y']) * (y - s['y'])) ** 0.5
		if (s['reach'] > distance):
			speed = (s['reach'] - distance) ** 2
			if (max_speed == None or max_speed < speed):
				optimal_s = s
				max_speed = speed
	if (optimal_s == None):
		return None
	else:
		return optimal_s, max_speed