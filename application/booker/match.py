import random
from models import *
from sqlalchemy import or_, and_
from collections.abc import Iterable

def flatten(container):
    for i in container:
        if isinstance(i, (list,tuple)):
            for j in flatten(i):
                yield j
        else:
            yield i

# Define the Player class
class Player:
    def __init__(self, name, health, attack_power, defense, finisher, before_health, image):
        self.name = name
        self.health = health
        self.attack_power = attack_power
        self.defense = defense
        self.finisher = finisher
        self.before_health = before_health
        self.image = image
        self.pinned = ""


    def turn(self):
        turn_list = [
            {
                "name": "standard_attack",
                "message": "{TARGET_NAME} [{TARGET_HEALTH}] is hit with a {MOVE} [{DAMAGE}] by {NAME} [{HEALTH}]",
            },
            {
                "name": "comeback",
                "message": "{NAME} [{HEALTH}] starts rallying the crowd behind them &#128293; [+{COMEBACK_PLUS}!]",
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
        # print(move)
        damage = random.randint(1, self.attack_power)
        turn = self.turn()
        comeback_plus = 10
        
        if turn[0]["name"] == "finisher":
            damage = damage*10
            finishercount =+ 1

        output.append(turn[0]["message"].format(
                NAME=self.name,
                HEALTH=self.health,
                TARGET_NAME=target.name,
                TARGET_HEALTH=target.health,
                MOVE=move.name,
                DAMAGE=damage,
                COMEBACK_PLUS=comeback_plus,
                FINISHER=self.finisher,
            ))

        if turn[0]["name"] == "comeback":
            self.health += comeback_plus
            damage = 0

        target.health -= damage
        # attempt a pin if damage is low...
        if target.health < 10:
            output.append(self.pin(target))
        
        return output

    def pin(self, target):
        output=[]
        output.append(f"{self.name} [{self.health}] attempts a pin on {target.name} [{target.health}]...")

        count = random.randint(1, 4)
        for number in range(1,4):
            if number == count and number < 3:
                output.append(f"{target.name} kicks out at {number}!!")
                target.health = target.health + 5
                break
            elif number == 3:
                output.append(f"It's a 3 count! {self.name} eliminates {target.name} &#129702;")
                target.pinned = "true"
                target.health = 0

        return output

    def is_alive(self):
        return self.health > 0

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
            image = participants_sql[index].img
            player = Player(name, health, attack_power, defense, finisher, before_health, image)
            players.append(player)
            index=index+1
        self.players=players

class PostMatch:
    def __init__(self, winner, losers, outcome):

        update_winner = Roster.query.filter_by(name=winner).first()
        update_winner.level = update_winner.level + 1
        update_winner.wins = update_winner.wins + 1

        # # Update the loser
        for x in losers:
            update_loser = Roster.query.filter_by(name=x).first()
            # update_loser.health = (update_loser.health) - 5
            update_loser.losses = update_loser.losses + 1
            update_loser.morale = update_loser.morale - 5

        # # Update Results        
        losers = ', '.join(losers)
        result =  str(f"{winner} defeats {losers}")
        description = ', '.join(outcome)
        print(description)
        new_result = Result(
            result=result,
            rating="2",
            winner=winner,
            loser=losers,
            description=description,
        )
        
        db.session.add(new_result)
        
        db.session.commit()
    
    def generateRating(count, finishercount):
        # # Work out match rating:
        bonuses = 10
        nearMisses = 1
        rating = (
                int(count) / 10
                + bonuses
                + nearMisses
                + finishercount
        )

        return rating

# Main game loop
class Booker:
    def __init__(self, playerIds):
        output=[]
        losers=[]
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
        count=0
        global finishercount
        finishercount = 0
        while True:
            count += 1
            for player in players:
                if not player.is_alive():
                    # print(f"checking if {player.name} is alive with health {player.health}" )
                    if not player.pinned and player.name not in losers:
                        output.append(f"{player.name} is unconcious and cannot continue!")
                    losers.append(player.name) if player.name not in losers else losers
                    continue

                # print(f"\n{player.name}'s turn:")
                target = random.choice([p for p in players if p != player and p.is_alive()])
                move = random.choice(moves)
                output.append(player.attack(target, move))
                    
            # Check if there is only one player left
            alive_players = [player for player in players if player.is_alive()]
            if len(alive_players) == 1:
                winner = alive_players[0]                
                self.winner = winner
                self.output = list(flatten(output))
                PostMatch(winner.name,losers,self.output)
                self.rating = PostMatch.generateRating(count, finishercount)
                return 

            # Check if all players are defeated
            if len(alive_players) == 0:
                print("\nIt's a draw!")
                output.append(f"\nIt's a draw!")
                return

            random.shuffle(players)  # Shuffle the list of players for the next round
