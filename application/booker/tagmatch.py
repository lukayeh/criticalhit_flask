import random
from random import randint
from unicodedata import name
from colorama import Fore, Back, Style


def findkeys(node, kv):
    if isinstance(node, list):
        for i in node:
            for x in findkeys(i, kv):
                yield x
    elif isinstance(node, dict):
        if kv in node:
            yield node[kv]
        for j in node.values():
            for x in findkeys(j, kv):
                yield x


class Booker:
    def __init__(self, participants, bonuses, moves):

        print("Running the tagmatch_runner")

        team_1 = []
        team_1.append(participants["team_1"]["member_1"])
        team_1.append(participants["team_1"]["member_2"])
        print("test team_1")

        print("end test team_1")

        team_2 = []
        team_2.append(participants["team_2"]["member_1"])
        team_2.append(participants["team_2"]["member_2"])
        print("TEAM 1:")
        print(team_1)
        print("TEAM 2:")
        print(team_2)

        comeback_plus = 5
        finisher_count = 0
        roundup = []
        count = 0

        attacker = random.choice(team_1)
        # print(f"attacker is: {attacker.name}")
        # print(f"attacker health is: {attacker.health}")
        # print(f"attacker health is: {attacker}")
        defender = random.choice(team_2)
        # print(f"defender is: {defender.name}")
        # print(f"defender health is: {defender.health}")

        attacker_key = attacker.name
        defender_key = defender.name
        attacker.match_role = "attacker"
        defender.match_role = "defender"
        attacker_health = attacker.health
        defender_health = defender.health

        while True:
            count += 1
            rand = randint(0, 5)
            hit = int(attacker.attack) / int(defender.defense) * rand

            # use turn var to determine who's going to attack and who's going to defend (1 = attacker, 2 = defender)
            turn_list = [
                1,
                2,
                "attk_come_back",
                "def_come_back",
                "finisher",
                "attackTag",
                "defendTag",
            ]

            turn = random.choices(
                turn_list,
                weights=(50, 50, 10, 10, 10, 10, 10),
            )

            if 1 in turn:
                move = random.choice(moves)
                outcome = f"{str(defender_key)} [{str(defender_health)}] is hit with a {move} [{str(hit)}] by  {str(attacker_key)} [{str(attacker_health)}]"
                defender_health = int(defender_health) - hit
                roundup.append(outcome)
                # print(roundup)

            elif 2 in turn:
                move = random.choice(moves)
                outcome = f"{str(attacker_key)} [{str(attacker_health)}] is hit with a {move} [{str(hit)}] by  {str(defender_key)} [{str(defender_health)}]"
                attacker_health = int(attacker_health) - hit
                roundup.append(outcome)
                # print(roundup)

            elif "attackTag" in turn:
                outcome = (
                    f"{str(attacker_key)} [{str(attacker_health)}] goes for the tag!"
                )
                print("TEST TEST TEST")
                print("TEST TEST TEST")
                attacker.health = attacker_health
                roundup.append(outcome)
                # Tag in!
                lastChoice = attacker
                attacker = random.choice(team_1)
                while lastChoice.id == attacker.id:
                    attacker = random.choice(team_1)

                attacker_key = attacker.name
                attacker.match_role = "attacker"
                attacker_health = attacker.health

                outcome = f"{str(attacker_key)} [{str(attacker_health)}] is now the legal man &#128079;!"
                roundup.append(outcome)
                # print(roundup)

            elif "defendTag" in turn:
                outcome = (
                    f"{str(defender_key)} [{str(defender_health)}] goes for the tag!"
                )
                defender.health = defender_health
                roundup.append(outcome)
                # Tag in!
                lastChoice = defender
                defender = random.choice(team_2)
                while lastChoice.id == defender.id:
                    defender = random.choice(team_2)
                defender_key = defender.name
                defender.match_role = "defender"
                defender_health = defender.health

                outcome = f"{str(defender_key)} [{str(defender_health)}] is now the legal man &#128079;!"
                roundup.append(outcome)

            elif "attk_come_back" in turn:
                outcome = f"{str(attacker_key)} [{str(attacker_health)}] starts rallying the crowd behind them &#128293; [+{str(comeback_plus)}!]"
                attacker_health = int(attacker_health) + comeback_plus
                roundup.append(outcome)

            elif "def_come_back" in turn:
                outcome = f"{str(defender_key)} [{str(defender_health)}] starts rallying the crowd behind them &#128293; [+{str(comeback_plus)}!]"
                defender_health = int(defender_health) + comeback_plus
                roundup.append(outcome)

            elif "finisher" in turn:
                who = random.sample([defender, attacker], 2)
                success = random.choice(["success", "failure"])
                if "success" in success:
                    damage = 10 * random.randint(1, 10)
                    finisher_count = finisher_count + 1
                    if "defender" in who[1].match_role:
                        defender_health = int(defender_health) - damage
                    else:
                        attacker_health = int(attacker_health) - damage
                else:
                    damage = 0

                outcome = f"{str(who[0].name)} attempts their finisher {who[0].finisher} on {str(who[1].name)} it was a {success} &#128079; [-{damage}!]"
                roundup.append(outcome)

            # Work out rating based on number of stages and how random choices
            rating = (
                int(count) / 10
                + int(attacker.level)
                + int(defender.level)
                + int(defender.attack)
                + int(attacker.attack)
                + bonuses
            )
            if rating < 20:
                self.stars = 1
            elif rating >= 20 and rating < 40:
                self.stars = 2
            elif rating >= 40 and rating < 60:
                self.stars = 3
            elif rating >= 60 and rating < 80:
                self.stars = 4
            elif rating >= 80:
                self.stars = 5
            else:
                self.stars = 0

            self.roundup = roundup
            # Declare the winner!
            if int(defender_health) <= 0:
                self.result = f"{str(team_1)} defeats {str(team_2)}"
                self.winner = []
                for x in team_1:
                    self.winner.append(x.name)
                self.loser = []
                for x in team_2:
                    self.loser.append(x.name)
                break
            elif int(attacker_health) <= 0:
                self.result = f"{str(team_2)} defeats {str(team_1)}"
                self.winner = []
                for x in team_2:
                    self.winner.append(x.name)
                self.loser = []
                for x in team_1:
                    self.loser.append(x.name)
                break
