from flask import Flask, request, render_template_string, jsonify
from prometheus_flask_exporter import PrometheusMetrics
from sqlalchemy import create_engine, Column, String
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker
import requests
import os

app = Flask(__name__)
metrics = PrometheusMetrics(app)

# Database setup
DB_USER = os.environ.get("DB_USER", "postgres")
DB_PASSWORD = os.environ.get("DB_PASSWORD")
DB_HOST = os.environ.get("DB_HOST")
DB_PORT = os.environ.get("DATABASE_PORT", 5432)
DB_DB = os.environ.get("DATABASE_DB", "bar")
DB_URL = f"postgresql+psycopg2://{DB_USER}:{DB_PASSWORD}@{DB_HOST}:{DB_PORT}/{DB_DB}?sslmode=require"
engine = create_engine(DB_URL)
Session = sessionmaker(bind=engine)
Base = declarative_base()

class IPRecord(Base):
    __tablename__ = "ip_records"
    ip = Column(String, primary_key=True)
    location = Column(String)

Base.metadata.create_all(engine)

# HTML template
HTML_FORM = """
<!DOCTYPE html>
<html>
<head><title>IP Locator</title></head>
<body>
  <h1>IP Locator(HaHAHa finalay ...)</h1>
  <form method="POST">
    <label>Enter IP: </label>
    <input type="text" name="ip" required>
    <input type="submit" value="Lookup">
  </form>
  {% if location %}
    <p><strong>IP:</strong> {{ ip }}</p>
    <p><strong>Location:</strong> {{ location }}</p>
  {% endif %}
</body>
</html>
"""

def get_location_from_api(ip):
    # Using ipinfo.io free API
    try:
        response = requests.get(f"https://ipinfo.io/{ip}/json")
        if response.status_code == 200:
            data = response.json()
            return data.get("city", "Unknown") + ", " + data.get("region", "") + ", " + data.get("country", "")
    except:
        pass
    return "Unknown"

@app.route("/", methods=["GET", "POST"])
def index():
    location = None
    ip = None
    if request.method == "POST":
        ip = request.form["ip"]
        session = Session()
        record = session.query(IPRecord).filter_by(ip=ip).first()
        if record:
            location = record.location
        else:
            location = get_location_from_api(ip)
            new_record = IPRecord(ip=ip, location=location)
            session.add(new_record)
            session.commit()
        session.close()
    return render_template_string(HTML_FORM, ip=ip, location=location)

if __name__ == "__main__":
    app.run(host="0.0.0.0", port=5000)
