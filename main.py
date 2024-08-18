from scrapers.search_scraper import SearchScraper
from scrapers.document_scraper import DocScraper
from config import Config

def main():
    config = Config()
    search_scraper = SearchScraper(config)
    doc_scraper = DocScraper(config)

    # search_scraper.search("LH 35")
    # urls = search_scraper.parse_results()
    # search_scraper.find_next()

    urls = doc_scraper.load(config.JSON_FILE)
    doc_scraper.scrape_all_docs(urls)


if __name__ == "__main__":
    main()
