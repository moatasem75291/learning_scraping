from bs4 import BeautifulSoup
import requests
import os

root = "https://subslikescript.com/movies"
TARGET_URL = f"https://subslikescript.com/movies_letter-A"
CWD = os.path.dirname(__file__)
MOVIES_TRANSCRIPTS = f"{CWD}\movies_transcripts_letter-A"
os.makedirs(MOVIES_TRANSCRIPTS, exist_ok=True)


def get_site_content(url):
    response = requests.get(url)
    soup = BeautifulSoup(response.text, "html.parser")
    return soup


soup = get_site_content(TARGET_URL)

# Get the last page number
last_page = soup.find("ul", class_="pagination").find_all("li")[-2].text


# Get all the movie links
movie_links = []
for page in range(1, int(last_page) + 1)[:2]:
    url = f"{TARGET_URL}?page={page}"
    soup = get_site_content(url)
    elements = soup.find("ul", class_="scripts-list").find_all("li")
    for element in elements:
        movie_links.append((root + element.find("a")["href"]).replace("/movies", ""))


for link in movie_links:
    soup = get_site_content(link)
    movie_name = soup.find("h1").text.strip()
    article = soup.find("article", class_="main-article")
    transcript = article.find("div", class_="full-script").text.strip()
    title = movie_name.replace(":", " ")
    title = title.replace("?", "")
    with open(f"{MOVIES_TRANSCRIPTS}\{title}.txt", "w", encoding="utf-8") as file:
        file.write(title.center(80, " ") + "\n\n")
        file.write(transcript)
    print(f"{title} movie script saved successfully!")

print("[INFO] All movie scripts saved successfully!")
