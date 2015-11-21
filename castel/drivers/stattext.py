from collections import Counter
import decimal
import functools
import regex

from castel.drivers.engine import Engine

class Stattext(Engine):
    def __init__(self):
        self.total_words = None
        self.total_lines = None
        self.total_letters = None
        self.avg_letters_per_word = None
        self.precision = 1

    def get_total_words(self, text_wrapper):
        if not self.total_words:
            self.total_words = self._count_words(text_wrapper)

        return self.total_words

    def get_total_lines(self, text_wrapper):
        if not self.total_lines:
            self.total_lines = self._count_lines(text_wrapper)

        return self.total_lines

    def get_total_letters(self, text_wrapper):
        if not self.total_letters:
            self.total_letters = self._count_letters(text_wrapper)

        return self.total_letters

    def get_avg_letters_per_word(self, text_wrapper):
        if not self.avg_letters_per_word:
            self.avg_letters_per_word = self._avg_letters(text_wrapper,
                                                         precision=self.precision)

        return self.avg_letters_per_word

    def most_common_letter(self, text_wrapper):
        total_occurences = Counter()
        for line in text_wrapper:
            # L matches the letter \p is for matching a single point code
            # \p{L} matches any single letter
            letters = regex.findall(r'[\p{L}]', line.lower())
            total_occurences.update(letters)

        if not total_occurences:
            return

        letter_occurences = total_occurences.most_common()
        # we create a list of the letter with the same occurences of the
        # first most frequent letter found
        most_common = list(filter(lambda x: x[1] == letter_occurences[0][1],
                                  letter_occurences))
        result = ""
        # concatenate the results
        for letter in most_common:
            result = result + str(letter[0]) + " "

        return result.rstrip()    
    
    def _avg_letters(self, text_wrapper, precision=1):
        avg = 0
        tot_words = self.get_total_words(text_wrapper)
        if tot_words == 0:
            return 0
        text_wrapper.seek(0)
        tot_letters = self.get_total_letters(text_wrapper)
        avg = decimal.Decimal((tot_letters / tot_words))
      
        return float(round(avg, precision)) if precision > 0 else float(int(avg))

    def _count_letters(self, text_wrapper):
        total_letters = 0
        for line in text_wrapper:
            total_letters += len(regex.findall(r'[\p{L}]|\p{N}', line))

        return total_letters
    def _count_words(self, text_wrapper):
        total_words = 0
        for line in text_wrapper:
             # we exclude words formed just by signs (no unicode point letter or digit)
             words_list = list(filter(lambda x:regex.findall(r'[\p{L}|\p{N}]', x), line.split()))
             total_words += len(words_list)

        return total_words

    def _count_lines(self, text_wrapper):
        lines = -1
        for lines, line in enumerate(text_wrapper):
            pass
        return lines + 1
