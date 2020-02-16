import requests
f=open('downloaded_file','wb+')
ufr = requests.get("")
f.write(ufr.content)
f.close()
