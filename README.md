# Recruitment Networks in College Football

College football is one of the largest revenue drivers for universities across the country, bringing in an average of over 39 million per school per year. Having a winning team magnifies the potential income, with the most successful programs like Georgia and Alabama making almost 170 million dollars in revenue in 2021. Having a successful program is deeply reliant on the school’s high school recruiting process. In this paper, we will look at the recruiting processes of some of the top football programs in the country. Specifically, we will analyze the results of their recruits from the lens of network science. Analyzing the processes and preferences of these top schools can help bring to light the most effective strategies and help smaller schools with less resources improve their recruiting process. We will use network science to try to understand the geographic and social trends that such programs leverage in their recruiting efforts.

# Web Scraper

Currently, this scraper gets 2022 highschool football recruiting data from 247Sports and retrieves lists of offers or commits for a college.

To run the scraper and save the results in a csv, open a terminal the scrapy project folder and run the following command:

```
scrapy crawl recruit_spider -o results.csv
```

