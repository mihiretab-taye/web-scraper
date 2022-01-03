from bs4 import BeautifulSoup, element
from datetime import datetime
from requests import get
from sys import argv
import json

def scrapper(url):
    """Main Scrapper Function
    
    Keyword arguments:
    url -- the url for the news article
    Return: a dictionary file containing the title, content, updated date, modified date and author of the article
    """
    # url to html and then to parsed content
    html_content = get(url).text
    parsed_content = BeautifulSoup(html_content, "html.parser")
    
    # published date
    raw_pub_date = parsed_content.find("meta", property="article:published_time")["content"]
    published_date = datetime.strptime(raw_pub_date, "%Y-%m-%dT%H:%M:%S.%fZ")
    
    
    # modified date
    raw_mod_date = parsed_content.find("meta", property="article:modified_time")["content"]
    modified_date = datetime.strptime(raw_mod_date, "%Y-%m-%dT%H:%M:%S.%fZ")
    
    
    # article author
    raw_author = parsed_content.find("meta", attrs={"name": "byl"})["content"]
    author = raw_author[3:] # remove "By" boilerplate at the start of this attribute
    
    
    # article title
    title = parsed_content.find("h1", attrs={"data-testid": "headline"}).get_text()
    
    
    # remove figure and emphasized contents
    for i in parsed_content.find_all("figure"):
        parsed_content.figure.decompose()
    for i in parsed_content.find_all("em"):
        i.decompose()
    
    # take the article body part only as html file
    parsed_content = parsed_content.find("section", attrs={"name": "articleBody"})
    
    # parse the article body content with appropriate breaks
    content = ''
    for tag in parsed_content.descendants:
        if isinstance(tag, element.Tag) and tag.name == "p":
            content += "\n\n"

        if isinstance(tag, element.NavigableString):
            content += tag

    # putting all together as a dictionary and string
    article = {
        "TITLE": title,
        "CONTENT": content.strip(),
        "AUTHOR": author,
        "PUBLISHED DATE": published_date,
        "MODIFIED DATE": modified_date,
    }
    
    article_str = "TITLE: {}\n\n".format(title)
    article_str += "CONTENT: {}\n\n".format(content.strip())
    article_str += "AUTHOR: {}\n".format(author)
    article_str += "PUBLISHED DATE: {}\n".format(published_date)
    article_str += "MODIFIED DATE: {}\n".format(modified_date)
    
    
    return article, article_str
    
if __name__ == "__main__":
    url_arg = argv[1]
    article, article_str = scrapper(url_arg)
    print(article_str)
    