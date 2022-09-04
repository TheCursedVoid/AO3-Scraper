# AO3-Scraper
This is an AO3 Scraper. It allows you to save the bookmarks, and works of a user, and your own subscriptions.

Windows thinks that the .exe is a virus so I included the source code. You'll need to donwload both python files and have them in the same folder for it to work. It has only been tested on windwos. There are libraries need to be installed for the python script to work. They are tkinter, mechanicalsoup, bs4, and pathlib. All other libaries should come installed with Python, but if not you can just check the imports.

This script has not been optimized. There are probably a lot of instances where things could be done faster, or more efficiently, and there is definently some dead code in there. This was orignially just a simple script to get the links of all my bookmarks so I can upload to wayback. 

If there are a lot of pages and fics it can take a while. I've put in measures to avoid rate limits, but you can still hit it, especially if you run it a lot. I've only tested it for downloading PDFs and just the links. I'm assuming the other file types work, but I don't know for sure.
