import sys

from classes import SakClass, Game, Human, Computer

# Create SakClass object
# Scrabble in greek edition has 102 letters
sak = SakClass(102)

# Create game object
game = Game("Scrabble")

# Read player's name
nameHuman = input("Welcome to scrabble!\nEnter your name please: ")

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
                word = game.readWord(active_player, sak)
            elif active_player == pComputer:
                word = pComputer.play(game, algorithmOption)
                # Increase computer counters
                if word == 'p':
                    pComputer.totalPassesComputer += 1
                else:
                    pComputer.totalWordsComputer += 1
            if word == 'q':
                game.gameOver(pHuman, pComputer)
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
                # game.printGameInfo(active_player, sak)
            # Change active player
            active_player = game.changePlayer(active_player, pHuman, pComputer)
    elif playerChoice == 4:
        print("Quitting the game...")
        sys.exit()
