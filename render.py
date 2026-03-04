from flask import Flask, request, jsonify
import pandas as pd
import numpy as np
from scipy import stats

app = Flask(__name__)

@app.route("/")
def home():
    return """
    <h2>CSV Hypothesis Testing</h2>

    <form action="/test" method="post" enctype="multipart/form-data">
        Upload CSV: <input type="file" name="file"><br><br>

        Column Name: <input type="text" name="column"><br><br>

        Significance Level (alpha): <input type="text" name="alpha"><br><br>

        Hypothesized Mean (H0): <input type="text" name="H0"><br><br>

        <input type="submit" value="Run Hypothesis Test">
    </form>
    """

@app.route("/test", methods=["POST"])
def hypothesis_test():

    file = request.files["file"]
    column = request.form["column"]
    alpha = float(request.form["alpha"])
    H0 = float(request.form["H0"])

    df = pd.read_csv(file)

    if column not in df.columns:
        return jsonify({"error": "Column not found in dataset"})

    data = df[column].dropna()

    xbar = np.mean(data)
    n = len(data)
    sd = np.std(data, ddof=1)

    se = sd / np.sqrt(n)

    tcal = (xbar - H0) / se

    t_neg = stats.t.ppf(alpha / 2, n - 1)
    t_pos = stats.t.ppf(1 - alpha / 2, n - 1)

    p_value = stats.t.cdf(tcal, n - 1) * 2

    if tcal < t_neg or tcal > t_pos:
        result = "Reject H0"
    else:
        result = "Fail to Reject H0"

    return jsonify({
        "column": column,
        "sample_mean": float(xbar),
        "n": n,
        "t_score": float(tcal),
        "p_value": float(p_value),
        "critical_negative": float(t_neg),
        "critical_positive": float(t_pos),
        "result": result
    })


if __name__ == "__main__":
    app.run(host="0.0.0.0", port=10000)

