import random
from datetime import date, timedelta
from pathlib import Path
import pandas as pd


class DatasetGenerator:
    CUSTOMERS = ["Acme Corp", "Globex", "Initech", "Umbrella Inc", "Soylent Co"]
    CATEGORIES = {
        "Software": ["Analytics Pro", "AI Assistant", "CRM Suite"],
        "Cloud": ["Cloud Storage", "Compute Instance", "CDN Service"],
        "AI": ["AI Assistant", "Vision API", "Chatbot Builder"],
        "Hardware": ["Server Rack", "Laptop Pro", "Network Switch"],
    }
    COUNTRIES = ["France", "Germany", "Spain", "Italy", "Morocco", "USA"]

    def __init__(self, n: int = 150):
        self.output_path = Path(__file__).resolve().parents[1] / "storage" / "data.csv"
        self.n = n

    def generate_rows(self) -> list[dict]:
        rows = []
        start_date = date(2026, 1, 1)
        for i in range(1, self.n + 1):
            category = random.choice(list(self.CATEGORIES.keys()))
            product = random.choice(self.CATEGORIES[category])
            rows.append(
                {
                    "id": i,
                    "date": (start_date + timedelta(days=random.randint(0, 240))).isoformat(),
                    "customer": random.choice(self.CUSTOMERS),
                    "category": category,
                    "product": product,
                    "quantity": random.randint(1, 20),
                    "unit_price": round(random.uniform(50, 2000), 2),
                    "country": random.choice(self.COUNTRIES),
                }
            )
        return rows

    def run(self) -> None:
        rows = self.generate_rows()
        self.output_path.parent.mkdir(parents=True, exist_ok=True)
        df = pd.DataFrame(rows)
        df.to_csv(self.output_path, index=False)
        return {"data":df.to_dict(orient="records")}