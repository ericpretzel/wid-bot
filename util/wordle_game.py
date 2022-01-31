from random import randint
import config

class WordleGame:
    def __init__(self):
        self.word = self.get_word()
        self.guesses = set()
        self.result = None

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

    Also modifies the game's result.

    result -> True if game is won
           -> False if game is lost
           -> None if game is still going
    """
    def check(self, guess: str):
        if len(guess) != 5:
            raise InvalidGuessException('Please guess a **five** letter word.')
        if guess in self.guesses:
            raise InvalidGuessException('Already guessed that word!')
        if not self.is_valid(guess):
            raise InvalidGuessException(f'"{guess}" is not in the word list.')
        self.guesses.add(guess)

        if guess == self.word:
            self.result = True
        elif len(self.guesses) >= 6:
            self.result = False
        else: 
            self.result = None

        count = {c : self.word.count(c) for c in guess}
        emojis = ['' for _ in range(len(guess))]
        for i in range(len(guess)):
            if guess[i] == self.word[i]:
                emojis[i] = '🟩'
                count[guess[i]] -= 1
        for i in range(len(guess)):
            if guess[i] == self.word[i]: continue
            elif guess[i] in self.word and count[guess[i]] > 0:
                emojis[i] = '🟨'
                count[guess[i]] -= 1
            else:
                emojis[i] = '⬛'
        return emojis

class InvalidGuessException(Exception):
    pass
