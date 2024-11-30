import os
import time

from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import Select
import pandas as pd

website_url = "https://www.adamchoi.co.uk/overs/detailed"
CWD = os.path.dirname(__file__)
driver = webdriver.Chrome()
season = "23/24"

driver.get(website_url)

# Find button by xpath
all_matches_button = driver.find_element(
    By.XPATH, '//label[@analytics-event="All matches"]'
)
all_matches_button.click()

# Find select by id

season_select = Select(driver.find_element(By.ID, "season"))
season_select.select_by_visible_text(season)
matches = driver.find_elements(By.TAG_NAME, "tr")
time.sleep(6)
date = []
home_team = []
away_team = []
score = []

for match in matches:
    try:
        if len(match.find_elements(By.XPATH, "./td")) == 4:
            date.append(match.find_element(By.XPATH, "./td[1]").text)
            home_team.append(match.find_element(By.XPATH, "./td[2]").text)
            score.append(match.find_element(By.XPATH, "./td[3]").text)
            away_team.append(match.find_element(By.XPATH, "./td[4]").text)
    except:
        pass

pd.DataFrame(
    {
        "date": date,
        "home_team": home_team,
        "score": score,
        "away_team": away_team,
    }
).to_csv(f"{CWD}\\matches_season_{season.replace('/', '_')}.csv", index=False)
