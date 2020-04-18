from bs4 import BeautifulSoup
import requests

url = "https://www.a2oj.com/Ladder11.html"

data = requests.get(url).text
soup = BeautifulSoup(data, features="lxml")

tables = soup.findAll("table")

header = tables[0]

for data in header.find_all("tr"):
    print(data.find_all("td")[0].get_text())

problems = tables[1]
headings = [th.get_text() for th in problems.find("tr").find_all("th")]
print(headings)

datasets = []
for row in problems.find_all("tr")[1:]:
    tds = row.find_all("td")
    # print(tds)
    id = tds[0].get_text()
    prob = tds[1].find("a").get('href')
    platform = tds[2].get_text()
    difficulty = tds[3].get_text()
    dataset = [id, prob, platform, difficulty]
    print(dataset)
    datasets.append(dataset)

# print(datasets)
