'''
HX edited for endnote20. This script only suit for MacOS. 
Origin script comes from Bill Seufzer, NASA.
You can see orig script in https://community.endnote.com/t/scripting-endnote/260221
Thx for Bill's sharing!
'''
from appscript import *
import unicodedata
import string

en = app('Endnote 20')

theListOfRefs = en.retrieve(u'shown', records_in=en.documents[1])
# cite_key_list contain all row cite_key (i.e., without duplicate case's suffix)
cite_key_list = list()
alphabet = list(string.ascii_lowercase) # a list contain lowercase letters from 'a' -> 'z'
for aRef in theListOfRefs:
   # get the unformatted record
   unf_rec = en.unformatted_record(aRef)
   # unf_rec will look like {Armstrong, 1969 #1}
   # find the positions of the comma, #, and the }
   comPos=unf_rec.find(',')
   hashPos=unf_rec.find('#')
   end=unf_rec.find('}')
   author=unf_rec[1:comPos]
   #remove any spaces from the authors name and replace with '_'
   # BibTex does not like spaces in the citation key
   spaces=author.count(' ')
   if spaces > 0:
      author=author.replace(' ','_')
   if len(author) == 0:
      author='No_Author'
   year=unf_rec[comPos+2:hashPos-1]
   if len(year) == 0:
      year='xxxx'
   rec_num=unf_rec[hashPos+1:end]

   # assemble the citation key
   cite_key = author + '_' + year
   key_freq = cite_key_list.count(cite_key)
   cite_key_list.append(cite_key) # append only cite_key without suffix 
   # if dumplcate cite_key, give it a suffix based on freq and alhpabet
   if key_freq > 0 : 
      cite_key = cite_key + alphabet[key_freq]
   # this flattens the citation key into ascii
   # cite_key = unicodedata.normalize('NFKD',cite_key).encode('ascii','ignore')
   print(cite_key)
   # put the cite key into EndNote Label field
   en.set_field('Label',to=cite_key, of_record=aRef)

