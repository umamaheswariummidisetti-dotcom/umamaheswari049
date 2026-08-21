from flask import Flask, render_template, request
import joblib
import numpy as np

app = Flask(__name__)

# Load trained model
model = joblib.load("crop_model.pkl")

crop_info = {
"wheat": "Wheat prefers cool, dry weather during ripening and fertile, well-drained soil.",
"sorghum": "Sorghum is drought-tolerant and performs well in hot, dry conditions with moderate soils.",
"pulses (pigeon pea / tur)": "Pulses fix nitrogen, grow in semi-arid to sub-humid climates, and tolerate low to moderate rainfall.",
"groundnut": "Groundnut requires warm temperatures, sandy loam soils, and moderate rainfall, with well-distributed rains during pod formation.",
"soybean": "Soybean grows well in warm, moist climates with fertile, well-drained soils and moderate rainfall.",
"sugarcane": "Sugarcane demands high water and warm, humid conditions, and thrives on fertile, well-drained soils with good sunlight.",
"mustard (rapeseed)": "Mustard prefers cool, dry climates during flowering and ripening, and grows on well-drained fertile soils.",
"chili (dry chillies)": "Chili requires warm temperatures, well-drained fertile soils, and moderate irrigation; sensitive to waterlogging.",
"banana": "Banana grows well in humid tropical climates.",
"mango": "Mango requires sunny weather and well-drained soil.",
"coffee": "Coffee grows best in cool climates with sufficient rainfall.",
"coconut": "Coconut thrives in coastal and humid regions.",
"rice": "Rice thrives in warm, humid conditions with abundant water and grows best in fertile, well-drained clay or loamy soil."
}

crop_details = {
"rice": {
"season": "Kharif",
"water": "High",
"yield": "High"
},
"maize": {
"season": "Kharif/Rabi",
"water": "Moderate",
"yield": "High"
},
"cotton": {
"season": "Kharif",
"water": "Moderate",
"yield": "Medium"
},
"wheat": {
"season": "Rabi",
"water": "Moderate",
"yield": "High"
},
"sorghum": {
"season": "Kharif/Rabi",
"water": "Low",
"yield": "Medium"
},
"pulses (pigeon pea / tur)": {
"season": "Kharif/Rabi",
"water": "Low",
"yield": "Low to Medium"
},
"groundnut": {
"season": "Kharif/Rabi",
"water": "Moderate",
"yield": "Medium"
},
"soybean": {
"season": "Kharif",
"water": "Moderate",
"yield": "Medium to High"
},
"sugarcane": {
"season": "Perennial (planted Feb–May)",
"water": "High",
"yield": "High"
},
"mustard (rapeseed)": {
"season": "Rabi",
"water": "Low to Moderate",
"yield": "Medium"
},
"chili (dry chillies)": {
"season": "Rabi/Kharif (depending on variety)",
"water": "Low to Moderate",
"yield": "Low to Medium"
},
"banana": {
"season": "Perennial (year-round production)",
"water": "High",
"yield": "High"
}
}


@app.route("/")
def home():
    return render_template("index.html")


@app.route("/predict", methods=["POST"])
def predict():
    try:
        # Get values from HTML form
        nitrogen = float(request.form["nitrogen"])
        phosphorous = float(request.form["phosphorous"])
        potassium = float(request.form["potassium"])
        temperature = float(request.form["temperature"])
        humidity = float(request.form["humidity"])
        ph = float(request.form["ph"])
        rainfall = float(request.form["rainfall"])

        # Create input array
        features = np.array([[
            nitrogen,
            phosphorous,
            potassium,
            temperature,
            humidity,
            ph,
            rainfall
        ]])

        # Predict crop
        prediction = model.predict(features)[0]
        prediction_key = str(prediction).lower()

        suitability = "High"
        analysis = []
        if rainfall > 150:
            analysis.append("✓ Good Rainfall")

        if 5.5 <= ph <= 7.5:
            analysis.append("✓ Suitable Soil pH")

        if humidity > 60:
            analysis.append("✓ Adequate Humidity")

        if nitrogen > 40:
            analysis.append("✓ Sufficient Nitrogen")

        score = len(analysis)

        if score >= 4:
            suitability = "High"
        elif score >= 2:
            suitability = "Medium"
        else:
            suitability = "Low"

        recommendations = []

        if rainfall < 100:
            recommendations.append("Use drip irrigation to conserve water.")
            

        if ph < 5.5:
            recommendations.append("Apply lime to increase soil pH.")


        elif ph > 7.5:
            recommendations.append("Use organic matter to reduce soil alkalinity.")
        

        if nitrogen < 40:
            recommendations.append("Increase nitrogen-rich fertilizers.")

        if humidity > 80:
            recommendations.append("Monitor crops for fungal diseases.")


        recommendations.append("Practice crop rotation to maintain soil fertility.")

        recommendations.append("Use organic fertilizers whenever possible.")

        
        environmental_insights = []

        if rainfall > 150:
            environmental_insights.append("Adequate rainfall supports healthy crop growth.")


        if humidity > 60:
            environmental_insights.append(
        "Humidity levels are favorable for cultivation."
    )

        if 5.5 <= ph <= 7.5:
            environmental_insights.append(
        "Soil pH is within the optimal range."
    )
        patterns = []

        patterns.append(
    "Most crops perform best when soil pH is between 5.5 and 7.5."
)

        if rainfall > 150:
            patterns.append(
        "Current rainfall conditions favor water-intensive crops."
    )

        if humidity > 70:
            patterns.append(
        "Higher humidity supports crops such as rice and banana."
    )

        if temperature > 25:
            patterns.append(
        "Warm temperatures are suitable for tropical crops."
    )
        resource_optimization = []

        if rainfall > 150:
            resource_optimization.append(
        "Reduce irrigation frequency to save water."
    )

        if nitrogen > 80:
            resource_optimization.append(
        "Avoid excessive nitrogen fertilizer usage."
    )

        resource_optimization.append(
    "Practice crop rotation to improve soil fertility."
)

        resource_optimization.append(
    "Use organic fertilizers for sustainable farming."
)
        decision_support = []

        if suitability == "High":
            decision_support.append(
        f"{prediction} is highly recommended under current conditions."
    )

        elif suitability == "Medium":
            decision_support.append(
        "Improve environmental conditions for better productivity."
    )

        else:
         decision_support.append(
        "Current conditions are not ideal for cultivation."
    )

        decision_support.append(
    "Monitor soil nutrients regularly."
)
        print("Prediction:", prediction)
        print("Type:", type(prediction))
        print(prediction_key)
        description = crop_info.get(
            prediction_key,
            "No crop information available."
        )
        details = crop_details.get(
            prediction_key,
            {}
        )
        return render_template(
            "index.html",
            prediction=prediction,
            description=description,
            details=details,
            suitability=suitability,
            analysis=analysis,
            recommendations=recommendations,
            environmental_insights=environmental_insights,
            patterns=patterns,
            resource_optimization=resource_optimization,
            decision_support=decision_support
        )
    except Exception as e:
        return render_template(
            "index.html",
            prediction="prediction failed",
            description=str(e)
        )


if __name__ == "__main__":
    app.run(debug=True)

