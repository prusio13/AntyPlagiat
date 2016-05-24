import difflib
import Levenshtein
import os
import re
from collections import Counter

f1path = "data/reportToCheck.txt"
f2path = ""
file1=open(f1path,"r", encoding='iso-8859-2')
text1 = file1.read().lower()
text1list = re.split("[^a-z]", text1)   #biore tylko ciagi zlozone ze znakow, reszte wycinam
text1list_clean = []
for word in text1list:
    if len(word)>0:
        text1list_clean.append(word)
text1list_clean.sort()  #alfabetycznie
print("wystapien slow: ", len(text1list_clean))
cnt = Counter()
for word in text1list_clean:    #zliczam wystapienia slow
    cnt[word] += 1
print (cnt)
print ("roznych slow: ", len(cnt))

# files_in_dir = os.listdir("data/reports/")
# for file_in_dir in files_in_dir:
#     f2path = "data/reports/" + file_in_dir
#     file2 = open(f2path, "r", encoding='iso-8859-2')    #kodowanie plikow windowsowych
#     text2 = file2.read().lower()
#     print ("Scanning file:", file_in_dir)
#
#     matching_blocks = list()
#     sm = difflib.SequenceMatcher(None, text1, text2)
#     matching_block_number = 0
#     matching_blocks_length = 0
#     max_length = (len(text1) if (len(text1) > len(text2)) else len(text1))
#     for block_info in sm.get_matching_blocks():  # zwraca 3-el tablice zaw. pozycje bloku w pierwszym tekscie, drugim tekscie i dlugosc bloku
#         # print ("a[%d] and b[%d] match for %d elements" % block)
#         if (block_info[2] > 50):
#             print("---------------------------------------------------")
#             block = text1[block_info[0]:block_info[0] + block_info[2]]
#             print(block)
#             print("\nDlugosc bloku:", block_info[2])
#             matching_block_number += 1
#             matching_blocks_length += block_info[2]
#             matching_blocks.append(block)
#
#     #print("Odleglosc Levenshteina: ", Levenshtein.distance(text2, text1))  # ile operacji na znakach nalezy wykonac aby z jedengo tekstu otrzymac drugi
#     #print(Levenshtein.seqratio(text1, text2))
#     print("wykrytych blokow:", matching_block_number, "- %d" % matching_blocks_length,
#           "/ %d znakow w tekscie" % len(text2), "-", "%d%% pokrycia" % (matching_blocks_length / len(text2) * 100))
#     file2.close()
#     print("#####################################################")


# file2 = open(f2path, "r", encoding='iso-8859-2')
# text2 = file2.read()
# print(text2)

file1.close()


