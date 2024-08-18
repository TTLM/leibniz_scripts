# Leibniz Manuscript Scripts

## Search Scraper
Simulates a search and then parses the results page source to collect the links to all the search results. 

### search(query)
Automates a Chrome browser and simulates a search on https://digitale-sammlungen.gwlb.de/sammlungen/sammlungsliste with a given search term.

### find_next()
Finds the HTML tag containing the link to the next page of search results. Test method.

### parse_results()
Parses through search results to grab the link for each search result, iterating through the results pages, then writes all the links to a JSON. Contains a brief delay before iterating through pages to avoid spamming the website with requests. Requires user to first use the search() method to ensure that the first search results page is the driver's current page. search.html provides an example of the source for the "LH 35" search result page.

## Document Scraper
Downloads entire work PDFs from the urls collected with SearchScraper's methods. Splits downloaded PDFs into separate PDFs for each page.

### load(url_list)
Loads a list of urls from a JSON.

### download_pdf(url, save_path)
Downloads a pdf and writes it to the save_path. url must be a download link.

### scrape_doc(page_url)
Finds the entire work download link on a page, finds the document's name, finds or creates a file path based on the document's name, then uses download_pdf() to download the entire work pdf to that filepath.

### scrape_all_docs(urls)
Downloads a pdf from each url in urls using scrape_doc(). Contains a brief delay between individual downloads to avoid spamming the website with requests.

### split_pages(source_folder, filename, out_folder)
Splits a document pdf into separate pdfs for each page and writes them to a folder in out_folder. Assumes that the source pdf will have a file path of {source_folder}/{filename}/{filename}.pdf. The output file path is {out_folder}/{filename}_{pagenum}.pdf.

### split_all(source_folder, out_folder)
Splits all the document pdfs in source_folder into individual page pdfs using split_pages().

## Notes

### Google Drive Integration
Currently, automatically uploading the files to Google Drive looks a bit difficult, and would require the owner of the project directory to adjust some settings. See the below links for more info:
https://developers.google.com/drive/api/quickstart/python
https://thepythoncode.com/article/using-google-drive--api-in-python

### Misc
- The folders data/downloads/ and data/pages/ are not included because of the file sizes involved. 
- In the future, the pagination methods may be moved out of DocumentScraper and into a new class. 
- One may also want to update the methods in DocumentScraper to handle different file organization and naming conventions.

