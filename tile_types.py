from typing import Tuple
import numpy as np

graphic_dt = np.dtype(
    [
        ("ch", np.int32),
        ("fg", "3B"),
        ("bg", "3B"),
    ]
)

tile_dt = np.dtype(
    [
        ("walkable", np.bool), # True if the tile can be walkable over
        ("transparent", np.bool), # True if the tile doesn't block FOV
        ("dark", graphic_dt), # Graphics for when the tile is not in FOV
        ("light", graphic_dt) # Graphics for when the tile is in FOV 
    ]
)

def new_tile(
        *, # Enforces the use of keywordsn so the paramter order doesn't matter
        walkable: int,
        transparent: int,
        dark: Tuple[int, Tuple[int, int, int], Tuple[int, int, int]],
        light: Tuple[int, Tuple[int, int, int], Tuple[int, int, int]]
) -> np.ndarray:
    return np.array((walkable, transparent, dark, light), dtype=tile_dt)

fog = np.array((ord(" "), (255, 255, 255), (0, 0, 0)), dtype=graphic_dt)

floor = new_tile(
    walkable=True,
    transparent=True,
    dark=(ord(" "), (255, 255, 255), (50, 50, 150)),
    light=(ord(" "), (255, 255, 255), (200, 180, 50))
)

wall = new_tile(
    walkable=False,
    transparent=False,
    dark=(ord(" "),(255, 255, 255), (0, 0, 100)),
    light=(ord(" "), (255, 255, 255), (130,110,50))
)