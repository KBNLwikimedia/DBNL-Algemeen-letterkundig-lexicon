# From https://stackabuse.com/download-files-with-python/
import requests
import os
fh = open ('ImageURLs.txt' , 'r')
strData = fh.read()
fh.close()

listData = []
for row in strData.split("\n"):
	if row.strip() != '' :
		listData.append(row.strip())
	print(str(row.strip()))

print('Beginning file download with requests')

for strUrl in listData:
    r = requests.get(strUrl)
    localfilename=os.path.basename(strUrl) #https://stackoverflow.com/questions/18727347/how-to-extract-a-filename-from-a-url-append-a-word-to-it#18727481
    localpath='downloads/'+ str(localfilename)
    with open(localpath, 'wb') as f:
        f.write(r.content)



