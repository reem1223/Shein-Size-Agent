import os
import time
from flask import Flask, render_template, request, jsonify
from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.chrome.options import Options
from webdriver_manager.chrome import ChromeDriverManager

app = Flask(__name__)

# פרופיל המידות שלך (בס"מ)
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
    
    if not url:
        return jsonify({"error": "נא להזין לינק תקין"}), 400

    # הגדרות לעבודה חלקה ב-Render
    chrome_options = Options()
    chrome_options.add_argument("--headless")
    chrome_options.add_argument("--no-sandbox")
    chrome_options.add_argument("--disable-dev-shm-usage")
    chrome_options.add_argument("user-agent=Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.0.0 Safari/537.36")

    driver = None
    try:
        # הפעלת הדפדפן בסביבת השרת
        service = Service(ChromeDriverManager().install())
        driver = webdriver.Chrome(service=service, options=chrome_options)
        
        # דימוי ניתוח מהיר עבור 3 מידות
        results = [
            {"size": "L", "percent": 91, "details": "התאמה מעולה בחזה ובמותניים (לפי 104.5cm)"},
            {"size": "XL", "percent": 86, "details": "מידה רחבה יותר, מומלץ למראה Oversize"},
            {"size": "M", "percent": 74, "details": "עלול להיות צמוד מדי באזור המותניים"}
        ]
        
        # החזרת התוצאות
        return jsonify({"options": results})

    except Exception as e:
        print(f"Error: {e}")
        return jsonify({"error": "הסוכן לא הצליח להתחבר לאתר. נסה שוב."}), 500
    finally:
        if driver:
            driver.quit()

if __name__ == '__main__':
    # הגדרת פורט דינמי עבור Render
    port = int(os.environ.get("PORT", 5000))
    app.run(host='0.0.0.0', port=port)