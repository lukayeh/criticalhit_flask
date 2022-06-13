import os, json
import logging
import random
from random import randint
from unicodedata import name
from colorama import Fore, Back, Style


def booker(participants):

    print("Running the tagmatch_runner")
    # print(participants)
    team_1 = []
    team_1.append(participants['team_1']['member_1']['stats'].name)
    team_1.append(participants['team_1']['member_2']['stats'].name)
    team_2 = []
    team_2.append(participants['team_2']['member_1']['stats'].name)
    team_2.append(participants['team_2']['member_2']['stats'].name)
    print("TEAM 1:")
    print(team_1)
    print("TEAM 2:")
    print(team_2)   

    roundup = []
    count = 0
    
    while True:
        count += 1
        rand = randint(0, 5)
        attacker = rand(team_1)
        print(f"attacker is: {attacker}")
        defender = rand(team_2)
        print(f"attacker is: {defender}")
        # hit = (int(attacker.attack)/int(defender.defense)*rand)

        # # use turn var to determine who's going to attack and who's going to defend (1 = attacker, 2 = defender) 
        # turn_list = [1, 2, 'attk_come_back', 'def_come_back', 'finisher']
        
        # turn = random.choices(turn_list, weights=(50, 50, 5, 5, 10))
        
        # # define some moves
        # move_list = ['suplex','dropkick','uppercut','punch','german suplex','piledriver','ddt','clothesline','back breaker']

        # # start the turn based attack/defense system
        # if 1 in turn:
        #   move = random.choice(move_list)
        #   outcome=f"{str(defender_key)} [{str(defender_health)}] is hit with a {move} [{str(hit)}] by  {str(attacker_key)} [{str(defender_health)}]"
        #   defender_health = int(defender_health) - hit
        #   roundup.append(outcome)
        #   # print(roundup)

        # elif 2 in turn:
        #   move = random.choice(move_list)
        #   defender_health = int(defender_health) - hit
        #   outcome=f"{str(attacker_key)} [{str(defender_health)}] is hit with a {move} [{str(hit)}] by  {str(defender_key)} [{str(defender_health)}]"
        #   roundup.append(outcome)
        #   # print(roundup)

        # elif "attk_come_back" in turn:
        #   attacker_health = int(attacker_health) + comeback_plus
        #   outcome=f"{str(attacker_key)} [{str(attacker_health)}] starts rallying the crowd behind them &#128293; [+{str(comeback_plus)}!]"
        #   roundup.append(outcome)

        # elif "def_come_back" in turn:
        #   defender_health = int(defender_health) + comeback_plus
        #   outcome=f"{str(defender_key)} [{str(defender_health)}] starts rallying the crowd behind them &#128293; [+{str(comeback_plus)}!]"
        #   roundup.append(outcome)
    # attacker     = participants[0]
    # defender     = participants[1]
    # attacker_key = attacker.name
    # defender_key = defender.name
    # attacker.match_role = "attacker"
    # defender.match_role = "defender"
    # attacker_health = attacker.health
    # defender_health = defender.health

    # comeback_plus = 5

    # print( Fore.GREEN + str(attacker_key).upper() + " VS " + str(defender_key).upper() + Style.RESET_ALL)
    # match=f"{str(attacker_key)} VS {str(defender_key)}"
    # roundup = []
    # count = 0
    # finisher_count = 0

    # while True:
    #   count += 1
    #   rand = randint(0, 5)
    #   hit = (int(attacker.attack)/int(defender.defense)*rand)

    #   # use turn var to determine who's going to attack and who's going to defend (1 = attacker, 2 = defender) 
    #   turn_list = [1, 2, 'attk_come_back', 'def_come_back', 'finisher']
      
    #   turn = random.choices(turn_list, weights=(50, 50, 5, 5, 10))
      
    #   # define some moves
    #   move_list = ['suplex','dropkick','uppercut','punch','german suplex','piledriver','ddt','clothesline','back breaker']

    #   # start the turn based attack/defense system
    #   if 1 in turn:
    #     move = random.choice(move_list)
    #     outcome=f"{str(defender_key)} [{str(defender_health)}] is hit with a {move} [{str(hit)}] by  {str(attacker_key)} [{str(defender_health)}]"
    #     defender_health = int(defender_health) - hit
    #     roundup.append(outcome)
    #     # print(roundup)

    #   elif 2 in turn:
    #     move = random.choice(move_list)
    #     defender_health = int(defender_health) - hit
    #     outcome=f"{str(attacker_key)} [{str(defender_health)}] is hit with a {move} [{str(hit)}] by  {str(defender_key)} [{str(defender_health)}]"
    #     roundup.append(outcome)
    #     # print(roundup)

    #   elif "attk_come_back" in turn:
    #     attacker_health = int(attacker_health) + comeback_plus
    #     outcome=f"{str(attacker_key)} [{str(attacker_health)}] starts rallying the crowd behind them &#128293; [+{str(comeback_plus)}!]"
    #     roundup.append(outcome)

    #   elif "def_come_back" in turn:
    #     defender_health = int(defender_health) + comeback_plus
    #     outcome=f"{str(defender_key)} [{str(defender_health)}] starts rallying the crowd behind them &#128293; [+{str(comeback_plus)}!]"
    #     roundup.append(outcome)

    #   elif "finisher" in turn:
    #     who=random.sample([defender, attacker], 2)
    #     print(who)
    #     success=random.choice(['success','failure'])
    #     if 'success' in success:
    #       damage = (10*random.randint(1, 10))
    #       finisher_count = finisher_count + 1
    #       if 'defender' in who[1].match_role:
    #         defender_health = int(defender_health) - damage
    #       else:
    #         attacker_health = int(attacker_health) - damage
    #     else:
    #       damage = 0
        
    #     outcome=f"{str(who[0].name)} attempts their finisher {who[0].finisher} on {str(who[1].name)} it was a {success} &#128079; [-{damage}!]"
    #     roundup.append(outcome)

    #   # Declare the winner! 
    #   if int(defender_health) <= 0:
    #     result = f"{str(attacker_key)} defeats {str(defender_key)}"
    #     winner = f"{str(attacker_key)}"
    #     loser = f"{str(defender_key)}"
    #     # Work out rating based on number of stages and how random choices
    #     rating = int(count)/10+int(attacker.level)+int(defender.level)+int(defender.attack)+int(attacker.attack)+bonuses
    #     if rating < 20:
    #         stars=1
    #     elif (rating >= 20 and rating < 40):
    #         stars=2
    #     elif (rating >= 40 and rating < 60):
    #         stars=3
    #     elif (rating >= 60 and rating < 80):
    #         stars=4
    #     elif (rating >= 80):
    #         stars=5
    #     else: 
    #         stars=0
    #     print(rating)
    #     return(match,roundup,result,winner,loser,stars)
    #     # break
    #   elif int(attacker_health) <= 0:
    #     result = f"{str(defender_key)} defeats {str(attacker_key)}"
    #     winner = f"{str(defender_key)}"
    #     loser = f"{str(attacker_key)}"
    #     # Work out rating based on number of stages and how random choices
    #     rating = int(count)/10+int(attacker.level)+int(defender.level)+int(defender.attack)+int(attacker.attack)+bonuses
    #     if rating < 20:
    #         stars=1
    #     elif (rating >= 20 and rating < 40):
    #         stars=2
    #     elif (rating >= 40 and rating < 60):
    #         stars=3
    #     elif (rating >= 60 and rating < 80):
    #         stars=4
    #     elif (rating >= 80):
    #         stars=5
    #     else: 
    #         stars=0
    #     print(rating)
        # return(match,roundup,result,winner,loser,stars)
    return(participants)
        # break


    # {% if (booker[5]|int < 20) %}
    # &#11088;
    # {% elif (booker[5]|int >= 20 and booker[5]|int < 40) %}
    # &#11088; &#11088;
    # {% elif (booker[5]|int >= 40 and booker[5]|int < 60) %}
    # &#11088; &#11088; &#11088;
    # {% elif (booker[5]|int >= 60 and booker[5]|int < 80) %}
    # &#11088; &#11088; &#11088; &#11088;
    # {% elif (booker[5]|int >= 80) %}
    # &#11088; &#11088; &#11088; &#11088; &#11088;
    # {% else %}
    # no star
    # {% endif %}
      #return(match,roundup,result,winner,loser)
      
  



