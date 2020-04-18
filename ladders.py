from bs4 import BeautifulSoup
import requests
import urllib

url = "https://www.a2oj.com/Ladders.html"

data = requests.get(url).text
soup = BeautifulSoup(data, features="lxml")
tables = soup.findAll("table")

headings = [th.get_text() for th in tables[0].find("tr").find_all("th")]
# print(headings)

final_data = ""
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
        link = "{}".format(name)
        problems_count = tds[2].get_text()
        dataset = [id, name, link, problems_count]
        final_data += "|<ul><li>- [ ] Done</li></ul>|{}|[{}]({}/README.md)|{}|\n".format(
            id, name, urllib.parse.quote_plus(link), problems_count)

# print(datasets)
print(final_data)
