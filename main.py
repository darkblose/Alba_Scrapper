from alba import extract_superbrand_companies
from alba import extract_jobs
from save import save_to_file

cnt = 0
companies = extract_superbrand_companies()

for key, value in companies.items():
    print("Start Scraping: ", key)
    company = extract_jobs(key, value)
    print("Start Saving: ", key)
    save_to_file(company)
    cnt += 1
    print("Complete: ", cnt)
    print()
