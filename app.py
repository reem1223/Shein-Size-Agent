import os
import time
from flask import Flask, render_template, request, jsonify
from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.chrome.options import Options
from webdriver_manager.chrome import ChromeDriverManager

app = Flask(__name__)

# הגדרות המידות שלך (בס"מ)
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
    
    # הגדרות Chrome לעבודה בשרת ענן
    chrome_options = Options()
    chrome_options.add_argument("--headless")
    chrome_options.add_argument("--no-sandbox")
    chrome_options.add_argument("--disable-dev-shm-usage")
    chrome_options.add_argument("--disable-gpu")
    chrome_options.add_argument("user-agent=Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.0.0 Safari/537.36")

    driver = None
    try:
        # אתחול הדפדפן
        service = Service(ChromeDriverManager().install())
        driver = webdriver.Chrome(service=service, options=chrome_options)
        
        # סימולציית ניתוח (כאן תתבצע הגלישה האמיתית בעתיד)
        if url:
            # שלוש תוצאות ממוינות לפי התאמה
            results = [
                {"size": "L", "percent": 91, "details": "חזה: +0.5 ס\"מ | מותניים: התאמה מושלמת"},
                {"size": "XL", "percent": 86, "details": "חזה: +3.5 ס\"מ | מותניים: +2.0 ס\"מ"},
                {"size": "M", "percent": 74, "details": "חזה: -2.5 ס\"מ | מותניים: -1.5 ס\"מ"}
            ]
            return jsonify({"options": results})
        return jsonify({"error": "URL missing"}), 400

    except Exception as e:
        return jsonify({"error": str(e)}), 500
    finally:
        if driver:
            driver.quit()

if __name__ == '__main__':
    # התאמה לפורט של Render
    port = int(os.environ.get("PORT", 5000))
    app.run(host='0.0.0.0', port=port)