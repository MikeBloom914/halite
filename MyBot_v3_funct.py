import hlt
import logging
from collections import OrderedDict

game = hlt.Game("SheckyBot_v3funct")
logging.info("Go Shecky bot")

#### TO DO. ADD GOING TO VULNERABLE PLANETS AND TEAM STUFF####


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

    players = game_map.all_players()
    if len(players) == 2:
        my_team_ships = my_ships
        team_mate_id = my_id
    else:
        team_mate_id = None
        if my_id == 0 or my_id == 1:
            team_mate_id = my_id + 2
        elif my_id == 2 or my_id == 3:
            team_mate_id = my_id - 2

        team_mate_ships = game_map.get_player(team_mate_id).all_ships()
        my_team_ships = my_ships + team_mate_ships

    # logging.info("my id:" + str(my_id))
    # logging.info("teamid:" + str(team_mate_id))
    # logging.info("my ships:" + str(len(my_ships)))
    # logging.info("teamships: " + str(len(team_mate_ships)))
    # logging.info("myteam" + str(len(my_team_ships)))

    command_queue = []

    for ship in my_ships:
        shipid = ship.id

        if ship.docking_status != ship.DockingStatus.UNDOCKED:
            continue

        entities_by_distance = game_map.nearby_entities_by_distance(ship)
        entities_by_distance = OrderedDict(sorted(entities_by_distance.items(), key=lambda x: x[0]))

    ### Ship info ###

        my_undocked_ships = [ship for ship in my_ships if ship.docking_status == ship.DockingStatus.UNDOCKED]
        my_docked_ships = [ship for ship in my_ships if ship.docking_status == ship.DockingStatus.DOCKED]

        closest_enemy_ships = [entities_by_distance[distance][0] for distance in entities_by_distance if isinstance(entities_by_distance[distance][0], hlt.entity.Ship) and entities_by_distance[distance][0] not in my_team_ships]

    ### Planet info ###
        closest_empty_planets = [entities_by_distance[distance][0] for distance in entities_by_distance if isinstance(entities_by_distance[distance][0], hlt.entity.Planet) and not entities_by_distance[distance][0].is_owned()]

        closest_owned_planets = [entities_by_distance[distance][0] for distance in entities_by_distance if isinstance(entities_by_distance[distance][0], hlt.entity.Planet) and entities_by_distance[distance][0].is_owned()]

        my_planets = [planet for planet in closest_owned_planets if planet.owner.id == my_id]
        my_planets_full = [planet for planet in my_planets if planet.is_full()]
        my_planets_not_full = [planet for planet in my_planets if not planet.is_full()]

        my_team_planets = [planet for planet in closest_owned_planets if planet.owner.id == my_id or planet.owner.id == team_mate_id]

        enemy_planets = [planet for planet in closest_owned_planets if planet.owner.id != my_id or planet.owner.id != team_mate_id]

        vulnerable_enemy_planets = [planet for planet in enemy_planets if len(planet.all_docked_ships()) == 1]

        vulnerable_enemy_ships = [ship for ship in vulnerable_enemy_planets]

        logging.info("vul:" + str(len(vulnerable_enemy_planets)))
        #     continue

        closest_planets = [entities_by_distance[distance][0] for distance in entities_by_distance if isinstance(entities_by_distance[distance][0], hlt.entity.Planet)]
        closest_outside_planets = [planet for planet in closest_planets if planet.id > 3]

        distance_between_my_ship_and_enemy_ship = ship.calculate_distance_between(closest_enemy_ships[0])

        ##### GAME TIME #####
        ##### I pretty much tested out every theory with every list in every order that I could think of...easily spend over a week just testing that out and came up with this final answer as winning the most #####

        if turn_num <= 6 and len(my_ships) > len(closest_enemy_ships) + 2:
            navigate_ship(closest_enemy_ships[0])
            #logging.info("myships: " + str(my_id))
            #logging.info("team_ships: " + str(team_ship))

        else:
            if len(my_planets_not_full) > 0 and len(closest_enemy_ships) > 0:

                distance_between_my_ship_and_enemy_ship = ship.calculate_distance_between(closest_enemy_ships[0])

                distance_between_my_ship_and_my_planet_not_full = ship.calculate_distance_between(my_planets_not_full[0])

                if distance_between_my_ship_and_enemy_ship < 18:
                    navigate_ship(closest_enemy_ships[0])
                    logging.info("kill close ship:")
                else:
                    docking(my_planets_not_full[0], 0)
                    logging.info("fillerUp:")

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
