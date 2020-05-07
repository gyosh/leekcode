import re

class PhraseIterator:
    def __init__(self, s):
        self.s = s
        self.p = 0
        self.len = len(s)

    def find_next(self, phrase):
        d = 0
        l_phrase = len(phrase)
        while self.p + d + l_phrase - 1 < self.len:
            match = True
            for i in range(l_phrase):
                if phrase[i] != self.s[self.p + d + i]:
                    match = False
                    break
            if match:
                return d
            d += 1
        return -1

    # Forward phrase
    def skip(self, phrase):
        if self.find_next(phrase) != 0:
            raise Exception('Unable to skip {}: `{}`'.format(phrase, self.__look_ahead()))
        self.p += len(phrase)

    def skip_r(self, rgx):
        cur_s = ''
        pattern = re.compile('^' + rgx + '$')
        while (self.p < self.len) and bool(re.match(pattern, cur_s + self.s[self.p])):
            cur_s += self.s[self.p]
            self.p += 1
        return cur_s

    def can_skip(self, phrase):
        return self.find_next(phrase) == 0

    # Find right after phrase
    def seek(self, phrase):
        d = self.find_next(phrase)
        if d == -1:
            raise Exception('Unable to seek {}: `{}`'.format(phrase, self.__look_ahead()))
        e_idx = self.p + d
        between = self.s[self.p:e_idx]
        self.p = e_idx + len(phrase)
        return between

    def seek_one(self, phrases):
        for p in phrases:
            if self.find_next(p) != -1:
                return self.seek(p)
        return -1

    def current_char(self):
        return self.s[self.p]

    def next_char(self):
        ret = self.s[self.p]
        self.p += 1
        return ret

    def end(self):
        return self.p == self.len

    def __look_ahead(self, size=50):
        e_idx = min(self.p + size, self.len)
        return self.s[self.p:e_idx] + '...'