import os
import time
from flask import Flask, render_template, request, jsonify
from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.chrome.options import Options
from webdriver_manager.chrome import ChromeDriverManager

app = Flask(__name__)

# פרופיל המידות המדויק שלך (בס"מ)
MY_PROFILE = {
    "bust": 104.5, "waist": 103, "hips": 109.5,
    "inseam": 76, "total_length": 80, "shoes": 27.3
}

@app.route('/')
def home():
    return render_template('index.html')

@app.route('/analyze', methods=['POST'])
def analyze():
    data = request.json
    url = data.get('url')
    
    # הגדרות Chrome לעבודה בשרת ענן (Render)
    chrome_options = Options()
    chrome_options.add_argument("--headless")
    chrome_options.add_argument("--no-sandbox")
    chrome_options.add_argument("--disable-dev-shm-usage")
    chrome_options.add_argument("--disable-gpu")
    # התחזות לדפדפן רגיל כדי למנוע חסימה
    chrome_options.add_argument("user-agent=Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.0.0 Safari/537.36")

    driver = None
    try:
        service = Service(ChromeDriverManager().install())
        driver = webdriver.Chrome(service=service, options=chrome_options)
        
        driver.get(url)
        time.sleep(5) # זמן טעינה לאתר SHEIN

        # נתוני סימולציה מבוססים על המידות שלך
        # במציאות כאן יבוצע חילוץ נתונים מה-HTML של הדף
        results = [
            {
                "size": "L", 
                "percent": 91, 
                "details": f"חזה: גדול ב-0.5 ס\"מ ({105}) | מותניים: התאמה מושלמת ({103})"
            },
            {
                "size": "XL", 
                "percent": 86, 
                "details": f"חזה: גדול ב-3.5 ס\"מ ({108}) | מותניים: גדול ב-2.0 ס\"מ ({105})"
            },
            {
                "size": "M", 
                "percent": 74, 
                "details": f"חזה: קטן ב-2.5 ס\"מ ({102}) | מותניים: קטן ב-1.5 ס\"מ ({101.5})"
            }
        ]
        
        # החזרת התוצאות ממוינות מהגבוה לנמוך
        return jsonify({"options": sorted(results, key=lambda x: x['percent'], reverse=True)})

    except Exception as e:
        print(f"Server Error: {e}")
        return jsonify({"error": "הסוכן לא הצליח לגשת לנתוני האתר"}), 500
    finally:
        if driver:
            driver.quit()

if __name__ == '__main__':
    # הגדרת פורט שמתאימה ל-Render
    port = int(os.environ.get("PORT", 5000))
    app.run(host='0.0.0.0', port=port)