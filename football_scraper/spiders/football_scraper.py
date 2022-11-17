import scrapy

class FootballSpider(scrapy.Spider):
    name = 'football_spider'
    
    start_urls = ['https://247sports.com/Season/2022-Football/CompositeRecruitRankings/']

    def parse(self, response):
        """
        Callback used by Scrapy to process downloaded responses.

        Args:
            response (Response): An object that represents an HTTP response, fed to the Spiders for processing

        Yields:
            A new request with the page of recruits and a callback to parse_player_list(). 
        """
        # Set the url to go to next.
        pages = 10
        for num in range(pages, 0, -1):
            next_page = response.urljoin(f'?page={num}')
            yield scrapy.Request(next_page, callback=self.parse_player_list)

    def parse_player_list(self, response):
        """
        Callback used to process each actor included in the credits page.

        Args:
            response (Response): An object that represents an HTTP response, fed to the Spiders for processing

        Yields:
            A new request with an player's recruitment page and a callback to parse_player_page(). 
        """
        # Get relative links for all players on the page.
        links = [a.attrib["href"].split("?")[0] for a in response.css("div.status a.expand-anchor")]

        for link in links:
            # Set the url to go to next.
            next_page = response.urljoin(link + "/RecruitInterests/")
            yield scrapy.Request(next_page, callback=self.parse_player_page)

    def parse_player_page(self, response):
        """
        Callback used to process each actor's credits page and read each movie or show they have acted in.

        Args:
            response (Response): An object that represents an HTTP response, fed to the Spiders for processing

        Yields:
            A dictionary containing the players's name and the school's name. 
        """
        # Get the player's name.
        player = response.css('a.mini-header-comp__main-info-name::text').get()

        offer = 0
        # Looks at schools that gave offers. (Not produced, written, etc.)
        for school in response.css('.first_blk'):  
            # Get the schools's name
            s_name = school.css('a::text').get().strip()
            offer += 1

            yield {
                "name" : player,
                "school" : s_name,
                "committed" : (offer <= 1)
                }