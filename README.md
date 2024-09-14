<!-- GETTING STARTED -->
## Getting Started

To get a local copy up and running follow these simple steps.

1. `pip3 install -r requirements.txt`
2. `gunicorn -w 4 -b 0.0.0.0:5000 app:app`

### Prerequisites

You must have python3 and gunicorn (version 23.0.0) installed on your local machine
