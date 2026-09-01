from flask import Flask, request, jsonify
import pandas as pd
from src.triage import AfyaTriageEngine

app = Flask(__name__)
engine = AfyaTriageEngine()

tier_mapping = {
    1: "Level 1 - Critical",
    2: "Level 2 - Emergent",
    3: "Level 3 - Urgent",
    4: "Level 4 - Non-urgent"
}

@app.route('/', methods=['GET'])
def health_check():
    return jsonify({"status": "healthy", "service": "Afya Triage Microservice"})

@app.route('/triage', methods=['POST'])
def triage_patient():
    try:
        data = request.get_json()
        required = ['systolic_bp', 'diastolic_bp', 'heart_rate', 'respiratory_rate', 'oxygen_saturation', 'temperature']
        for field in required:
            if field not in data:
                return jsonify({"error": f"Missing required field: {field}"}), 400

        df = pd.DataFrame([data])
        levels, overrides = engine.classify(df)

        level = int(levels[0])
        return jsonify({
            "triage_level": level,
            "category": tier_mapping[level],
            "hypoxia_safety_override": bool(overrides[0])
        })
    except Exception as e:
        return jsonify({"error": str(e)}), 500

@app.route('/triage/batch', methods=['POST'])
def triage_batch():
    try:
        data = request.get_json()
        if not isinstance(data, list):
            return jsonify({"error": "Payload must be a JSON array of patient vital objects"}), 400

        df = pd.DataFrame(data)
        levels, overrides = engine.classify(df)

        results = []
        for lvl, ovr in zip(levels, overrides):
            level = int(lvl)
            results.append({
                "triage_level": level,
                "category": tier_mapping[level],
                "hypoxia_safety_override": bool(ovr)
            })

        return jsonify({"count": len(results), "results": results})
    except Exception as e:
        return jsonify({"error": str(e)}), 500

if __name__ == "__main__":
    app.run(host="0.0.0.0", port=8000)
