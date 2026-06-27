import plotly.express as px
import plotly.graph_objects as go
import pandas as pd


def plot_score_comparison(results: list[dict]):
    df = pd.DataFrame(results)
    fig = go.Figure()
    fig.add_trace(go.Bar(name="Overall", x=df["name"], y=df["overall_score"]))
    fig.add_trace(go.Bar(name="Semantic", x=df["name"], y=df["semantic_score"]))
    fig.add_trace(go.Bar(name="TF-IDF", x=df["name"], y=df["tfidf_score"]))
    fig.add_trace(go.Bar(name="Skills", x=df["name"], y=df["skill_score"]))
    fig.update_layout(
        title="Candidate Score Comparison",
        xaxis_title="Candidates",
        yaxis_title="Score (%)",
        barmode="group",
        height=450,
    )
    return fig


def plot_skill_heatmap(results: list[dict], all_skills: list[str]):
    data = []
    for r in results:
        row = [1 if s in r["matched_skills"] else 0 for s in all_skills]
        data.append(row)
    fig = px.imshow(
        data,
        x=all_skills,
        y=[r["name"] for r in results],
        color_continuous_scale="blues",
        title="Skill Match Matrix",
        labels={"x": "Skills", "y": "Candidates"},
        aspect="auto",
    )
    fig.update_layout(height=300 + len(results) * 50)
    return fig


def plot_top_skills(skills_freq: dict):
    df = pd.DataFrame(list(skills_freq.items()), columns=["Skill", "Count"])
    df = df.sort_values("Count", ascending=True).tail(15)
    fig = px.bar(df, x="Count", y="Skill", orientation="h", title="Top Skills Across All Resumes")
    fig.update_layout(height=400)
    return fig
