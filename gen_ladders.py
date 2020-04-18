from bs4 import BeautifulSoup
import requests
import os
import errno

for ladder in range(4, 32 + 1):

    url = "https://www.a2oj.com/Ladder{}.html".format(ladder)

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
    print(final_data)
    dir_name = ladder_name.split(":")[1]
    print(dir_name)
    try:
        os.makedirs(dir_name)
    except OSError as e:
        if e.errno != errno.EEXIST:
            raise
    file = open(os.path.join(dir_name, "README.md"), 'w')
    file.write(final_data)
    file.close()
