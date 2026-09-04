```python
from flask import Flask, request, render_template_string
import pickle
import os

# ============================================================
# FLASK APP
# ============================================================

app = Flask(__name__)


# ============================================================
# LOAD MODEL AND VECTORIZER
# ============================================================

with open("sentiment.pkl", "rb") as model_file:
    model = pickle.load(model_file)

with open("vectorizer.pkl", "rb") as vectorizer_file:
    vectorizer = pickle.load(vectorizer_file)


# ============================================================
# HTML + CSS
# ============================================================

HTML = """
<!DOCTYPE html>
<html lang="en">

<head>

    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">

    <title>SentimentAI | Sentiment Analyzer</title>

    <style>

        * {
            margin: 0;
            padding: 0;
            box-sizing: border-box;
            font-family: Arial, Helvetica, sans-serif;
        }

        body {

            min-height: 100vh;

            background:
                radial-gradient(
                    circle at 10% 10%,
                    rgba(99, 102, 241, 0.35),
                    transparent 35%
                ),

                radial-gradient(
                    circle at 90% 90%,
                    rgba(6, 182, 212, 0.30),
                    transparent 35%
                ),

                linear-gradient(
                    135deg,
                    #020617,
                    #0f172a,
                    #111827
                );

            color: white;

            display: flex;

            justify-content: center;

            align-items: center;

            padding: 30px;

        }


        /* ==============================
           MAIN CONTAINER
        ============================== */

        .container {

            width: 100%;

            max-width: 850px;

        }


        /* ==============================
           HEADER
        ============================== */

        .header {

            text-align: center;

            margin-bottom: 30px;

        }


        .badge {

            display: inline-block;

            padding: 8px 18px;

            border-radius: 50px;

            background: rgba(255,255,255,0.08);

            border: 1px solid rgba(255,255,255,0.15);

            color: #cbd5e1;

            font-size: 14px;

            margin-bottom: 18px;

            backdrop-filter: blur(10px);

        }


        h1 {

            font-size: 52px;

            font-weight: 800;

            letter-spacing: -2px;

        }


        .gradient {

            background:

                linear-gradient(
                    90deg,
                    #818cf8,
                    #22d3ee
                );

            -webkit-background-clip: text;

            -webkit-text-fill-color: transparent;

        }


        .subtitle {

            margin-top: 12px;

            color: #94a3b8;

            font-size: 17px;

        }


        /* ==============================
           FEATURES
        ============================== */

        .features {

            display: flex;

            justify-content: center;

            gap: 10px;

            margin-top: 20px;

            flex-wrap: wrap;

        }


        .feature {

            padding: 7px 14px;

            border-radius: 50px;

            background: rgba(255,255,255,0.06);

            border: 1px solid rgba(255,255,255,0.08);

            color: #94a3b8;

            font-size: 13px;

        }


        /* ==============================
           MAIN CARD
        ============================== */

        .card {

            background: rgba(15, 23, 42, 0.78);

            border: 1px solid rgba(255,255,255,0.12);

            border-radius: 25px;

            padding: 35px;

            box-shadow:

                0 25px 70px
                rgba(0,0,0,0.45);

            backdrop-filter: blur(20px);

        }


        /* ==============================
           LABEL
        ============================== */

        label {

            display: block;

            margin-bottom: 12px;

            color: #e2e8f0;

            font-size: 15px;

            font-weight: 600;

        }


        /* ==============================
           TEXT AREA
        ============================== */

        textarea {

            width: 100%;

            min-height: 180px;

            resize: vertical;

            padding: 18px;

            border-radius: 16px;

            border: 1px solid #334155;

            outline: none;

            background: rgba(2,6,23,0.75);

            color: white;

            font-size: 16px;

            line-height: 1.6;

            transition: all 0.3s ease;

        }


        textarea::placeholder {

            color: #64748b;

        }


        textarea:focus {

            border-color: #818cf8;

            box-shadow:

                0 0 0 3px
                rgba(129,140,248,0.15);

        }


        /* ==============================
           BUTTON
        ============================== */

        .button {

            width: 100%;

            margin-top: 20px;

            padding: 16px;

            border: none;

            border-radius: 14px;

            background:

                linear-gradient(
                    90deg,
                    #6366f1,
                    #06b6d4
                );

            color: white;

            font-size: 16px;

            font-weight: 700;

            cursor: pointer;

            transition: all 0.3s ease;

            box-shadow:

                0 10px 30px
                rgba(99,102,241,0.30);

        }


        .button:hover {

            transform: translateY(-3px);

            box-shadow:

                0 15px 35px
                rgba(6,182,212,0.35);

        }


        .button:active {

            transform: translateY(0);

        }


        /* ==============================
           RESULT CARD
        ============================== */

        .result {

            margin-top: 30px;

            padding: 28px;

            border-radius: 20px;

            text-align: center;

            background:

                rgba(255,255,255,0.05);

            border:

                1px solid
                rgba(255,255,255,0.10);

        }


        .result-label {

            color: #64748b;

            font-size: 13px;

            letter-spacing: 1px;

            margin-bottom: 12px;

        }


        .sentiment {

            font-size: 38px;

            font-weight: 800;

            margin-bottom: 15px;

        }


        .positive {

            color: #34d399;

        }


        .negative {

            color: #fb7185;

        }


        .neutral {

            color: #facc15;

        }


        .unknown {

            color: #60a5fa;

        }


        /* ==============================
           CONFIDENCE
        ============================== */

        .confidence {

            color: #cbd5e1;

            font-size: 15px;

        }


        .confidence strong {

            color: white;

        }


        .progress-container {

            width: 100%;

            height: 8px;

            background: #1e293b;

            border-radius: 20px;

            overflow: hidden;

            margin-top: 12px;

        }


        .progress {

            height: 100%;

            border-radius: 20px;

            background:

                linear-gradient(
                    90deg,
                    #6366f1,
                    #22d3ee
                );

        }


        /* ==============================
           FOOTER
        ============================== */

        .footer {

            text-align: center;

            margin-top: 25px;

            color: #475569;

            font-size: 13px;

        }


        /* ==============================
           MOBILE
        ============================== */

        @media (max-width: 600px) {

            body {

                padding: 15px;

            }

            h1 {

                font-size: 38px;

            }

            .subtitle {

                font-size: 15px;

            }

            .card {

                padding: 22px;

            }

            textarea {

                min-height: 150px;

            }

            .sentiment {

                font-size: 30px;

            }

        }

    </style>

</head>


<body>


<div class="container">


    <!-- HEADER -->

    <div class="header">

        <div class="badge">

            🤖 AI-Powered NLP

        </div>


        <h1>

            <span class="gradient">

                SentimentAI

            </span>

        </h1>


        <p class="subtitle">

            Analyze the sentiment of your text using Machine Learning

        </p>


        <div class="features">

            <span class="feature">

                ⚡ TF-IDF

            </span>

            <span class="feature">

                🧠 Naive Bayes

            </span>

            <span class="feature">

                📊 Confidence Score

            </span>

            <span class="feature">

                🚀 Flask

            </span>

        </div>

    </div>


    <!-- MAIN CARD -->

    <div class="card">


        <form method="POST">


            <label for="text">

                ✍️ Enter your text

            </label>


            <textarea

                id="text"

                name="text"

                placeholder="Example: I absolutely loved this product! The quality is amazing..."

                required>{{ user_text }}</textarea>


            <button

                class="button"

                type="submit">

                🔍 Analyze Sentiment

            </button>


        </form>


        {% if sentiment %}

        <!-- RESULT -->

        <div class="result">


            <div class="result-label">

                SENTIMENT ANALYSIS RESULT

            </div>


            <div class="sentiment {{ sentiment_class }}">

                {{ sentiment_emoji }}

                {{ sentiment }}

            </div>


            {% if confidence is not none %}

            <div class="confidence">

                Model Confidence:

                <strong>

                    {{ confidence }}%

                </strong>


                <div class="progress-container">

                    <div

                        class="progress"

                        style="width: {{ confidence }}%;">

                    </div>

                </div>

            </div>

            {% endif %}


        </div>

        {% endif %}


    </div>


    <div class="footer">

        Built with Python • Flask • Scikit-learn • Machine Learning

    </div>


</div>


</body>

</html>
"""


# ============================================================
# HOME ROUTE
# ============================================================

@app.route("/", methods=["GET", "POST"])
def home():

    sentiment = None

    confidence = None

    user_text = ""

    sentiment_class = "unknown"

    sentiment_emoji = "🤖"


    if request.method == "POST":

        user_text = request.form.get("text", "").strip()


        if user_text:

            # ------------------------------------------
            # Convert text into TF-IDF features
            # ------------------------------------------

            text_vector = vectorizer.transform([user_text])


            # ------------------------------------------
            # Predict sentiment
            # ------------------------------------------

            prediction = model.predict(text_vector)[0]


            # ------------------------------------------
            # Confidence
            # ------------------------------------------

            if hasattr(model, "predict_proba"):

                probabilities = model.predict_proba(text_vector)[0]

                confidence = round(
                    max(probabilities) * 100,
                    2
                )


            # ------------------------------------------
            # Convert prediction to readable format
            # ------------------------------------------

            prediction_text = str(prediction).lower()


            if (
                prediction_text == "1"
                or "positive" in prediction_text
            ):

                sentiment = "Positive"

                sentiment_class = "positive"

                sentiment_emoji = "😊"


            elif (
                prediction_text == "0"
                or "negative" in prediction_text
            ):

                sentiment = "Negative"

                sentiment_class = "negative"

                sentiment_emoji = "😞"


            elif "neutral" in prediction_text:

                sentiment = "Neutral"

                sentiment_class = "neutral"

                sentiment_emoji = "😐"


            else:

                sentiment = str(prediction)

                sentiment_class = "unknown"

                sentiment_emoji = "🤖"


    return render_template_string(

        HTML,

        sentiment=sentiment,

        confidence=confidence,

        user_text=user_text,

        sentiment_class=sentiment_class,

        sentiment_emoji=sentiment_emoji

    )


# ============================================================
# HEALTH CHECK
# ============================================================

@app.route("/health")
def health():

    return {

        "status": "healthy",

        "message": "SentimentAI is running successfully"

    }


# ============================================================
# LOCAL DEVELOPMENT
# ============================================================

if __name__ == "__main__":

    app.run(

        host="0.0.0.0",

        port=int(
            os.environ.get(
                "PORT",
                5000
            )
        )

    )
```
