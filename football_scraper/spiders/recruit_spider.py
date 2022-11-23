import scrapy
import re

class RecruitSpider(scrapy.Spider):
    name = 'recruit_spider'
    
    college = 'ucla'
    
    # To scrape offers
    start_urls = [f'https://247sports.com/college/{college}/Season/2022-Football/Offers/?ViewPath=~/Views/SkyNet/RecruitInterest/_SimpleDetailedSetForSeason.ascx']

    # To scrape commits
    # start_urls = [f'https://247sports.com/college/{college}/Season/2022-Football/Commits/']

    def parse(self, response):
        """
        Callback used by Scrapy to process downloaded responses.

        Args:
            response (Response): An object that represents an HTTP response, fed to the Spiders for processing

        Yields:
            The players that recieved offers from a school, their high schools, and cities. 
        """
        # Select each player on the recruiting list.
        players = [recruit for recruit in response.css("div.recruit")]
        
        regex = r'(.*)\s\((.*),\s(\w+)\)'

        for p in players:
            # Extract geodata from text in the format: School (City, State)
            hs, city, state = re.findall(regex, p.css("span::text").get().strip())[0]
            
            yield {
                "name" : p.css("a::text").get().strip(),
                "school" : hs,
                "city" : city,
                "state" : state,
                }