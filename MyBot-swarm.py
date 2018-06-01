import hlt
import logging
from collections import OrderedDict

game = hlt.Game("testBot")
logging.info("Go test bot")


def largest_dockable_planet(planets):
    if planets:
        return max([planet for planet in planets if not planet.is_owned()], key=lambda x: x.radius)
    else:
        return None


my_planets = []


def my_owned_planets(planets):
    for planet in largest_dockable_planet():
        if planet.is_owned().get_me():
            my_planets.append(planet)


while True:
    game_map = game.update_map()
    command_queue = []

    team_ships = game_map.get_me().all_ships()

    for ship in game_map.get_me().all_ships():
        shipid = ship.id
        if ship.docking_status != ship.DockingStatus.UNDOCKED:
            continue

        entities_by_distance = game_map.nearby_entities_by_distance(ship)
        entities_by_distance = OrderedDict(sorted(entities_by_distance.items(), key=lambda x: x[0]))

        closest_empty_planets = [entities_by_distance[distance][0] for distance in entities_by_distance if isinstance(entities_by_distance[distance][0], hlt.entity.Planet) and not entities_by_distance[distance][0].is_owned()]

        closest_enemy_ships = [entities_by_distance[distance][0] for distance in entities_by_distance if isinstance(entities_by_distance[distance][0], hlt.entity.Ship) and entities_by_distance[distance][0] not in team_ships]
        if len(my_planets) <= len(closest_empty_planets):
            # if len(closest_empty_planets) >= 6:
            target_planet = largest_dockable_planet(closest_empty_planets)
            if target_planet:
                if ship.can_dock(target_planet):
                    command_queue.append(ship.dock(target_planet))
                else:
                    navigate_command = ship.navigate(
                        ship.closest_point_to(target_planet),
                        game_map,
                        speed=int(hlt.constants.MAX_SPEED),
                        ignore_ships=True)
                    if navigate_command:
                        command_queue.append(navigate_command)
        # elif len(my_planets) <= len(closest_empty_planets):
        #     # elif len(closest_empty_planets) == 5:
        #     target_planet = closest_empty_planets[0]
        #     if target_planet:
        #         if ship.can_dock(target_planet):
        #             command_queue.append(ship.dock(target_planet))
        #         else:
        #             navigate_command = ship.navigate(
        #                 ship.closest_point_to(target_planet),
        #                 game_map,
        #                 speed=int(hlt.constants.MAX_SPEED),
        #                 ignore_ships=False)
        #             if navigate_command:
        #                 command_queue.append(navigate_command)

        # elif len(closest_empty_planets) == 3:
        #     target_planet = closest_empty_planets[0]
        #     if target_planet:
        #         if ship.can_dock(target_planet):
        #             command_queue.append(ship.dock(target_planet))
        #         else:
        #             navigate_command = ship.navigate(
        #                 ship.closest_point_to(target_planet),
        #                 game_map,
        #                 speed=int(hlt.constants.MAX_SPEED),
        #                 ignore_ships=False)
        #             if navigate_command:
        #                 command_queue.append(navigate_command)

        elif len(closest_enemy_ships) > 0:
            target_ship = closest_enemy_ships[0]
            navigate_command = ship.navigate(
                ship.closest_point_to(target_ship),
                ### to destroy a planet have ship.(through the planet) ###
                game_map,
                speed=int(hlt.constants.MAX_SPEED),
                ignore_ships=False)

            if navigate_command:
                command_queue.append(navigate_command)

    game.send_command_queue(command_queue)
    #  turn over
# game over
