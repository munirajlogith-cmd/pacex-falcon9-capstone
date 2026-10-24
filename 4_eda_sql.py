"""Lab 4: EDA with SQL (sqlite3). Run each query and screenshot the output for the slides."""
import sqlite3
import pandas as pd
from config import SPACEX_CSV

df = pd.read_csv(SPACEX_CSV).rename(columns=lambda c: c.strip())
con = sqlite3.connect("my_data1.db")
df.to_sql("SPACEXTBL", con, if_exists="replace", index=False)
print(df.columns.tolist())  # check exact column names against the queries below

QUERIES = {
    "1. Unique launch sites": 'SELECT DISTINCT "Launch_Site" FROM SPACEXTBL',
    "2. Sites starting with CCA (5 rows)":
        "SELECT * FROM SPACEXTBL WHERE Launch_Site LIKE 'CCA%' LIMIT 5",
    "3. Total payload mass for NASA (CRS)":
        "SELECT SUM(PAYLOAD_MASS__KG_) FROM SPACEXTBL WHERE Customer = 'NASA (CRS)'",
    "4. Average payload mass for F9 v1.1":
        "SELECT AVG(PAYLOAD_MASS__KG_) FROM SPACEXTBL WHERE Booster_Version LIKE 'F9 v1.1%'",
    "5. First successful ground pad landing":
        "SELECT MIN(Date) FROM SPACEXTBL WHERE Landing_Outcome = 'Success (ground pad)'",
    "6. Drone ship successes, payload 4000-6000 kg":
        "SELECT DISTINCT Booster_Version FROM SPACEXTBL WHERE Landing_Outcome = "
        "'Success (drone ship)' AND PAYLOAD_MASS__KG_ BETWEEN 4000 AND 6000",
    "7. Mission outcome counts":
        "SELECT Mission_Outcome, COUNT(*) AS n FROM SPACEXTBL GROUP BY Mission_Outcome",
    "8. Boosters with max payload":
        "SELECT DISTINCT Booster_Version FROM SPACEXTBL WHERE PAYLOAD_MASS__KG_ = "
        "(SELECT MAX(PAYLOAD_MASS__KG_) FROM SPACEXTBL)",
    "9. 2015 drone ship failures":
        "SELECT substr(Date,6,2) AS month, Landing_Outcome, Booster_Version, Launch_Site "
        "FROM SPACEXTBL WHERE Landing_Outcome = 'Failure (drone ship)' AND substr(Date,0,5) = '2015'",
    "10. Landing outcomes ranked, 2010-06-04 to 2017-03-20":
        "SELECT Landing_Outcome, COUNT(*) AS n FROM SPACEXTBL WHERE Date BETWEEN "
        "'2010-06-04' AND '2017-03-20' GROUP BY Landing_Outcome ORDER BY n DESC",
}

for title, q in QUERIES.items():
    print("\n" + title)
    print(q)
    print(pd.read_sql_query(q, con).to_string(index=False))
