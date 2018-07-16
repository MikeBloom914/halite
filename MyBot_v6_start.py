import hlt
import logging
from collections import OrderedDict

game = hlt.Game("The Abyss_v6_start")
logging.info("Go Abyss bot")

#### TO DO ADD GOING TO VULNERABLE PLANETS AND TEAM STUFF####
### ADD VIABLE PLANETS TO ALL PLANETS LISTS NECESSARY###

# This function gets list of planets in order of size by radius starting with the max #


def largest_dockable_planet(planets):
    if planets:
        return max([planet for planet in planets if not planet.is_owned()], key=lambda x: x.radius)
    else:
        return None


#This fuction is used when I want to travel to/ dock on a planet.  I also gave the option of using a speed less than the constant max#

def docking(target_planet, less_than):
    # if target_planet.get_remaining_resources() != 0:
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

#This funciton navigates my ship to where I want it to#


def navigate_ship(target_ship, less_than):
    navigate_command = ship.navigate(
        ship.closest_point_to(target_ship),
        game_map,
        speed=int(hlt.constants.MAX_SPEED + less_than),
        max_corrections=21,
        angular_step=2,
        ignore_ships=False)

    if navigate_command:
        command_queue.append(navigate_command)


def distance(target_one, target_two):
    distance = target_one.calculate_distance_between(target_two)
    return distance


turn_num = 0

#### Quadrant Centers of Map ####
TopL = hlt.entity.Position(60, 40)
TopR = hlt.entity.Position(180, 40)
BotR = hlt.entity.Position(180, 120)
BotL = hlt.entity.Position(60, 120)
center = hlt.entity.Position(120, 80)

#### CORNERS OF MAP ####
tlc = hlt.entity.Position(1, 1)
trc = hlt.entity.Position(239, 1)
brc = hlt.entity.Position(239, 159)
blc = hlt.entity.Position(1, 159)

Corners = [tlc, trc, brc, blc]

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

    # logging.info(type(my_id))
    # logging.info(type(team_mate_id))
    # logging.info(type(my_team_ships))
    # logging.info(type(team_mate_ships))

    # logging.info("my id:" + str(my_id))
    # logging.info("team_mate_id:" + str(team_mate_id))
    # logging.info("my ships:" + str(len(my_ships)))
    # logging.info("team_mate_ships: " + str(len(team_mate_ships)))
    # logging.info("my_team_ships" + str(len(my_team_ships)))
    # logging.info("team_mate_ships:" + str(team_mate_ships))
    # logging.info("my_team_ships:" + str(my_team_ships))
    command_queue = []

    entities = {}
    for ship in my_ships:
        # entities[ship.id] = {'state': ship.docking_status}
        if ship.docking_status != ship.DockingStatus.UNDOCKED:
            if ship.planet.remaining_resources == 0:
                command_queue.append(ship.undock())
                logging.info('undocking' + str(turn_num))

            else:
                continue

        else:
            entities_by_distance = game_map.nearby_entities_by_distance(ship)
            entities_by_distance = OrderedDict(sorted(entities_by_distance.items(), key=lambda x: x[0]))

            closest_owned_planets = [entities_by_distance[distance][0] for distance in entities_by_distance if isinstance(entities_by_distance[distance][0], hlt.entity.Planet) and entities_by_distance[distance][0].is_owned()]

            my_planets = [planet for planet in closest_owned_planets if planet.owner.id == my_id]
            my_planets_full = [planet for planet in my_planets if planet.is_full()]
            my_planets_not_full = [planet for planet in my_planets if not planet.is_full()]

            ### Ship info ###

            my_undocked_ships = [ship for ship in my_ships if ship.docking_status == ship.DockingStatus.UNDOCKED]
            my_defenseless_ships = [ship for ship in my_ships if ship.docking_status != ship.DockingStatus.UNDOCKED]

            closest_enemy_ships = [entities_by_distance[distance][0] for distance in entities_by_distance if isinstance(entities_by_distance[distance][0], hlt.entity.Ship) and entities_by_distance[distance][0] not in my_team_ships]

            enemy_defenseless_ships = [ship for ship in closest_enemy_ships if ship.docking_status != ship.DockingStatus.UNDOCKED]

        ### Planet info ###
            closest_empty_planets = [entities_by_distance[distance][0] for distance in entities_by_distance if isinstance(entities_by_distance[distance][0], hlt.entity.Planet) and not entities_by_distance[distance][0].is_owned()]

            closest_empty_viable_planets = [planet for planet in closest_empty_planets if planet.get_remaining_resources() != 0]

            enemy_planets = [planet for planet in closest_owned_planets if planet.owner.id != my_id or planet.owner.id != team_mate_id]

            vulnerable_enemy_planets = [planet for planet in enemy_planets if len(planet.all_docked_ships()) == 1]

            vulnerable_enemy_ships = [ship for ship in vulnerable_enemy_planets]

            closest_planets = [entities_by_distance[distance][0] for distance in entities_by_distance if isinstance(entities_by_distance[distance][0], hlt.entity.Planet)]

            closest_outside_planets = [planet for planet in closest_empty_viable_planets if planet.id > 3]

            ##### GAME TIME #####
            ##### I pretty much tested out every theory with every list in every order that I could think of...easily spend over a week just testing that out and came up with this final answer as winning the most #####

            if turn_num <= 7:
                if ship.id == 0 or ship.id == 5 or ship.id == 10 or ship.id == 15:
                    docking(closest_empty_viable_planets[0], -2)
                if ship.id == 1 or ship.id == 6 or ship.id == 11 or ship.id == 16:
                    docking(closest_empty_viable_planets[0], -1)
                if ship.id == 2 or ship.id == 7 or ship.id == 12 or ship.id == 17:
                    docking(closest_empty_viable_planets[0], 0)
                if ship.id == 3 or ship.id == 8 or ship.id == 13 or ship.id == 18:
                    docking(closest_empty_viable_planets[0], -1)
                if ship.id == 4 or ship.id == 9 or ship.id == 14 or ship.id == 19:
                    docking(largest_dockable_planet(closest_outside_planets), 0)

            else:

                if len(enemy_defenseless_ships) > 0 and len(my_undocked_ships) > len(enemy_defenseless_ships):
                    navigate_ship(enemy_defenseless_ships[0], 0)

                else:
                    if len(my_planets_not_full) > 0:
                        if len(closest_enemy_ships) > 0:

                            if distance(ship, closest_enemy_ships[0]) < 18:

                                navigate_ship(closest_enemy_ships[0], 0)
                                # logging.info("kill close ship")
                                continue
                            else:
                                if ship.can_dock(my_planets_not_full[0]):
                                    command_queue.append(ship.dock(my_planets_not_full[0]))
                                    # logging.info("dock unfull planet")
                                    continue
                            # logging.info("myships: " + str(my_id))
                            # logging.info("team_ships: " + str(team_ship))

                    if len(closest_empty_viable_planets) > 0:
                        if len(closest_enemy_ships) > 0:
                            if ship.can_dock(closest_empty_viable_planets[0]):
                                command_queue.append(ship.dock(closest_empty_viable_planets[0]))
                                # logging.info("dock empty planet")
                                continue

                            else:
                                if distance(ship, closest_enemy_ships[0]) <= (distance(ship, closest_empty_viable_planets[0]) * .4):
                                    navigate_ship(closest_enemy_ships[0], 0)
                                    # logging.info("getting en ship")

                                else:
                                    navigate_ship(closest_empty_viable_planets[0], 0)
                                    # logging.info("go to empty planet")

                    elif len(closest_enemy_ships) > 0:
                        # if len(vulnerable_enemy_planets) > 0:
                        if len(vulnerable_enemy_ships) > 0:
                            if distance(ship, closest_enemy_ships[0]) < 18:

                                navigate_ship(closest_enemy_ships[0], 0)
                                # logging.info("kill close ship")
                                continue
                            # if distance(ship, vulnerable_enemy_planets[0]) < distance(ship, closest_enemy_ships[0]):
                            if distance(ship, vulnerable_enemy_ships[0]) < distance(ship, closest_enemy_ships[0]) * .4:
                                navigate_ship(vulnerable_enemy_ships[0], 0)
                                logging.info("vulnerable_enemy_ships")
                            else:
                                navigate_ship(closest_enemy_ships[0], 0)
                                # logging.info("kill all ships!")

    # logging.info("Ship IDs: " + str([_.split(' ')[1] for _ in command_queue]))
    # logging.info("Command Q: " + str(command_queue))
    turn_num += 1
    logging.info("Turn: " + str(turn_num))
    game.send_command_queue(command_queue)

    #  turn over
# game over

    ### Make sure starting ships do not crash ###

    ### After starting ships start to make more ships ###
