import hlt
import logging
import os
from collections import OrderedDict

try:
    os.remove("_1SheckyBotktest")
    os.remove("_0SheckyBot")
except:
    pass

game = hlt.Game("SheckyBotktest'")
logging.info("Go Shecky bot")


def largest_dockable_planet(planets):
    if planets:
        return max([planet for planet in planets if not planet.is_owned()], key=lambda x: x.radius)
    else:
        return None


def docking(target_planet, less_than):
    if target_planet:
        if ship.can_dock(target_planet):
            command_queue.append(ship.dock(target_planet))
        else:
            navigate_command = ship.navigate(
                ship.closest_point_to(target_planet),
                game_map,
                speed=int(hlt.constants.MAX_SPEED + less_than),
                ignore_ships=False)
            if navigate_command:
                command_queue.append(navigate_command)


def navigate_ship(target_ship):
    navigate_command = ship.navigate(
        ship.closest_point_to(target_ship),
        game_map,
        speed=int(hlt.constants.MAX_SPEED),
        ignore_ships=False)

    if navigate_command:
        command_queue.append(navigate_command)


turn_num = 0

#### Quadrant Centers of Map ####
TopL = hlt.entity.Position(60, 40)
TopR = hlt.entity.Position(180, 40)
BotR = hlt.entity.Position(180, 120)
BotL = hlt.entity.Position(60, 120)
center = hlt.entity.Position(120, 80)


Corners = [TopL, TopR, BotL, BotR]

while True:
    game_map = game.update_map()
    my_id = game_map.get_me().id
    my_ships = game_map.get_me().all_ships()
    all_planets = game_map.all_planets()
    outside_planets = [planet for planet in all_planets if planet.id > 3]

    command_queue = []
    # for planet in all_planets:
    #     logging.info('{} {}'.format(planet.id, planet.get_remaining_resources()))

    for ship in my_ships:
        shipid = ship.id

        if ship.docking_status != ship.DockingStatus.UNDOCKED:
            # continue
            #
            # State: the ship is undocked
            #
            if ship.get_planet() != None:
                # logging.info('{}'.format(ship.get_planet()))
                #
                # State: the ship is docked on a planet with a globally unique identifier
                #
                for planet in all_planets:
                    # logging.info('planet id: {}'.format(planet.id))
                    logging.info('planet_id: {}'.format(planet.id))
                    logging.info('type(planet_id): {}'.format(type(planet.id)))

                    logging.info('ship_id: {}'.format(ship.get_planet().id))
                    logging.info('type(ship_id): {}'.format(type(ship.get_planet().id)))
                    # FIXME ship.get_planet returns a weird type (hlt.entity.Planet),
                    # but we only want the id of the planet so the following control flow
                    # behaves as expected.
                    if planet.id == ship.get_planet().id:
                        #
                        # Desired State: the value of the iterator is equal to the value of the
                        #                globally unique identifier that the ship is docked on
                        #
                        logging.info('planet id equals ship get planet')
                        if planet.get_remaining_resources() <= 100:
                            command_queue.append(ship.undock())
                            logging.info('{} {}'.format(planet.id, planet.get_remaining_resources()))

                            logging.info('undocking' + str(turn_num))
                            # navigate_ship(closest_enemy_ships[0])

            else:
                continue

                #

        entities_by_distance = game_map.nearby_entities_by_distance(ship)
        entities_by_distance = OrderedDict(sorted(entities_by_distance.items(), key=lambda x: x[0]))

    ### Ship info ###

        my_undocked_ships = [ship for ship in my_ships if ship.docking_status == ship.DockingStatus.UNDOCKED]
        my_docked_ships = [ship for ship in my_ships if ship.docking_status == ship.DockingStatus.DOCKED]

        closest_enemy_ships = [entities_by_distance[distance][0] for distance in entities_by_distance if isinstance(entities_by_distance[distance][0], hlt.entity.Ship) and entities_by_distance[distance][0] not in my_ships]

    ### Planet info ###
        closest_empty_planets = [entities_by_distance[distance][0] for distance in entities_by_distance if isinstance(entities_by_distance[distance][0], hlt.entity.Planet) and not entities_by_distance[distance][0].is_owned()]

        closest_owned_planets = [entities_by_distance[distance][0] for distance in entities_by_distance if isinstance(entities_by_distance[distance][0], hlt.entity.Planet) and entities_by_distance[distance][0].is_owned()]

        my_planets = [planet for planet in closest_owned_planets if planet.owner.id == my_id]
        my_planets_full = [planet for planet in my_planets if planet.is_full()]
        my_planets_not_full = [planet for planet in my_planets if not planet.is_full()]

        enemy_planets = [planet for planet in closest_owned_planets if planet.owner.id != my_id]
        enemy_planets_not_full = [planet for planet in enemy_planets if not planet.is_full()]

        closest_planets = [entities_by_distance[distance][0] for distance in entities_by_distance if isinstance(entities_by_distance[distance][0], hlt.entity.Planet)]
        closest_outside_planets = [planet for planet in closest_planets if planet.id > 3]

        distance_between_my_ship_and_enemy_ship = ship.calculate_distance_between(closest_enemy_ships[0])

        ##### GAME TIME #####
        ##### I pretty much tested out every theory with every list in every order that I could think of...easily spend over a week just testing that out and came up with this final answer as winning the most #####

        if turn_num <= 6 and len(my_ships) > len(closest_enemy_ships) + 2:
            navigate_ship(closest_enemy_ships[0])

        else:
            if len(my_planets_not_full) > 0 and len(closest_enemy_ships) > 0:

                distance_between_my_ship_and_enemy_ship = ship.calculate_distance_between(closest_enemy_ships[0])

                distance_between_my_ship_and_my_planet_not_full = ship.calculate_distance_between(my_planets_not_full[0])

                if distance_between_my_ship_and_enemy_ship < 18:
                    navigate_ship(closest_enemy_ships[0])
                else:
                    docking(my_planets_not_full[0], 0)

            elif len(closest_empty_planets) > 0 and len(closest_enemy_ships) > 0:
                if ship.can_dock(closest_empty_planets[0]):
                    command_queue.append(ship.dock(closest_empty_planets[0]))
                    continue

                distance_between_my_ship_and_empty_planet = ship.calculate_distance_between(closest_empty_planets[0])

                distance_between_my_ship_and_outside_planet = ship.calculate_distance_between(closest_outside_planets[0])

                if distance_between_my_ship_and_enemy_ship < distance_between_my_ship_and_empty_planet * .6:
                    navigate_ship(closest_enemy_ships[0])

                else:
                    docking(closest_empty_planets[0], 0)

            elif len(closest_enemy_ships) > 0:
                navigate_ship(closest_enemy_ships[0])
    logging.info("turn_num: " + str(turn_num))
    turn_num += 1
    logging.info("Turn: " + str(turn_num))
    game.send_command_queue(command_queue)

    #  turn over
# game over

##################WHEN DONE THROW IN A BUNCH OF RANDOM STUFF TO THROW OTHER PEOPLE OFF, IE VARIABLES,################
  ######################################FUUNCTIONS, COMMENTS SAYING HOW IMPORT IT IS #########################################

    #         ### have bots chase me when there are x amount of ships ###
    #         ### can do distance to coordinates for diff coordinance ###

    ### Make sure starting ships do not crash ###

    ### After starting ships start to make more ships ###
