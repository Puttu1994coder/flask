from flask import Flask, request, jsonify, render_template_string

app = Flask(__name__)

# Keywords for funnel stage detection
AWARENESS_KEYWORDS = ["flats in", "apartments", "rent in", "studio apartments"]
CONSIDERATION_KEYWORDS = ["best", "compare", "review", "pricing", "amenities", "near metro"]

FUNNEL_KEYWORDS = {
    "awareness": ["what is", "how to", "guide", "tips"],
    "consideration": ["best", "compare", "vs", "review"],
    "conversion": ["buy", "discount", "book", "pricing"]
}

# Landing content
landing_pages = {
    "awareness": "<h2>Welcome! Discover what we do and how it helps you</h2>",
    "consideration": "<h2>Explore features, compare options, and learn why we’re the best</h2>",
    "conversion": "<h2>Ready to act? Book now and get exclusive benefits!</h2>",
}

# Web-based intent detection
def detect_intent(user_input):
    user_input_lower = user_input.lower()
    if any(keyword in user_input_lower for keyword in CONSIDERATION_KEYWORDS):
        return "Consideration"
    elif any(keyword in user_input_lower for keyword in AWARENESS_KEYWORDS):
        return "Awareness"
    else:
        return "Unknown"

# API-based funnel detection
def detect_funnel_stage(query):
    for stage, words in FUNNEL_KEYWORDS.items():
        if any(word in query.lower() for word in words):
            return stage
    return "awareness"

# HTML generator
def generate_landing_page(intent, user_input):
    if intent == "Awareness":
        heading = "Explore Premium Flats in Whitefield"
        content = """
            <p>Looking for modern homes in Whitefield? Our zero-hassle premium apartments are designed for comfort and convenience.</p>
            <ul>
                <li>Studio, 1BHK, 2BHK options</li>
                <li>24/7 Maintenance Support</li>
                <li>Book Remotely with Ease</li>
            </ul>
        """
    elif intent == "Consideration":
        heading = "Why Choose Kots Flats in Whitefield?"
        content = """
            <p>Comparing options? Here's why Kots is your best pick for premium rentals in Whitefield:</p>
            <ul>
                <li>Fully Furnished with Top-Class Amenities</li>
                <li>Near Major Tech Parks</li>
                <li>Transparent Pricing. Zero Brokerage.</li>
            </ul>
        """
    else:
        heading = "Tell Us More"
        content = "<p>We couldn't determine your needs. Try searching again with more details.</p>"

    html = f"""
    <!DOCTYPE html>
    <html>
    <head>
        <title>{heading}</title>
    </head>
    <body>
        <h1>{heading}</h1>
        <h3>User Input: {user_input}</h3>
        {content}
    </body>
    </html>
    """
    return html

# Route for browser
@app.route("/", methods=["GET", "POST"])
def home():
    if request.method == "POST":
        user_input = request.form["query"]
        intent = detect_intent(user_input)
        html = generate_landing_page(intent, user_input)
        return render_template_string(html)

    return '''
        <form method="post">
            <label>Enter your search query:</label><br><br>
            <input type="text" name="query" style="width:300px;">
            <input type="submit" value="Generate Landing Page">
        </form>
    '''

# Route for Postman/API
@app.route("/generate", methods=["POST"])
def generate():
    data = request.get_json()
    query = data.get("query", "")
    if not query:
        return jsonify({"error": "Query is required"}), 400

    stage = detect_funnel_stage(query)
    content = landing_pages.get(stage)

    return jsonify({
        "funnel_stage": stage,
        "landing_page_html": content
    })

if __name__ == "__main__":
    app.run(debug=True, port=5001)
