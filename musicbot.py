from bs4 import BeautifulSoup
import random
import urllib2
import time
import requests
import telepot
import unirest
import codecs
import urllib
import httplib
import base64
import os
from acrcloud.recognizer import ACRCloudRecognizer
import wget
import json


def handle(msg):
    content_type, chat_type,chat_id = telepot.glance(msg)
    username=msg['from']['first_name']
    chat_id=msg['from']['id']
    print(content_type)
    if( (content_type) == 'text') :
        command=msg['text']
        if(command == '/start'):
            bot.sendMessage(chat_id,WELCOME)
        elif ((command.split(' ', 1)[0]).lower()=='mood'):
            sendmoodsong(msg)
        elif (command.split(' ', 1)[0].lower()=='lyrics'):
            sendLyrics(msg)
        elif (command.split(' ', 1)[0].lower()=='video'):
            sendvideo(msg,command.split(' ', 1)[0])
        elif (command.split(' ', 1)[0].lower()=='audio'):
            sendvideo(msg,command.split(' ', 1)[0])
        elif (command.split(' ',1)[0].lower()=='quotes'):
            sendQuote1(msg)
        elif(command.lower() == 'top20' or command.lower() == 'top 20' ):
            top20(msg);
        elif(command.split(' ',1)[0].lower()=='musicreview'):
           musicreview(msg)
        elif(command.split(' ',1)[0].lower()=='artist'):
           artist(msg)
        else:
            bot.sendMessage(chat_id,'You have entered wrong keyword...')
            correction(command.split(' ', 1)[0],chat_id)
            bot.sendMessage(chat_id,'Please go through the instructions..')
            time.sleep(2)
            bot.sendMessage(chat_id,WELCOME)
    elif((content_type)=='photo'):
        moodbyimage(msg,chat_id)

    elif((content_type)=='voice'):
        collect_metadata(msg,chat_id)

    else:
        bot.sendMessage(chat_id,'You have entered wrong keyword...')
        bot.sendMessage(chat_id,'Please go through the instructions..')
        time.sleep(2)
        bot.sendMessage(chat_id,WELCOME)
        

def moodbyimage(msg,chat_id):
    print(msg)
    print(msg['photo'][2]['file_id'])
    file_id=msg['photo'][2]['file_id']
    filep=bot.getFile(file_id)
    print(filep)
    abc=filep['file_path']
    print(abc)
    newres="https://api.telegram.org/file/bot"+botid+"/"+abc
    print(newres)
    image(msg,newres)
    

def image(msg,newres):
    headers = {
       'Content-Type': 'application/json',
       'Ocp-Apim-Subscription-Key': '*******************************',
    }

    params = urllib.urlencode({
    })

    body={
     'url': str(newres),
        }
    
    print(body['url']+".............")
    chat_id=msg['from']['id'] 
    try:
        print(newres)
        conn = httplib.HTTPSConnection('api.projectoxford.ai')
        print(params)
        conn.request("POST", "/emotion/v1.0/recognize?%s" % params, str(body) , headers)
        response = conn.getresponse()
        data = response.read()
        print(data+"......")
        result = json.loads(data)
        print(result)
        happy=result[0]['scores']['happiness']
        sad=result[0]['scores']['sadness']
        print(happy)
        print(sad)

        if(happy<sad):
            print('asd')
            bot.sendMessage(chat_id,'Songs for your Sad mood- ')
            time.sleep(2)
            url='http://mr-jatt.com/'
            url1='http://mr-jatt.com/tag.php?t=Sad%20Song'
            try:
                you=urllib2.urlopen(url1)
                youhtml=you.read()
                you.close()
                soup=BeautifulSoup(youhtml,'html.parser')
                a=soup.find_all('a',{'href':True,'class':'touch'})
                for i in range(5):
                    print(a[i].string)
                    href1=url+a[i]['href']
                    href2=downloadlink(href1)
                    if(href2!=0):
                        bot.sendMessage(chat_id,href2)
            except Exception as e:
                print(e)
                bot.sendMessage(chat_id,'Not found')

        else:
            print('asd1')
            bot.sendMessage(chat_id,'Songs for your Happy mood- ')
            time.sleep(2)
            url='http://mr-jatt.com/'
            url1='http://mr-jatt.com/tag.php?t=Bhangra%20Song'
            print(url1)
            try:
                you=urllib2.urlopen(url1)
                print('a1')
                youhtml=you.read()
                you.close()
                print('a12')
                soup=BeautifulSoup(youhtml,'html.parser')
                print('a13')
                a=soup.find_all('a',{'href':True,'class':'touch'})
                print(len(a))
                for i in range(5):
                    print(a[i].string)
                    href1=url+a[i]['href']
                    href2=downloadlink(href1)
                    if(href2!=0):
                        bot.sendMessage(chat_id,href2)

            except Exception as e:
                print(e)
                bot.sendMessage(chat_id,'Not found')

        conn.close()

    except Exception as e:
        print('exception.......')
        bot.sendMessage(chat_id,'Please retake the photo')

 
def correction(song,id):
   headers = {
       'Content-Type': 'application/x-www-form-urlencoded',
       'Ocp-Apim-Subscription-Key': '********************************',
   }

   params = urllib.urlencode({
   })
  
   try:
       conn = httplib.HTTPSConnection('api.cognitive.microsoft.com')
       print('let me check')
       print(song+song)
       conn.request("POST", "/bing/v5.0/spellcheck/?%s" % params, "text="+song , headers)
       response = conn.getresponse()
       data = response.read()
       print(data)
       result = json.loads(data)
       if( (len(result['flaggedTokens'])) == 0 ):
           print('get the previous value')
           return song
       else:
           suggestions=result['flaggedTokens'][0]['suggestions'][0]['suggestion']
           #bot.sendMessage(id,'You have entered a wrong keyword')
           bot.sendMessage(id,'The correct keyword is -')
           bot.sendMessage(id,suggestions)
           conn.close()
           print('get the suggestions ')
           return suggestions

   except Exception as e:
        print("in corr exception")


def musicreview(msg):
    username=msg['from']['first_name']
    print('....'+username)
    chat_id=msg['from']['id']
    command=msg['text']
    print(chat_id)
    print(command)
    movie=command.split(' ',1)[1]
    movie=movie.replace(" ","-")
    movie=movie.lower()
    print(movie)
    url='http://www.glamsham.com/music/reviews/'+movie+'-music-review.asp'
    print(url)
    try :
        you=urllib2.urlopen(url)
        youhtml=you.read()
        you.close()
        soup=BeautifulSoup(youhtml,'html.parser')
        a=soup.find_all('div',{'style':'text-align:justify', 'class':'col-sm-12'})
        print(len(a))
        
        b=''
        for i in range(len(a)): 
           print i
           for j in range(165,len(a[i].text)):
              b+=a[i].text[j]
           bot.sendMessage(chat_id,b)
    except Exception as e:
         print(e)
         bot.sendMessage(chat_id,'Not found')

def artist(msg):
    username=msg['from']['first_name']
    print('....'+username)
    chat_id=msg['from']['id']
    command=msg['text']
    print(chat_id)
    print(command)
    artistname=command.split(' ',1)[1]
    artistname=artistname.replace(" ","-")
    artistname=artistname.lower()
    print(artistname)
    url='http://gaana.com/artist/'+artistname+'/songs'
    print(url)
    try :
        you=urllib2.urlopen(url)
        youhtml=you.read()
        you.close()
        soup=BeautifulSoup(youhtml,'html.parser')
        a=soup.find_all('a',{'class':'sng_c','data-type' : 'playSong'})
        print(len(a))
        if((len(a))!=0):
            for i in range(1,len(a),2):
                 if(i%3!=0):
                      print i
                      print(a[i]['href'])
                      bot.sendMessage(chat_id,a[i]['href'])

        if((len(a))==0):
            print("no data found")
            bot.sendMessage(chat_id,'no data found')

        
    except Exception as e:
        print(e)
        bot.sendMessage(chat_id,'Not found')
   
 
def top20(msg):
    username=msg['from']['first_name']
    print('....'+username)
    chat_id=msg['from']['id']
    command=msg['text']
    print(chat_id)
    print(command+command)
    url='http://www.radiomirchi.com/more/mirchi-top-20/'
    try:
        you=urllib2.urlopen(url)
        youhtml=you.read()
        you.close()
        soup=BeautifulSoup(youhtml,'html.parser')
        a=soup.find_all('h2')
        b=soup.find_all('img',{'src':'/main/MirchiTop20/images/playIcon.png'})
        print(len(a))
        print(len(b))
        for i in range(0,len(b),2):
           print i
           print(b[i].string)
           print(b[i]['data-vid-src'])
           bot.sendMessage(chat_id,b[i]['data-vid-src'])
    except Exception as e:
         print(e)
         bot.sendMessage(chat_id,'Not found')  

def sendQuote1(msg):
    
    print ('Message of menu wanted ',msg)
    username=msg['from']['first_name']
    chat_id=msg['from']['id']
    command=msg['text']

    
    myhtml = """ <h1>Just as Jesus created wine from water,we humans are capable of transmuting emotion into music.</h1><h1>Music is a moral law. It gives soul to the universe, wings to the mind, flight to the imagination, and charm and gaiety to life and to everything</h1><h1>Music can change the world because it can change people.</h1><h1>Music is a higher revelation than all wisdom and philosphy. Music is the electrical soil in which the spirit lives, thinks and invents</h1><h1>Music does bring people together. It allows us to experience the same emotions. People everywhere are the same in heart and spirit. No matter what language we speak, what color we are, the form of our politics or the expression of our love and our faith,music proves: We are the same.</h1>
  <h1>I have my own particular sorrows, loves, delights;and you have yours. But sorrow, gladness, yearning, hope, love, belong to all of us, in all times and in all places. Music is the only means whereby we feel these emotions in their universality.</h1><h1>Music washes away from the soul the dust of everyday life</h1><h1>Do you know that our soul is composed of harmony?</h1><h1>I think music in itself is healing. It's an explosive expression of humanity. It's something we are all touched by. No matter what culture we're from,everyone loves music.</h1><h1>There is no feeling, except the extremes of fear and grief, that does not find relief in music.</h1><h1>Music was my refuge. I could crawl into the space between the notes and curl my back to loneliness.</h1><h1>After silence, that which comes closest to expressing the inexpressible is music.</h1><h1>Without music life would be a mistake</h1><h1>If music be the food of love then play on</h1><h1>Where words fail, Music speaks</h1><h1>Music is forever; music should grow and mature with you, following you right on up until u die.</h1>"""

    mylist=[]
    for item in myhtml.split("</h1>"):
        if "<h1>" in item:
            mylist.append(item [ item.find("<h1>")+len("<h1>") : ])
            print(mylist)
    bot.sendMessage(chat_id,random.choice(mylist))


def sendLyrics(msg):
    username=msg['from']['first_name']
    chat_id=msg['from']['id']
    command=msg['text']
    command=command.split(' ',1)[1]
    p=command.index('-')
    songname=command[:p]
    songname=songname.replace(" ","")
    songname=songname.lower()
    artist=command[p+1:]
    artist=artist .replace(" ","")
    artist=artist.lower()
    find(artist,songname,chat_id,msg)

def sendmoodsong(msg):
    username=msg['from']['first_name']
    chat_id=msg['from']['id']
    command=msg['text']
    command=command.split(' ',1)[1]
    command.title()
    command1 = command+' Song'
    command1 = codecs.encode(command1,'utf-8')
    query = urllib.quote(command1)
    url='http://mr-jatt.com/'
    url1= "http://mr-jatt.com/tag.php?t=" + query
    try:
        you=urllib2.urlopen(url1)
        youhtml=you.read()
        you.close()
        soup=BeautifulSoup(youhtml,'html.parser')
        a=soup.find_all('a',{'href':True,'class':'touch'})
        for i in range(5):
            print(a[i].string)
            print(i)
            href1=url+a[i]['href']
            href2=downloadlink(href1)
            if(href2!=0):
                bot.sendMessage(chat_id,href2)

    except Exception as e:
        print(e)
        bot.sendMessage(chat_id,'Not found')

def downloadlink(href1):
    try:
        you1=urllib2.urlopen(href1)
        youhtml1=you1.read()
        you1.close()
        soup=BeautifulSoup(youhtml1,'html.parser')
        a=soup.find_all('a',{'href':True,'class':'touch'})
        print('........')
        print(a)
        z=[]
        if(len(a)!=0):
            for i in range(len(a)):
                print(a[i]['href'])
                z.append("".join(a[i]['href'].split()))
            return z[1]
        else:
            return 0
    except Exception as e:
        print(e)
        bot.sendMessage(chat_id,'Not found')
    



def sendAudio(msg,a):
    url1= "https://www.youtube.com"
    href1=url1+a[0]['href']
    print(href1)
    downloadaudio1(href1,msg)
    href2=url1+a[1]['href']
    print(href2)
    downloadaudio1(href2,msg)

def downloadaudio1(url,msg):
    baseurl='http://www.youtubeinmp3.com/download/?video='
    finalurl=baseurl+url
    print(finalurl)
    try:
        you=urllib2.urlopen(finalurl)
        youhtml=you.read()
        you.close()
        soup=BeautifulSoup(youhtml,'html.parser')
        a=soup.find_all('a',{'href':True,'class':'button button-gray'})
        a1=soup.find_all('a',{'href':True,'class':'button fullWidth'})
        print(len(a1))
        print('/////////')
        
        print(a1[0]['href'])
        print(a[1]['href'])

        print('//////')
        
        print('www.youtubeinmp3.com'+a1[0]['href'])
        print('...........')
        username=msg['from']['first_name']
        print('....'+username)
        chat_id=msg['from']['id']
        bot.sendMessage(chat_id,'www.youtubeinmp3.com'+a1[0]['href'])
        '''
        print(a[0]['href'])
        print(a[1]['href'])
        print(a[2]['href'])
        downloadaudio2(a[1]['href'],msg)
        '''
        print('end')
    except Exception as e:
        print(e)


def sendvideo(msg,typ):
    username=msg['from']['first_name']
    chat_id=msg['from']['id']
    command=msg['text']
    command=command.replace(' ','+')
    cd=command.split('+',1)
    c=''.join(cd[1])
    url='https://www.youtube.com/results?search_query='+c
    url1= "https://www.youtube.com"
    try:
        you=urllib2.urlopen(url)
        youhtml=you.read()
        you.close()
        soup=BeautifulSoup(youhtml,'html.parser')
        a=soup.find_all('a',{'href':True,'class':'yt-uix-sessionlink','aria-hidden':'true'})
        print(len(a))
        if(typ.lower()=='audio'):
           sendAudio(msg,a)
        else:
           for i in range(3):
               href1=url1+a[i]['href']
               bot.sendMessage(chat_id,href1)
    except Exception as e:
        print(e)
        bot.sendMessage(chat_id,'Not found')

    
def find(artist,song,id,msg):
    try:
        print('.'+artist+'.'+song+'.')
        urll='http://www.azlyrics.com/lyrics/%s/%s.html'%(artist,song)
        print(urll)
   
        try:
           atozfile=urllib2.urlopen(urll)
           atozhtml=atozfile.read()
           atozfile.close()
           soup=BeautifulSoup(atozhtml,'html.parser')
           a=soup.find_all('div')
           print ('lyrics found j%s' %a[22].text)
           if (a[22].text is not None):
               bot.sendMessage(id,a[22].text)
        except Exception as e:
            print("[Errno {0}] {1}".format(e.errno, e.strerror))
            lyrics1(msg)
        return 
    except Exception as e:
        return e


def lyrics1(msg):
    username=msg['from']['first_name']
    print('....'+username)
    chat_id=msg['from']['id']
    command=msg['text']
    command=command.split(' ',1)[1]
    p=command.index('-')
    songname=command[:p]
    print(songname)
    artist=command[p+1:]
    print(artist)
    songname1=songname.replace(' ','-')
    print(songname1)
    artist1=artist.replace(' ','-')
    print(artist1)
    s="-"
    dict=[songname1,artist1]
    final_str=s.join(dict)
    print(final_str)
    try:
        
        urll='http://www.lyricsbell.com/%s'%(final_str)
        print(urll)
        atozfile=urllib2.urlopen(urll)
        atozhtml=atozfile.read()
        atozfile.close()
        soup=BeautifulSoup(atozhtml,'html.parser')
        for row in soup.find_all('div',attrs={"class" :"lyrics-col"}):
            for script in soup("script"):
                soup.script.extract()
            print(row.text)

        bot.sendMessage(chat_id,row.text)
  
    except Exception as e:
        print('nhi milya')
        bot.sendMessage(chat_id,'no data found')
        return e


def collect_metadata(msg,chtid):
    
    file_id=msg["voice"]["file_id"]        
    filep=bot.getFile(file_id) 
    re = ACRCloudRecognizer(config)
    abc=filep["file_path"]        
    newres="https://api.telegram.org/file/bot"+botid+"/"+abc
    file_name = wget.download(newres)
    respon=re.recognize_by_file(file_name, 0)
    result = json.loads(respon)
    if(result["status"]["msg"]=="Success"):
        print(result)
        name=result["metadata"]["music"][0]["title"]
        artist=result["metadata"]["music"][0]["artists"][0]["name"]
        album=result["metadata"]["music"][0]["album"]["name"]
        bot.sendMessage(chtid,"Song Name : "+name+"\nArtist : "+artist+"\nAlbum : "+album)
    else:
        bot.sendMessage(chtid,"No data found\nPlease try again")

  
bot=telepot.Bot(botid)
config = {
    'host':'ap-southeast-1.api.acrcloud.com',
    'access_key':'*******************************',
    'access_secret':'vEusgif3DOH8b23VqJHzCiCylBC0QRCehpX7ceZl',
    'timeout':10
    }


bot.getMe()
bot.message_loop(handle)
print('Listening......')
WELCOME='''Hello.!!I am music bot.I can help you with almost everything and anything related to the music world.
You can seek my help by using these commands:

- /start-Introduction
- Audio songname - Want to listen to your favourite music offline.Let me know ,will download the song for you.
- Lyrics songname-artistname - Access the lyrics of any song.
- Video videoname - Why settle with audio,if video can be accessed.I will provide the online streaming of any music video available.
- Artist artistname-Dying to listen yo your favourite singers latest songs.Let me know his/her name will provide a playlist of their most loved songs.
- Selfie lover-Click a selfie and send it.I will detect your happy or sad mood and send a playlist accordingly.
- Recorded audio-Their is this one song you have been chanting for days but dont know the name so cant find it.Record an audio and send it to me I will tell the song name,artist name and the album name.
- Mood romantic - So romance is in the air.Let me know,will send a playlist of superhit romantic songs.
- Mood sad - Aww you are sad.Let me know,will send a playlist of some nice sad songs.
- Mood bhangra - So Moto for now is - Keep calm and bhangra on.Let me know,will send a playlist of punjabi bhangra songs.
- Mood funny - Want to laugh? Let me know,will send a playlist that will for sure tickle your funny bone.
- Quotes - Access to some soothing music quotes surely help at times.
- top20-Have missed out on latest songs? Let me know,will provide videos of the latest top ranked 20 songs on just one go.
'''

latitude=0.0
longitude=0.0
while 1:
    time.sleep(5)

