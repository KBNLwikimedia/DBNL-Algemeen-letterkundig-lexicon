# Describe what this file does

# The following code is PD-self & CC-zero
import os.path
import pandas as pd
from pathlib import Path

#https://www.geeksforgeeks.org/python-filter-list-of-strings-based-on-the-substring-list/
# def Filter(string, substr):
#     return [str for str in string if
#             any(sub[2:-2] in str for sub in substr)]


currentdir = os.path.dirname(os.path.realpath(__file__))  # Path of this .py file
parentdir=Path(currentdir).parent.parent #(grand)Parent folder path, see https://stackoverflow.com/questions/2860153/how-do-i-get-the-parent-directory-in-python
exceldir="_alfabetisch"
excelfile = "dbnl-all-alfabetisch-begrippen-A-Z-BesteVersieTotNuToe.xlsx"
excelpath = str(parentdir) + "\\" + str(exceldir) + "\\" + str(excelfile)
#print(excelpath)

# We'll extract two sheets
#1. 'Lemma-Links-LiteratuurTemp' // holding the *online literature references* to be matched with the literature in 'Literatuur_Klaar'
#2. 'Literatuur_Klaar' // holding *all literature references*, to which the online references in the sheet 'Lemma-Links-LiteratuurTemp' need to be matched

############ Sheet 1 #########################
sheetname1 = "Lemma-Links-LiteratuurTemp"
df1temp = pd.read_excel(excelpath, sheet_name=sheetname1, header=0)
df1temp.fillna(0, inplace=True) #fill empty cells with 0
#Only extract relevant columns
df1 = df1temp[['LemmaURL','LinkLabel', 'LinkURL']]

# From this df1 we want to extract a dict-list-tuple with the following structure:
# {
# 'https://www.dbnl.org/tekst/dela012alge01_01/dela012alge01_01_00015.php': [
# {'LinkLabel': 'Const van rhetoriken', 'LinkURL': 'https://www.dbnl.org/tekst/cast005cons01_01/downloads.php'}],
#
# 'https://www.dbnl.org/tekst/dela012alge01_01/dela012alge01_01_00016.php':[
# {'LinkLabel': 'Anastasio en de schaal van Richter', 'LinkURL': 'https://www.dbnl.org/tekst/over018anas01_01/'},
# {'LinkLabel': 'Filosofie van de algemene literatuurwetenschap', 'LinkURL': 'https://www.dbnl.org/tekst/buur004filo01_01/'},
# {'LinkLabel': 'Literatuur bij benadering', 'LinkURL': 'https://www.dbnl.org/tekst/beek009lite01_01/'}],
#
# 'https://www.dbnl.org/tekst/dela012alge01_01/dela012alge01_01_00091.php': [
# {'LinkLabel': 'Dizionario di abbreviature latine ed italiane', 'LinkURL': 'http://www.hist.msu.ru/Departments/Medieval/Cappelli/index.html'},
# {'LinkLabel': 'Lexicon abbreviaturarum; Wörterbuch lateinischer und italienischer Abkürzungen', 'LinkURL': 'http://inkunabeln.ub.uni-koeln.de/vdibProduction/handapparat/nachs_w/cappelli/cappelli.html'}],
#
# 'https://www.dbnl.org/tekst/dela012alge01_01/dela012alge01_01_00108.php': [
# {'LinkLabel': 'Aeneïs', 'LinkURL': 'http://www.hs-augsburg.de/~harsch/Chronologia/Lsante01/Vergilius/ver_ae00.html'},
# {'LinkLabel': 'Anders of beter: emulatie in de renaissancistische literatuurtheorie', 'LinkURL': 'https://www.dbnl.org/tekst/_zev001200501_01/_zev001200501_01_0017.php'},
# {'LinkLabel': 'Gysbreght van Aemstel', 'LinkURL': 'https://www.dbnl.org/tekst/vond001gysb01_01/'},
# {'LinkLabel': 'Iphigeneia in Aulis', 'LinkURL': 'http://classics.mit.edu/Euripides/iphi_aul.html'},
# {'LinkLabel': 'Jephtes sive votum', 'LinkURL': 'http://visualiseur.bnf.fr/Visualiseur?Destination=Gallica&O=NUMM-052289'},
# {'LinkLabel': 'Jeptha', 'LinkURL': 'https://www.dbnl.org/titels/titel.php?id=vond001jept01'}],
# ...
# }

#https://stackoverflow.com/questions/51244920/pandas-dataframe-to-dict-while-keeping-duplicate-rows
matching_dict = dict(df1.set_index('LemmaURL').groupby(level = 0).apply(lambda x : x.to_dict(orient= 'records')))  # Has above data structure
#print(matching_dict) # Has above data structure

############ Sheet 2 #########################
sheetname2 = "Literatuur_Klaar"
df2temp = pd.read_excel(excelpath, sheet_name=sheetname2, header=0)
df2temp.fillna(0, inplace=True) #fill empty cells with 0
#Only extract relevant columns
df2 = df2temp[['LemmaURL', 'Literatuur']]
literature_dict = dict(df2.set_index('LemmaURL').groupby(level = 0).apply(lambda x : x.to_dict(orient= 'list')))
#print(literature_dict)

# 'https://www.dbnl.org/tekst/dela012alge01_01/dela012alge01_01_00942.php':
# {'Literatuur':[
# 'G. Kazemier, In de voorhof der poëzie (1965), p. 194 e.v.',
# 'J.C. Kamerbeek, ‘Problematiek van de vergelijkingen in Homerus’ Ilias’ in Forum der Letteren 3 (1962), p. 33-47',
# "J.L. Ready, Character, narrator, and simile in the 'Iliad' (2011)."
# ]},
# 'https://www.dbnl.org/tekst/dela012alge01_01/dela012alge01_01_00943.php':
# {'Literatuur':[
# 'B.J.H. Schulpen, Explorations in bilingual word recognition: cross-model, cross sectional and cross language effects (2003)',
# 'H.C. Whitford, A dictionary of American homophones and homographs with illustrative examples and exercises (1966)',
# 'J.P. Jaffré & C. Brissand, Morphographie & homophones verbaux (2006).'
# ]},
# 'https://www.dbnl.org/tekst/dela012alge01_01/dela012alge01_01_00944.php':
# {'Literatuur': [
# 'H.C. Whitford, A dictionary of American homophones and homographs with illustrative examples and exercises (1966).'
# ]},

############# Now do the matching #################
# Approach:
# Get 1st LemmaURL from matching_dict
# Find corresponding LemmaURL in literature_dict
# For that pair of corresponding LemmaURLs:
## Get first LinkLabel from matching_dict (for that specific LemmaURL)
## See if the value of LinkLabel occurs in any values of 'Literatuur' from literature_dict (for that specific LemmaURL)
## If a match is found, append (in a separate column/field) the LinkURL from matching_dict to the matched value from literature_dict (for that specific LemmaURL)
## Repeat for next LinkLabel .....

for LemmaURL1 in matching_dict.keys():
    #print('################## '+str(LemmaURL1)+' #################################')
    for LemmaURL2 in literature_dict.keys():
       if LemmaURL1 == LemmaURL2: #Find lemmas that have both urls/links in them, as well as literature sources

           #Create list of LinkLabels from matching_dict (for specific LemmaURL)
           linklabellist = [linkdict['LinkLabel'] for linkdict in matching_dict[LemmaURL1]]
           #print('linklabellist = ' + str(linklabellist))

           #Create list of literature references from literature_dict (for specific LemmaURL)
           litdict=literature_dict[LemmaURL1]
           litlist=litdict['Literatuur'] #list of literature sources
           #print('litlist = ' + str(litlist))

           # Now check for each element in 'linklabellist' if it is a substring of one of the elements from 'litlist'
           #https://www.geeksforgeeks.org/python-filter-list-of-strings-based-on-the-substring-list/
           if litlist: #Litlist does not always exist
               for linklabel in linklabellist:
                   for lit in litlist:
                       if linklabel[1:-1] in lit: #omit first 2 and last 2 chars from matching linklabel, increase to eg linklabel[8:-8] for looser matching
                          print('{}*****{}*****{}'.format(LemmaURL1,linklabel,lit)) #,linkdict['LinkURL']))
