from flask import Flask, request, jsonify
import pandas as pd
from src.triage import AfyaTriageEngine

app = Flask(__name__)
engine = AfyaTriageEngine()

@app.route('/health', methods=['GET'])
def health_check():
    return jsonify({
        "status": "healthy",
        "service": "afya-triage",
        "version": "1.0.0"
    }), 200

@app.route('/triage', methods=['POST'])
def triage_single():
    data = request.get_json()
    if not data:
        return jsonify({"error": "No input data provided"}), 400
    
    df = pd.DataFrame([data])
    levels, overrides = engine.classify(df)
    
    return jsonify({
        "triage_level": int(levels[0]),
        "category": f"Level {levels[0]} - {engine.get_level_name(levels[0])}",
        "hypoxia_safety_override": bool(overrides[0])
    }), 200

@app.route('/triage/batch', methods=['POST'])
def triage_batch():
    data = request.get_json()
    if not isinstance(data, list):
        return jsonify({"error": "Batch payload must be a JSON array"}), 400
    
    df = pd.DataFrame(data)
    levels, overrides = engine.classify(df)
    
    results = []
    for level, override in zip(levels, overrides):
        results.append({
            "triage_level": int(level),
            "category": f"Level {level} - {engine.get_level_name(level)}",
            "hypoxia_safety_override": bool(override)
        })
        
    return jsonify({
        "count": len(results),
        "results": results
    }), 200

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=8000)
