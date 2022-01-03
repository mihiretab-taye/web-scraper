from argparse import ArgumentParser
# from bs4 import BeautifulSoup
# import requests


def receive_args():
    default_url = "https://www.nytimes.com/2020/09/02/opinion/remote-learning-coronavirus.html?action=click&module=Opinion&pgtype=Homepagehttps://www.nytimes.com/2020/09/02/opinion/remote-learning-coronavirus.html?action=click&module=Opinion&pgtype=Homepage"
    args = ArgumentParser()
    args.add_argument("-u", "--url", default=default_url, help="url for news article")
    return vars(args.parse_args())

if __name__ == "__main__":
    args = receive_args()