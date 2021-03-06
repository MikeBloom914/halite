import hlt
import logging
import os
from collections import OrderedDict
######Made two lists of ships to do two different things at the same time#####

game = hlt.Game("SheckyBotv2_split")
logging.info("Go Shecky bot")


def largest_dockable_planet(plan):
    # logging.info("test" + str(plan))
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
    for ship in my_ships:
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

        my_planets_full = []

        for planet in my_planets:
            if planet.is_full():
                my_planets_full.append(planet)

        enemy_planets_not_full = []

        for planet in closest_owned_planets:
            if planet.owner.id != my_id:
                if not planet.is_full():
                    enemy_planets_not_full.append(planet)

        enemy_planets_owned = []
        for planet in closest_owned_planets:
            if planet.owner.id != my_id:
                enemy_planets_owned.append(planet)

        closest_enemy_ships = [entities_by_distance[distance][0] for distance in entities_by_distance if isinstance(entities_by_distance[distance][0], hlt.entity.Ship) and entities_by_distance[distance][0] not in my_ships]

        if len(my_ships) <= 3:
            if len(closest_empty_planets) > 0:
                if shipid % 2 == 0:
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
                        continue

                elif shipid % 2 != 0:
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
                        continue

            elif len(closest_enemy_ships) > 0:
                target_ship = closest_enemy_ships[0]
                navigate_command = ship.navigate(
                    ship.closest_point_to(target_ship),
                    game_map,
                    speed=int(hlt.constants.MAX_SPEED),
                    ignore_ships=False)

                if navigate_command:
                    command_queue.append(navigate_command)

        elif len(my_ships) > 3:
            if len(my_ships) > len(closest_enemy_ships) + 2:
                target_ship = closest_enemy_ships[0]
                navigate_command = ship.navigate(
                    ship.closest_point_to(target_ship),
                    game_map,
                    speed=int(hlt.constants.MAX_SPEED),
                    ignore_ships=False)

                if navigate_command:
                    command_queue.append(navigate_command)

            elif len(my_ships) <= len(closest_enemy_ships) + 2:
                if len(closest_empty_planets) >= 6:
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

                    # elif len(closest_enemy_ships) > 0:
                    #     target_ship = closest_enemy_ships[0]
                    #     navigate_command = ship.navigate(
                    #         ship.closest_point_to(target_ship),
                    #         game_map,
                    #         speed=int(hlt.constants.MAX_SPEED / 1.25),
                    #         ignore_ships=False)

                    #     if navigate_command:
                    #         command_queue.append(navigate_command)

                elif len(closest_empty_planets) == 5:
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
                elif len(closest_empty_planets) == 1:
                    target_planet = closest_empty_planets[0]
                    if target_planet:
                        if ship.can_dock(target_planet):
                            command_queue.append(ship.dock(target_planet))
                        else:
                            navigate_command = ship.navigate(
                                ship.closest_point_to(target_planet),
                                game_map,
                                speed=int(hlt.constants.MAX_SPEED / 1.5),
                                ignore_ships=False)
                            if navigate_command:
                                command_queue.append(navigate_command)
                elif len(closest_enemy_ships) > 0:
                    target_ship = closest_enemy_ships[0]
                    navigate_command = ship.navigate(
                        ship.closest_point_to(target_ship),
                        game_map,
                        speed=int(hlt.constants.MAX_SPEED),
                        ignore_ships=False)

                    if navigate_command:
                        command_queue.append(navigate_command)

            elif len(closest_enemy_ships) > 0:
                target_ship = closest_enemy_ships[0]
                navigate_command = ship.navigate(
                    ship.closest_point_to(target_ship),
                    game_map,
                    speed=int(hlt.constants.MAX_SPEED),
                    ignore_ships=False)

                if navigate_command:
                    command_queue.append(navigate_command)
    #####
    turn_num += 1
    game.send_command_queue(command_queue)
    #  turn over
# game over
