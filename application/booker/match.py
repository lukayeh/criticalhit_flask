import random
from models import *
from sqlalchemy import or_, and_
from collections.abc import Iterable

def flatten(xs):
    for x in xs:
        if isinstance(x, Iterable) and not isinstance(x, (str, bytes)):
            yield from flatten(x)
        else:
            yield x

# Define the Player class
class Player:
    def __init__(self, name, health, attack_power, defense, finisher, before_health):
        self.name = name
        self.health = health
        self.attack_power = attack_power
        self.defense = defense
        self.finisher = finisher
        self.before_health = before_health


    def turn(self):
        turn_list = [
            {
                "name": "standard_attack",
                "message": "{TARGET_NAME} [{TARGET_HEALTH}] is hit with a {MOVE} [{DAMAGE}] by {NAME} [{HEALTH}]",
            },
            {
                "name": "comeback",
                "message": "{NAME} [{HEALTH}] is having a comeback  &#127775;!",
            },
            {
                "name": "finisher",
                "message": "{NAME} [{HEALTH}] goes for their finisher {FINISHER} on {TARGET_NAME} [{TARGET_HEALTH}] for {DAMAGE} damage. &#127881;",
            },
        ]

        choiceWeights = [50, 5, 5]
        turn = random.choices(turn_list, choiceWeights)
        return turn

    def attack(self, target, move):
        output=[]
        print(move)
        damage = random.randint(1, self.attack_power)
        turn = self.turn()

        if turn[0]["name"] == "comeback":
            self.health = self.health + 10
            damage = 0
        
        if turn[0]["name"] == "finisher":
            print("turn is a finisher")
            damage = damage*10

        output.append(turn[0]["message"].format(
                NAME=self.name,
                HEALTH=self.health,
                TARGET_NAME=target.name,
                TARGET_HEALTH=target.health,
                MOVE=move.name,
                DAMAGE=damage,
                FINISHER=self.finisher,
            ))
        print(output)
        target.health -= damage
        # attempt a pin if damage is low...
        if target.health < 10:
            output.append(self.pin(target))
        
        return output

    def pin(self, target):
        output=[]
        output.append(f"{self.name} is attempting a pin on {target.name}")

        count = random.randint(1, 4)
        for number in range(1,4):
            print(f"{number}..")
            if number == count and number < 3:
                output.append(f"{target.name} kicks out at {number}")
                break
            elif number == 3:
                output.append(f"It's a 3 count! {self.name} eliminates {target.name} &#129702;")
                target.health = 0

        return output

    def is_alive(self):
        return self.health > 0


# Function to determine the winner(s)
def determine_winner(players):
    winners = []
    max_health = max(player.health for player in players)
    for player in players:
        if player.health == max_health:
            winners.append(player)
    return winners

def retrieve_moves():
        # Retrieve moves list
        moves = Moves.query.all()
        moves_list = []
        for move in moves:
            moves_list.append(move.name)

        return moves

class PrepareMatch:
    def __init__(self, ids):

        # Prepare participants
        participants_sql = Roster.query.filter(or_(Roster.id == v for v in ids)).all()

        self.participants=participants_sql

        players = []
        numPlayers=len(ids)
        index=0
        while index < numPlayers:
            name = participants_sql[index].name
            health = participants_sql[index].health
            before_health = participants_sql[index].health
            attack_power = participants_sql[index].attack
            defense = participants_sql[index].defense
            finisher = participants_sql[index].finisher
            player = Player(name, health, attack_power, defense, finisher, before_health)
            players.append(player)
            index=index+1
        self.players=players

# Main game loop
class Booker:
    def __init__(self, playerIds):
        output=[]
        moves=retrieve_moves()
        prematch=PrepareMatch(playerIds)
        players=prematch.players
        self.players = players
        print(players)
        random.shuffle(players)  # Shuffle the list of players

        # Print player stats
        for player in players:
            print(
                f"{player.name}: Health={player.health}, Attack Power={player.attack_power}"
            )

        while True:
            for player in players:
                if not player.is_alive():
                    continue

                print(f"\n{player.name}'s turn:")
                target = random.choice([p for p in players if p != player and p.is_alive()])
                move = random.choice(moves)
                output.append(player.attack(target, move))
                    
            # Check if there is only one player left
            alive_players = [player for player in players if player.is_alive()]
            if len(alive_players) == 1:
                winner = alive_players[0]                
                self.winner = winner
                self.output = flatten(output)
                return 

            # Check if all players are defeated
            if len(alive_players) == 0:
                print("\nIt's a draw!")
                output.append(f"\nIt's a draw!")
                return

            random.shuffle(players)  # Shuffle the list of players for the next round
