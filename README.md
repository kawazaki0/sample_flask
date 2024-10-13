# Sample Flask Project

This is a sample Flask project.

## Installation

1. Clone the repository:
    ```sh
    git clone https://github.com/kawazaki0/sample_flask.git
    cd sample_flask
    ```

2. Create a virtual environment:
    ```sh
    python -m venv venv
    source venv/bin/activate  # On Windows use `venv\Scripts\activate`
    ```

3. Install the dependencies:
    ```sh
    pip install -r requirements.txt
    ```

## Running the Application

1. Set environment variables:
    ```sh
    export FLASK_SKIP_DOTENV=1  # on Windows use `set FLASK_SKIP_DOTENV=1`
    ```

2. Run the Flask application:
    ```sh
    python sample_flask/app.py
    ```

3. Open your web browser and go to `http://127.0.0.1:5000/`.

## Test

Run the tests:
    ```sh
    pytest
    ```

## License

This project is licensed under the MIT License.
