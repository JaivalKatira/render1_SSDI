from flask import Flask, request, render_template_string
import pandas as pd
import numpy as np
from scipy import stats

app = Flask(__name__)

html_page = """
<!DOCTYPE html>
<html>
<head>
<title>CSV Hypothesis Testing</title>

<style>
body{
    background:#111;
    color:white;
    font-family:Arial;
    display:flex;
    justify-content:center;
    align-items:center;
    height:100vh;
}

.container{
    background:#1e1e1e;
    padding:40px;
    border-radius:10px;
    width:450px;
}

h2{
    text-align:center;
}

input, select{
    width:100%;
    padding:8px;
    margin-top:5px;
    margin-bottom:15px;
    border-radius:5px;
    border:none;
}

button{
    width:100%;
    padding:10px;
    background:white;
    color:black;
    border:none;
    border-radius:5px;
    font-weight:bold;
}

button:hover{
    background:#ddd;
}

.result{
    margin-top:20px;
    background:#222;
    padding:15px;
    border-radius:5px;
}
</style>

<script>
function loadColumns(){

    let fileInput = document.getElementById("file")

    let reader = new FileReader()

    reader.onload = function(e){

        let text = e.target.result

        let firstLine = text.split("\\n")[0]

        let columns = firstLine.split(",")

        let dropdown = document.getElementById("column")

        dropdown.innerHTML=""

        columns.forEach(col=>{
            let option = document.createElement("option")
            option.value=col
            option.text=col
            dropdown.appendChild(option)
        })
    }

    reader.readAsText(fileInput.files[0])
}
</script>

</head>

<body>

<div class="container">

<h2>CSV Hypothesis Testing</h2>

<form action="/test" method="post" enctype="multipart/form-data">

<label>Upload CSV</label>
<input type="file" name="file" id="file" onchange="loadColumns()" required>

<label>Select Column</label>
<select name="column" id="column"></select>

<label>Significance Level (α)</label>
<input type="number" step="0.01" name="alpha" value="0.05">

<label>Hypothesized Mean (H0)</label>
<input type="number" step="0.01" name="H0">

<button type="submit">Run Hypothesis Test</button>

</form>

{% if result %}

<div class="result">

<h3>Results</h3>

Sample Mean: {{mean}} <br>
Sample Size: {{n}} <br>
T-score: {{t}} <br>
P-value: {{p}} <br>

<h3>{{result}}</h3>

</div>

{% endif %}

</div>

</body>
</html>
"""


@app.route("/")
def home():
    return render_template_string(html_page)


@app.route("/test", methods=["POST"])
def hypothesis_test():

    file = request.files["file"]
    column = request.form["column"]
    alpha = float(request.form["alpha"])
    H0 = float(request.form["H0"])

    df = pd.read_csv(file)

    data = df[column].dropna()

    xbar = np.mean(data)
    n = len(data)
    sd = np.std(data, ddof=1)

    se = sd / np.sqrt(n)

    tcal = (xbar - H0) / se

    p_value = stats.t.cdf(tcal, n - 1) * 2

    if p_value < alpha:
        result = "Reject Null Hypothesis"
    else:
        result = "Fail to Reject Null Hypothesis"

    return render_template_string(
        html_page,
        result=result,
        mean=round(xbar,3),
        n=n,
        t=round(tcal,3),
        p=round(p_value,5)
    )


if __name__ == "__main__":
    app.run(host="0.0.0.0", port=10000)

