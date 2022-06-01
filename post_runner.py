import os, json
import logging
import random
from random import randint
from colorama import Fore, Back, Style


def booker(participants,bonuses,omgmoment,runin_moment):
    # Percentage calculator
    def percentage(part, whole):
      percentage = 100 * float(part)/float(whole)
      return str(percentage) + "%"

    print("Running the post_runner")
    print(f"BONUS IS {bonuses}")

    attacker_key = participants[0]['name']
    defender_key = participants[1]['name']
    attacker     = participants[0]
    defender     = participants[1]
    comeback_plus = 5

    attacker["role"] = "attacker"
    defender["role"] = "defender"

    print( Fore.GREEN + str(attacker_key).upper() + " VS " + str(defender_key).upper() + Style.RESET_ALL)
    match=f"{str(attacker_key)} VS {str(defender_key)}"
    roundup = []
    count = 0
    finisher_count = 0

    if omgmoment == 'true':
      omgmoment_likelihood = 25
    else:
      omgmoment_likelihood = 0

    if runin_moment == 'true':
      run_in_likelihood = 25
    else:
      run_in_likelihood = 0

    while True:
      count += 1
      rand = randint(0, 5)
      hit = (int(attacker['attack'])/int(defender['defense'])*rand)
      attacker_health=(percentage(int(attacker['health']), 100))
      defender_health=(percentage(int(defender['health']), 100))

      # use turn var to determine who's going to attack and who's going to defend (1 = attacker, 2 = defender) 
      turn_list = [1, 2, 'attk_come_back', 'def_come_back', 'finisher','omgmoment','run_in']
      
      turn = random.choices(turn_list, weights=(50, 50, 5, 5, 10, omgmoment_likelihood, run_in_likelihood))
      
      # define some moves
      move_list = ['suplex','dropkick','uppercut','punch','german suplex','piledriver','ddt','clothesline','back breaker']

      # start the turn based attack/defense system
      if 'omgmoment' in turn:
        omg_list = ['suplex to the outside','diving elbow through the announce table','spear through the crowd barrier','powerbomb onto the ramp']
        moment = random.choice(omg_list)
        omgmoment_likelihood = 0
        who=random.sample([defender, attacker], 2)
        print(who)
        damage = (10*random.randint(1, 10))
        if 'defender' in who[1]['role']:
            defender['health'] = int(defender['health']) - damage
        else:
            attacker['health'] = int(attacker['health']) - damage
        # else:
        #   damage = 0
        # outcome=f"&#129324; WTF JUST HAPPENED OMFG {moment} &#129324;" 
        outcome=f"&#129324; WTF JUST HAPPENED! {str(who[0]['name'])} hits {str(who[1]['name'])} with a {moment} &#129324; [-{damage}!]"
        roundup.append(outcome)

      if 'run_in' in turn:
        outcome=f"A RUN IN OCCURS!!!"
        roundup.append(outcome)
        run_in_likelihood = 0

      if 1 in turn:
        move = random.choice(move_list)
        outcome=f"{str(defender_key)} [{str(defender_health)}] is hit with a {move} [{str(hit)}] by  {str(attacker_key)} [{str(attacker_health)}]"
        defender['health'] = int(defender['health']) - hit
        roundup.append(outcome)
        # print(roundup)

      elif 2 in turn:
        move = random.choice(move_list)
        attacker['health'] = int(attacker['health']) - hit
        outcome=f"{str(attacker_key)} [{str(attacker_health)}] is hit with a {move} [{str(hit)}] by  {str(defender_key)} [{str(defender_health)}]"
        roundup.append(outcome)
        # print(roundup)

      elif "attk_come_back" in turn:
        attacker['health'] = int(attacker['health']) + comeback_plus
        outcome=f"{str(attacker_key)} [{str(attacker_health)}] starts rallying the crowd behind them &#128293; [+{str(comeback_plus)}!]"
        roundup.append(outcome)

      elif "def_come_back" in turn:
        defender['health'] = int(defender['health']) + comeback_plus
        outcome=f"{str(defender_key)} [{str(defender_health)}] starts rallying the crowd behind them &#128293; [+{str(comeback_plus)}!]"
        roundup.append(outcome)

      elif "finisher" in turn:
        who=random.sample([defender, attacker], 2)
        print(who)
        success=random.choice(['success','failure'])
        if 'success' in success:
          damage = (10*random.randint(1, 10))
          finisher_count = finisher_count + 1
          if 'defender' in who[1]['role']:
            defender['health'] = int(defender['health']) - damage
          else:
            attacker['health'] = int(attacker['health']) - damage
        else:
          damage = 0
        
        outcome=f"{str(who[0]['name'])} attempts their finisher {who[0]['finisher']} on {str(who[1]['name'])} it was a {success} &#128079; [-{damage}!]"
        roundup.append(outcome)

      # Declare the winner! 
      if int(defender['health']) <= 0:
        result = f"{str(attacker_key)} defeats {str(defender_key)}"
        winner = f"{str(attacker_key)}"
        loser = f"{str(defender_key)}"
        # Work out rating based on number of stages and how random choices
        rating = int(count)/10+int(attacker['level'])+int(defender['level'])+int(defender['attack'])+int(attacker['attack'])+bonuses
        if rating < 20:
            stars=1
        elif (rating >= 20 and rating < 40):
            stars=2
        elif (rating >= 40 and rating < 60):
            stars=3
        elif (rating >= 60 and rating < 80):
            stars=4
        elif (rating >= 80):
            stars=5
        else: 
            stars=0
        print(rating)
        return(match,roundup,result,winner,loser,stars)
        # break
      elif int(attacker['health']) <= 0:
        result = f"{str(defender_key)} defeats {str(attacker_key)}"
        winner = f"{str(defender_key)}"
        loser = f"{str(attacker_key)}"
        # Work out rating based on number of stages and how random choices
        rating = int(count)/10+int(attacker['level'])+int(defender['level'])+int(defender['attack'])+int(attacker['attack'])+bonuses
        if rating < 20:
            stars=1
        elif (rating >= 20 and rating < 40):
            stars=2
        elif (rating >= 40 and rating < 60):
            stars=3
        elif (rating >= 60 and rating < 80):
            stars=4
        elif (rating >= 80):
            stars=5
        else: 
            stars=0
        print(rating)
        return(match,roundup,result,winner,loser,stars)
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
      
  



