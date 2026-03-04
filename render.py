from flask import Flask, jsonify
import numpy as np
from scipy import stats

app = Flask(__name__)

@app.route("/")
def hypothesis_test():

    alpha = 0.05
    xbar = 0.7
    H0 = 0.8
    n = 150

    SD = np.sqrt(xbar * (1 - xbar))
    s = SD / np.sqrt(n)

    tcal = (xbar - H0) / s

    t_table_negative = stats.t.ppf(alpha / 2, n - 1)
    t_table_positive = stats.t.ppf(1 - alpha / 2, n - 1)

    p_value = stats.t.cdf(tcal, n - 1) * 2

    if tcal < t_table_negative or tcal > t_table_positive:
        result = "Reject the Null Hypothesis (H0)"
    else:
        result = "Fail to Reject the Null Hypothesis (H0)"

    return jsonify({
        "Standard Error": float(s),
        "Calculated t-score": float(tcal),
        "Critical Negative": float(t_table_negative),
        "Critical Positive": float(t_table_positive),
        "P-value": float(p_value),
        "Result": result
    })


if __name__ == "__main__":
    app.run(host="0.0.0.0", port=10000)