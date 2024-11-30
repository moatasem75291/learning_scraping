from bs4 import BeautifulSoup
import requests
import os
import re

TARGET_URL = "https://subslikescript.com/movies"
CWD = os.path.dirname(__file__)
MOVIES_TRANSCRIPTS = f"{CWD}\movies_transcripts"
os.makedirs(MOVIES_TRANSCRIPTS, exist_ok=True)


def sanitize_filename(filename):
    return re.sub(r'[\\/*?"<>|]', "", filename)


def get_site_content(url):
    response = requests.get(url)
    soup = BeautifulSoup(response.text, "html.parser")
    return soup


soup = get_site_content(TARGET_URL)
elements = soup.find("ul", class_="scripts-list").find_all("li")
# Get all the movie links
movie_links = []
for element in elements:
    movie_links.append((TARGET_URL + element.find("a")["href"]).replace("/movies", ""))

# Get all the movie names
movie_names = []
for element in elements:
    movie_names.append(element.find("a").text.strip())

# Save the movie names and links in a file
with open(f"{CWD}\movie_links.txt", "w") as file:
    for i in range(len(movie_names)):
        file.write(f"{movie_names[i]}, {movie_links[i]}\n")

# Get the script of each movie
for i in range(len(movie_links)):
    title = movie_names[i].replace(":", " ")
    # sanitized_title = sanitize_filename(title)
    movie_url = movie_links[i]
    soup = get_site_content(movie_url)
    article = soup.find("article", class_="main-article")
    script = article.find("div", class_="full-script").get_text(
        strip=True, separator=" "
    )
    with open(f"{MOVIES_TRANSCRIPTS}\{title}.txt", "w", encoding="utf-8") as file:
        file.write(title.center(80, " ") + "\n\n")
        file.write(script)
    print(f"{title} movie script saved successfully!")
print("[INFO] All movie scripts saved successfully!")
