import requests
from datetime import datetime, timedelta

PARK_ID = 2
API_URL = f"https://queue-times.com/parks/{PARK_ID}/queue_times.json"

THRILL_RIDES = {
    "Colossus", "Nemesis Inferno", "SAW - The Ride", "Stealth",
    "The Swarm", "Hyperia", "Samurai", "Rush", "Detonator", "Tidal Wave"
}

def fetch_live_data():
    headers = {"User-Agent": "Mozilla/5.0"}
    response = requests.get(API_URL, headers=headers)
    response.raise_for_status()
    return response.json()

def filter_thrill_rides(data):
    thrill_rides = []
    for land in data['lands']:
        for ride in land['rides']:
            if ride['name'] in THRILL_RIDES and ride['is_open']:
                thrill_rides.append({
                    'name': ride['name'],
                    'wait': ride['wait_time']
                })
    return sorted(thrill_rides, key=lambda r: r['wait'])

def generate_html(rides):
    now = datetime.now().strftime("%Y-%m-%d %H:%M")
    one_hour_later = now + timedelta(hours=1)

    # Format as string
    one_hour_later_str = one_hour_later.strftime("%Y-%m-%d %H:%M")
    rows = ""
    for ride in rides:
        rows += f"<tr><td>{ride['name']}</td><td>{ride['wait']} minutes</td></tr>\n"

    html = f"""
    <!DOCTYPE html>
    <html lang="en">
    <head>
        <title>Thorpe Park Thrill Ride Queue Times</title>
        <!-- generated at {now} -->
        <style>
            body {{ font-family: Arial, sans-serif; padding: 2rem; background: #f8f8f8; }}
            table {{ border-collapse: collapse; width: 60%; margin: auto; background: white; box-shadow: 0 0 10px rgba(0,0,0,0.1); }}
            th, td {{ border: 1px solid #ddd; padding: 12px; text-align: center; }}
            th {{ background-color: #4CAF50; color: white; }}
            caption {{ font-size: 1.5rem; margin-bottom: 1rem; font-weight: bold; }}
            footer {{ text-align:center; margin-top: 2rem; font-size: 0.9rem; color: #555; }}
            a {{ color: #4CAF50; text-decoration: none; }}
            a:hover {{ text-decoration: underline; }}
        </style>
    </head>
    <body>
        <table>
            <caption>Live Thrill Ride Queue Times at Thorpe Park<br>As of {one_hour_later_str}</caption>
            <thead><tr><th>Ride</th><th>Wait Time</th></tr></thead>
            <tbody>
                {rows}
            </tbody>
        </table>
        <footer>
            Powered by <a href="https://queue-times.com/" target="_blank" rel="noopener noreferrer">Queue-Times.com</a>
        </footer>
    </body>
    </html>
    """
    return html

def main():
    data = fetch_live_data()
    rides = filter_thrill_rides(data)
    html = generate_html(rides)

    with open("index.html", "w", encoding="utf-8") as f:
        f.write(html)
    print("index.html generated successfully.")

if __name__ == "__main__":
    main()
