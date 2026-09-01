import json, math
import pandas as pd
from src.triage import AfyaTriageEngine

def generate_charts():
    # Load dataset & evaluate
    df = pd.read_csv("data/patient_triage_data.csv")
    engine = AfyaTriageEngine()
    levels, overrides = engine.classify(df)
    df['triage_level'] = levels

    counts = df['triage_level'].value_counts().sort_index()
    labels = {1: "Level 1 (Critical)", 2: "Level 2 (Emergent)", 3: "Level 3 (Urgent)", 4: "Level 4 (Non-urgent)"}
    colors = {1: "#dc2626", 2: "#ea580c", 3: "#d97706", 4: "#16a34a"}

    # Chart 1: Triage Level Distribution SVG
    total = len(df)
    svg_bars = ""
    y_pos = 50
    for level, count in counts.items():
        pct = (count / total) * 100
        width = int((count / total) * 350)
        color = colors.get(level, "#6b7280")
        label = labels.get(level, f"Level {level}")
        svg_bars += f'''
        <text x="20" y="{y_pos + 15}" fill="#f3f4f6" font-family="sans-serif" font-size="13">{label}</text>
        <rect x="160" y="{y_pos}" width="{width}" height="22" rx="4" fill="{color}" />
        <text x="{170 + width}" y="{y_pos + 16}" fill="#d1d5db" font-family="sans-serif" font-size="12">{count} ({pct:.1f}%)</text>
        '''
        y_pos += 40

    svg1 = f'''<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 600 230" width="100%" style="background:#111827; border-radius:8px; padding:10px;">
        <text x="20" y="30" fill="#ffffff" font-family="sans-serif" font-size="16" font-weight="bold">Afya Triage Population Distribution (N={total})</text>
        {svg_bars}
    </svg>'''

    with open("docs/triage_distribution.svg", "w") as f:
        f.write(svg1)

    print("[Visualizer]: Created docs/triage_distribution.svg")

if __name__ == "__main__":
    generate_charts()
