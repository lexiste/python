import sys
import mechanize
import logging

# start working with logging, basic file name, some options for time format, etc
# [-] check with ISO_8601 for time formats and standards (https://en.wikipedia.org/wiki/ISO_8601)
#  looking at various system logs they appear to use `Mon 01 2019 HH:MM:SS -0400` as the time stamp
logging.basicConfig(filename='crawler.log', filemode='a', level=logging.DEBUG, format='%(asctime)s %(name)-8s %(levelname)-8s %(message)s', datefmt='%b %d %Y %T %z')
logger = logging.getLogger(__name__)

"""
logging.debug('debug logging line')
logging.info('info logging line')
logging.warning('warning logging line')
logging.error('error logging line')
logging.critical('critical logging line')
"""

# based on prject work by Zero (@int0x33) offensize security day 13
def crawler(link):
    # create a new browser instance
    logger.info('Crawling %s', link)
    browser = mechanize.Browser()
    # add the user-agent, later we will fuzz this as well
    browser.addheaders = [('User-agent', 'Mozilla/5.0 (X11; Linux i586; rv:31.0) Gecko/20100101 Firefox/31.0')]
    # now capture the response
    response = browser.open(link)

    # loop through any/all links found
    for link in browser.links():
        logger.info(' -crawling sub-link %s', link.url)
        linkBrowser = mechanize.Browser()
        linkBrowser.addheaders = [('User-agent', 'Mozilla/5.0 (X11; Linux i586; rv:31.0) Gecko/20100101 Firefox/31.0')]
        try:
            linkBrowser.open(link.url)
            for linkLine in linkBrowser.links():
                print linkLine.url
        except Exception as e:
            # provide trackback capture with exc_info=True
            logger.error("exception raised in %s", e, exc_info=True)

crawler(sys.argv[1])
