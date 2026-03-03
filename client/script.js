/*
Client-side logic.

- Read CSV file in browser
- Parse two-column data (x,y)
- Send JSON request to API
- Display returned JSON
- Display returned image
*/

// ---------------------------------------------------------------------
// CONFIG
// ---------------------------------------------------------------------

const API_BASE_URL = "http://127.0.0.1:5000";

let lastResult = null;  // store server response
let inputFileName = "results"; // default out filename

// ---------------------------------------------------------------------
// CSV PARSER (with header)
// ---------------------------------------------------------------------

function parseCSV(text) {

    const lines = text.trim().split("\n");

    // First line = column labels
    const header = lines[0].split(",");
    const x_label = header[0].trim();
    const y_label = header[1].trim();

    let x = [];
    let y = [];

    // Start at line 1 (skip header)
    for (let i = 1; i < lines.length; i++) {
        const parts = lines[i].split(",");
        x.push(parseFloat(parts[0]));
        y.push(parseFloat(parts[1]));
    }

    return { x, y, x_label, y_label };
}


// -----------------------------------------------------------
// SEND DATA
// -----------------------------------------------------------
function sendData() {

    const file = document.getElementById("fileInput").files[0];
    const discText = document.getElementById("discInput").value;

    if (!file) {
        alert("Please select a CSV file.");
        return;
    }
    // Store original filename (without extension), usefull to set output name later..
    inputFileName = file.name.replace(/\.csv$/i, "");

    const reader = new FileReader();

    reader.onload = function(e) {

        const parsed = parseCSV(e.target.result);

        const disc = discText.length > 0
            ? discText.split(",").map(Number)
            : [];

        fetch(`${API_BASE_URL}/linear_trend`, {
            method: "POST",
            headers: {"Content-Type": "application/json"},
            body: JSON.stringify({
                x: parsed.x,
                y: parsed.y,
                disc: disc,
                x_label: parsed.x_label,
                y_label: parsed.y_label
            })
        })
        .then(res => res.json())
        .then(data => {

            lastResult = data;

            // Display only slope/intercept
            displayModelParameters(data.series);

            // Display plot
            document.getElementById("plotImg").src =
                "data:image/png;base64," + data.image;
            document.getElementById("resultContainer").style.display = "block";
        });
    };

    reader.readAsText(file);
}


// Set API link dynamically
document.addEventListener("DOMContentLoaded", function () {
    const apiLink = document.getElementById("apiLink");
    apiLink.href = API_BASE_URL;
    apiLink.textContent = API_BASE_URL;
});

// -----------------------------------------------------------
// DISPLAY ONLY MODEL PARAMETERS
// -----------------------------------------------------------

function displayModelParameters(series) {

    let text = "Estimated linear models (y=a*x+b) per segment:\n\n";

    series.forEach((seg, index) => {
        text += `Segment ${index + 1}:\n`;
        text += `   a (slope)     = ${seg.a}\n`;
        text += `   b (intercept) = ${seg.b}\n\n`;
    });

    document.getElementById("resultBox").textContent = text;
}

// -----------------------------------------------------------
// DOWNLOAD JSON (WITHOUT IMAGE)
// -----------------------------------------------------------

function downloadJSON() {

    if (!lastResult) return;

    const fullData = JSON.parse(JSON.stringify(lastResult));

    // Remove image field
    delete fullData.image;

    const blob = new Blob(
        [JSON.stringify(fullData, null, 4)],
        { type: "application/json" }
    );

    const url = URL.createObjectURL(blob);

    const a = document.createElement("a");
    a.href = url;

    // Use original CSV name
    a.download = inputFileName + "_model.json";

    a.click();

    URL.revokeObjectURL(url);
}
