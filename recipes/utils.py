from io import BytesIO
import base64

import matplotlib
matplotlib.use("Agg") 

import matplotlib.pyplot as plt


def get_graph() -> str:
    """Return current matplotlib figure as a base64 string."""
    buffer = BytesIO()
    plt.savefig(buffer, format="png", bbox_inches="tight")
    buffer.seek(0)
    image_png = buffer.getvalue()
    graph = base64.b64encode(image_png).decode("utf-8")
    buffer.close()
    plt.close() 
    return graph


def get_chart(chart_type: str, df):
    """
    chart_type: "#1" bar, "#2" pie, "#3" line
    df: pandas DataFrame (must include: name, cooking_time, difficulty)
    Returns base64 string or None.
    """
    if df is None or df.empty or not chart_type:
        return None


    plt.clf()
    plt.figure(figsize=(7, 4))

    if chart_type == "#1":

        plt.bar(df["name"], df["cooking_time"])
        plt.xticks(rotation=45, ha="right")
        plt.xlabel("Recipe")
        plt.ylabel("Cooking time (min)")
        plt.title("Cooking time per recipe")

    elif chart_type == "#2":

        counts = df["difficulty"].fillna("Unknown").value_counts()
        plt.pie(counts.values, labels=counts.index, autopct="%1.0f%%")
        plt.title("Difficulty distribution")

    elif chart_type == "#3":

        plt.plot(df["name"], df["cooking_time"], marker="o")
        plt.xticks(rotation=45, ha="right")
        plt.xlabel("Recipe")
        plt.ylabel("Cooking time (min)")
        plt.title("Cooking time trend")

    else:
        return None

    plt.tight_layout()
    return get_graph()
