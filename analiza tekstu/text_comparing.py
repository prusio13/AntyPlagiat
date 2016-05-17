import difflib
import Levenshtein
f1path = "text1.txt"
f2path = "text2.txt"

file1=open(f1path,"r")
file2=open(f2path,"r")
text1 = file1.read()
text2 = file2.read()

matching_blocks = list()
sm = difflib.SequenceMatcher(None,text1,text2)
matching_block_number = 0
matching_blocks_length = 0
max_length = (len(text1) if (len(text1) > len(text2)) else len(text1))
for block_info in sm.get_matching_blocks():          #zwraca 3-el tablice zaw. pozycje bloku w pierwszym tekscie, drugim tekscie i dlugosc bloku
    #print ("a[%d] and b[%d] match for %d elements" % block)
    if(block_info[2]>0):
        print("---------------------------------------------------")
        block = text1[block_info[0]:block_info[0] + block_info[2]]
        print(block,"\nDlugosc bloku:", block_info[2])
        matching_block_number += 1
        matching_blocks_length += block_info[2]
        matching_blocks.append(block)

#sm2 = difflib.SequenceMatcher(None,text2,text1,autojunk=False)
# for block_info in sm.get_matching_blocks():          #zwraca 3-el tablice zaw. pozycje bloku w drugim tekscie, drugim tekscie i dlugosc bloku
#     if(block_info[2]>0):
#         print(block_info)
#         block = text1[block_info[1]:block_info[1] + block_info[2]]
#         if block not in matching_blocks:
#             print("---------------------------------------------------")
#             print(block,"Dlugosc bloku: ", block_info[2])
#             matching_block_number += 1
#             matching_blocks_length += block_info[2]
#             matching_blocks.append(block)
print("---------------------------------------------------")
print("Odleglosc Levenshteina: ",Levenshtein.distance(text2,text1)) #ile operacji na znakach nalezy wykonac aby z jedengo tekstu otrzymac drugi
print(Levenshtein.seqratio(text1,text2))
print("wykrytych blokow:", matching_block_number,"- %d" %matching_blocks_length,"/ %d znakow w tekscie" %len(text2),"-","%d%% pokrycia"%(matching_blocks_length/len(text2)*100))
file1.close()
file2.close()

