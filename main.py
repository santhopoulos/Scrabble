import sys

from classes import SakClass, Game, Human, Computer


def guidelines():
    """
    Provides guidelines for playing Scrabble.

    1) Classes implemented: SakClass, Game, Player, Human, Computer

    2) Inheritance:
    Base class: Player
    Derived classes: Human, Computer

    3) Extension methods in derived classes:
    Class Computer: play(), minLetters(), maxLetters(), smart()
    Class Human: -

    4) Neither decorators nor operator overloading was needed in the Scrabble implementation.

    5) Dictionary data structure was used to handle the available words.

    6) MIN-MAX-SMART algorithms were implemented for the computer to play.

    7) Gameflow:
     User enters his name. A screen with the available options will appear. Choose 1, 2, 3 or 4
     If you choose 1 last game stats will appear.
     If you choose 2 you will be able to choose the algorithm to play the computer with
     If you choose 4 you will quit the game
     If you choose 3 you will start playing the game.


     IMPORTANT NOTES:
     1) By default the computer plays with the 'MIN LETTERS' algorithm. In case you want
     a different algorithm, when starting the game go to settings and change it.

     2) To be able to view the stats you will have to have played at least 1 game.

     3) When it is your turn to find a word,
     type it in UPPERCASE GREEK only. To pass your turn use 'p' and to quit use 'q'




    Usage: help(guidelines) to view this documentation.
    """


# Scrabble in greek edition has 102 letters (excluding wildcards)

# Create SakClass object with 102 letters
sak = SakClass(102)

# Create game object
game = Game("Scrabble")

# Read player's name
nameHuman = input("Welcome to Scrabble!\nEnter your name: ")

# Create human object
pHuman = Human(nameHuman)

# Create computer object
pComputer = Computer("PC")

# Game setup
game.setup(pHuman, pComputer, sak)

# Initialize gameOver flag
isGameOver = False

# Set active player
active_player = pHuman

# Set default algorithm to MIN LETTERS
algorithmOption = 1

word_dictionary = {}
# Load the words from the greek7.txt to a dictionary
with open("greek7.txt", "r", encoding='utf-8') as file:
    for line in file:
        word = line.strip()
        word_dictionary[word] = True

while True:
    game.displayStartingScreen()
    # Get player choice (1-4) and validity test for user input
    playerChoice = input("Select option: ")
    while playerChoice not in ["1", "2", "3", "4"]:
        print("Invalid input. Please select 1, 2, 3 or 4")
        playerChoice = input("Select option: ")
    playerChoice = int(playerChoice)

    if playerChoice == 1:
        print("Stats")
        game.loadLastGameStats()
    elif playerChoice == 2:
        print("Settings")
        game.displaySettingScreen()
        algorithmOption = input("Select algorithm: ")
        while algorithmOption not in ["1", "2", "3"]:
            print("Invalid input. Please select 1, 2 or 3")
            algorithmOption = input("Select algorithm: ")
        algorithmOption = int(algorithmOption)
    elif playerChoice == 3:
        print("Play")
        while not isGameOver and sak.numberOfLetters > 0:
            # Print information about the game
            game.printGameInfo(active_player, sak)
            # Read word and validate it
            if active_player == pHuman:
                word = game.readWord(active_player)
            elif active_player == pComputer:
                word = pComputer.play(game, algorithmOption)
                # Increase computer counters
                if word == 'p':
                    pComputer.totalPassesComputer += 1
                else:
                    pComputer.totalWordsComputer += 1
            if word == 'q':
                game.end(pHuman, pComputer)
            # Check if word exists
            elif word == 'p':
                game.passTurn(sak, active_player)
            else:
                # calculate word points and add it to the score of the active player
                word_points = game.calculateWordPoints(word)
                # Update active player's score
                active_player.score += word_points
                # Update sak
                game.updateSak(sak, active_player, word)
                # Print game info
                game.printGameInfoAfterMove(active_player, sak)
            # Change active player
            active_player = game.changePlayer(active_player, pHuman, pComputer)
            # Check if Sak is empty
            if sak.numberOfLetters <= 0:
                print("Sak has emptied! Game over!")
                game.end(pHuman, pComputer)
    elif playerChoice == 4:
        print("Quitting the game...")
        sys.exit()
