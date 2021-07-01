#Scriptje om een alfabetische Wiki-lijst uit een Excel te maken

import pandas as pd
import requests
from datetime import datetime

# Get current time
now = datetime.now()
current_time = now.strftime("%H:%M:%S")

# Make list ['A','B','C'... 'Y','Z']
# https://www.pythonpool.com/python-alphabet/
var='A'
alphabets=[]
# starting from the ASCII value of 'a' and keep increasing the value by i.
alphabets=[(chr(ord(var)+i)) for i in range(26)]
print(alphabets)

# Template for the entire page
pageHeaderTemplate='''
=Lijst van letterkundige begrippen in het Nederlandse taalgebied=
{{{{Inhoud abc}}}}
 '''

# Template for a letter block (A, B, C..)
blockTemplate = '''
== {letter} ==
'''

# Template for a single line (Lemma) in the list
# When there is a WP:NL article for the lemma , http status=200
lineTemplate_linked = ''';[[{wparticle}]] : {shortdescription}
'''
# When there is NO WP:NL article for the lemma, http status=404
lineTemplate_unlinked = ''';{wparticle} : {shortdescription}
'''

pageFooterTemplate='''
==Externe links==
* {{{{Sjabloon:Bronvermelding ALL}}}}

[[:Categorie:Taallijsten|Categorie:Taallijsten]]
 '''

def writeLine_linked(wparticle,shortdescription):
    lineText =lineTemplate_linked.format(
    wparticle = wparticle.capitalize(),
    shortdescription = shortdescription
    )
    return lineText

def writeLine_unlinked(wparticle,shortdescription):
    lineText =lineTemplate_unlinked.format(
    wparticle = wparticle.capitalize(),
    shortdescription = shortdescription
    )
    return lineText

####################################################

require_cols = ['Lemma','LemmaURL','1eZin_KernachtigeDefinitie-DescriptionWikidataNL']
df = pd.read_excel('dbnl-all-alfabetisch-begrippen-A-Z-Bewerking Calvin_25062021.xlsx', sheet_name='Beschrijvingen_GroenKolomG', usecols = require_cols, skiprows = 0)
# https://stackoverflow.com/questions/50253753/how-to-replace-accents-in-a-column-of-a-pandas-dataframe
df['Lemma_forsort']=df['Lemma'].str.lower().str.normalize('NFKD').str.encode('ascii', errors='ignore').str.decode('utf-8')
df=df.sort_values(by='Lemma_forsort', ascending=True)
#print(df.head(60))
dflist = df.values.tolist()

pageText = pageHeaderTemplate.format()
for letter in alphabets:
    blockText = blockTemplate.format(letter=letter)
    pageText += blockText
    for i in range(len(dflist)):
        #print(df['Lemma'][i])
        if df['Lemma_forsort'][i].startswith(letter.lower()):
            wpnl_url="https://nl.wikipedia.org/wiki/" + df['Lemma'][i].capitalize()
            #print(wpnl_url.replace(' ','_'))
            result = requests.get(wpnl_url)
            if result.status_code == 200:  # the article exists
                lineText = writeLine_linked(df['Lemma'][i], df['1eZin_KernachtigeDefinitie-DescriptionWikidataNL'][i])
            elif result.status_code == 404:
                lineText = writeLine_unlinked(df['Lemma'][i], df['1eZin_KernachtigeDefinitie-DescriptionWikidataNL'][i])
            pageText += lineText

pageText += pageFooterTemplate.format()
print(pageText)

################################################################################################
################################################################################################
# Write output to Wikipedia:NL using the API
target_page = "Gebruiker:CalvinKeutgen/Lijst_van_letterkundige_begrippen" #on https://nl.wikipedia.org/wiki/
api_url = 'https://nl.wikipedia.org/w/api.php'

#Ensure user is permissioned for createeditmovepage, uploadfile, uploadeditmovefile
USER=u'OlafJanssen'
PASS=u'passwd' #The wikimedia passwd
USER_AGENT='OlafJanssen'
headers={'User-Agent': USER_AGENT}

# get login token and log in
payload = {'action': 'query', 'format': 'json', 'utf8': '', 'meta': 'tokens', 'type': 'login'}
r1 = requests.post(api_url, data=payload)
#print(r1)
login_token=r1.json()['query']['tokens']['logintoken']
login_payload = {'action': 'login', 'format': 'json', 'utf8': '','lgname': USER, 'lgpassword': PASS, 'lgtoken': login_token}
#print(login_payload)
r2 = requests.post(api_url, data=login_payload, cookies=r1.cookies)
cookies=r2.cookies.copy()
#print(cookies)
# We have now logged in and can request edit tokens thusly:
def get_edit_token(cookies):
        edit_token_response=requests.post(api_url, data={'action': 'query',
                                                    'format': 'json',
                                                    'meta': 'tokens'}, cookies=cookies)
        return edit_token_response.json()['query']['tokens']['csrftoken']

#Now actually perform the edit:
edit_payload={
     "action": "edit",
     "title": target_page,
     "text": pageText,
     "summary": "Testupload via API door Gebruiker:OlafJanssen @" + str(current_time),
     "format":"json",
     "token": get_edit_token(cookies)
}

edit_response=requests.post(api_url, data=edit_payload,cookies=cookies,headers=headers)
editdata = edit_response.json()
print(editdata)

