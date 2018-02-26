class SearchAlgorithm:

    def __init__(self,word):
        self.en_yakın = []
        self.word = word

    def run(self,list_words, range_ = 1):
        result = []
        for word in list_words:
            if word not in result:
                if range_ == 1:
                    if len(word) == len(self.word):
                        result.append(word)
                elif range_ == 2:
                    if len(word) == len(self.word) or len(word) == len(self.word) - 1\
                    or len(word) == len(self.word) + 1:
                        result.append(word)
                elif range_ == 3:
                    if len(word) == len(self.word) or len(word) == len(self.word) -1 or len(word) == len(self.word) - 2 \
                    or len(word) == len(self.word) + 1 or len(word) == len(self.word) + 2:
                        result.append(word)
                elif range_ == 4:
                    if len(word) == len(self.word) or len(word) == len(self.word) -1 or len(word) == len(self.word) - 2 \
                    or len(word) == len(self.word) - 3 or len(word) == len(self.word) + 1 or len(word) == len(self.word) + 2 \
                    or len(word) == len(self.word) + 3:
                        result.append(word)
                elif range_ == 5:
                    if len(word) == len(self.word) or len(word) == len(self.word) -1 or len(word) == len(self.word) - 2\
                     or len(word) == len(self.word) - 3 or len(word) == len(self.word) - 4\
                     or len(word) == len(self.word) + 1 or len(word) == len(self.word) + 2 or len(word) == len(self.word) + 3 or len(word) == len(self.word) + 4:
                        result.append(word)
        return result
