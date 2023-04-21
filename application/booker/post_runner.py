import random
from random import randint
from unicodedata import name
from colorama import Fore, Back, Style


class Booker:
    def __init__(self, participants, bonuses, omgmoment, runin_moment, moves):

        print("Running the post_runner")
        print(f"BONUS IS {bonuses}")
        attacker = participants[0]
        defender = participants[1]
        attacker_key = attacker.name
        defender_key = defender.name
        attacker.match_role = "attacker"
        defender.match_role = "defender"
        attacker_health = attacker.health
        defender_health = defender.health

        comeback_plus = 5

        print(
            Fore.GREEN
            + str(attacker_key).upper()
            + " VS "
            + str(defender_key).upper()
            + Style.RESET_ALL
        )
        match = f"{str(attacker_key)} VS {str(defender_key)}"
        roundup = []
        count = 0
        finisher_count = 0

        if omgmoment == "true":
            omgmoment_likelihood = 25
        else:
            omgmoment_likelihood = 0

        if runin_moment == "true":
            run_in_likelihood = 25
        else:
            run_in_likelihood = 0

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
                "omgmoment",
                "run_in",
            ]

            turn = random.choices(
                turn_list,
                weights=(50, 50, 5, 5, 10, omgmoment_likelihood, run_in_likelihood),
            )

            # start the turn based attack/defense system
            if "omgmoment" in turn:
                omg_list = [
                    "suplex to the outside",
                    "diving elbow through the announce table",
                    "spear through the crowd barrier",
                    "powerbomb onto the ramp",
                ]
                moment = random.choice(omg_list)
                omgmoment_likelihood = 0
                who = random.sample([defender, attacker], 2)
                print(who)
                damage = 10 * random.randint(1, 10)
                if "defender" in who[1].match_role:
                    defender_health = int(defender_health) - damage
                else:
                    attacker_health = int(attacker_health) - damage
                outcome = f"&#129324; WTF JUST HAPPENED! {str(who[0].name)} hits {str(who[1].name)} with a {moment} &#129324; [-{damage}!]"
                roundup.append(outcome)

            if "run_in" in turn:
                outcome = f"A RUN IN OCCURS!!!"
                roundup.append(outcome)
                run_in_likelihood = 0

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

            elif "attk_come_back" in turn:
                attacker_health = int(attacker_health) + comeback_plus
                outcome = f"{str(attacker_key)} [{str(attacker_health)}] starts rallying the crowd behind them &#128293; [+{str(comeback_plus)}!]"
                roundup.append(outcome)

            elif "def_come_back" in turn:
                defender_health = int(defender_health) + comeback_plus
                outcome = f"{str(defender_key)} [{str(defender_health)}] starts rallying the crowd behind them &#128293; [+{str(comeback_plus)}!]"
                roundup.append(outcome)

            elif "finisher" in turn:
                who = random.sample([defender, attacker], 2)
                print(who)
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

            # Declare the winner!
            if int(defender_health) <= 0:
                self.result = f"{str(attacker_key)} defeats {str(defender_key)}"
                self.winner = f"{str(attacker_key)}"
                self.loser = f"{str(defender_key)}"
                self.roundup = roundup
                print(f"winner: {self.winner}")
                # return (match, roundup, result, winner, loser, self.stars)
                break
            elif int(attacker_health) <= 0:
                self.result = f"{str(defender_key)} defeats {str(attacker_key)}"
                self.winner = f"{str(defender_key)}"
                self.loser = f"{str(attacker_key)}"
                self.roundup = roundup
                print(f"winner: {self.winner}")
                # return (match, roundup, result, winner, loser, self.stars)
                break