import os
import xml.etree.ElementTree as ET
import sqlite3
import re
import shutil
from datetime import datetime

conn = sqlite3.connect('Books.db')

try:
    conn.execute("""CREATE TABLE Logging
                (Datetime datetime, Process text)""")
except sqlite3.OperationalError:
    print("Note: table 'Logging' already exists")
    conn.execute("""INSERT INTO Logging
                VALUES
                (datetime('now','localtime'), 'Error: table Logging already exists')""")

try:
    conn.execute("""CREATE TABLE Book_info
                (book_name text, number_of_paragraph int, number_of_words int, number_of_letters int,
                words_with_capital_letters int, words_in_lowercase int)""")
    conn.execute("""INSERT INTO Logging
                VALUES
                (datetime('now','localtime'), 'The table Book_info was created')""")
except sqlite3.OperationalError:
    print("Note: table 'Book_info' already exists")
    conn.execute("""INSERT INTO Logging
                VALUES
                (datetime('now','localtime'), 'Error: table Book_info already exists')""")
conn.commit()


class Parser:

    def __init__(self):
        self.directory = '../Project/Input/'
        self.files = os.listdir(self.directory)
        self.file = self.directory + '/'
        self.filter()
        self.getting_file()
        self.get_root()
        self.clean()
        self.book_title(book_name=0)
        self.get_formatted_text()
        self.counter_paragraph()
        self.get_word_list()
        self.counter_words()
        self.counter_letters()
        self.counter_words_with_capital_letters(words_with_capital_letters_count=0)
        self.counter_words_with_lower_case(lower_case_words_count=0)
        self.words_in_the_book()

    def filter(self):
        for i in self.files:
            file = self.file
            if not i.endswith(".fb2"):
                file += i
                shutil.move(file, '../Project/Incorrect_input/')
                conn.execute("""INSERT INTO Logging
                    VALUES
                    (datetime('now','localtime'), 'Files that don't have format .fb2 were moved to Incorrect_input.')
                    """)

    def getting_file(self):
        for i in self.files:
            file = self.file
            if i.endswith(".fb2"):
                file += i
                conn.execute("""INSERT INTO Logging
                            VALUES
                            (datetime('now','localtime'), 'File for parsing was found')""")
            else:
                conn.execute("""INSERT INTO Logging
                            VALUES
                            (datetime('now','localtime'), 'Error: The folder is empty')""")
            return i

    def get_root(self):
        self.root = ET.parse(self.getting_file()).getroot()
        return self.root

    def clean(self):
        for element in self.root.iter():
            element.tag = element.tag.partition('}')[-1]

    def book_title(self, book_name):
        for element in self.root.iter('book-title'):
            book_name = element.text
            break
        return book_name

    def get_formatted_text(self):
        words_only = []
        for section in self.root.iter('section'):
            for element in section.iter('p'):
                paragraph = element.text
                if paragraph:
                    words_only.append(paragraph)
        self.words_only = [i.replace('\xa0', '') for i in words_only if hasattr(i, 'replace')]
        return self.words_only

    def counter_paragraph(self):
        paragraphs = len(self.words_only)
        return paragraphs

    def get_word_list(self):
        self.word_list = []
        wordlist = []
        for i in self.words_only:
            wordlist1 = i.split()
            wordlist = wordlist + wordlist1
        for x in wordlist:
            x = re.sub(r"[,.—!@#*?:;«»\"\'()\']", "", x)
            if x != '':
                self.word_list.append(x)
        return self.word_list

    def counter_words(self):
        words_count = len(self.word_list)
        return words_count

    def counter_letters(self):
        symbols = '1234567890'
        letters = []
        for i in self.word_list:
            for m in i:
                if m in symbols:
                    continue
                letters.append(m)
        letters_count = len(letters)
        return letters_count

    def counter_words_with_capital_letters(self, words_with_capital_letters_count):
        for i in self.word_list:
            if i != i.lower():
                words_with_capital_letters_count += 1
        return words_with_capital_letters_count

    def counter_words_with_lower_case(self, lower_case_words_count):
        for i in self.word_list:
            if i == i.lower():
                lower_case_words_count += 1
        return lower_case_words_count

    def words_in_the_book(self):
        words_set = set()
        words = []
        count_words = []
        upper_cases = []
        for i in self.word_list:
            i_title = i.title()
            i_lower = i.lower()
            i_upper = i.upper()
            if i_title not in words_set:
                upper_case = self.word_list.count(i_title) + self.word_list.count(i_upper)
                count_word = upper_case + self.word_list.count(i_lower)
                words_set.add(i_title)
                words.append(i_title)
                count_words.append(count_word)
                upper_cases.append(upper_case)
        return words, count_words, upper_cases


if __name__ == '__main__':

    FB2Parser = Parser()

    book_name = FB2Parser.book_title(book_name=0)
    paragraphs = FB2Parser.counter_paragraph()
    count_words_in_the_book = FB2Parser.counter_words()
    count_letters = FB2Parser.counter_letters()
    counter_words_with_capital_letters = FB2Parser.counter_words_with_capital_letters(
                                                                                    words_with_capital_letters_count=0)
    counter_words_with_lower_case = FB2Parser.counter_words_with_lower_case(lower_case_words_count=0)

    conn.execute("""INSERT INTO Book_info
                            VALUES ('%s', '%d', '%d', '%d', '%d', '%d')"""
                 % (
                     book_name, paragraphs, count_words_in_the_book, count_letters, counter_words_with_capital_letters,
                     counter_words_with_lower_case
                     ))
    conn.commit()
    conn.execute("""INSERT INTO Logging
                        VALUES
                        (datetime('now','localtime'), 'The file was parsed and added to the table Book info')""")
    conn.commit()
    words_in_the_book_list, counter_words_in_the_book, words_in_the_book_with_upper_cases = FB2Parser.words_in_the_book()

    now = datetime.now()
    table_name = str(book_name) + '_' + str(now)
    conn.execute("""CREATE TABLE '{}'
                        (word text, count int, count_uppercase int)""".format(table_name))
    for i in range(len(words_in_the_book_list)):
        conn.execute("""INSERT INTO '%s'
                            VALUES ('%s', '%d', '%d')"""
                     % (table_name, words_in_the_book_list[i], counter_words_in_the_book[i],
                        words_in_the_book_with_upper_cases[i]))
        conn.commit()
    conn.execute("""INSERT INTO Logging
                        VALUES
                        (datetime('now', 'localtime'), 'Statistics about words from the file was add to the table')
                """)
    conn.commit()

    parsing_file = FB2Parser.getting_file()
    shutil.move(parsing_file, '../Project/Output/')
    conn.execute("""INSERT INTO Logging
                    VALUES
                    (datetime('now', 'localtime'), 'File was moved to the Output folder')""")
    conn.commit()
    conn.commit()

