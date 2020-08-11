from random import randint
import random
import csv

class Game:
    '''
    Class Struggle Board Game
    ©1978, Bertell Ollman

    "Class Struggle" reflects the real struggle between the classes in our society. 
    THE OBJECT OF THE GAME IS TO WIN THE REVOLUTION . . . ULTIMATELY. 
    Until then, classes—represented by different players—advance around the board, 
    making and breaking alliances, and picking up strengths and weaknesses that determine 
    the outcome of the elections and general strikes which occur along the way.
    
    In this abbreviated version of this game, there will be two players 
    who alternate taking turns rolling the dice, and will continue to gain assets 
    or debits as they traverse the spaces until either player lands on the end space.
    There is a card draw at every turn.

    As this is developed further, it would be great to program more than two players 
    into gameplay, the alliance strategy, better visualization, and advanced board actions
    from the original game rules.

    Attributes:
        the_end: a Boolean that controls the end-state condition
        the_winner: entire player class of the winner
        capitalist_count: number of moves of capitalist player (for plotting)
        worker_count: number of moves of worker player (for plotting)
    
    Methods:
        play: Called after initializing the Game to run the automated game-play
        get_stats: Print out player's current assets, debits, and position
        bordered: Create a thick border around formatted text blocks (dice display or card prompts)
        dice_roll: Outputs random number between 1-6 and formats dice display 
        card_display: Re-formats the long-form string from the chance card dictionary
        pull_card: Every turn, a player draws a card. This method will have separate actions for "asset", "debit", "position", "turn", and "confrontation"
        confrontation: A special type of action where the two players compares total of assets-debits to see who gets extra dice rolls

    '''
    def __init__(self, num_players):
        if num_players != 2:
            raise Exception("The gameplay you desire is out of the scope of this project.\nPlease suggest 2 players.")
        self.the_end = False
        self.the_winner = None
        self.the_winner, self.capitalist_count, self.worker_count = self.play()

    def play(self):
        # Create the board
        board = Board(15)
        board.create_board()
        print("-"*50)
        print(f"Game initialized! The last space is at position {board.end}.\nWhoever gets to that space first wins!")
        print("-"*50)
        # Create the players
        c = Player("capitalist")
        w = Player("worker")
        player_list = [c,w]
        print("-"*50)
        print(f"Players initialized! This is a {len(player_list)}-player game.")
        print("-"*50)
        # Game play
        while self.the_end is False:
            # Alternating player turns
            for player in player_list:
                # Start player turn
                print("\n\n\n")
                print("-"*50)
                print(f"{player.player_type.title()}'s turn! Starting at position {player.position}.")
                print("-"*50)
                self.helper(player)
                if self.the_end is True:
                    break
                # Check for skipped turns
                if player.turn < 0:
                    print("~*"*25)
                    print(f"THE {player.player_type.upper()} SKIPS A TURN!")
                    print("~*"*25)
                    player.turn += 1
                    continue
                # Check for extra turns
                elif player.turn > 0:
                    for number in range(player.turn):
                        # Insert the extra turn into the right position in the iterable list, 
                        # so extra turns are taken in sequence
                        if player.player_type == "capitalist":
                            player_list.insert(1, player)
                        if player.player_type == "worker":
                            player_list.insert(2, player)
                    # Reset the turn count after appending new turns to game play
                    player.turn = 0
                # Roll the dice!
                roll = self.dice_roll()
                # If you rolled past the end space, do nothing.
                if (player.position + roll) > board.end:
                    print("You can't move past the last space on the board, silly! Nothing happens. \n")
                # Game on! Move position.        
                elif (player.position + roll) < board.end: 
                    player.position += roll
                    print(f"Increase in position by {roll}.")
                    self.get_stats(player)
                    print("\nNow, Draw a card!")
                    if player.player_type == "capitalist":
                        self.pull_card(board, player, w)
                    elif player.player_type == "worker":
                        self.pull_card(board, player, c)
                # If you reached board's last space, end the game.      
                elif (player.position + roll) == board.end: 
                    self.the_end = True
                    self.the_winner = player
                    player.position += roll
                    print(f"THE {player.player_type.upper()} WINS!")
                    break
                # Exception for catching miscelleanous behaviors      
                else:
                    raise Exception("Something else is off here.")
                # Print out stats for the end of each turn
                self.get_stats(player)
            # Reset the iterable list
            if self.the_end is True:
                break
            player_list = [c,w]
        print(f"\nCapitalist play_count:{c.card_count} | Worker play_count:{w.card_count}\n")
        return self.the_winner, c.card_count, w.card_count
    
    def helper(self, player):
        answer = input("What would you like to do? You can:\n'Stats'\n'Play'\n'Exit'\n").lower()
        if answer == "stats":
            self.get_stats(player)
        elif answer == "play":
            return
        elif answer =="exit":
            self.the_end = True
            print("GAME CLOSING DOWN!")
            return
        else:
            print("That's not one of the menu choices. Try again.")
        self.helper(player)
    
    def get_stats(self, player):
        print("{:<10s} {:<10s} {:<10s}".format("Assets", "Debits", "Position"))
        print("{:<10.0f} {:<10.0f} {:<10.0f}".format(player.assets, player.debits, player.position))
        
    def bordered(self,text):
        lines = text.splitlines()
        width = max(len(s) for s in lines)
        res = ['┌' + '─' * width + '┐']
        for s in lines:
            res.append('│' + (s + ' ' * width)[:width] + '│')
        res.append('└' + '─' * width + '┘')
        print('\n'.join(res))
                
    def dice_roll(self):
        n=randint(1,6)   
        o,x='o '
        a='-'*5
        b=(x,o)[n>3]
        d=(x,o)[n>5]
        c=(x,o)[n>1]    
        dice_string = ' '+c+x+b+'\n '+d+(x,o)[n%2]+d+' \n '+b+x+c+' '
        self.bordered(dice_string)
        print(f"A {n} was rolled!\n")
        return n
    
    def card_display(self, text):
        # Reformat long text line to block of text that is around 30 characters wide
        x = text.split()
        new_string = ''
        new_line = ''
        for word in x:
            if len(new_line) < 30:
                new_line += ' '+word
            elif len(new_line) >= 30:
                new_string += new_line+' '+word+'\n'
                new_line = ''
        new_string += new_line+'\n'
        self.bordered(new_string)

    def pull_card(self, board, player, other_player):
        # Display card
        self.card_display(board.chance_cards[player.player_type][player.card_count]["prompt"])
        # Asset card
        if board.chance_cards[player.player_type][player.card_count]["action"] == "asset":
            change = int(board.chance_cards[player.player_type][player.card_count]["asset"])
            player.assets += change
            print(f"Your assets increase by {change}.\n")   
        # Debit card
        elif board.chance_cards[player.player_type][player.card_count]["action"] == "debit":
            change = int(board.chance_cards[player.player_type][player.card_count]["debit"])
            player.debits += change
            print(f"Your debits increase by {change}.\n")  
        # Position card
        elif board.chance_cards[player.player_type][player.card_count]["action"] == "position":
            change = int(board.chance_cards[player.player_type][player.card_count]["position"])
            if (player.position + change) == board.end: 
                self.the_end = True
                self.the_winner = player
                player.position += change
                print(f"THE {player.player_type.upper()} WINS!\n")
            elif (player.position + change) < board.end:
                player.position += change
                print(f"Your position changes by {change}.\n")
            elif (player.position + change) < 0:
                player.position = 0
                print(f"Your position is back to 0.\n")
            else:
                print("You can't go beyond the last space on the board, silly! Do nothing.\n")
        # Turn card
        elif board.chance_cards[player.player_type][player.card_count]["action"] == "turn":
            change = int(board.chance_cards[player.player_type][player.card_count]["turn"])
            if change < 0:
                print(f"You will have to skip {abs(change)} turn(s) on the next round.\n")
            if change > 0:
                print(f"You gain {change} extra turn(s) on the next round.\n")
            player.turn += change
        # Confrontation card
        elif board.chance_cards[player.player_type][player.card_count]["action"] == "confrontation":
            print("YOU HAVE DRAWN A CONFRONTATION!")
            print("WINNING THE CONFRONTATION SECURES")
            print("THE VICTORIOUS CLASS TWO FREE \nTHROWS OF THE DICE!\n") 
            self.confrontation(player,other_player)
        player.card_count += 1

    def confrontation(self, player, other_player):
        # Here's an example of where, in actual gameplay, we could collect player input.
        # For the purposes of the demo, the confrontation condition is when the 
        # player has more assets than debits.     
        answer = input("Do you want to confront the other player?\nYou need to net more assets than they do.\n").lower()
        if answer == "yes":
            player_total = player.assets - player.debits
            other_player_total = other_player.assets - other_player.debits
            if player_total > other_player_total:
                print("\nYou win this Confrontation. You earn 2 extra turns.\n")
                player.turn += 2
            elif player_total < other_player_total:
                print("\nYou lose this Confrontation. Other player earns 2 extra turns.\n")
                other_player.turn += 2
            elif player_total == other_player_total:
                print("\nThis confrontation is at a stalemate! Nothing happens.\n")
        elif answer =="No":
            print("\nBetter to sit this one out.\n") 
        else:
            print("\nPlease answer 'Yes' or 'No'. Try again\n")
            return self.confrontation(player, other_player)
            
class Player(Game):
    '''
    This class stores all of the attributes and methods for the main class players (Capitalist or Worker).
    
    Attributes:
        player_type: You can either be a "capitalist" or "worker"
        position: Player's integer position between 0 and the end space
        assets: Counter of player's assets collected throughout the game
        debits: Counter of player's assets collected throughout the game
        card_count: Counter of turns. It is also used to select a card from the shuffled dictionary of cards.
        turn: Counter of extra/skipped rolls of the dice. A positive calue implies the number of extra turns. 
            A negative value implies the number of skipped turns.
    
    You initialize a player with:
        At the 0th Position
        0 Assets
        0 Debits
        Counter of cards starting at 1.
        Counter of extra/skipped turns at 0.
        
    '''
    def __init__(self, player_type=None):
        if player_type not in ["capitalist", "worker"]:
            raise Exception("Are you a capitalist or worker? You need to decide.")
        self.player_type = player_type
        self.position = 0
        self.assets = 0
        self.debits = 0
        self.card_count = 1
        self.turn = 0
        
    def __str__(self):
        return player.player_type

class Board(Game):
    '''
    Attributes:
        end: End space of the game
        chance_cards: 
        
    Methods:
        create_board: Opens and stores data from worker and capitalist chance card CSV files.
        display_board: To be developed in later versions. Inteded to be a snapshot of the board game with players' positions.
        
    '''
    def __init__(self, end):
        self.end = end
        self.chance_cards = {}
    
    def create_board(self):
        worker_cards = []
        capitalist_cards = []
        worker_cards_dict = {}
        capitalist_cards_dict = {}
        
        # WORKER CHANCE CARD DECK
        # FIRST, READ THE CSV FILE + APPEND TO LIST
        worker_cards_csv = open("worker_cards_csv","rt",encoding="utf-8")
        csvin = csv.reader(worker_cards_csv)
        for row in csvin:
            worker_cards.append(row)
        worker_cards_csv.close()
        # GRAB THE HEADER
        worker_cards_header = worker_cards.pop(0)
        # SHUFFLE THE CARDS
        worker_cards *= 2
        random.shuffle(worker_cards)
        # REASSIGN CARD DECK INTO DICTIONARY FOR EASIER RETRIEVAL
        for number in range(1, len(worker_cards)+1):
            worker_cards_dict[number] = {}
            for sub_number in range(len(worker_cards_header)):
                worker_cards_dict[number][worker_cards_header[sub_number]]=worker_cards[number-1][sub_number]
        
        # CAPITALIST CHANCE CARD DECK
        # FIRST, READ THE CSV FILE + APPEND TO LIST
        capitalist_cards_csv = open("capitalist_cards_csv", "rt", encoding="utf-8")
        csvin2 = csv.reader(capitalist_cards_csv)
        for row in csvin2:
            capitalist_cards.append(row)
        capitalist_cards_csv.close()
        # GRAB THE HEADER
        capitalist_cards_header = capitalist_cards.pop(0)
        # SHUFFLE THE CARDS
        capitalist_cards *= 2
        random.shuffle(capitalist_cards)
        # REASSIGN CARD DECK INTO DICTIONARY FOR EASIER RETRIEVAL
        for number in range(1, len(capitalist_cards)+1):
            capitalist_cards_dict[number] = {}
            for sub_number in range(len(capitalist_cards_header)):
                capitalist_cards_dict[number][capitalist_cards_header[sub_number]]=capitalist_cards[number-1][sub_number]
        
        # MERGE DICTIONARIES
        self.chance_cards["capitalist"] = capitalist_cards_dict
        self.chance_cards["worker"] = worker_cards_dict
        
    # Visualization
    def display_board(self, player_1, player_2):
        # Updating board, taking in positional input from player_1 and player_2 attributes
        # Print out ASCII board game
        pass