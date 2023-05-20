from bs4 import BeautifulSoup
import requests

date = input("Which year you want to search? Type your answer in the format YYYY-MM-DD: ")
year = date.split("-")[0]


def top_100():

    lst = {}
    response = requests.get(url="https://www.billboard.com/charts/hot-100/"+date+"/")
    response.raise_for_status()

    soup = BeautifulSoup(response.text, "html.parser")

    all_songs = soup.find_all(name="h3", id="title-of-a-story", class_="a-no-trucate")
    all_artists = soup.find_all(name="span", class_="a-no-trucate")

    songs = [tag.getText().strip() for tag in all_songs]
    artists = [tag.getText().strip() for tag in all_artists]

    for i in range(len(songs)):
        lst[songs[i]] = artists[i]

    return lst
