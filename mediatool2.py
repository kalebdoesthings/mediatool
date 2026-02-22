

#!/usr/bin/python3

import os
import time
import json
from colorama import Fore,Back,Style
import requests
from simple_term_menu import TerminalMenu
import pyfiglet
from thefuzz import process
import requests
from bs4 import BeautifulSoup
import os
from simple_term_menu import TerminalMenu
from colorama import Fore, Back, Style, init
import time
import asyncio
import re
from urllib.parse import unquote
import threading
from thefuzz import fuzz
from datetime import datetime
import configparser



def setup():
    print("Welcome to setup...")
    realdebridapikey = input("Real Debrid Api Key: ")
    config["CONFIG"]["REAL_DEBRID_API_KEY"] = realdebridapikey
    with open("config.ini", "w") as configfile:
        config.write(configfile)

    omdbapikey = input("OMDB Api Key: ")
    config["CONFIG"]["OMDB_API_KEY"] = omdbapikey
    with open("config.ini", "w") as configfile:
        config.write(configfile)

    print("Path Example: /home/user/media")    
    mediapath = input("Media Path (This will create a movies and tvshow directory): " )
    
    config["CONFIG"]["MEDIA_PATH"] = mediapath
    with open("config.ini", "w") as configfile:
        config.write(configfile)

    config["CONFIG"]["FIRST_LAUNCH"] = "1"
    with open("config.ini", "w") as configfile:
        config.write(configfile)
        
        

        







config = configparser.ConfigParser()
config.read("config.ini")
FIRST_LAUNCH = config["CONFIG"]["FIRST_LAUNCH"]

if FIRST_LAUNCH == "0":
    setup()

else:
    apikey = config["CONFIG"]["REAL_DEBRID_API_KEY"]
    omdbapikey = config["CONFIG"]["OMDB_API_KEY"]
    mediapath = config["CONFIG"]["MEDIA_PATH"]    

def moviesearch():
    movies = os.listdir(f"{mediapath}/movies/")
    count = 0
    print("| q | To go back to menu")
    print("| addmovie | to add movie")
    

    query = input("Which movie?: ")


    if query == "q":
        os.system("clear")
        choose()
    elif query == "addmovie":
        os.system("clear")
        scrape()

    movienames = []
    for movie in movies:
        score = fuzz.partial_ratio(movie,query)
        if score > 60:
            print(f"{Fore.GREEN}Match Found{Style.RESET_ALL}")
            count = count + 1
            print(score)
            movienames.append(movie)
        else:
            print(f"{Fore.RED}Not a match{Style.RESET_ALL}")
    print(f"Amount of matches: {count}")
    for name in movienames:
        print(name)
    input("Press ENTER to continue...")
    os.system("clear")
    moviesearch()

def scrape():

    options = []
    print("| search | search for if movie exists")
    print("| q | Go back to main menu")
    search = input("Input search term: ")
    background = input("Send to background? (y) (n)")
    if background == "y":
        sendtoback = True
    else:
        sendtoback = False
    if search == "q":
        os.system("clear")
        choose()

    elif search == "search":
        
        search()



    searchparse = search.replace(" ","%20").replace("-b", "")

    pagecount = 1
    start_time = time.perf_counter()

    def timenow(message):
        current_time = time.perf_counter()
        final_time = start_time - current_time
        print(f"[{final_time}] {message}")

    atags = []
    coun5 = 1

    def getdata(pagecount):
        url = f"https://rargb.to/search/{pagecount}/?search={searchparse}&category[]=movies"
        timenow("Starting Search Request...")

        response = requests.get(url)

        if response.status_code == 200:
            timenow(f"{Fore.GREEN}Status Code 200 OK{Style.RESET_ALL}")
        else:
            timenow(f"{Fore.RED}Error occured{Style.RESET_ALL}")

        htmlresponse = response.text
        soup = BeautifulSoup(htmlresponse, 'html.parser')
        atags = soup.find_all('a')

        blacklist = {
            "/torrent/the-eagle-2011-1080p-bluray-x265-hevc-10bit-aac-5-1-tigole-qxr-5294715.html",
            "/torrent/mommys-little-star-2022-720p-web-dl-aac2-0-h264-lbr-5296687.html",
            "/torrent/the-bridge-on-the-river-kwai-1957-1080p-bluray-1600mb-dd2-0-x264-galaxyrg-5296661.html",
            "/torrent/color-my-world-with-love-2022-hallmark-720p-webrip-hevc-poke-5295948.html",
            "/torrent/the-godfather-1972-rm4k-repack-1080p-bluray-x265-hevc-10bit-aac-5-1-tigole-qxr-5297358.html",
            "/torrent/the-good-neighbor-2022-1080p-webrip-dd5-1-x-264-evo-5294301.html",
            "/torrent/firestarter-2022-720p-bluray-800mb-x264-galaxyrg-5294643.html",
            "/torrent/the-winston-affair-1964-robert-mitchum-war-1080p-brrip-x264-classics-5296579.html"
        }
        



        for tag in atags:
            href = tag.get('href')
            if "/torrent/" in href:
                if "4k" in href:
                    timenow(f"{Fore.RED}Has 4k in name REJECTED{Style.RESET_ALL}")
                elif "2160" in href:
                    timenow(f"{Fore.RED}Has 2160 in name REJECTED{Style.RESET_ALL}")
                elif href in blacklist:
                    print("NO")        
                else:
                    options.append(href)
                    print(href)
                    print(pagecount)

    threadlist2 = []

    while coun5 != 4:
        thread = threading.Thread(target=getdata,args=(pagecount,))
        threadlist2.append(thread)
        coun5 += 1
        pagecount += 1
        time.sleep(0.1)
        timenow("Adding thread to list")

    for t in threadlist2:
        t.start()
        timenow(f"{Fore.GREEN}Starting {t}{Style.RESET_ALL}")

    timenow(f"{Fore.GREEN}Waiting for threads to finish... {Style.RESET_ALL}")

    for t in threadlist2:
        t.join()

    os.system("clear")
    timenow(f"{Fore.GREEN}Threads finished{Style.RESET_ALL}")

    options_set = set(options)
    options.clear()
    options.extend(options_set)

    magnetlinks = []
    siteforlink = []
    count = 0
    magnetcount = len(options)
    baseurl="https://rargb.to"

    torrent_info = {}


    def gathermagnetlinks(pathtotorrent):
        correctedurl = f"{baseurl}{pathtotorrent}"
        timenow(f"{Fore.GREEN}Generated URL {correctedurl}{Style.RESET_ALL}")

        siteforlink.append(correctedurl)
        timenow(f"Sending request to {correctedurl}")

        magnetlinkresponse = requests.get(correctedurl)
        timenow(f"{Fore.GREEN}Recieved response code 200 from request{Style.RESET_ALL}")

        parse = BeautifulSoup(magnetlinkresponse.text, 'html.parser')
        magnetlinkatags = parse.find_all('a')

        title = "Unknown title"
        h1 = parse.find("h1")
        if h1:
                title = h1.get_text(strip=True)


        magnet = None
        for a in parse.find_all('a'):
                href2 = a.get('href')
                if href2 and "magnet" in href2:
                    magnet = href2
                    break

        size = "Unknown"
        for tr in parse.find_all("tr"):
                tds = tr.find_all("td")
                if len(tds) == 2 and "Size" in tds[0].get_text():
                    size = tds[1].get_text(strip=True)
                    break
        if magnet:
                torrent_info[pathtotorrent] = {
                    "title": title,
                    "size": size,
                    "magnet": magnet
                }
                timenow(f"{Fore.GREEN}Stored: {title} ({size}){Style.RESET_ALL}")
        else:
                timenow(f"{Fore.RED}NO magnet found for {correctedurl}{Style.RESET_ALL}")
    threadlist = []
    count = 0

    


    for pathtotorrent in options:
        thread = threading.Thread(target=gathermagnetlinks, args=(pathtotorrent,))
        threadlist.append(thread)

    threadcount = len(threadlist)

    for t in threadlist:
        t.start()
        count += 1
        timenow("{Fore.GREEN}Initializing Thread{Style.RESET_ALL}")
        timenow(f"{count}/{threadcount})")

    timenow("Waiting for threads to finish")

    for t in threadlist:
        t.join()

    os.system("clear")
    timenow(f"{Fore.GREEN}Threads Finished{Style.RESET_ALL}")



    optionsparsed = ["[q] Quit","[r] Restart search"]
    count = 0
    optionscount = len(options)
    query = str(search)


    paired_results = []

    for path in options:
        count += 1
        timenow(f"Parsing options {Fore.GREEN}{count}/{optionscount}{Style.RESET_ALL} ")

        if path in torrent_info:
                info = torrent_info[path]
        
                title = info["title"]
                size = info["size"]
                magnet = info["magnet"]
        
                label = f"{title}  ({size})"
                
                paired_results.append((label, magnet))
                optionsparsed.append(label)
    os.system("clear")

    current_timern = time.perf_counter()
    timenownow = current_timern - start_time
    print(f"{Fore.GREEN}Took {timenownow}{Style.RESET_ALL}")

    terminal_menu = TerminalMenu(optionsparsed, title="CHOOSE")
    menu_entry = terminal_menu.show()




    


    if optionsparsed[menu_entry] == "[q] Quit":
        print(f"{Fore.RED}Quitting...{Style.RESET_ALL}")
        time.sleep(0.5)
        os.system('clear')
        choose()

    elif optionsparsed[menu_entry] == "[r] Restart search":
        print("Restarting...")
        time.sleep(0.5)
        os.system("clear")
        scrape()







    else:
                selected_index = menu_entry - 2
                title, magnet = paired_results[selected_index]                


                headers =  {

                "Authorization": f"Bearer {apikey}",
                "Accept": "application/json"

                }
                apiurl = "https://api.real-debrid.com/rest/1.0/torrents/addMagnet"
                
                payload = {"magnet": magnet}
                response = requests.post(apiurl, data=payload, headers=headers)
                data = json.loads(response.text)
                torrentId = data["id"]
                print(torrentId)
                print(response.text)

                apiurl2 =  f"https://api.real-debrid.com/rest/1.0/torrents/selectFiles/{torrentId}"
                print(apiurl2)


                fileSelect = {"files":  "all"}


                selectFilesResponse = requests.post(apiurl2, data=fileSelect, headers=headers)
                print(selectFilesResponse.text)
                apiurl3 = f"https://api.real-debrid.com/rest/1.0/torrents/info/{torrentId}"
                torrentDetails = requests.get(apiurl3, headers=headers)


                getLink = json.loads(torrentDetails.text)
                linkToUnrestrict = getLink["links"]
                print(linkToUnrestrict)

                print(torrentDetails.text)

                for i in linkToUnrestrict:
                    apiurl4 = "https://api.real-debrid.com/rest/1.0/unrestrict/link"
                    payload2 = {"link": i}
                    unrestrictionData = requests.post(apiurl4, data=payload2, headers=headers)

                    linkDownloadGet = json.loads(unrestrictionData.text)

                    downloadLink = linkDownloadGet["download"]
                    print(f"{Fore.GREEN}Sending download to background{Style.RESET_ALL}")
                    if sendtoback == True:
                        os.system(f"nohup wget -q -c -P {mediapath}movies/ '{downloadLink}' >/dev/null 2>&1 &")                    
                    else:
                        os.system(f"wget -P {mediapath}/movies/ {downloadLink}")
                    time.sleep(0.5)
                os.system("clear")
                scrape()






links = []

def tvshow():
    os.system("clear")
    os.system(f"cd {mediapath}/tvshow/")
    dirs = os.listdir(f"{mediapath}/tvshow/")
    tvoptions = ["[a] OMDB Automation", "[n] Add New","[q] Quit"]
    


    for dir in dirs:
        index = dirs.index(dir)
        tvoptions.append(f"{dir}")

    tvshowmenu = TerminalMenu(tvoptions)
    menu_entry = tvshowmenu.show()
    
    if tvoptions[menu_entry] == "[q] Quit":
        os.system("clear")
        choose()

    if tvoptions[menu_entry] == "[a] OMDB Automation":
    
            
            
            
            def getMovieData():
                try:
                    os.system("clear")
                    movieName = input("TV Show Name: ")
                    print(movieName)
                    movieNameParsed = movieName.replace(" ","+")
                    print(movieNameParsed)
                    os.system("clear")
                    
                    response = requests.get(f"http://www.omdbapi.com/?t={movieNameParsed}&apikey={omdbapikey}")
            
                    data = response.json()    
                    print("Received JSON data:")
                    print(json.dumps(data, indent=2))
                    totalSeasons = data["totalSeasons"]
                    showTitle = data["Title"]
                    print(showTitle)
                    print(totalSeasons)

                    showTitleParsed = showTitle.replace(" ","_")
                    print(showTitleParsed)

                    totalSeasonsInt = int(totalSeasons)

                    
                    os.system(f"mkdir {mediapath}/tvshow/{showTitleParsed}")
                    
                    while totalSeasonsInt != 0:
                        os.system(f"mkdir {mediapath}/tvshow/{showTitleParsed}/Season_{totalSeasonsInt}")
                        totalSeasonsInt = totalSeasonsInt - 1

                    tvshow()      
                except Exception as e:
                    print(f"Error: {e}") 
                    time.sleep(3)
                    getMovieData()
            getMovieData()
            
            
                    
            
    
    elif  tvoptions[menu_entry]  == "[n] Add New":
        os.system("clear")
        print("Name of show?")
        showName = input("Enter show name: ")
        os.system(f"mkdir {mediapath}/tvshow/{showName}")
        print(f"{showName} Added!")
        time.sleep(1)
        tvshow()
        
    else:
        os.system("clear")
        options2 = ["[s] Seasons","[r] Rename","[d] Download"]
        choicemenu = TerminalMenu(options2, title=f"{tvoptions[menu_entry]} Options") 
        indexthing = choicemenu.show()

        if options2[indexthing] == "[s] Seasons":
            os.system("clear")
            seasons = os.listdir(f"{mediapath}/tvshow/{tvoptions[menu_entry]}")
            for season1 in seasons:
                print(f"{season1}")

            seasonCount = int(input("Enter number of seasons: "))

            while seasonCount != 0:
                    os.system(f"mkdir {mediapath}/tvshow/{tvoptions[menu_entry]}/Season_{seasonCount}")
                    seasonCount = seasonCount - 1

            print("Seasons Added!")
            recount = os.listdir(f"{mediapath}/tvshow/{tvoptions[menu_entry]}")
            print(recount)
            time.sleep(1)
            tvshow()
                




        if options2[indexthing] == "[r] Rename":
            print(f"What do you want to rename {tvoptions[menu_entry]} to?")
            rename = input("Enter Input: ")
            os.system(f"mv {mediapath}/tvshow/{tvoptions[menu_entry]} {mediapath}/tvshow/{rename}")
            print(f"New name is {rename}")
            time.sleep(1)
            os.system("clear")
            choose()
        if options2[indexthing] == "[d] Download":
            def download():
                os.system("clear")
                showDir = os.listdir(f"{mediapath}/tvshow/{tvoptions[menu_entry]}")

                seasonsmenuoptions = ["[q] Quit"]

                for dir in showDir:
                    seasonmediacheck = os.listdir(f"{mediapath}/tvshow/{tvoptions[menu_entry]}/{dir}")    
                    combined = '\t'.join(seasonmediacheck)
                    mediafiletypes = ["mkv","mp4","mov","avi","wmv","webm","3gp"]
                
                    for mediatype in mediafiletypes:
                        if mediatype in combined:
                            seasonsmenuoptions.append(f"{dir} Media Files Found")
                            break
                        
                    else:
                        seasonsmenuoptions.append(dir)
                seasons_menu = TerminalMenu(seasonsmenuoptions)
                entry = seasons_menu.show()

                seasonentry = seasonsmenuoptions[entry].replace("Media Files Found", "")
            
            
                if seasonsmenuoptions[entry] == "[q] Quit":
                    tvshow()


        
                magnetlink = input("Enter Magnet Link: ")
                    
                apikey2 = "5AMHGCYIS6YMQ3IKEGJLQQ77J3HSPGPA5OS6QOFE2VXYFWA5QGTA"
            
                print(apikey2)
                headers =  {

                    "Authorization": f"Bearer {apikey2}",
                    "Accept": "application/json"

                    }

                if magnetlink != None:
                        
                        apiurl = "https://api.real-debrid.com/rest/1.0/torrents/addMagnet"
                        
                        payload = {"magnet": magnetlink}
                        response = requests.post(apiurl, data=payload, headers=headers)
                        data = json.loads(response.text)
                        torrentId = data["id"]
                        print(torrentId)
                        print(response.text)

                        apiurl2 =  f"https://api.real-debrid.com/rest/1.0/torrents/selectFiles/{torrentId}"
                        print(apiurl2)
                    

                        fileSelect = {"files":  "all"}
                    

                        selectFilesResponse = requests.post(apiurl2, data=fileSelect, headers=headers)
                        print(selectFilesResponse.text)
                        apiurl3 = f"https://api.real-debrid.com/rest/1.0/torrents/info/{torrentId}"
                        torrentDetails = requests.get(apiurl3, headers=headers)


                        getLink = json.loads(torrentDetails.text)
                        linkToUnrestrict = getLink["links"]
                        print(linkToUnrestrict)
                    
                        print(torrentDetails.text)

                        for i in linkToUnrestrict:
                            apiurl4 = "https://api.real-debrid.com/rest/1.0/unrestrict/link"
                            payload2 = {"link": i}
                            unrestrictionData = requests.post(apiurl4, data=payload2, headers=headers)

                            linkDownloadGet = json.loads(unrestrictionData.text)

                            downloadLink = linkDownloadGet["download"]
                            downloadtext = f"Starting Download For {downloadLink}"
                            os.system(f"echo {downloadtext}")
                            os.system(f"nohup wget {downloadLink} -P {mediapath}/tvshow/{tvoptions[menu_entry]}/{seasonsmenuoptions[entry]}/ >/dev/null 2>&1 &")
            
                                        
                        os.system("clear")
                        download()
        download()    


                        

                    
                


def movies():
    links = []
    os.system("cd {mediapath}/movies/")
    quit = False
    while quit == False:   
        print(f"[{Fore.GREEN}q{Style.RESET_ALL}] to go back.")
        magnetlink = input("Enter Magnet Link: ")
        print(magnetlink)
        os.system("clear")
        if magnetlink != "quit" and magnetlink != "done":
            links.append(magnetlink)
        print(links)


            
        headers =  {

        "Authorization": f"Bearer {apikey}",
        "Accept": "application/json"

        }


        
        if magnetlink == "q":
            print(f"{Fore.GREEN}Going back to main menu...{Style.RESET_ALL}")
            time.sleep(0.5)
            os.system("clear")
            choose()
        
        if magnetlink == "done":

            while links:
                
                apiurl = "https://api.real-debrid.com/rest/1.0/torrents/addMagnet"
                url = links[0]
                links.pop(0)
                payload = {"magnet": url}
                response = requests.post(apiurl, data=payload, headers=headers)
                data = json.loads(response.text)
                torrentId = data["id"]
                print(torrentId)
                print(response.text)

                apiurl2 =  f"https://api.real-debrid.com/rest/1.0/torrents/selectFiles/{torrentId}"
                print(apiurl2)
            

                fileSelect = {"files":  "all"}
            

                selectFilesResponse = requests.post(apiurl2, data=fileSelect, headers=headers)
                print(selectFilesResponse.text)
                apiurl3 = f"https://api.real-debrid.com/rest/1.0/torrents/info/{torrentId}"
                torrentDetails = requests.get(apiurl3, headers=headers)


                getLink = json.loads(torrentDetails.text)
                linkToUnrestrict = getLink["links"]
                print(linkToUnrestrict)
            
                print(torrentDetails.text)

                for i in linkToUnrestrict:
                    apiurl4 = "https://api.real-debrid.com/rest/1.0/unrestrict/link"
                    payload2 = {"link": i}
                    unrestrictionData = requests.post(apiurl4, data=payload2, headers=headers)

                    linkDownloadGet = json.loads(unrestrictionData.text)

                    downloadLink = linkDownloadGet["download"]
                    
                    os.system(f"wget -P {mediapath}/movies/ {downloadLink}")
    

                os.system("clear")


                

        if magnetlink == "quit":
            os.system("clear")
            print("Quitting...")
            quit = True
            
        




def choose():

    os.system("clear")
    
    result = pyfiglet.figlet_format("Mediatool V2")
    print(Fore.GREEN + result)
    print(Style.RESET_ALL)



    options = [
            "[m] Movies",
            "[t] TV Shows",
            "[s] Search",
            "[e] Edit Config",
            "[q] Quit"
        ]


    cursor_color = ("fg_white")
    highlightstyle = ("bg_blue", "fg_white")

    terminal_menu = TerminalMenu(


        options,
        title="┌──────────────────────────┐\n"
              "│        Main Menu         │\n"
              "└──────────────────────────┘",
        menu_cursor=">",
        cycle_cursor=True


    )
    menu_entry_index = terminal_menu.show()
    selection = options[menu_entry_index]




    print(f"You have selected: {selection}")

    if selection == "[e] Edit Config":
        setup()

    elif selection == "[m] Movies":
        print(Fore.GREEN + "You chose Movies!")
        time.sleep(0.5)
        print(Style.RESET_ALL)
        os.system("clear")
        options = ["Manual","RARBG Scrape"]
        moviechoose = TerminalMenu(options,title="Choose movie download type")
        menu_entry_index2 = moviechoose.show()
        selection = options[menu_entry_index2]
        if selection == "Manual":
            os.system("clear")
            movies()
        elif selection == "RARBG Scrape":
            os.system("clear")
            scrape()


        
    elif selection == "[t] TV Shows":
        print(Fore.GREEN + "You chose TV Shows!")
        time.sleep(0.5)
        print(Style.RESET_ALL)
        os.system("clear")
        tvshow()  



    elif selection == "[s] Search":
        os.system("clear")
        options = ["[m] Movies", "[q] Quit"]
        choosey = TerminalMenu(options,title="Search for stuff in media library")
        menu_entry3 = choosey.show()
        selection = options[menu_entry3]
        if selection == "[m] Movies":
            os.system("clear")
            moviesearch()
        elif selection == "[q] Quit":
            os.system("clear")
            choose()

    else:
        print(f"{Fore.RED}Quitting!{Style.RESET_ALL}")
        time.sleep(1)
        os.system("clear")
        exit()




choose()



















