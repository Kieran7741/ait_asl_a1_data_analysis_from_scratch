# Applied scripting languages assignment 1

* Data science from scratch using python without existing statistics modules.
* This assignment was completed as part of a Postgraduate Cert in Artificial Intelligence in AIT
## Getting Started

### Prerequisites

Clone this repo from github.

### Installing

This project has been tested on macOS and on Ubuntu

It is recommended that you create a virtual environment and pip install the contents of requirements.txt
```
python3.7 -m venv .env
source .env/bin/activate
pip install -r requirements.txt
```

### Running

To run the project ensure you are in the root of the project.

```
python main.py 'Arsenal'
python main.py 'Manchester United'
```

### Running flask app

The flask app will be served on the localhost port 5000

```
python app.py
```

Visit http://127.0.0.1:5000/dashboard/Arsenal to display the dashboard

### Running unit tests

Ensure you are in the root of the project. The below shows the running of test_conversions.py
```
python -m unittest utils.tests.test_conversions
```


## Authors

* **Kieran Lyons** - *Initial work* - [Kieran7741](https://github.com/Kieran7741)


