import scraper
def main ():
    
    StaticData = scraper.ReallyStatic()  #- Code to fill Static Data table commented out as it is already filled and running again will give a duplicate primary key error
    setOfNumbers = StaticData.getData()
    Scraper1 = scraper.Dynamic()
    Scraper1.getData(setOfNumbers) #set of numbers is a set with ints 1-102
   

main()