import scrapy


class QuoteSpider(scrapy.Spider):
    # identifies the Spider. It must be unique within a project,
    # that is, you can’t set the same name for different Spiders.
    name = "quotes"
    '''
    Instead of implementing a start_requests() method that generates scrapy.Request objects from URLs, you can just define a 
        start_urls class attribute with a list of URLs. This list will then be used by the default implementation of start_requests() 
        to create the initial requests for your spider:
    '''
    # start_urls = [
    #     'http://quotes.toscrape.com/page/1/',
    #     'http://quotes.toscrape.com/page/2/',
    # ]

    def start_requests(self):
        '''
        must return an iterable of Requests (you can return a list of requests or write a generator function) 
        which the Spider will begin to crawl from. Subsequent requests will be generated successively from these initial requests.
        '''
        urls = [
            'http://quotes.toscrape.com/page/1/'
        ]
        for url in urls:
            yield scrapy.Request(url=url, callback=self.parse)

    def parse(self, response):
        '''
        method that will be called to handle the response downloaded for each of the requests made. 
        The response parameter is an instance of TextResponse that holds the page content and has 
        further helpful methods to handle it.
        '''
        quotes = response.css('div.quote')
        # scrape data
        # TODO: bug - only scraping first quote on each page
        print("There are %d quotes on page '%s'" % (len(quotes), response.url))
        for quote in quotes:
            # create dict from elements on current page
            # before passing it on to the parse_author
            data = {
                "page": response.url,
                "text": quote.css('span.text::text').get(),
                "tags": quote.css('div.tags>a::text').getall()
            }
            about_page = quote.css('.author + a::attr(href)').get()
            if about_page is not None:
                author_request = scrapy.Request(response.urljoin(
                    about_page), callback=self.parse_author)
                author_request.meta['data'] = data
                yield author_request
            else:
                data["author"] = None
                yield data
        '''
        Scrapy’s mechanism of following links: when you yield a Request in a callback method, 
        Scrapy will schedule that request to be sent and register a callback method to be executed when that request finishes.
        '''
        # after finishing scrape of current page,
        # follow links recursively (depth-first-search)
        next_pages = response.css('.pager a::attr(href)').getall()
        for next_page in next_pages:
            yield scrapy.Request(response.urljoin(next_page), callback=self.parse)
            # As a shortcut for creating Request objects you can also use response.follow
            # Unlike scrapy.Request, response.follow supports relative URLs directly - no need to call urljoin.
            # yield response.follow(next_page, callback=self.parse)

        # You can also pass a selector to response.follow instead of a string; this selector should extract necessary attributes:
        # for href in response.css('li.next a::attr(href)'):
            # yield response.follow(href, callback=self.parse)

    def parse_author(self, response):
        '''
        More specific parse method for parsing author about pages
        '''
        data = response.meta['data']
        data = data.copy()
        shortdescription = self.css_extract(
            response, 'div.author-description::text')
        if shortdescription is not '':
            shortdescription = shortdescription[:shortdescription.index(
                '. ')+1]
        data["author"] = {
            "name": self.css_extract(response, 'h3.author-title::text'), "birthday": self.css_extract(response, '.author-born-date::text'), "birthlocation": self.css_extract(response, '.author-born-location::text').replace('in ', ''), "shortdescription": shortdescription, "link": response.url
        }
        yield data

    def css_extract(self, response, query: str) -> str:
        return response.css(query).get(default='').strip()
