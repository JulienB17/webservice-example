# webservice-example

# Segmented Linear Trend Web Service

This project is a simple example of a client-server web architecture using:

- Front-end: web (HTML + JavaScript + CSS)
- Back-end: Flask (Python)
- Scientific computation: Python (NumPy + Matplotlib)

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
- Flask API (app.py). *All end points listed in app.py with '@app.route' decorator.*
- Scientific computation logic (toolbox.py)

Separation of concerns:
- API layer (Flask)
- Numerical processing layer (NumPy)
- Visualization layer (Matplotlib)

---

# 2. Installation

Python required libraries are listed in `env/requirements.txt`. We recommand to use [conda environment](https://docs.conda.io/projects/conda/en/latest/user-guide/tasks/manage-environments.html).

## 2.1 With Conda Environment

A Conda environment file is provided in `env/`:
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
Then you can lauch API in this env (see next section 3.)


## 2.2 With requirements.txt

Install the libraries in another environment (e.g., pyenv, an existing conda environment, etc.) or in the base environment (not recommended!):
```
pip install -r env/requirements.txt
```

---

# 3. Run the Application

From the `server` directory, lauch flask server (already in `app.py` __main__):

```
python app.py
```
The server runs on [http://127.0.0.1:5000](http://127.0.0.1:5000).

Open the client in a browser. From the `client` directory you can lauch a http server (avoid "Cross origin" issues):
```
python -m http.server 8000
```

> API domain & port may be configure: 
> server/app.py: var `HOST` and `PORT`
> client/script.js: const `API_BASE_URL`
> Be consistent between client & server API address!

---
# 4. Example usage

## Open CSV data
Example CSV data available in `doc/GOLD_h.csv`, with height time series of GOLD GNSS station (more info on [webigs-ref](https://webigs-rf.ign.fr/stations/GOLD) & [ITRF](https://itrf.ign.fr/en/station/GOLD-40405S028) websites).

For this simple example:
- Comma ',' separator
- Exactly 2 columns (x, y)
- First line considered as header (i.e. columns labels)

## Submit data to server using API
Click on `Compute Trend` button.
Data send as JSON, result received as JSON (see 5. Section)


## See results
Server send througth API:
- Graph (time serie as point, model red lines)
- JSON (downloadable with button)

## Retry with discontinuities
User can add date discontinuities to calculate segmented linear trend. In form x values 
GOLD casediscontinuities: 1995.9,2000,2019,...
Re-submit as you want & adjust dates of discontinuities! Then you can save final graph & download JSON file (with a,b coeff by segment).

---

# 5. JSON Exchange Format

## Client -> Server

POST `/api/linear_trend`

```json
{
    "x": [1,2,3,...],
    "y": [10,11,13,...],
    "disc": [25,48,72],
    "x_label": "time",
    "y_label": "height"
}
```

## Server -> Client

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


# 6. Author

[Julien Barneoud](https://www.ipgp.fr/annuaire/barneoud/)
