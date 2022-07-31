import csv

def save_to_file(company):
    try:
        file = open(f"data/{company['name']}.csv", mode="w", encoding="utf-8-sig")
        writer = csv.writer(file)
        writer.writerow(["place","title","time","pay","date"])

        for job in (company["jobs"]):
            writer.writerow(list(job.values()))
    except:
        pass