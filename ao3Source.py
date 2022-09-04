# this class is for the ao3 link
import mechanicalsoup
from bs4 import BeautifulSoup
import requests
import time
from datetime import date
from datetime import datetime
from pathlib import Path, PurePath
import requests
import urllib
import re


class AO3Fic:
    def __init__(self):
        self.ficName='fgfhgjf'
        self.ficAuthor=''
        self.isChapterFic=False
        self.isSub=False
        self.ficID=''
        self.ficLink=''
        self.lastUpdate=''
        self.downloadDate=''
        self.chapterCount=''

        

    def getFicName(self):
        return self.ficName
    def getFicAuthor(self):
        return self.ficAuthor
    def setFicLink(self, link):
        self.ficLink=link
    def setFicName(self, name):
        self.ficName=name
    def setFicAuthor(self, author):
        self.ficAuthor=author
    def setFicID(self, ID):
        self.ficID=ID
    def setUpdateDate(self, updateDate):
        self.lastUpdate=updateDate
    def setDownloadDate(self, downloadDate):
        self.downloadDate=downloadDate
    def setChapterCount(self, chapter):
        chapterCount=chapter.split('/')
        self.chapterCount=chapterCount[0]
    def setIsChapter(self, isChapter):
        self.isChapterFic=isChapter
    def getIsChapter(self):
        return self.isChapterFic
    def setIsSub(self, isSub):
        self.isSub=isSub
    def getIsSub(self):
        return self.isSub
    def __str__(self):
        return f"{self.ficName} by {self.ficAuthor}\n"
    def __repr__(self):

        return f"{self.ficName} by {self.ficAuthor}"


class AO3Data:

    def __init__(self):
        #open web browser
        self.browser=mechanicalsoup.StatefulBrowser()
        self.loginInfo=[]
        self.isLogin=False
        self.dlUsername=""
        self.dlType=0
        self.dlTypeName=""
        self.isReadyForDownload=False
        self.ficList=[]
        self.ficPageList=[]
        self.downloadLocation=''
        self.dlFileType=''
        self.ficCounter=0
        self.RequestCounter=0
        self.rateLimit=False
    #URL enders
    viewAdult = "view_adult=true"
    viewFull = "view_full_work=true"
    ao3Link = "https://archiveofourown.org"
    ao3User = "https://archiveofourown.org/users/"

    def setIsReadyForDL(self, value):
        self.isReadyForDownload=value
    def getIsReadyForDL(self):
        return self.isReadyForDownload
    
    def setDownloadLocation(self, dlLocation):
        self.downloadLocation=dlLocation
    def getDownloadLocation(self):
        return self.downloadLocation
    def reset(self):
        self.loginInfo=[]
        self.isLogin=False
        self.dlUsername=""
        self.dlType=0
        self.dlTypeName=""
        
    def setLogin(self, username, password):
        #this will be called by gui when user inputs username and password.
        self.loginInfo=[username, password]
        print(self.loginInfo)
    
    def Login(self):

        if( self.isLogin==True):
            "was logged in, now logging out"
            self.Logout()
        #open login page
        
        loginURL=self.ao3User + "login"
        linkWorks=False

        self.browser.open(loginURL)
        self.RequestCounter=self.RequestCounter+1
        print("REQUEST COUNTER IS "+str(self.RequestCounter))

        if self.browser.page is None:
            raise Exception("Rate Limit. Please wait a while before trying again.")
        #login payload
        payload= ({"user[login]": self.loginInfo[0],
                   "user[password]": self.loginInfo[1]})
        form = self.browser.select_form('form[action="/users/login"]')
        form.set_input(payload)
        self.browser.submit_selected()

        #if the url changed then login was successful
        if self.browser.url == loginURL:
            #throw exception
            raise Exception("Login Failed. Please check your username and password")
        else:
            #return a success
            self.isLogin=True
            print("login passed")
    def Logout(self):
        if self.isLogin == False:
            pass
        else:
            self.browser.open(self.ao3User+"logout")

            self.RequestCounter=self.RequestCounter+1
            form = self.browser.select_form('form[action="/users/logout"]')
            self.browser.submit_selected()
            #create soup object
            soup=self.browser.page
            if(soup.find(class_="logged-out") == None):
                raise Exception("Logout Failed")
            else:
                self.isLogin=False
                print("Logged out")
    def getBrowserPage(self):
        return self.browser.page
        
    def setUserName(self, username):
        #gets the username of the user who stuff wants to download
        print("user name is "+username)
        #check if username exists. If user does not exist page redirects to people/search
        userLink=self.ao3User+username
        linkWorks=False
        while (not linkWorks):
            self.browser.open(userLink)
            self.RequestCounter=self.RequestCounter+1
            print("REQUEST COUNTER IS "+str(self.RequestCounter))
            if self.browser.page is None:
                self.rateLimit=True
                time.sleep(60)
            else:
                self.rateLimit=False
                linkWorks=True

#        self.browser.open(self.ao3User+username)
#        self.RequestCounter=self.RequestCounter+1
        print("REQUEST COUNTER IS "+str(self.RequestCounter))
        #print(self.browser.page)
        if self.browser.page is None:
            print("rateLimit?")
            
        if (self.browser.url != (self.ao3User+username)):
            #throw an exception
            #user does not exist
            print("user does not exist")
            print(self.browser.url)
            raise Exception("User does not exist")
            pass
        else:
            self.dlUsername=username
            print(self.dlUsername)
            #set
            return "success"
        
    def checkDownloadValidity(self, downloadType, username):
        #if download type is 2 then that means subscriptions
        if (downloadType==2):
            #check if username = login
            if( not (self.isLogin) or (self.loginInfo[0] != username)):
                print(not self.isLogin)
                print(self.loginInfo[0])
                print(username)
                raise Exception("Cannot download subscription from that user")
        print("pass")

    def setDownloadType(self, downloadType):
        if(downloadType==0):
            self.dlTypeName="bookmarks"
        elif(downloadType==1):
            self.dlTypeName="works"
        elif(downloadType==2):
            self.dlTypeName="subscriptions"
        self.dlType=downloadType

    def saveSubs(self, storyList):
        for section in storyList:
            sectionLinks=section.find_all("a")
            workLink=self.ao3Link+(sectionLinks[0].get("href"))

            if "series" in workLink:
                time.sleep(1)
                linkWorks=false
                while (not linkWorks):
                    self.browser.open(workLink)
                    self.RequestCounter=self.RequestCounter+1
                    print("REQUEST COUNTER IS "+str(self.RequestCounter))
                    if self.browser.page is None:
                        self.rateLimit=True
                        time.sleep(60)
                    else:
                        self.rateLimit=False
                        linkWorks=True

                self.ficPageList.append(workLink)
                page=self.browser.page
                head=page.find_all("li", class_="blurb")
                self.saveWorks(head)
            else:
                self.ficList.append(AO3Fic())
                workName=sectionLinks[0].get_text()
                #check if anon
                if len(sectionLinks) == 1:
                    workAuthor= "Anonymous"
                else:
                    workAuthor=sectionLinks[1].get_text()
                workID=workLink.split("/")[-1]
                self.ficList[-1].setFicName(workName)
                self.ficList[-1].setFicAuthor(workAuthor)
                self.ficList[-1].setFicID(workID)
                self.ficList[-1].setFicLink(workLink)
                self.ficList[-1].setIsSub(True)
                print(self.ficList[-1])
                
    def saveWorks(self, storyList):
        #This creates and ao3Fic object for every story in list
        for section in storyList:

            
            
            
            header=section.find("div", class_="header module")
            if header is None:
                #header is none when bookmark has been deleted
                continue
            
            sectionLinks=header.select("h4 a")
            workLink=self.ao3Link+(sectionLinks[0].get("href"))

            #skip external works
            if "external_works" in workLink:
                continue
            
            #check if work or series
            if "series" in workLink:
                linkWorks=False
                print("is series. Wait a bit to avoid rateLimit")
                time.sleep(1)
                #if series, recursive function
                #open workLink
                #self.ficPageList.append(workLink)
                while(not linkWorks):
                    self.browser.open(workLink)
                    self.RequestCounter=self.RequestCounter+1
                    print("REQUEST COUNTER IS "+str(self.RequestCounter))
                    page=self.browser.page
                    if page is not None:
                        linkWorks=True
                        self.rateLimt=False
                    else:
                        linkWorks=False
                        self.rateLimit=True
                        time.sleep(60)
                    head=page.find_all("li", class_="blurb")
                    

                self.saveWorks(head)
            else:
                print("is work")
                #create ao3Fic
                self.ficList.append(AO3Fic())
                stats=section.find("dl", class_="stats")
                workName=sectionLinks[0].get_text()
                if len(sectionLinks) == 1:
                    workAuthor="Anonymous"
                else:
                    workAuthor=sectionLinks[1].get_text()
                workID = workLink.split("/")[-1]
                workDate= header.find("p", class_="datetime").get_text()
                #workDate= datetime.strptime(workDate,"%d %m %Y")
                downloadDate= datetime.now().strftime("%d %m %Y")
                chapters=stats.find("dd", class_="chapters")
                chapters=chapters.get_text()

                if chapters != "1/1":
                    #is chapter fic
                    self.ficList[-1].setIsChapter(True)
                    #workLink=self.browser.open(workLink).url
                
                self.ficList[-1].setFicName(workName)
                self.ficList[-1].setFicAuthor(workAuthor)
                self.ficList[-1].setFicID(workID)
                self.ficList[-1].setFicLink(workLink)
                self.ficList[-1].setUpdateDate(workDate)
                self.ficList[-1].setDownloadDate(downloadDate)
                self.ficList[-1].setChapterCount(chapters)
                
                print(self.ficList[-1])
                print(self.ficList[-1].ficLink)
            #if self.ficList[-1].getIsChapter():
                #time.sleep(5)
                
    def getNumPages(self, downloadPage):
        nextPage=downloadPage.find("li", class_="next")
        if nextPage is not None:
            lastPage=nextPage.find_previous_sibling("li")
            pageNum=lastPage.getText()
        else:
            pageNum=1
        return pageNum
            
    def getHeaders(self, isSub, downloadPage):
        if isSub:
            return downloadPage.find_all("dt")
        else:
            return downloadPage.find_all("div", class_="header module")
    def getDownloadPage(self):
        return self.ao3User+self.dlUsername+"/"+self.dlTypeName
    
    #this function creates a list of AO3Fic objects
    def openDLPage(self):
        dlPageURL=self.ao3User+self.dlUsername+"/"+self.dlTypeName
        print(dlPageURL)
        linkWorks = False
        while(not linkWorks):
            self.browser.open(dlPageURL)
            self.RequestCounter=self.RequestCounter+1
            print("REQUEST COUNTER IS "+str(self.RequestCounter))
            if self.browser.page is None:
                linkWorks=False
                self.rateLimit=True
                time.sleep(60)
            else:
                linkWorks=True
                self.rateLimit=False
    #choose
    def downloadPage(self, dlPageURL, pgNum):
        
        self.downloadWorks(dlPageURL, pgNum)
            
    
        
    def downloadWorks(self, dlPageURL, pgNum):
        #this gets the work information frm the page to be downloaded
        
        print("Page #"+str(pgNum))
        
        if pgNum==1:
            self.ficPageList.append(dlPageURL)
        dlPageURL=dlPageURL+"?page="+str(pgNum)
        linkWorks = False
        while(not linkWorks):
            self.browser.open(dlPageURL)
            self.RequestCounter=self.RequestCounter+1
            print("REQUEST COUNTER IS "+str(self.RequestCounter))
            if self.browser.page is None:
                linkWorks=False
                self.rateLimit=True
                time.sleep(60)
            else:
                linkWorks=True
                self.rateLimit=False
        self.ficPageList.append(dlPageURL)
            
        print(self.browser.url)
        downloadPage=self.browser.page
        #in works and bookmarks stories are dividied into lists with classes that include both blurb and group

        if self.dlTypeName=="subscriptions":
            storyList=downloadPage.find("dl", class_="subscription")
            storyList=storyList.find_all("dt")
        else:
            storyList=downloadPage.find_all("li", class_="blurb")
        
        #print("storylist")
        #print(storyList)
            
            
        #print("headers")
        #print(headers)
        if storyList is not None:
            #headers is none if there are no works
            if self.dlTypeName=="subscriptions":
                self.saveSubs(storyList)
            else:
                self.saveWorks(storyList)

            
                
           
        time.sleep(5)
            
    def getFics(self):
        #open url to books/work/sub page
        self.openDLPage()
        dlPageURL=self.ao3User+self.dlUsername+"/"+self.dlTypeName
        self.ficPageList.append(dlPageURL)
        #create soup page to use beautiful soup navigation.
        downloadPage = self.browser.page
        print("downlaod page is "+dlPageURL)
        
        #link to next page
        #returns none if there is only one page
        nextPage=downloadPage.find("li", class_="next")
        if nextPage is not None:
            #print("next page is ")
            #print(nextPage)
            #get last page. This is the page that's right before the next page link
            lastPage=(nextPage.find_previous_sibling("li"))
            lastPage=lastPage.getText()
            nextPage=nextPage.find("a").get("href")
            nextPage=self.ao3Link+nextPage

            print("there are "+str(lastPage)+"pages")
        else:
            lastPage=1
        #get fanfic page headers i is what spot in list  
        i=0
        for x in range(1,int(lastPage)+1):
            print("Page #"+str(x))
            self.ficPageList.append(dlPageURL+"?page="+str(x))
            print(self.browser.url)

            #in works and bookmarks stories are dividied into lists with classes that include both blurb and group
            if self.dlTypeName=="subscriptions":
                storyList=downloadPage.find("dl", class_="subscription")
                storyList=storyList.find_all("dt")
            else:
                storyList=downloadPage.find_all("li", class_="blurb")

            #print("storylist")
            #print(storyList)
            
            
            #print("headers")
            #print(headers)
            if storyList is not None:
                #headers is none if there are no works
                if self.dlTypeName=="subscriptions":
                    self.saveSubs(storyList)
                else:
                    self.saveWorks(storyList)                

                if nextPage is not None:
                    linkWorks = False
                    while(not linkWorks):
                        self.browser.open(dlPageURL)
                        self.RequestCounter=self.RequestCounter+1
                        print("REQUEST COUNTER IS "+str(self.RequestCounter))
                        if self.browser.page is None:
                            linkWorks=False
                            self.rateLimit=True
                            time.sleep(60)
                        else:
                            linkWorks=True
                            self.rateLimit=False
                    downloadPage=self.browser.page
                    if downloadPage is None:
                        print("failed to open. Try again")
                    nextPage=dlPageURL+"?page="+str(x+2)
                
           
            time.sleep(5)
    def setDlFileType(self, fileType):
            self.dlFileType=fileType
            
    def downloadToFile(self):
        parentDir=Path(self.downloadLocation)
        userPath=PurePath(parentDir, self.dlUsername.lower(), self.dlTypeName)
        userPath=Path(userPath)
        print("parentDir")
        print(parentDir)
        print("userPath")
        print(userPath)
        if not userPath.exists():
            print("Do not exist")
            #create path
            userPath.mkdir(parents=True)

        #link path
        linkPath=PurePath(userPath, 'allLinks.text')
        linkPath=Path(linkPath)

        f= linkPath.open("w")

        self.ficCounter=0
        for fic in self.ficList:
            f.write(fic.ficLink)
            f.write("\n")
            f.write(fic.ficLink+'?'+self.viewAdult)
            f.write("\n")
            f.write(fic.ficLink+'?'+self.viewFull)
            f.write("\n")
            f.write(fic.ficLink+'?'+self.viewAdult+'&'+self.viewFull)
            f.write("\n")
            self.ficCounter= self.ficCounter+1
            if self.dlFileType =="links":
                continue
            #download  is download.archiveofour.org/downloads/workid/randomname/filetype
            dlLink="https://download.archiveofourown.org/downloads/"+fic.ficID+"/work."+self.dlFileType
            print(dlLink)
            linkWorks = False
            while not linkWorks:
                r = requests.get(dlLink, allow_redirects=True)
                self.RequestCounter=self.RequestCounter+1
                print("REQUEST COUNTER IS "+str(self.RequestCounter))
                statusCode= r.status_code

                if statusCode == 429:
                    self.rateLimit=True
                    linkWorks=False
                    time.sleep(60)
                else:
                    linkWorks=True
                    self.rateLimit=False

            statuscode=0
            cd=r.headers.get('content-disposition')

            #if cd is none, means rate limit is hit

            fileName= re.findall('filename="(.+)"',cd)[0]
            print("filename is")
            print(fileName)

            #if file for author does not exist
            authorPath=Path(PurePath(userPath,fic.ficAuthor))
            if not authorPath.exists():
                authorPath.mkdir(parents=True)
            
            filePath=Path(PurePath(authorPath, fileName))
        
            save= filePath.open("wb")
            save.write(r.content)
            save.close()
            
            if (self.ficCounter %60)==0:
                time.sleep(60)
            else:
                time.sleep(1)
            
        f.close()
        linkPath=PurePath(userPath, 'allPages.text')
        linkPath=Path(linkPath)

        f= linkPath.open("w")
        for page in self.ficPageList:
            f.write(page)
            f.write("\n")

        f.close()
                        
            

        

if __name__ == "__main__":
    pass
   