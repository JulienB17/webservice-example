/*
Client-side logic.

Responsibilities:
- Read CSV file in browser
- Parse two-column data (x,y)
- Send JSON request to API
- Display returned JSON
- Display returned image

No scientific computation is done here.
*/

// ---------------------------------------------------------------------
// CONFIGURATION
// ---------------------------------------------------------------------

// Default: local development server
const API_BASE_URL = "http://127.0.0.1:5000";




// ---------------------------------------------------------------------
// CSV PARSER
// ---------------------------------------------------------------------
/**
 * Parse a simple 2-column CSV file (x,y).
 * Assumes comma-separated values.
 */
function parseCSV(text) {

    const lines = text.trim().split("\n");

    let x = [];
    let y = [];

    lines.forEach(line => {

        const parts = line.split(",");

        x.push(parseFloat(parts[0]));
        y.push(parseFloat(parts[1]));
    });

    return {x, y};
}


// ---------------------------------------------------------------------
// API CALL
// ---------------------------------------------------------------------
/**
 * Send data to Flask API using POST JSON.
 */
function sendData() {

    const file = document.getElementById("fileInput").files[0];
    const discText = document.getElementById("discInput").value;

    if (!file) {
        alert("Please select a CSV file.");
        return;
    }

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
                disc: disc
            })
        })
        .then(res => res.json())
        .then(data => {

            // Display JSON result
            document.getElementById("result").textContent =
                JSON.stringify(data.series, null, 4);

            // Display image
            document.getElementById("plotImg").src =
                "data:image/png;base64," + data.image;
        });
    };

    reader.readAsText(file);
}
