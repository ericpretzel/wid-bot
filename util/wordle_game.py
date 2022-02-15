from random import randint
import config

class WordleGame:
    """
    Represents a game of Wordle.
    """

    def __init__(self, hard: bool):
        self.word = self.get_word()
        self.guesses = list()
        self.result = None
        self.hard = hard
        self.keyboard = {c : '⬜' for c in 'qwertyuiopasdfghjklzxcvbnm'}

    def get_word(self) -> str:
        """
        Gets a random word from the curated Wordle word list.

        Most of the words in this list are very commonly used.
        """
        with open(config.WORDLE_WORD_LIST) as f:
            words = [s.strip() for s in f.readlines()]
            i = randint(0, len(words) - 1)
            return words[i]
    
    def is_valid(self, word: str) -> bool:
        """
        Returns true if word is a valid English five-letter word.
        """
        with open(config.FIVE_LETTER_WORDS) as f:
            return word in {s.strip() for s in f.readlines()}

    def check(self, guess: str) -> "list[str]":
        """
        Checks if the guess is valid, then modifies the result of the game and updates the letters that the player has used.

        esult is changed to: 
        
            - True if game is won

            - False if game is lost

            - None if game is still going

        hard mode:

            - all green letters must be re-used

            - must use same yellow letters as previous guess
        
        Returns `get_emojis_for(guess)` if all checks pass.
        """    
        if len(guess) != 5:
            raise InvalidGuessException('Please guess a **five** letter word.')
        if guess in self.guesses:
            raise InvalidGuessException('Already guessed that word!')
        if not self.is_valid(guess):
            raise InvalidGuessException(f'"{guess}" is not in the word list.')
        
        if self.hard and len(self.guesses) > 0:
            prev = self.guesses[-1]
            prev_emojis = self.get_emojis_for(prev)
            yellow_letters = []
            for i, c in enumerate(prev_emojis):
                if c == '🟨': yellow_letters.append(prev[i])

            for i, c in enumerate(guess):
                if prev_emojis[i] == '🟩':
                    if c != prev[i]:
                        raise InvalidGuessException("Hard mode: must use correct letters from previous guesses!")
                else:
                    if c in yellow_letters:
                        yellow_letters.remove(c)
            if len(yellow_letters) > 0:
                raise InvalidGuessException("Hard mode: must use correct letters from previous guesses!")
        
        self.guesses.append(guess)

        if guess == self.word:
            self.result = True
        elif len(self.guesses) >= 6:
            self.result = False
        else: 
            self.result = None

        emojis = self.get_emojis_for(guess)

        for i, c in enumerate(guess):
            if emojis[i] == '🟩':
                self.keyboard[c] = emojis[i]
            elif self.keyboard[c] == '⬜':
                self.keyboard[c] = emojis[i]
        
        return emojis

    
    def get_emojis_for(self, guess: str) -> "list[str]":
        """
        Returns a list indicating the result of each letter.

        ⬛ - incorrect

        🟨 - correct, but wrong spot

        🟩 - correct, and right spot
        """
        count = {c : self.word.count(c) for c in guess}
        emojis = ['' for _ in range(len(guess))]
        for i, c in enumerate(guess):
            if c == self.word[i]:
                emojis[i] = '🟩'
                count[c] -= 1
        for i, c in enumerate(guess):
            if c == self.word[i]: continue
            elif c in self.word and count[c] > 0:
                emojis[i] = '🟨'
                count[c] -= 1
            else:
                emojis[i] = '⬛'
        return emojis


class InvalidGuessException(Exception):
    pass
