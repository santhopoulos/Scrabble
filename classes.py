import json
import random
import sys
from itertools import permutations

LETTER_VALUES = {
    "Α": 1,
    "Β": 8,
    "Γ": 4,
    "Δ": 4,
    "Ε": 1,
    "Ζ": 10,
    "Η": 1,
    "Θ": 10,
    "Ι": 1,
    "Κ": 2,
    "Λ": 3,
    "Μ": 3,
    "Ν": 1,
    "Ξ": 10,
    "Ο": 1,
    "Π": 2,
    "Ρ": 2,
    "Σ": 1,
    "Τ": 1,
    "Υ": 2,
    "Φ": 8,
    "Χ": 8,
    "Ψ": 10,
    "Ω": 3,
}


class SakClass:
    LETTER_QUANTITY = {
        "Α": 12,
        "Β": 1,
        "Γ": 2,
        "Δ": 2,
        "Ε": 8,
        "Ζ": 1,
        "Η": 7,
        "Θ": 1,
        "Ι": 8,
        "Κ": 4,
        "Λ": 3,
        "Μ": 3,
        "Ν": 6,
        "Ξ": 1,
        "Ο": 9,
        "Π": 4,
        "Ρ": 5,
        "Σ": 7,
        "Τ": 8,
        "Υ": 4,
        "Φ": 1,
        "Χ": 1,
        "Ψ": 1,
        "Ω": 3,
    }

    def __init__(self, number_of_letters):
        self.numberOfLetters = number_of_letters

    def getLetters(self, n):
        """
        Returns n random letters from the SakClass, subtracting the selected letters from the total pool.
        """
        letters = []
        for i in range(n):
            if sum(self.LETTER_QUANTITY.values()) == 0:
                print("SakClass is empty!")
                return letters
            letter = random.choice(list(self.LETTER_QUANTITY.keys()))
            while self.LETTER_QUANTITY[letter] == 0:
                letter = random.choice(list(self.LETTER_QUANTITY.keys()))
            self.LETTER_QUANTITY[letter] -= 1
            letters.append(letter)
        self.numberOfLetters -= n
        return letters

    def putBackLetters(self, letters):
        """Puts back in the sack the letters """
        for letter in letters:
            if letter in self.LETTER_QUANTITY:
                self.LETTER_QUANTITY[letter] += 1
            else:
                print('wrong letter')
        self.numberOfLetters += len(letters)

    def randomizeSak(self):
        """Returns an array of 7 randomized letters"""
        return self.getLetters(7)

    def printSakStatus(self):
        """Prints information about the current status of the Sak """
        print("Letters left:", self.LETTER_QUANTITY, "\n Letters remaining: ", self.numberOfLetters)


class Player:
    current_letters = []
    score = 0

    def __init__(self, name):
        self.name = name

    def printCurrentLetters(self):
        print(self.current_letters)

    def printCurrentLettersFormatted(self):
        """prints current letters and their values in a formatted way"""
        print("Available letters and their values: ", end="")
        for letter in self.current_letters:
            print(f"{letter},{LETTER_VALUES[letter]} \t", end="")
        print()  # add a new line  at the end

    def getLetterValues(self, letters):
        """Receives an array of letters and returns a dictionary with the value of each letter """
        letter_values = {}
        for letter in letters:
            if letter in LETTER_VALUES:
                letter_values[letter] = LETTER_VALUES[letter]
        return letter_values


class Human(Player):

    def __init__(self, name):
        self.totalWordsHuman = 0
        self.totalPassesHuman = 0
        super().__init__(name)


class Computer(Player):

    def __init__(self, name):
        self.totalWordsComputer = 0
        self.totalPassesComputer = 0
        super().__init__(name)

    def play(self, game, algorithmOption):
        if algorithmOption == 1:
            # Play min letters algorithm
            return self.minLetters(game)
        elif algorithmOption == 2:
            # Play max letters algorithm
            return self.maxLetters(game)
        elif algorithmOption == 3:
            # Play smart algorithm
            return self.smart(game)

    def minLetters(self, game):
        print("--- Min letters algorithm ---")
        # Get all permutations of the available letters, starting with length 2
        perms = []
        for i in range(2, len(self.current_letters) + 1):
            for p in permutations(self.current_letters, i):
                perms.append(''.join(p))

        # Find the first valid word in the dictionary (assuming uppercase)
        with open('greek7.txt', 'r', encoding='utf-8') as f:
            for line in f:
                word = line.strip()
                if word in perms:
                    print("Word played by computer:", word, " - ", game.calculateWordPoints(word), " points")
                    game.wordsformed += 1
                    return word
        print("Computer could not find valid word. Computer is passing its turn!")
        return 'p'

    def maxLetters(self, game):
        print("--- Max letters algorithm ---")
        for i in range(len(self.current_letters), 1, -1):
            perms = [''.join(p) for p in permutations(self.current_letters, i)]
            with open('greek7.txt', 'r', encoding='utf-8') as f:
                for line in f:
                    word = line.strip()
                    if word in perms:
                        print("Word played by computer: ", word, " - ", game.calculateWordPoints(word), " points")
                        game.wordsformed += 1
                        return word
        print("Computer could not find valid word. Computer is passing its turn!")
        return 'p'

    def smart(self, game):
        print("--- Smart algorithm ---")

        # Get all permutations of the available letters, starting with length 2
        perms = []
        for i in range(2, len(self.current_letters) + 1):
            for p in permutations(self.current_letters, i):
                perms.append(''.join(p))

        # Find the valid words with the highest point value
        max_word = ''
        max_points = 0
        with open('greek7.txt', 'r', encoding='utf-8') as f:
            for line in f:
                word = line.strip()
                if word in perms:
                    points = game.calculateWordPoints(word)
                    if points > max_points:
                        max_word = word
                        max_points = points

        if max_word:
            print("Word played by computer: ", max_word, " - ", game.calculateWordPoints(max_word), " points")
            game.wordsformed += 1
            return max_word
        else:
            print("Computer could not find valid word. Computer is passing its turn!")
            return 'p'


class Game:
    wordsformed = 0

    def __init__(self, gameName):
        self.gameName = gameName

    def displayStartingScreen(self):
        """Displays the starting screen for the Scrabble game."""
        print("******** WELCOME TO SCRABBLE ********")
        print("-------------------------")
        print("1: Stats")
        print("2: Settings")
        print("3: Play")
        print("4: Quit")
        print("-------------------------")

    def printScore(self, pHuman, pComputer):
        print(f"Player: {pHuman.name} - Score: {pHuman.score}")
        print(f"Player: {pComputer.name} - Score: {pComputer.score}")

    def readWord(self, active_player):
        while True:
            word = input("Enter your word or press 'p' to pass your turn or press 'q' to quit: ")
            if word == 'q':
                return word
            elif word == 'p':
                # increase human player passes by one
                active_player.totalPassesHuman += 1
                return 'p'
            # Check if word cant be formed with the available letters and if it exists in the greek7.txt
            elif self.validateWord(active_player, word) and self.wordExists(word):
                # Increase words formed by one
                active_player.totalWordsHuman += 1
                # Print word points message
                print(f"Word played by {active_player.name}: {word} - {self.calculateWordPoints(word)} points")
                return word
            else:
                print("Invalid word. Please try again.")

    def validateWord(self, player, word):
        """Validates if the given word can be formed from the current_letters array"""
        available_letters = player.current_letters.copy()  # create a copy of current_letters
        for letter in word:
            if letter not in available_letters:
                print(f"---Word '{word}' can't be formed with the available letters---")
                return False
            available_letters.remove(letter)
        return True

    def wordExists(self, word):
        """Checks if the word is a valid word in greek7.txt"""
        with open('greek7.txt', 'r', encoding='utf-8') as f:
            for line in f:
                if word == line.strip():
                    self.wordsformed += 1
                    return True
        print(f"---Word '{word}' does not exist---")
        return False

    def calculateWordPoints(self, word):
        """Calculates the point value of a word based on the global LETTER_VALUES dictionary"""
        word_points = 0
        for letter in word:
            letter_points = LETTER_VALUES.get(letter, 99999)
            word_points += letter_points
        return word_points

    def printGameInfo(self, player, sak):
        print("******************************************************")
        print("Playing: ", player.name)
        print("Score: ", player.score)
        print("Available letters: ", player.current_letters)
        player.printCurrentLettersFormatted()
        print("Letters remaining in the sak: ", sak.numberOfLetters)
        print("******************************************************")

    def printGameInfoAfterMove(self, player, sak):
        print("------------------------------------------------------")
        print("Player:", player.name, "- Score:", player.score, "- Letters remaining in the sak:", sak.numberOfLetters)
        print("Available letters: ", player.current_letters)
        print("------------------------------------------------------")

    def setup(self, pHuman, pComputer, sak):
        # Initialize sak for human player
        pHuman.current_letters = sak.randomizeSak()
        # Initialize sak for pc player
        pComputer.current_letters = sak.randomizeSak()

    def end(self, pHuman, pComputer):
        if pHuman.score > pComputer.score:
            winner = pHuman.name
        elif pHuman.score < pComputer.score:
            winner = pComputer.name
        else:
            winner = 'Game is a tie'
        print("Goodbye!")
        print(f"Player: {pHuman.name} - Score: {pHuman.score} ")
        print(f"Player: {pComputer.name} - Score: {pComputer.score}")
        print(f"Winner: {winner}")
        # Save in a file game info like the winner, scores, number of words formed, number of passes etc
        self.saveGameStats(pHuman, pComputer, winner)
        sys.exit()

    def updateSak(self, sak, active_player, word):
        for letter in word:
            if letter in active_player.current_letters:
                active_player.current_letters.remove(letter)
        new_letters = sak.getLetters(7 - len(active_player.current_letters))
        active_player.current_letters.extend(new_letters)
        # print("Updated current letters:", active_player.current_letters)

    def passTurn(self, sak, active_player):
        sak.putBackLetters(active_player.current_letters)
        active_player.current_letters = sak.getLetters(len(active_player.current_letters))
        print("Turn passed. New available letters: ", active_player.current_letters)
        # print("LETTERS IN THE SAK:", sak.numberOfLetters)
        # print(sak.LETTER_QUANTITY)

    def changePlayer(self, active_player, pHuman, pComputer):
        if active_player == pHuman:
            active_player = pComputer
        else:
            active_player = pHuman
        return active_player

    def saveGameStats(self, pHuman, pComputer, winner):
        stats = {
            "winner": winner,
            "human_score": pHuman.score,
            "computer_score": pComputer.score,
            "human_name": pHuman.name,
            "computer_name": pComputer.name,
            "words_formed": self.wordsformed,
            "words_formed_human": pHuman.totalWordsHuman,
            "words_formed_computer": pComputer.totalWordsComputer,
            "passes_computer": pComputer.totalPassesComputer,
            "passes_human": pHuman.totalPassesHuman
        }
        with open("lastgamestats.json", "w") as f:
            json.dump(stats, f)

    def loadLastGameStats(self):
        try:
            with open("lastgamestats.json", "r") as f:
                stats = json.load(f)

            # extract the stats from the JSON object
            winner = stats["winner"]
            human_score = stats["human_score"]
            human_name = stats["human_name"]
            computer_score = stats["computer_score"]
            computer_name = stats["computer_name"]
            words_formed = stats["words_formed"]
            words_formed_human = stats["words_formed_human"]
            words_formed_computer = stats["words_formed_computer"]
            passes_human = stats["passes_human"]
            passes_computer = stats["passes_computer"]

            # print the stats to the console
            print("-------------------------------------------------")
            print("Last game stats:")
            print(f"Winner: {winner}")
            print(f"Player: {human_name} - Score {human_score}")
            print(f"Player: {computer_name} - Score {computer_score}")
            print(f"Total words formed: {words_formed}")
            print(f"Words formed by {human_name}: {words_formed_human}")
            print(f"Words formed by Computer: {words_formed_computer}")
            print(f"Total passes by {human_name}: {passes_human}")
            print(f"Total passes by Computer: {passes_computer}")
            print("-------------------------------------------------")
        except FileNotFoundError:
            print("-------------------------------------------------")
            print("No previous game stats found!")
            print("-------------------------------------------------")

    def displaySettingScreen(self):
        print("-----------------------------------------")
        print("Please select the algorithm that you wish the Computer to play with. Choose 1, 2 or 3")
        print("1 - MIN LETTERS")
        print("2 - MAX LETTERS")
        print("3 - SMART")
        print("-----------------------------------------")
