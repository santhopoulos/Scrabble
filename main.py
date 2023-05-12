from classes import SakClass, Player, Game, Human, Computer

# Create SakClass object
sak = SakClass(104)

# Create game object
game = Game("Scrabble")

# Create human object
pHuman = Human('Stratos')

# Create computer object
pComputer = Computer("PC")

# Game setup
game.setup(pHuman, pComputer, sak)

# Initialize gameOver flag
isGameOver = False

# Set active player
active_player = pHuman

# Get player choice (1-4) and validity test for user input
playerChoice = input("Select from options 1-4: ")
while playerChoice not in ["1", "2", "3", "4"]:
    game.displayStartingScreen()
    print()
    playerChoice = input("Select from options 1-4: ")
playerChoice = int(playerChoice)

if playerChoice == 1:
    print("Option1")
    game.printScore(pHuman, pComputer)
elif playerChoice == 2:
    print("Option2")
elif playerChoice == 3:
    while not isGameOver and sak.numberOfLetters > 0:
        # Print information about the game
        game.printGameInfo(active_player, sak)
        # Read word and validate it
        if active_player == pHuman:
            word = game.readWord(active_player, sak)
        elif active_player == pComputer:
            word = pComputer.maxLetters(game)
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
            game.printGameInfo(active_player, sak)
        # Change active player
        active_player = game.changePlayer(active_player, pHuman, pComputer)

elif playerChoice == 4:
    print("Option4")

