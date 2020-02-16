import requests
f=open('downloaded_file','wb+')
ufr = requests.get("https://sun9-60.userapi.com/c850636/v850636562/90953/BaeK3fP5KUw.jpg")
f.write(ufr.content)
f.close()
