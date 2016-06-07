"""
report_to_check/raport do sprawdzenia - nowy raport dodany przez studenta
text2/skanowany raport/plik - istniejacy w bazie raport do ktorego przyrownywany jest raport do sprawdzenia
coverage - jaka czesc sprawdzanego raportu znajduje sie w innym raporcie (przykladowo: sprawdzany raport bedacy
    w calosci fragmentem innego bedzie mial wartosc coverage = 1)

wersja wykorzystujca find_longest_match (szybsze) i get_matching_blocks (wolniejsze)
po oznaczeniu przez pierwsza z metod plik oznaczony
    jako podejrzany nie jest skanowany przzez druga metode
"""

import difflib
import os
import re
from collections import Counter


class AnalyzedReport:
    file_path = ""
    matching_blocks = []
    matching_text_fragments = []
    coverage = 0

    def __init__(self, file_path, blocks, text_fragments, coverage):
        self.file_path = file_path
        self.matching_blocks = blocks
        self.matching_text_fragments = text_fragments
        self.coverage = coverage

    def get_info(self):
        print(self.file_path+" POKRYCIE: %.2f" % self.coverage)

# parametry
min_block_length = 50
min_coverage_limit = 0.15   # wymagany min stosunek dlugosci dopasowanych blokow do dlugosci raportu do sprawdzenia
f1path = "data/reportToCheck.txt"
existing_reports_dir = "data/reports/2016-/"
file1=open(f1path, "r", encoding='iso-8859-2')
report_to_check = file1.read().lower()
# wypisuje na biezaco wyniki porwnywania z kolejnymi tekstami/plikami
debug = False

similar_reports = []    # przechowuje obiekty typu AnalyzedReport
f2path = ""
files_in_dir = list(os.listdir(existing_reports_dir)) # list(["spraw_0001"])
for file_in_dir in files_in_dir:
    f2path = existing_reports_dir + file_in_dir
    file2 = open(f2path, "r", encoding='iso-8859-2')    # kodowanie plikow windowsowych
    text2 = file2.read().lower()
    text_fragments = list()
    if debug:
        print("Scanning file:", file_in_dir)
    matching_block_number = 0
    matching_blocks_length = 0

    report_to_check_tmp = report_to_check[:]
    sm = difflib.SequenceMatcher(text_fragments, report_to_check_tmp, text2)
    block_info = sm.find_longest_match(0, len(report_to_check_tmp), 0, len(text2))
    matching_block_length = block_info[2]
    while(matching_block_length > min_block_length):
        text_fragment = report_to_check_tmp[block_info[0]:block_info[0] + matching_block_length]
        matching_block_number += 1
        matching_blocks_length += matching_block_length
        text_fragments.append(text_fragment)
        report_to_check_tmp = report_to_check_tmp.replace(text_fragment, '')
        if debug:
            print("---------------------------------------------------")
            print(text_fragment)
            print(block_info)
        block_info = sm.find_longest_match(0, len(report_to_check_tmp), 0, len(text2))
        matching_block_length = block_info[2]

    coverage = matching_blocks_length / len(report_to_check)
    analyzed_report = AnalyzedReport(f2path, sm.get_matching_blocks(),text_fragments,coverage)
    if coverage > min_coverage_limit:
        similar_reports.append(analyzed_report)
        files_in_dir.remove(file_in_dir)
    file2.close()
    if debug:
        print("wykrytych blokow:", matching_block_number, "- %d" % matching_blocks_length,
              "/ %d znakow w tekscie" % len(report_to_check), "-", "%d%% pokrycia" % (coverage * 100))
        print("#####################################################")

for file_in_dir in files_in_dir:
    f2path = existing_reports_dir + file_in_dir
    file2 = open(f2path, "r", encoding='iso-8859-2')    # kodowanie plikow windowsowych
    text2 = file2.read().lower()
    text_fragments = list()
    if debug:
        print("Scanning file:", file_in_dir)
    matching_block_number = 0
    matching_blocks_length = 0
    sm = difflib.SequenceMatcher(None, report_to_check, text2, autojunk=False)
    # zwraca 3-el tablice zaw. pozycje bloku w report_to_check, w report_to_check, dlugosc tego bloku
    # ostatnia trojka zawiera same zera
    for block_info in sm.get_matching_blocks():
        # print ("a[%d] and b[%d] match for %d elements" % block)
        if block_info[2] > min_block_length:
            block = report_to_check[block_info[0]:block_info[0] + block_info[2]]
            if debug:
                print("---------------------------------------------------")
                print(block)
                print("\nDlugosc bloku:", block_info[2])
            matching_block_number += 1
            matching_blocks_length += block_info[2]
            text_fragments.append(block)

    coverage = matching_blocks_length / len(report_to_check)
    analyzed_report = AnalyzedReport(f2path, sm.get_matching_blocks(),text_fragments,coverage)
    if coverage > min_coverage_limit:
        similar_reports.append(analyzed_report)
        files_in_dir.remove(file_in_dir)
    file2.close()
    if debug:
        print("wykrytych blokow:", matching_block_number, "- %d" % matching_blocks_length,
              "/ %d znakow w tekscie" % len(report_to_check), "-", "%d%% pokrycia" % (coverage * 100))
        print("#####################################################")

print("Wynik skanowania: ")
for report in similar_reports:
    report.get_info()
file1.close()
