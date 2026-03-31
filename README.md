# Hash Table Analyzer

A Flask web application that visualizes how hash tables behave using different hash functions, collision strategies, and table sizes.

##  Features

* Builds **12 hash tables**:

  * 2 hash functions
  * 2 collision strategies (linear & quadratic probing)
  * 3 table sizes (1009, 2003, 5003)
* Displays:

  * Load factor
  * Collisions
  * Filled & empty slots
* Search any word across all tables
* Compare lookup performance (in microseconds)
* Highlights the fastest result

## Concepts Demonstrated

* Hash functions (sum & polynomial)
* Collision handling techniques
* Load factor and performance impact
* Time complexity comparison

##  Project Structure

```
hash-table-analyzer/
├── app.py
├── hashing_core.py
├── words.txt
├── requirements.txt
├── static/
│   └── style.css
└── templates/
    ├── index.html
    └── dashboard.html
```

##  Installation & Run

1. Clone the repository:

```
git clone https://github.com/your-username/hash-table-analyzer.git
cd hash-table-analyzer
```

2. Install dependencies:

```
pip install -r requirements.txt
```

3. Run the app:

```
python app.py
```

4. Open in browser:

```
http://127.0.0.1:5000
```

##  How It Works

* Click **Build Hash Tables** to generate all tables
* Use the search bar to look up a word
* Compare performance across all configurations
* The fastest lookup is highlighted

##  Technologies

* Python
* Flask
* HTML/CSS


---

Made as a data structures portfolio project.
