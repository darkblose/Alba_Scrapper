import requests
from bs4 import BeautifulSoup
import math


def extract_superbrand_companies():
    alba_url = "http://www.alba.co.kr"
    companies = {}

    alba_result = requests.get(alba_url)
    alba_soup = BeautifulSoup(alba_result.text, "html.parser")
    super_brand = alba_soup.find("div", {"id": "MainSuperBrand"})
    impacts = super_brand.find_all("li", {"class": "impact"})
    for impact in impacts:
        URL = impact.find("a")["href"]
        company = impact.find("span", {"class": "company"}).string
        companies[company] = URL
    return companies


def extract_jobs(name, company_url):
    alba_result = requests.get(company_url)
    alba_soup = BeautifulSoup(alba_result.text, "html.parser")
    try:
        job_counts = alba_soup.find('p', {'class': "jobCount"}).text
        job_counts = job_counts.replace(',', '')
        job = int(job_counts[:-1])
        max_page = math.ceil(job / 50)
        name = name.replace("/", "_")
        company = {'name': name, 'jobs': []}

        for i in range(1, max_page + 1):
            url = f'{company_url}job/brand/main.asp?page={i}&pagesize=50'
            alba_result = requests.get(url)
            alba_soup = BeautifulSoup(alba_result.text, "html.parser")
            tbody = alba_soup.find("div", {"id": "NormalInfo"}).find("tbody")
            rows = tbody.find_all("tr", {"class": {"", "divide"}})
            for row in rows:
                local = row.find("td", {"class": "local"})
                if local:
                    local = local.text.replace(u'\xa0', ' ')

                title = row.find("td", {"class": "title"})
                if title:
                    title = title.find("a").find("span", {"class": "company"}).text.strip()
                    title = title.replace(u'\xa0', ' ')

                time = row.find("td", {"class": "data"})
                if time:
                    time = time.text.replace(u'\xa0', ' ')

                pay = row.find("td", {"class": "pay"})
                if pay:
                    pay = pay.text.replace(u'\xa0', ' ')

                date = row.find("td", {"class": "regDate last"})
                if date:
                    date = date.text.replace(u'\xa0', ' ')

                job = {
                    "place": local,
                    "title": title,
                    "time": time,
                    "pay": pay,
                    "date": date
                }
                company['jobs'].append(job)

        return company
    except:
        pass

