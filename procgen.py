from __future__ import annotations
from typing import Tuple, Iterator, List, TYPE_CHECKING
import random
from game_map import GameMap
import tile_types
import entities_factory
import tcod

if TYPE_CHECKING:
    from entity import Entity

class RectangularRoom:
    def __init__(self, x:int, y: int, width: int, height: int):
        self.x1 = x
        self.y1 = y
        self.x2 = x + width
        self.y2 = y + height

    @property
    def center(self) -> Tuple[int, int]:
        center_x = int((self.x1 + self.x2) / 2)
        center_y = int((self.y1 + self.y2) / 2)

        return center_x,center_y
    
    @property
    def inner(self) -> Tuple[slice, slice]:
        return slice(self.x1 + 1, self.x2), slice(self.y1 + 1, self.y2)
    
    def intersects(self, other: RectangularRoom) -> bool:
        """ Return True if this room overlaps with another RectangularRoom. """
        return (
            self.x1 <= other.x2
            and self.x2 >= other.x1
            and self.y1 <= other.y2
            and self.y2 >= other.y1
        )
    
def place_entities(
        room: RectangularRoom, dungeon: GameMap, maximum_monsters: int
) -> None:
    number_of_monsters = random.randint(0, maximum_monsters)

    for i in range(number_of_monsters):
        x = random.randint(room.x1 + 1, room.x2 - 1)
        y = random.randint(room.y1 + 1, room.y2 - 1)

        if not any(entity.x == x and entity.y == y for entity in dungeon.entities):
            if random.random() < 0.8:
                entities_factory.orc.spawn(dungeon, x, y)
            else:
                entities_factory.troll.spawn(dungeon, x, y)


def tunnel_between(
        start: Tuple[int, int], end: Tuple[int, int]
) -> Iterator[Tuple[int, int]]:
    x1, y1 = start
    x2, y2 = end
    if random.random() < 0.5: # 50% chance
        # Move horizontally then vertically
        corner_x, corner_y = x2, y1
    else:
        # Mover vertically then horizontally
        corner_x, corner_y = x1, y2
    
    # Generate the coordinates for the tunnel
    for x, y in tcod.los.bresenham((x1, y1), (corner_x, corner_y)).tolist():
        yield x, y
    for x, y in tcod.los.bresenham((corner_x, corner_y), (x2, y2)).tolist():
        yield x, y

def generate_dungeon(
        max_rooms: int,
        room_min_size: int,
        room_max_size: int,
        map_width: int,
        map_height: int,
        player: Entity,
        max_enemies_per_room:int
) -> GameMap:
    dungeon = GameMap(map_width, map_height, entities=[player])

    rooms: List[RectangularRoom] = []

    for r in range(max_rooms):
        room_width = random.randint(room_min_size, room_max_size)
        room_height = random.randint(room_min_size, room_max_size)

        x = random.randint(0, dungeon.width - room_width - 1)
        y = random.randint(0, dungeon.height - room_height - 1)

        new_room = RectangularRoom(x, y, room_width, room_height)

        # Check if any existing room instersects with the new one
        if any(new_room.intersects(other_room) for other_room in rooms):
            continue # Rooms intersects so we skip it
        # If there's no intersection, we can continue
        dungeon.tiles[new_room.inner] = tile_types.floor

        if len(rooms) == 0:
            # The first room, where the player starts
            player.x, player.y = new_room.center
        else: 
            # We carve a tunnel as well with the previous room
            for x, y in tunnel_between(rooms[-1].center, new_room.center):
                dungeon.tiles[x, y] = tile_types.floor

        place_entities(new_room, dungeon, max_enemies_per_room)
        rooms.append(new_room)

    return dungeon