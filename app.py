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

def calculate_match(product_sizes, my_sizes):
    """מחשב ציון התאמה ובונה פירוט השוואה"""
    total_diff = 0
    count = 0
    details = []
    
    for key, val in product_sizes.items():
        if key in my_sizes:
            diff = val - my_sizes[key]
            total_diff += abs(diff) / my_sizes[key]
            count += 1
            status = "גדול ב-" if diff > 0 else "קטן ב-"
            details.append(f"{key}: {status}{abs(round(diff, 1))} ס\"מ")
    
    score = max(0, 100 - (total_diff / count * 100)) if count > 0 else 0
    return round(score), " | ".join(details)

@app.route('/')
def home():
    return render_template('index.html')

@app.route('/analyze', methods=['POST'])
def analyze():
    data = request.json
    url = data.get('url')
    
    # הגדרות Chrome לעבודה בענן (Render/Heroku)
    chrome_options = Options()
    chrome_options.add_argument("--headless")
    chrome_options.add_argument("--no-sandbox")
    chrome_options.add_argument("--disable-dev-shm-usage")
    chrome_options.add_argument("--disable-gpu")
    
    driver = None
    try:
        # הפעלת הדפדפן
        service = Service(ChromeDriverManager().install())
        driver = webdriver.Chrome(service=service, options=chrome_options)
        
        driver.get(url)
        time.sleep(5) # המתנה לטעינת האתר

        # נתוני סימולציה (כאן יבוא החילוץ האמיתי מה-HTML בהמשך)
        mock_data = [
            {"size": "M", "dims": {"bust": 102, "waist": 100}},
            {"size": "L", "dims": {"bust": 106, "waist": 104}},
            {"size": "XL", "dims": {"bust": 112, "waist": 110}}
        ]
        
        all_results = []
        for item in mock_data:
            score, detail_str = calculate_match(item["dims"], MY_PROFILE)
            all_results.append({
                "size": item["size"],
                "percent": score,
                "details": detail_str
            })
        
        # מיון לפי אחוזי התאמה
        sorted_results = sorted(all_results, key=lambda x: x['percent'], reverse=True)[:3]
        
        return jsonify({"options": sorted_results})

    except Exception as e:
        print(f"Server Error: {e}")
        return jsonify({"error": str(e)}), 500
    finally:
        if driver:
            driver.quit()

if __name__ == '__main__':
    # התאמה לפורט של Render
    port = int(os.environ.get("PORT", 5000))
    app.run(host='0.0.0.0', port=port)