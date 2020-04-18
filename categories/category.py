from bs4 import BeautifulSoup
import requests
import urllib
import os
import re

write_to_file = False


def get_problems(cat_heading, url):
    data = requests.get(url).text
    soup = BeautifulSoup(data, features="lxml")
    table = soup.findAll("table")[0]

    prob_data = ""

    prob_data += "# {}\n".format(cat_heading)
    prob_data += "\n"
    prob_data += "\n"

    headings = table.find_all('th')
    heading_text = "| Checkbox | ID | Problem Name"
    for i in range(2, len(headings)):
        heading_text += "|{}".format(headings[i].get_text())

    prob_data += heading_text + "|\n"
    prob_data += "|:---:" * (len(headings) + 1) + "|"
    prob_data += "\n"
    # print(table)
    for row in table.find_all("tr")[1:]:
        tds = row.find_all("td")

        prob = "|<ul><li>- [ ] Done</li></ul>"
        id = tds[0].get_text()
        name = tds[1].get_text()
        link = tds[1].find("a").get('href')
        prob += "|{}|[{}]({})".format(id, name, link)
        for i in range(2, len(tds)):
            prob += "|{}".format(tds[i].get_text())
        prob += "|\n"
        prob_data += prob
        # print(prob)

    file = open(os.path.join("categories", cat_heading, "README.md"), 'w')
    file.write(prob_data)
    file.close()


base_url = "https://www.a2oj.com/"
url = "https://www.a2oj.com/Categories.html"

data = requests.get(url).text
soup = BeautifulSoup(data, features="lxml")
tables = soup.findAll("table")

headings = [th.get_text() for th in tables[0].find("tr").find_all("th")]
# print(headings)

final_data = "#Categories\n"
final_data += "\n"

heading_text = "| Checkbox | ID  | Category | Problems Count |\n"

final_data += heading_text
final_data += "|---|:---:|:---:|---|\n"

for row in tables[0].find_all("tr")[1:]:
    tds = row.find_all("td")
    id = tds[0].get_text()
    name = tds[1].get_text()
    link = "{}".format(name)
    problems_count = tds[2].get_text()
    dataset = [id, name, link, problems_count]
    dir_name = re.sub('[\,\\\/\&\?\(\)]', ' ', name).rstrip()
    dir_name = re.sub(' +', '_', dir_name)
    dir_name = "{}. {}".format(id.zfill(3), dir_name)
    final_data += "|<ul><li>- [ ] Done</li></ul>|{}|[{}]({}/README.md)|{}|\n".format(
        id, name, urllib.parse.quote(dir_name), problems_count)
    # print(dir_name)
    # os.mkdir("categories/{}. {}".format(id.zfill(3), dir_name))
    category_link = base_url + tds[1].find('a').get('href')
    print(dir_name)
    if write_to_file:
        print(get_problems(dir_name, category_link))

print(final_data)
if write_to_file:
    file = open(os.path.join("categories", "README.md"), 'w')
    file.write(final_data)
    file.close()

print("Done")
