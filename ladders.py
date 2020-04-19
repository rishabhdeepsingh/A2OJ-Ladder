from bs4 import BeautifulSoup
import requests
import urllib
import os
import re

write_to_file = False


def get_ladder(dir_name, url):
    url = "https://www.a2oj.com/{}".format(url)

    data = requests.get(url).text
    soup = BeautifulSoup(data, features="lxml")
    tables = soup.findAll("table")

    header = tables[0].find_all("tr")
    ladder_name = header[0].find_all("td")[0].get_text().rstrip()
    description = header[1].find_all("td")[0].get_text().rstrip().split(":")[1]
    difficulty = header[2].find_all("td")[0].get_text().rstrip()
    final_data = ""

    final_data += "# {}".format(ladder_name)
    final_data += "\n"
    final_data += "## {}\n".format("Description")
    final_data += description
    final_data += "\n"
    final_data += "## {}".format(difficulty)
    final_data += "\n"
    final_data += "\n"

    problems = tables[1]
    prob_headings = [th.get_text()
                     for th in problems.find("tr").find_all("th")]
    heading_text = "| Checkbox | ID  | Problem Name | Online Judge | Difficulty |\n"

    final_data += heading_text
    final_data += "|---|:---:|:---:|---|---|\n"

    datasets = []
    for row in problems.find_all("tr")[1:]:
        tds = row.find_all("td")
        # print(tds)
        id = tds[0].get_text()
        name = tds[1].get_text()
        link = tds[1].find("a").get('href')
        platform = tds[2].get_text()
        difficulty = tds[3].get_text()
        dataset = [id, name, link, platform, difficulty]
        final_data += "|<ul><li>- [ ] Done</li></ul>|{}|[{}]({})|{}|{}|\n".format(id,
                                                                                  name, link, platform, difficulty)
        datasets.append(dataset)

    # print(datasets)
    # print(final_data)
    os.makedirs("ladders/" + dir_name)
    file = open(os.path.join("ladders", dir_name, "README.md"), 'w')
    file.write(final_data)
    file.close()


url = "https://www.a2oj.com/Ladders.html"

data = requests.get(url).text
soup = BeautifulSoup(data, features="lxml")
tables = soup.findAll("table")

headings = [th.get_text() for th in tables[0].find("tr").find_all("th")]
# print(headings)

final_data = "# A2OJ-Ladder\n\n"
# print(header)
heading_text = "| Checkbox | ID  | Name | Problems Count |\n"

final_data += heading_text
final_data += "|---|:---:|:---:|---|\n"

for table_no in range(2):
    for row in tables[table_no].find_all("tr")[1:]:
        tds = row.find_all("td")
        # print(tds)
        id = tds[0].get_text()
        name = tds[1].get_text()
        link = tds[1].find('a').get('href')
        problems_count = tds[2].get_text()
        dir_name = re.sub('[\,\\\/\&\?\(\)]', ' ', name).rstrip()
        dir_name = "{}. {}".format(id.zfill(2), name)
        final_data += "|<ul><li>- [ ] Done</li></ul>|{}|[{}]({}/README.md)|{}|\n".format(
            id, name, "ladders/" + urllib.parse.quote(dir_name), problems_count)
        print(dir_name, link)
        # get_ladder(dir_name, link)
# print(datasets)
# print(final_data)

if write_to_file:
    file = open('README.md', 'w')
    file.write(final_data)
    file.close()
