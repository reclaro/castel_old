from abc import ABCMeta, abstractmethod

class Engine(metaclass=ABCMeta):

    def open_file(self, file_name):
        return open(file_name, encoding="utf-8")

    @abstractmethod
    def get_total_lines(self, text_wrapper):
        pass
    
    @abstractmethod
    def get_total_words(self, text_wrapper):
        pass

    @abstractmethod
    def most_common_letter(self, text_wrapper):
        pass

    @abstractmethod
    def get_avg_letters_per_word(self, text_wrapper):
        pass
