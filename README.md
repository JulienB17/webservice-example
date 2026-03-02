# webservice-example

# Segmented Linear Trend Web Service

This project is a simple example of a client-server web architecture using:

- Front-end: HTML + JavaScript
- Back-end: Flask (Python)
- Scientific computation: NumPy + Matplotlib

The web service computes segmented linear trends from a 2-column CSV time series.

---

# 1. Project Structure

```

project/
│
├── client/
│   ├── index.html
│   └── script.js
│
└── server/
    ├── app.py
    └── toolbox.py
```

## client/
Contains the web interface:
- CSV file upload
- Discontinuity input
- API request (JSON)
- Plot visualization
- JSON result download

## server/
Contains:
- Flask API (app.py)
- Scientific computation logic (toolbox.py)

Separation of concerns:
- API layer (Flask)
- Numerical processing layer (NumPy)
- Visualization layer (Matplotlib)

---

# 2. Installation

## 2.1 Create Conda Environment

A Conda environment file is provided:

```

webservice_env.yml

```

Create environment:

```

conda env create -f webservice_env.yml

```

Activate:

```

conda activate webservice_env

```

---

# 3. Run the Application

From the `server` directory:

```

python app.py

```

The server runs on:

```

[http://127.0.0.1:5000](http://127.0.0.1:5000)

```

Open the client in a browser (served via Flask or HTTP server).

---

# 4. JSON Exchange Format

## Client → Server

POST `/api/linear_trend`

```json
{
    "x": [1,2,3,...],
    "y": [10,11,13,...],
    "disc": [25,48,72],
    "x_label": "time",
    "y_label": "height"
}
````

## Server → Client

```json
{
    "series": [
        { "x": [...], "y": [...], "a": 0.02, "b": 4.3 },
        { "x": [...], "y": [...], "a": 0.01, "b": 5.1 }
    ],
    "disc": [25,48,72],
    "x_label": "time",
    "y_label": "height",
    "image": "base64_encoded_png"
}
```

Downloaded JSON (simplified):

```json
{
    "disc": [25,48,72],
    "x_label": "time",
    "y_label": "height",
    "series": [
        { "a": 0.02, "b": 4.3 },
        { "a": 0.01, "b": 5.1 }
    ]
}
```


# 5. Author

[Julien Barneoud](https://www.ipgp.fr/annuaire/barneoud/)
