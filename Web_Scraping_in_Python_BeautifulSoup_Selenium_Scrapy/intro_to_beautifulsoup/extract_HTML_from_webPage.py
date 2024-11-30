from bs4 import BeautifulSoup
import requests
import os

TARGET_URL = "https://subslikescript.com/movie/Titanic-120338"  # Titanic movie script
CWD = os.path.dirname(__file__)


def extract_HTML_from_webPage(url):
    response = requests.get(url)
    return response.text


content = extract_HTML_from_webPage(TARGET_URL)
soap = BeautifulSoup(content, "html.parser")

# Search for the article tag
article = soap.find("article", class_="main-article")

# Get the movie title
title = article.find("h1").text

# Get the movie script
transcript = article.find(
    "div",
    class_="full-script",
).get_text(strip=True, separator=" ")


# Save the movie script to a file
with open(f"{CWD}\{title}.txt", "w") as file:
    file.write(title.center(80, " ") + "\n\n")
    file.write(transcript)

print(f"Movie script saved to {title}.txt")
