from random import randint
import config

class WordleGame:
    """
    Starts a new game bound to a player
    Only one game can be played at a time by a player
    """
    def __init__(self, player):
        self.word = self.get_word()
        self.player = player
        self.guesses = set()
    
    """
    Return True if game is won
    Return False if game is lost
    Return None if game is still going
    """
    def result(self):
        if self.word in self.guesses:
            return True
        elif len(self.guesses) >= 6:
            return False
        return None

    def get_word(self):
        with open(config.WORDLE_WORD_LIST) as f:
            words = [s.strip() for s in f.readlines()]
            i = randint(0, len(words) - 1)
            return words[i]
    
    def is_valid(self, word):
        with open(config.FIVE_LETTER_WORDS) as f:
            return word in {s.strip() for s in f.readlines()}

    """
    Returns a list indicating the result of each letter.
    ⬛ - incorrect
    🟨 - correct, but wrong spot
    🟩 - correct, and right spot
    """
    def check(self, guess: str):
        if len(guess) != 5:
            raise InvalidGuessException('Please guess a **five** letter word.')
        if guess in self.guesses:
            raise InvalidGuessException('Already guessed that word!')
        if not self.is_valid(guess):
            raise InvalidGuessException(f'"{guess}" is not in the word list.')
        self.guesses.add(guess)
        result = []

        count = {c : self.word.count(c) for c in guess}

        for i in range(len(guess)):
            if guess[i] == self.word[i]:
                e = '🟩'
                count[guess[i]] -= 1
            elif guess[i] in self.word and count[guess[i]] > 0:
                e = '🟨'
                count[guess[i]] -= 1
            else:
                e = '⬛'
            result.append(e)
        return result

class InvalidGuessException(Exception):
    pass


