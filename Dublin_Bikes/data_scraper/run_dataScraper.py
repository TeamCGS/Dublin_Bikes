import scraper
def main ():
    
    #scraper.main()
    Scraper2 = scraper.Static()
    Scraper2.getData()
   # StaticData = scraper.ReallyStatic()  - Code to fill Static Data table commented out as it is already filled and running again will give a duplicate primary key error
   # StaticData.getData()

main()