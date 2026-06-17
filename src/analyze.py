import pandas as pd
import plotly.express as px
import plotly.graph_objects as go
from plotly.subplots import make_subplots

def analyze(path="data/kepler_clean.csv"):
    df = pd.read_csv(path)

    bins = [0, 1.25, 2, 4, 6, 14, 100]
    labels = ["Rocky", "Super-Earth", "Sub-Neptune", "Neptune", "Sub-Jovian", "Jovian"]
    df["size_class"] = pd.cut(df["koi_prad"], bins=bins, labels=labels)

    df_temp = df.dropna(subset=["koi_teq"])
    hz = df_temp[(df_temp["koi_teq"] >= 200) & (df_temp["koi_teq"] <= 320)]

    fig = make_subplots(rows=1, cols=3, subplot_titles=(
        "Period vs Radius", "Planet Size Distribution", "Habitable Zone Candidates"
    ))

    # Chart 1
    fig.add_trace(go.Scatter(
        x=df["koi_period"], y=df["koi_prad"],
        mode="markers", marker=dict(size=3, opacity=0.4, color="steelblue"),
        name="Planets"
    ), row=1, col=1)

    # Chart 2
    counts = df["size_class"].value_counts().reindex(labels)
    fig.add_trace(go.Bar(
        x=counts.index.tolist(), y=counts.values, marker_color="coral", name="Size"
    ), row=1, col=2)

    # Chart 3
    fig.add_trace(go.Histogram(
        x=df_temp["koi_teq"], nbinsx=60, name="All planets",
        marker_color="gray", opacity=0.6
    ), row=1, col=3)
    fig.add_trace(go.Histogram(
        x=hz["koi_teq"], nbinsx=30, name=f"HZ candidates (n={len(hz)})",
        marker_color="green", opacity=0.8
    ), row=1, col=3)

    fig.update_xaxes(type="log", row=1, col=1)
    fig.update_yaxes(type="log", row=1, col=1)
    fig.update_layout(title="Kepler Exoplanet Trends", height=500)
    fig.write_html("kepler_trends.html")
    fig.show()
    print(f"Habitable Zone candidates: {len(hz)}")
    print("Chart saved to kepler_trends.html")

if __name__ == "__main__":
    analyze()