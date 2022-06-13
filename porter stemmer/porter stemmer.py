import sys

class PorterStemmer:

    def __init__(self):

        self.buffer = ""  # buffer for word to be stemmed
        self.k = 0
        self.k0 = 0
        self.offset = 0   # j is a general offset into the string

    def cons(self, i):
        """cons(i) is TRUE <=> b[i] is a consonant."""
        if self.buffer[i] == 'a' or self.buffer[i] == 'e' or self.buffer[i] == 'i' or self.buffer[i] == 'o' or self.buffer[i] == 'u':
            return 0
        if self.buffer[i] == 'y':
            if i == self.k0:
                return 1
            else:
                return (not self.cons(i - 1))
        return 1

    def m(self):
        n = 0
        i = self.k0
        while 1:
            if i > self.offset:
                return n
            if not self.cons(i):
                break
            i = i + 1
        i = i + 1
        while 1:
            while 1:
                if i > self.offset:
                    return n
                if self.cons(i):
                    break
                i = i + 1
            i = i + 1
            n = n + 1
            while 1:
                if i > self.offset:
                    return n
                if not self.cons(i):
                    break
                i = i + 1
            i = i + 1

    def vowelinstem(self):
        for i in range(self.k0, self.offset + 1):
            if not self.cons(i):
                return 1
        return 0

    def doublec(self, j):
        if j < (self.k0 + 1):
            return 0
        if (self.buffer[j] != self.buffer[j-1]):
            return 0
        return self.cons(j)

    def cvc(self, i):
        if i < (self.k0 + 2) or not self.cons(i) or self.cons(i-1) or not self.cons(i-2):
            return 0
        ch = self.buffer[i]
        if ch == 'w' or ch == 'x' or ch == 'y':
            return 0
        return 1

    def ends(self, s):
        length = len(s)
        if s[length - 1] != self.buffer[self.k]: # tiny speed-up
            return 0
        if length > (self.k - self.k0 + 1):
            return 0
        if self.buffer[self.k-length+1:self.k+1] != s:
            return 0
        self.offset = self.k - length
        return 1

    def setto(self, s):
        length = len(s)
        self.buffer = self.buffer[:self.offset+1] + s + self.buffer[self.offset+length+1:]
        self.k = self.offset + length

    def r(self, s):
        if self.m() > 0:
            self.setto(s)

    def step1ab(self):
        if self.buffer[self.k] == 's':
            if self.ends("sses"):
                self.k = self.k - 2
            elif self.ends("ies"):
                self.setto("i")
            elif self.buffer[self.k - 1] != 's':
                self.k = self.k - 1
        if self.ends("eed"):
            if self.m() > 0:
                self.k = self.k - 1
        elif (self.ends("ed") or self.ends("ing")) and self.vowelinstem():
            self.k = self.offset
            if self.ends("at"):   self.setto("ate")
            elif self.ends("bl"): self.setto("ble")
            elif self.ends("iz"): self.setto("ize")
            elif self.doublec(self.k):
                self.k = self.k - 1
                ch = self.buffer[self.k]
                if ch == 'l' or ch == 's' or ch == 'z':
                    self.k = self.k + 1
            elif (self.m() == 1 and self.cvc(self.k)):
                self.setto("e")

    def step1c(self):
        if (self.ends("y") and self.vowelinstem()):
            self.buffer = self.buffer[:self.k] + 'i' + self.buffer[self.k+1:]

    def step2(self):
        if self.buffer[self.k - 1] == 'a':
            if self.ends("ational"):   self.r("ate")
            elif self.ends("tional"):  self.r("tion")
        elif self.buffer[self.k - 1] == 'c':
            if self.ends("enci"):      self.r("ence")
            elif self.ends("anci"):    self.r("ance")
        elif self.buffer[self.k - 1] == 'e':
            if self.ends("izer"):      self.r("ize")
        elif self.buffer[self.k - 1] == 'l':
            if self.ends("bli"):       self.r("ble") # --DEPARTURE--
            # To match the published algorithm, replace this phrase with
            #   if self.ends("abli"):      self.r("able")
            elif self.ends("alli"):    self.r("al")
            elif self.ends("entli"):   self.r("ent")
            elif self.ends("eli"):     self.r("e")
            elif self.ends("ousli"):   self.r("ous")
        elif self.buffer[self.k - 1] == 'o':
            if self.ends("ization"):   self.r("ize")
            elif self.ends("ation"):   self.r("ate")
            elif self.ends("ator"):    self.r("ate")
        elif self.buffer[self.k - 1] == 's':
            if self.ends("alism"):     self.r("al")
            elif self.ends("iveness"): self.r("ive")
            elif self.ends("fulness"): self.r("ful")
            elif self.ends("ousness"): self.r("ous")
        elif self.buffer[self.k - 1] == 't':
            if self.ends("aliti"):     self.r("al")
            elif self.ends("iviti"):   self.r("ive")
            elif self.ends("biliti"):  self.r("ble")
        elif self.buffer[self.k - 1] == 'g': # --DEPARTURE--
            if self.ends("logi"):      self.r("log")
        


    def step3(self):
        if self.buffer[self.k] == 'e':
            if self.ends("icate"):     self.r("ic")
            elif self.ends("ative"):   self.r("")
            elif self.ends("alize"):   self.r("al")
        elif self.buffer[self.k] == 'i':
            if self.ends("iciti"):     self.r("ic")
        elif self.buffer[self.k] == 'l':
            if self.ends("ical"):      self.r("ic")
            elif self.ends("ful"):     self.r("")
        elif self.buffer[self.k] == 's':
            if self.ends("ness"):      self.r("")

    def step4(self):
        if self.buffer[self.k - 1] == 'a':
            if self.ends("al"): pass
            else: return
        elif self.buffer[self.k - 1] == 'c':
            if self.ends("ance"): pass
            elif self.ends("ence"): pass
            else: return
        elif self.buffer[self.k - 1] == 'e':
            if self.ends("er"): pass
            else: return
        elif self.buffer[self.k - 1] == 'i':
            if self.ends("ic"): pass
            else: return
        elif self.buffer[self.k - 1] == 'l':
            if self.ends("able"): pass
            elif self.ends("ible"): pass
            else: return
        elif self.buffer[self.k - 1] == 'n':
            if self.ends("ant"): pass
            elif self.ends("ement"): pass
            elif self.ends("ment"): pass
            elif self.ends("ent"): pass
            else: return
        elif self.buffer[self.k - 1] == 'o':
            if self.ends("ion") and (self.b[self.offset] == 's' or self.b[self.offset] == 't'): pass
            elif self.ends("ou"): pass
            # takes care of -ous
            else: return
        elif self.buffer[self.k - 1] == 's':
            if self.ends("ism"): pass
            else: return
        elif self.buffer[self.k - 1] == 't':
            if self.ends("ate"): pass
            elif self.ends("iti"): pass
            else: return
        elif self.buffer[self.k - 1] == 'u':
            if self.ends("ous"): pass
            else: return
        elif self.buffer[self.k - 1] == 'v':
            if self.ends("ive"): pass
            else: return
        elif self.buffer[self.k - 1] == 'z':
            if self.ends("ize"): pass
            else: return
        else:
            return
        if self.m() > 1:
            self.k = self.offset

    def step5(self):
        self.offset = self.k
        if self.buffer[self.k] == 'e':
            a = self.m()
            if a > 1 or (a == 1 and not self.cvc(self.k-1)):
                self.k = self.k - 1
        if self.buffer[self.k] == 'l' and self.doublec(self.k) and self.m() > 1:
            self.k = self.k -1

    def stem(self, p, i, j):
        self.buffer = p
        self.k = j
        self.k0 = i
        if self.k <= self.k0 + 1:
            return self.buffer

        self.step1ab()
        self.step1c()
        self.step2()
        self.step3()
        self.step4()
        self.step5()
        return self.buffer[self.k0:self.k+1]


if __name__ == '__main__':
    p = PorterStemmer()
    if len(sys.argv) > 1:
        for f in sys.argv[1:]:
            infile = open(f, 'r')
            while 1:
                output = ''
                word = ''
                line = infile.readline()
                if line == '':
                    break
                for c in line:
                    if c.isalpha():
                        word += c.lower()
                    else:
                        if word:
                            output += p.stem(word, 0,len(word)-1)
                            word = ''
                        output += c.lower()
                print(output,end=' ')
            infile.close()