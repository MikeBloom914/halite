"""
Welcome to your first Halite-II bot!

This bot's name is Settler. It's purpose is simple (don't expect it to win complex games :) ):
1. Initialize game
2. If a ship is not docked and there are unowned planets
2.a. Try to Dock in the planet if close enough
2.b If not, go towards the planet

Note: Please do not place print statements here as they are used to communicate with the Halite engine. If you need
to log anything use the logging module.
"""
# Let's start by importing the Halite Starter Kit so we can interface with the Halite engine
import hlt
# Then let's import the logging module so we can print out information
import logging


def largest_dockable_planet(planets):
    if planets:
        return max([planet for planet in planets if not planet.is_owned()], key=lambda x: x.radius)
    return None


def entitiy_is_viable(entity):
    return isinstance(entity, hlt.entity.Planet) and not entity.is_owned()


def nearest_dockable_planet(entities_by_distance):
    for distance in sorted(entities_by_distance.keys()):
        nearest_planet = next((nearest_entity for nearest_entity in entities_by_distance[distance] if entity_is_viable(nearest_entity)))
        if nearest_planet:
            return nearest_planet


# GAME START
# Here we define the bot's name as Settler and initialize the game, including communication with the Halite engine.
game = hlt.Game("CloseFinder")
# Then we print our start message to the logs
logging.info("Starting my CloseFinder bot!")

while True:
    # TURN START
    game_map = game.update_map()

    command_queue = []
    for ship in game_map.get_me().all_ships():
        if ship.docking_status != ship.DockingStatus.UNDOCKED:
            continue

        entities_by_distance = game_map.nearby_entities_by_distance(ship)
        nearest_planet = nearest_dockable_planet(entities_by_distance)
        if nearest_planet:
            if ship.can_dock(nearest_planet):
                command_queue.append(ship.dock(nearest_planet))
            else:
                navigate_command = ship.navigate(
                    ship.closest_point_to(nearest_planet),
                    ### to destroy a planet have ship.(through the planet) ###
                    game_map,
                    speed=int(hlt.constants.MAX_SPEED),
                    ignore_ships=False)
                if navigate_command:
                    command_queue.append(navigate_command)
            break

    # Send our set of commands to the Halite engine for this turn
    game.send_command_queue(command_queue)
    # TURN END
# GAME END
