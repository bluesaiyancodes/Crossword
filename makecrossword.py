import random
import pymysql


class Crossword:
    size = 0
    crossword_list = []

    def __init__(self):
        print("### Welcome to the crossword puzzle maker ###")
        while True:
            self.size = int(input("\nEnter the square size of crossword: "))
            if self.size < 3:
                print("Too small input. Enter another value.")
                print("subramania is a mad fellow")
                continue
            else:
                for i in range(0, self.size):
                    self.crossword_list.append([])
                    for j in range(0, self.size):
                        self.crossword_list[i].append(0)
                break

    def word_picker(self):
        query = "select sl,word from dictionary;"
        (words, count_words) = self.connect_database(query)
        for i in range(0, self.size):
            for j in range(0, self.size):
                if self.crossword_list[i][j] == 0:
                    random_int = random.randint(1, 1000)  # take a random number
                    for k in range(random_int, random_int + count_words - 1):  # init the for loop acc to rand int
                        rand_seed = k % count_words  # pick num based on dictionary size
                        word_to_place = words[rand_seed][1]
                        if self.word_placability(word_to_place, i, j, "across"):
                            # print(word_to_place + " at " + str(i) + ", " + str(j))
                            self.word_setting(word_to_place, i, j, "across")
                        elif self.word_placability(word_to_place, i, j, "down"):
                            # print(word_to_place + " at " + str(i) + ", " + str(j))
                            self.word_setting(word_to_place, i, j, "down")
                            break

                elif self.crossword_list[i][j] == "X":
                    continue



    def connect_database(self, query):
        try:
            db = pymysql.connect("localhost", "root", "Bishal-2583", "pythondbase")
            cursor = db.cursor()
            cursor.execute(query)
            data = cursor.fetchall()
            datacount = cursor.rowcount
        except:
            print("Unable to fetch information")
        db.close()
        words = []
        for i in data:
            words.append([i[0], i[1]])
        return words, datacount

    def word_placability(self, word, x, y, stat):
        if stat == "across":
            if len(word) > (self.size - y):
                return False
            else:
                for i in range(y, y + len(word)):
                    if self.crossword_list[x][i] != 0:
                        return False
        else:
            if len(word) > (self.size - x):
                return False
            else:
                for i in range(x, x+len(word)):
                    if self.crossword_list[i][y] != 0:
                        return False
        return True

    def word_setting(self, word, x, y, stat):
        if stat == "across":
            i = y
            for iter_aplha in word:
                self.crossword_list[x][i] = iter_aplha
                i += 1
            if i < self.size:
                self.crossword_list[x][i] = "X"
        else:
            i = x
            for iter_aplha in word:
                self.crossword_list[i][y] = iter_aplha
                i += 1
            if i < self.size:
                self.crossword_list[i][y] = "X"

    def view_crossword(self):
        print("")
        for i in range(0, self.size):
            for j in range(0, self.size):
                print(self.crossword_list[i][j], end="  ")
            print("")


crossword_obj = Crossword()
crossword_obj.word_picker()
crossword_obj.view_crossword()

print("program executed succefully")
