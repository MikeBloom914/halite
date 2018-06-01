import hlt
import logging
import os
from collections import OrderedDict

try:
    os.remove("_1SheckyBot5")
    os.remove("_0SheckyBot5")
except:
    pass

game = hlt.Game("SheckyBot5")
logging.info("Go Shecky bot")


def largest_dockable_planet(plan):
    logging.info("test" + str(plan))
    if plan:
        return max([planet for planet in plan if not planet.is_owned()], key=lambda x: x.radius)
    else:
        return None


turn_num = 0

while True:
    game_map = game.update_map()
    command_queue = []

    my_ships = game_map.get_me().all_ships()
    my_id = game_map.get_me().id
    for ship in game_map.get_me().all_ships():
        shipid = ship.id
        if ship.docking_status != ship.DockingStatus.UNDOCKED:
            continue

        entities_by_distance = game_map.nearby_entities_by_distance(ship)
        entities_by_distance = OrderedDict(sorted(entities_by_distance.items(), key=lambda x: x[0]))

        closest_empty_planets = [entities_by_distance[distance][0] for distance in entities_by_distance if isinstance(entities_by_distance[distance][0], hlt.entity.Planet) and not entities_by_distance[distance][0].is_owned()]

        closest_owned_planets = [entities_by_distance[distance][0] for distance in entities_by_distance if isinstance(entities_by_distance[distance][0], hlt.entity.Planet) and entities_by_distance[distance][0].is_owned()]
        my_planets = []
### have bots chase me when they get to a certain distance ###
### can do distance to coordinates for diff coordinance ###
        for planet in closest_owned_planets:
            if planet.owner.id == my_id:
                my_planets.append(planet)

        my_planets_not_full = []

        for planet in my_planets:
            if not planet.is_full():
                my_planets_not_full.append(planet)

        enemy_planets_not_full = []

        for planet in closest_owned_planets:
            if planet.owner.id != my_id:
                if not planet.is_full():
                    enemy_planets_not_full.append(planet)

        enemy_planets_owned = []
        for planet in closest_owned_planets:
            if planet.owner.id != my_id:
                enemy_planets_owned.append(planet)

        logging.info("turn number: {}".format(turn_num))
        logging.info("len of my_planets: " + str(len(my_planets)))
        logging.info("len of my_planets_not_full: " + str(len(my_planets_not_full)))
        logging.info("enemy_planets_not_full: " + str(len(enemy_planets_not_full)))

        closest_enemy_ships = [entities_by_distance[distance][0] for distance in entities_by_distance if isinstance(entities_by_distance[distance][0], hlt.entity.Ship) and entities_by_distance[distance][0] not in my_ships]

        if turn_num <= 12:
            if len(my_planets) <= 2:
                target_planet = largest_dockable_planet(closest_empty_planets)
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
            else:
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

        elif 12 < turn_num <= 80:
            if len(closest_empty_planets) >= 3:
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

            else:
                target_ship = closest_enemy_ships[0]
                navigate_command = ship.navigate(
                    ship.closest_point_to(target_ship),
                    game_map,
                    speed=int(hlt.constants.MAX_SPEED),
                    ignore_ships=False)

                if navigate_command:
                    command_queue.append(navigate_command)

        elif 50 < turn_num <= 90:
            if len(enemy_planets_not_full) <= len(my_planets_not_full):
                target_planet = enemy_planets_not_full[0]
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

            else:
                target_ship = closest_enemy_ships[0]
                navigate_command = ship.navigate(
                    ship.closest_point_to(target_ship),
                    game_map,
                    speed=int(hlt.constants.MAX_SPEED),
                    ignore_ships=False)

                if navigate_command:
                    command_queue.append(navigate_command)

        elif 120 > turn_num > 90:
            if len(closest_empty_planets) > 1:
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

            else:
                target_ship = closest_enemy_ships[0]
                navigate_command = ship.navigate(
                    ship.closest_point_to(target_ship),
                    game_map,
                    speed=int(hlt.constants.MAX_SPEED),
                    ignore_ships=False)

                if navigate_command:
                    command_queue.append(navigate_command)

        else:
            target_ship = closest_enemy_ships[0]
            navigate_command = ship.navigate(
                ship.closest_point_to(target_ship),
                game_map,
                speed=int(hlt.constants.MAX_SPEED),
                ignore_ships=False)

            if navigate_command:
                command_queue.append(navigate_command)

    turn_num += 1
    game.send_command_queue(command_queue)
    #  turn over
# game over
