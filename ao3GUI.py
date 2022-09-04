import tkinter as tk
from tkinter import ttk
from tkinter import filedialog as fd
from tkinter import messagebox
import os
import ao3Source as ao3
import time
import threading


# Create App class
class AO3App(tk.Tk):
    
    
        
    
        
    
    #when this object is created it will follow the below steps for creation
    def __init__(self, *args, **kwargs):
        tk.Tk.__init__(self, *args, **kwargs) #call tk initialization
        self.title("AO3 Link Scraper")
        self.geometry("500x250")
        self.resizable(False,False)


        #create AO3 Object
        self.ao3Data=ao3.AO3Data()
        
        #create frame that will hold all other frames
        self.container = ttk.Frame(self, padding="3 3 12 12", borderwidth=3, relief="raised")
        self.container.grid(column=0, row=0, sticky="nwes")
        self.currentFrame="StartWindow"
        self.previousFrame="StartWindow" #This keeps the value of the last frame for the rate window fcn

        self.isDownloading=False
        #The Views
        #create list that holds frame names
        self.frames={}
        #F is our framesc
        for F in(StartWindow, LoginWindow,DownloadTypeWindow,FileSaveWindow,FicListWindow,DownloadWindow,RateLimitWindow):
            page_name= F.__name__
            #create the frame F by sending our container frame and adding it our tk controller
            #frame=F(self.container, self)
            self.create_frame(page_name)
            #add that frame to frame list
            #self.frames[page_name]=frame

            #frame.grid(row=0, column=0, sticky="nsew")

        #show our first frame
        self.show_frame("StartWindow")
        self.rate_limit()
        
    def create_frame(self, page_name):
        frameName=globals()[page_name]
        
        frame=frameName(self.container,self)
        self.frames[page_name]=frame
        frame.grid(row=0, column=0, sticky="nsew")
    #show frame function
    def show_frame(self, page_name):
        if self.currentFrame != "RateLimitWindow":
            self.previousFrame=self.currentFrame

        self.currentFrame=page_name
        #show frame for given page name

        ''' for frame in self.frames.values()
                frame.grid_remove()'''
        oldframe= self.frames[page_name]
        oldframe.tkraise()
        if page_name=="FicListWindow":
            print("fic Window")
            if self.ao3Data.getIsReadyForDL():
                if not self.isDownloading:
                    print("updateWindow")
                    oldframe.updateWindow()
    def start_Thread(self, thread):
        thread.start()
    
    def rate_limit(self):
        # check if ratelimit flag is set
        
        rateLimitFlag=self.ao3Data.rateLimit
        if rateLimitFlag:
            print("rate Limit Hit")
            print("the previous frame is")
            print(self.previousFrame)
            if self.previousFrame != "RateLimitWindow":
                self.show_frame("RateLimitWindow")
        else:
            print("rate Limit not Hit")
            if self.currentFrame == "RateLimitWindow":
                self.show_frame(self.previousFrame)
        self.after(5000, self.rate_limit)



                          

# start window frame
class StartWindow(ttk.Frame):
    def __init__(self, parent, controller):
        ttk.Frame.__init__(self, parent) #call frame initiazliation

        self.controller = controller
        
        #create style?
        
        #Title Frame
        self.titleFrame=ttk.Frame(self)
    
        #Content Frame
        self.contentFrame=ttk.Frame(self)

        #Navigation Frame
        self.navFrame=ttk.Frame(self)

        
        welcomemsg="WELCOME TO AO3 LINK SCRAPER"
        welcomeLabel=ttk.Label(self.titleFrame, text=welcomemsg,wraplength=500)
        welcomeLabel.grid(column=0, row=0, columnspan=3)

        contentmsg="Do you want to log in?"
        contentLabel=ttk.Label(self.contentFrame, text=contentmsg, wraplength=500)
        contentLabel.grid(column=0, row=1, columnspan=3)
        yesButton=ttk.Button(self.navFrame, text="Yes", command=lambda:controller.show_frame("LoginWindow"))
        yesButton.grid(column=0, row=2)
        noButton=ttk.Button(self.navFrame, text="No", command=self.noLogin)
        noButton.grid(column=2, row=2)
        
       

        ''' Start window frame.
        Have 3 frames that are packed in order.
        Title, Content, and Navigation '''
        self.titleFrame.pack()
        self.contentFrame.pack()
        self.navFrame.pack()

    def noLogin(self):
        self.controller.ao3Data.Logout()
        self.controller.show_frame("DownloadTypeWindow")
        
#login window frame
class LoginWindow(ttk.Frame):
    
    def __init__(self, parent, controller):
        ttk.Frame.__init__(self,parent)
        self.controller = controller
        
        #Title Frame
        self.titleFrame=ttk.Frame(self)
    
        #Content Frame
        self.contentFrame=ttk.Frame(self)

        #Navigation Frame
        self.navFrame=ttk.Frame(self)


        #Title widgets
        titleLabel=ttk.Label(self.titleFrame, text="AO3 LINK SCRAPER")
        titleLabel2=ttk.Label(self.titleFrame, text="LOGIN")

        #Content widgets
        userLabel=ttk.Label(self.contentFrame, text="Username:")
        passLabel=ttk.Label(self.contentFrame, text="Password:")

        username=tk.StringVar()
        password=tk.StringVar()
        self.userInput=ttk.Entry(self.contentFrame,textvariable=username, text="Username:")
       
        self.passInput=ttk.Entry(self.contentFrame, textvariable=password, text="Password:")
        submitButton=ttk.Button(self.navFrame, text="Submit", command=self.submitLogin)
        backButton=ttk.Button(self.navFrame, text="Back", command=lambda:controller.show_frame("StartWindow"))
        
        titleLabel.grid(column=0,row=0)
        titleLabel2.grid(column=1,row=0)
        userLabel.grid(column=0,row=0)
        passLabel.grid(column=0,row=1)
        self.userInput.grid(column=1, row=0)
        self.passInput.grid(column=1, row=1)
        submitButton.grid(column=3, row=0)
        backButton.grid(column=0, row=0)

        self.titleFrame.pack()
        self.contentFrame.pack()
        self.navFrame.pack()

        
    def submitLogin(self):
        #set login info
        self.controller.ao3Data.setLogin(self.userInput.get(), self.passInput.get())
        #try login
        try:
            self.controller.ao3Data.Login()
        except Exception as error:
            #something could not login. check username or password
            messagebox.showwarning(title='Error', message=repr(error))
            
        else:
            #go to next page
            self.controller.show_frame("DownloadTypeWindow")
            
        
                                                          
        
#save type frame
class DownloadTypeWindow(ttk.Frame):
    def __init__(self, parent, controller):
        ttk.Frame.__init__(self,parent)
        self.controller=controller


        #Title Frame
        titleFrame=ttk.Frame(self)
    
        #Content Frame
        contentFrame=ttk.Frame(self)

        #Navigation Frame
        navFrame=ttk.Frame(self)

        titleLabel=ttk.Label(titleFrame, text="Download Options")
        usrmsg='''Enter the name of the user whose works, bookmarks or subscriptions you want to download.\nYou can only download your own subscriptions.'''
        usrmsgLabel=ttk.Label(contentFrame, text=usrmsg, wraplength=500)
        usrNameLabel= ttk.Label(contentFrame, text="Username:")
        self.usrInputValue=tk.StringVar()
        self.usrInput= ttk.Entry(contentFrame,textvariable=self.usrInputValue, text="Username")
        
        msg='''Do you want to download Bookmarks, Works, or Subscriptions?'''
        msgLabel=ttk.Label(contentFrame, text=msg,wraplength=500)

        self.downloadType=tk.IntVar()
        bookmarks=ttk.Radiobutton(contentFrame, text="Bookmarks", value=0, variable=self.downloadType)
        bookmarks.invoke()
        works=ttk.Radiobutton(contentFrame, text="Works", value=1, variable=self.downloadType)

        #if user is not logged in disable subscritpions
        subscriptions=ttk.Radiobutton(contentFrame, text="Subscriptions", value=2, variable=self.downloadType)
        self.nextButton=ttk.Button(navFrame, text="Next", command=self.checkDownloadSelection)

        #blur out next button until radio selection is chosen
        homeButton=ttk.Button(navFrame, text="Home", command=lambda:controller.show_frame("StartWindow"))

        #content placement
        #username entry
        usrmsgLabel.grid(column=0, row=0, columnspan=4)
        usrNameLabel.grid(column=0, row=1)
        self.usrInput.grid(column=1, row=1)
        #downloadtype entru
        msgLabel.grid(column=0, row=2, columnspan=3)
        bookmarks.grid(column=0, row=3)
        works.grid(column=1, row=3)
        subscriptions.grid(column=2, row=3)
        self.nextButton.grid(column=2, row=0)
        homeButton.grid(column=0, row=0)

        titleFrame.pack()
        contentFrame.pack()
        navFrame.pack()
    def startFicList(self):
        self.controller.ao3Data.openDLPage()
        self.controller.ao3Data.getNumPages(self.controller.ao3Data.getBrowserPage())
        self.controller.ao3Data.setIsReadyForDL(True)
        self.nextButton['state']='!disabled'
        self.controller.show_frame("FicListWindow")
    def checkDownloadSelection(self):
        #this makes sure you put correct username and have valid work and subscirptions
        self.nextButton['state']='disabled'
        buttonValue=self.getButtonValue()
        print("Button Value is ")
        print(buttonValue)
        username = self.usrInput.get()
        try:
            self.controller.ao3Data.setUserName(username)
        except:
            #user doesn't exist
            self.nextButton['state']='!disabled'
            messagebox.showwarning(title='Username Error', message='This user does not exist.')
        else:    
        
            try:
                #check if username is same as logged in user
                self.controller.ao3Data.checkDownloadValidity(buttonValue, username)   
            except:
                #can't download subs from user
                self.nextButton['state']='!disabled'
                messagebox.showwarning(title='Username Error', message='Can only download subs from yourself.')
                
            else:
                self.controller.ao3Data.setDownloadType(buttonValue)
                self.startFicList()
    
    def getButtonValue(self):
        return self.downloadType.get()

        
        
class FileSaveWindow(ttk.Frame):

    
    
    def __init__(self, parent, controller):
        ttk.Frame.__init__(self,parent)
        self.controller=controller


        #Title Frame
        titleFrame=ttk.Frame(self)
    
        #Content Frame
        contentFrame=ttk.Frame(self)

        #Navigation Frame
        navFrame=ttk.Frame(self)

        
        msg="Where do you want to save the file?"

        

        descriptionMsg='''This will create a folder with the username of what's being dowloaded.
Inside that folder there will be a folder named bookmars, works, or subs depending on your previous selection.
Those folders will contain the file with the links.'''

        titleLabel=ttk.Label(titleFrame, text="AO3 LINK SCRAPER")
        titleLabel2=ttk.Label(titleFrame, text="SAVE")
        #get current directory
        currDir=os.getcwd()
        print(os.getcwd())
        print(type(currDir))
        
        descriptionLabel=ttk.Label(contentFrame, text=descriptionMsg,wraplength=500)
        
        self.fileLocation=tk.StringVar()
        

        fileLabel=ttk.Label(contentFrame,text="Destination Folder",wraplength=500)
        fileEntry=ttk.Entry(contentFrame, textvariable=self.fileLocation)

        fileButton=ttk.Button(contentFrame, text="Select Directory", command=self.selectDir)
        
        nextButton=ttk.Button(navFrame, text="Next", command=lambda:controller.show_frame("DownloadWindow"))
        backButton=ttk.Button(navFrame, text="Back", command=lambda:controller.show_frame("DownloadTypeWindow"))

        titleLabel.grid(column=0,row=0)
        titleLabel2.grid(column=0,row=1)
        descriptionLabel.grid(column=0, row=0,columnspan=3)
        fileLabel.grid(column=0,row=1, sticky="W")
        fileEntry.grid(column=0, row=2, columnspan=2, sticky="EW")
        fileButton.grid(column=2, row=2)
        backButton.grid(column=0, row=0)
        nextButton.grid(column=2, row=0)


        titleFrame.pack()
        contentFrame.pack()
        navFrame.pack()
    def selectDir(self):
        filepath=tk.filedialog.askdirectory(initialdir=os.getcwd(), title="Save")
        print(filepath)
        self.fileLocation.set(filepath)
        self.controller.ao3Data.setDownloadLocation(filepath)

    
        
#
class FicListWindow(ttk.Frame):
    def __init__(self, parent, controller):
        ttk.Frame.__init__(self,parent)
        self.controller=controller

        self.titleFrame=ttk.Frame(self)

        
            
        msg="Gathering list of fics. Please wait.\nAverage download time is 5 sec per page to avoid rate issues.\nIf it says not responding, it's probably fine. Leave it be."
        self.titleLabel=ttk.Label(self.titleFrame, text=msg)
        
            
        self.titleLabel.grid(column=0, row=0)

        self.titleFrame.pack()
            
        
    def getNextButton(self):
        self.nextButton = ttk.Button(self.titleFrame, text="Next", command=lambda:self.controller.show_frame("FileSaveWindow"))
        self.nextButton.grid(column=0, row=3)
    def updateWindow(self):
        print("update Window")
        if(self.controller.ao3Data.getIsReadyForDL()):
            numPages=self.controller.ao3Data.getNumPages(self.controller.ao3Data.getBrowserPage())
            
            self.pageLabel=ttk.Label(self.titleFrame)
            self.pageLabel.configure(text=f'There are {numPages} Pages')
            
            self.downloadLabel=ttk.Label(self.titleFrame)
            self.downloadLabel.configure(text=f'Downloading Page X')
            self.pageLabel.grid(column=0, row=1)
            self.downloadLabel.grid(column=0, row=2)

            self.thread = threading.Thread(target=self.getFics,args=(numPages,),daemon=True)
            self.controller.start_Thread(self.thread)
            self.controller.isDownloading=True
            
            
    def openDownloadPage(self):
        self.controller.ao3Data.openDLPage()
    def getNumPages(self):
        downloadPage = self.browser.page
        return self.controller.ao3Data.getNumPages(downloadPage)
    
    def getFics(self,numPages):
        self.controller.update()
        dlPageURL= self.controller.ao3Data.getDownloadPage()
        #print("wait")
        #self.controller.after(5000)
        #print("after")
        for x in range(1, int(numPages)+1):
            self.downloadLabel['text']=(f'Downloading Page {x}/{numPages}')
            self.controller.update()
            self.controller.ao3Data.downloadPage(dlPageURL,int(x))
        self.downloadLabel['text']=(f'Downloaded {numPages}/{numPages} NumPages')
        self.getNextButton()
        #self.thread.join()
        
                
#class loading frame

class DownloadWindow(ttk.Frame):
    def __init__(self, parent, controller):
        ttk.Frame.__init__(self,parent)
        self.controller=controller

        
        self.ButtonFrame=ttk.Frame(self)
        
        msg="How do you want to save the list of fics. Txt file of URLS? AZW3? EPUB? MOBI? PDF? HTML?"
        instrLabel=ttk.Label(self.ButtonFrame,text=msg,wraplength=500)
        self.selected=tk.StringVar()
        r1=ttk.Radiobutton(self.ButtonFrame, text="URL file", value="links", variable=self.selected)
        r2=ttk.Radiobutton(self.ButtonFrame, text="AZW3", value="azw3", variable=self.selected)
        r3=ttk.Radiobutton(self.ButtonFrame, text="EPUB", value="epub", variable=self.selected)
        r4=ttk.Radiobutton(self.ButtonFrame, text="MOBI", value="mobi", variable=self.selected)
        r5=ttk.Radiobutton(self.ButtonFrame, text="PDF", value="pdf", variable=self.selected)
        r6=ttk.Radiobutton(self.ButtonFrame, text="HTML", value="html", variable=self.selected)

        self.thread=threading.Thread(target=self.downloadFics,daemon=True)
        self.updateThread=threading.Thread(target=self.updatePage,daemon=True)
        self.downloadBtn=ttk.Button(self.ButtonFrame,text="Download", command=self.startDownload)
        

        instrLabel.grid(column=0, row=0, columnspan=6)
        r1.grid(column=0, row=1)
        r2.grid(column=1, row=1)
        r3.grid(column=2, row=1)
        r4.grid(column=3, row=1)
        r5.grid(column=4, row=1)
        r6.grid(column=5, row=1)
        self.downloadBtn.grid(column=2, row=2, columnspan=2)
        self.ButtonFrame.pack()
        #Thread(target=self.updatePage).start()

    def startDownload(self):
        self.downloadBtn['state']="disabled"
        self.controller.start_Thread(self.updateThread)
        self.controller.start_Thread(self.thread)

    def updatePage(self):
        saveNum=self.controller.ao3Data.ficCounter
        totalFics = len(self.controller.ao3Data.ficList)
        savedLabel=ttk.Label(self.ButtonFrame)
        savedLabel.grid(column=0, row=3, columnspan=6) 
        while saveNum < totalFics:
            savedLabel['text']=(f'Saving {saveNum}/{totalFics} fics')
            saveNum=self.controller.ao3Data.ficCounter

        savedLabel['text']=(f'Saved {totalFics} fics')
        
        #self.updateThread.join()
        
        
    def downloadFics(self):
        #self.downloadBtn.state(['disabled'])
        self.controller.ao3Data.setDlFileType(self.selected.get())
        self.controller.ao3Data.downloadToFile()
        #self.downloadBtn.state(['!disabled'])
        #self.thread.join()
        self.downloadBtn['state']="!disabled"

class RateLimitWindow(ttk.Frame):
    def __init__(self, parent, controller):
        ttk.Frame.__init__(self,parent)
        self.controller=controller
        self.msgFrame=ttk.Frame(self)
        msg='''RATE LIMIT HIT.\nWAITING BEFORE CONTINUING\n
        The more you hit the rate limit the longer it lasts, and the more it appears.\n
        When rate limit appears a request is made every minute to check if rate limit is gone.\n
        Rate limit is set by IP so accessing ao3 on other devices on the same network would add to the ratelimit counter.\n
        Usually takes about 5 minutes for rate limit to disappear'''  
        msgLabel=ttk.Label(self.msgFrame, text=msg,wraplength=500)
        msgLabel.pack()
        self.msgFrame.pack()

app=AO3App()

app.mainloop()
