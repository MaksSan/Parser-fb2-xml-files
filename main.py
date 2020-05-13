import os
import xml.etree.ElementTree as ET
import sqlite3

class Task1:

    def __init__(self, filename):
        self.root = ET.parse(filename).getroot()
        self.clean()
        self.book_title()
        self.clean_print()
        self.un_words()
        self.create_db()

    def clean(self):
        for element in self.root.iter():
            element.tag = element.tag.partition('}')[-1]

    def book_title(self):
        self.book_title = 0
        for element in self.root.iter('book-title'):
            self.book_title = element.text
            break

    def remove_symbols(self, paragraph):
        symbols_to_remove = [',', '.', '—', '!', '?', ':', '«', '»', '"', '(', ')', '\xa0']
        for symbol in symbols_to_remove:
            if symbol in paragraph:
                paragraph = paragraph.replace(symbol, '')
        return paragraph

    def clean_print(self):
        self.number_of_paragraphs = 0
        self.number_of_words = 0
        self.number_of_letters = 0
        self.number_words_with_capital_letters = 0
        self.number_words_in_lowercase = 0
        self.unique_words = dict()
        self.count_uppercase = 0
        self.count_uppercase = 0

        for element in self.root.iter('p'):
            paragraph = element.text
            if paragraph:
                self.number_of_paragraphs += 1

                words_only = self.remove_symbols(paragraph)
                list_of_words = words_only.split(' ')
                self.number_of_words += len(list_of_words)      #Numbers of words

                letters_only = words_only.replace(' ', '')
                self.number_of_letters += len(letters_only)     #Nembers of letters

                for word in words_only.split():
                    if word != word.lower():
                        self.number_words_with_capital_letters += 1            #Number words with capital letters
                    else:
                        self.number_words_in_lowercase += 1                     #Number words in lowercase

                for word in list_of_words:
                    if word in self.unique_words:
                        self.unique_words[word] = self.unique_words[word] + 1
                    else:
                        self.unique_words[word] = 1                                 #Unique words

                for word in words_only.split():
                    if word[0].isupper():
                        self.count_uppercase += 1

    def un_words(self):
        self.wordsjust = ()
        self.count_of_unique_word = 0
        for word in self.unique_words:
            self.wordsjust = word
            self.count_of_unique_word = self.unique_words[word]

    def create_db(self):
        conn = sqlite3.connect("first_db.db")
        cursor = conn.cursor()

        cursor.execute("""CREATE TABLE information
                          (book_name text, number_of_paragraphs integer, number_of_words integer,
                           number_of_letters integer, number_words_with_capital_letters integer,
                           number_words_in_lowercase integer)
                       """)

        cursor.execute("""CREATE TABLE addition
                                  (wordsjust text, count integer, count_uppercase integer)
                               """)

        cursor.execute("""INSERT INTO information VALUES (?,?,?,?,?,?)""",
                   (self.book_title, self.number_of_paragraphs, self.number_of_words, self.number_of_letters,
                    self.number_words_with_capital_letters, self.number_words_in_lowercase)
                   )

        cursor.execute("""INSERT INTO addition VALUES (?,?,?)""",
                       (self.wordsjust, self.count_of_unique_word, self.count_uppercase)
                       )

        conn.commit()


if __name__ == '__main__':
    Task1('example.fb2')