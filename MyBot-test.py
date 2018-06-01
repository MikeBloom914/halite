import hlt
import logging
from collections import OrderedDict
import os

try:
    os.remove("1_testBot.log")
except:
    pass

game = hlt.Game("testBot")
logging.info("Go test bot")


def largest_dockable_planet(planets):
    if planets:
        return max([planet for planet in planets if not planet.is_owned()], key=lambda x: x.radius)
    else:
        return None


turn_num = 0

while True:
    game_map = game.update_map()
    command_queue = []

    team_ships = game_map.get_me().all_ships()
    my_id = game_map.get_me().id

    for ship in game_map.get_me().all_ships():
        turn_num += 1
        shipid = ship.id
        if ship.docking_status != ship.DockingStatus.UNDOCKED:
            continue

        entities_by_distance = game_map.nearby_entities_by_distance(ship)
        entities_by_distance = OrderedDict(sorted(entities_by_distance.items(), key=lambda x: x[0]))

        closest_empty_planets = [entities_by_distance[distance][0] for distance in entities_by_distance if isinstance(entities_by_distance[distance][0], hlt.entity.Planet) and not entities_by_distance[distance][0].is_owned()]

        closest_owned_planets = [entities_by_distance[distance][0] for distance in entities_by_distance if isinstance(entities_by_distance[distance][0], hlt.entity.Planet) and entities_by_distance[distance][0].is_owned()]

        my_planets = []

        for planet in closest_owned_planets:
            if planet.owner.id == my_id:
                my_planets.append(planet)

        my_planets_not_full = []

        closest_enemy_ships = [entities_by_distance[distance][0] for distance in entities_by_distance if isinstance(entities_by_distance[distance][0], hlt.entity.Ship) and entities_by_distance[distance][0] not in team_ships]

        if len(my_planets) <= len(closest_empty_planets) and len(closest_enemy_ships) > 0:

            logging.info("turn number: {}".format(turn_num))
            logging.info("len of list: " + str(len(my_planets)))

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
        elif len(closest_empty_planets):
            target_planet = closest_empty_planets[0]
            if target_planet:
                if ship.can_dock(target_planet):
                    command_queue.append(ship.dock(target_planet))
                else:
                    navigate_command = ship.navigate(
                        ship.closest_point_to(target_planet),
                        game_map,
                        speed=int(hlt.constants.MAX_SPEED),
                        ignore_ships=False)
                    if navigate_command:
                        command_queue.append(navigate_command)

        # elif len(my_planets) <= len(closest_empty_planets):
        # elif len(closest_empty_planets) == 5:
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
        # elif 3 > len(closest_empty_planets) >= 0:

        elif len(closest_enemy_ships) > 0:
            target_ship = closest_enemy_ships[0]
            navigate_command = ship.navigate(
                ship.closest_point_to(target_ship),
                game_map,
                speed=int(hlt.constants.MAX_SPEED),
                ignore_ships=False)

            if navigate_command:
                command_queue.append(navigate_command)

    game.send_command_queue(command_queue)
    #  turn over
# game over
