import json
from find_customers.webscraping import linkedin

jobs = ["Presidente", "Vicepresidente"
        "Gerente", "Gerente general", 
        "Co-founder", "Cofounder", "Founder", 
        "CEO", "CTO", "COO", "CMO"]
FROM_PAGE, TO_PAGE = 1, 10

if __name__ == "__main__":

    with linkedin() as scrape, open("data/creds.json") as file:
        creds = json.load(file)
        USR, PWD = creds["usr"], creds["pwd"]
    
        scrape.login(USR, PWD)
        results = scrape.extract_info_by_job(jobs, FROM_PAGE, TO_PAGE)