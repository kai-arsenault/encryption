#! /bin/python

class UserInfo:
    def __init__(self):
        self.message = input("Enter message: ")
        self.key = input("Enter key (must be integer): ")

    def NewInfo(self):
        self.__init__()


# This class can be used to manipulate (encrypt or decrypt) a message (ceaser and rail fence cipher) with a key
class Manipulate:
    def __init__(self, info):
        self.message = info.message
        self.key = int(info.key)
    
    # Ceaser cipher style substitution
    def __Substitution(self, key):
        newmsg = ""
        for i in range(len(self.message)):
            # Used function definition https://docs.python.org/3/library/functions.html#ord
            asciival = ord(self.message[i])
            if asciival > 32 or asciival < 126:
                # For all chr() used function definition https://docs.python.org/3/library/functions.html#chr
                if asciival + key > 126:
                    newmsg += chr((asciival + key) % 126 + 31)
                elif asciival + key < 32:
                    newmsg += chr((asciival + key) + 95)
                else:
                    newmsg += chr(asciival + key)
        self.message = newmsg

    # Ceaser cipher style substitution, encryption only    
    def __EncryptSubstitution(self):
        self.__Substitution(self.key)
    
    # Rail fence cipher style transposition, encryption only
    def __EncryptTransposition(self):
        rows = []
        for i in range(self.key + 1):
            rows.append('')
        counter = 0
        for i in range(len(self.message)):
            row = i % (self.key + (self.key - 2))       # Will reset the row every time it reaches the top row
            # If the row exceeds number of rows the key allows, then subtract multiples of two from the row size until resets
            if row >= self.key:
                counter += 2
                row = row - counter
            else:
                counter = 0
            rows[row] += self.message[i]
        newmsg = ""
        for i in range(self.key):
            newmsg += rows[i]
        self.message = newmsg
    
    # Decrypt a fully encrypted message
    def TripleDESEncrypt(self):
        for i in range(0, 3):
            self.__EncryptSubstitution()
            self.__EncryptTransposition()
        return self.message
    
    # Ceaser cipher style substitution, decryption only
    def __DecryptSubstitution(self):
        self.__Substitution(self.key * -1)
    
    # Rail fence cipher style transposition, decryption only
    def __DecryptTransposition(self):
        rows = []
        for i in range(self.key + 1):
            rows.append("")
        # Populate rows for decryptioni
        for i in range(self.key):
            # Populate first row for decryption
            if i == 0:
                sectionlength = 1 + int((len(self.message) - 1) / ((self.key - 1) * 2)) # Find how many 'peaks' in rail fence cipher
                rows[i] = self.message[:sectionlength]
                previous = sectionlength
            # Populate last row for decryption
            elif i == self.key - 1:
                if len(self.message) > self.key:
                    rows[i] = self.message[previous:]                                   # Remaining characters are in last row
            # Populate all other rows for decryption
            else:
                peaktopeak = (self.key - 1) * 2
                sectionlength = 2 * int((len(self.message) - 1) / peaktopeak)           # Guarunteed minimum length of section
                remaining = (len(self.message) - 1) % peaktopeak                        # Remaining characters past each peak to peak
                # Two extra characters for td sr3e row
                if remaining >= peaktopeak - i:
                    sectionlength += 2
                # One extra characters for the row
                elif remaining >= i:
                    sectionlength += 1
                rows[i] = self.message[previous:(sectionlength + previous)]
                previous += sectionlength
        # Use the previously populated rows to then decrypt the message
        newmsg = ""
        counter = 0
        stringindex = []
        for i in range(self.key):
            stringindex.append(0)
        # For each character in the message access each of the populated row arrays and grab the appropraite character
        for i in range(len(self.message)):
            row = i % (self.key + (self.key - 2))       # Will reset the row every time it reaches the top row
            # If the row exceeds number of rows the key allows, then subtract multiples of two from the row size until resets 
            if row >= self.key:
                counter += 2
                row = row - counter
            else:
                counter = 0
            newmsg += rows[row][stringindex[row]]
            stringindex[row] += 1
        self.message = newmsg
    
    # Decrypt a fully encrypted message
    def TripleDESDecrypt(self):
        for i in range(0, 3):
            self.__DecryptTransposition()
            self.__DecryptSubstitution()
        return self.message
    
    # Full encryption and then full decryption
    def FullTripleDES(self):
        self.TripleDESEncrypt()
        print("\nEncrypted Message:", self.message)
        self.TripleDESDecrypt()
        print("Decrypted Message:", self.message)


# Main()
info = UserInfo()
manipulate = Manipulate(info)
manipulate.FullTripleDES()
