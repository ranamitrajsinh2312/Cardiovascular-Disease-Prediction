# Cardio Dashboard API

This project is a RESTful API for the Cardio Dashboard application. It provides endpoints for accessing model performance metrics and other related data.

## Project Structure

- `api_server.py`: Contains the main application logic for the API server, defining endpoints and handling requests and responses.
- `requirements.txt`: Lists the dependencies required for the Python application.
- `vercel.json`: Configuration file for deploying the API server on Vercel.

## Setup Instructions

1. **Clone the Repository**
   ```bash
   git clone <repository-url>
   cd cardio-dashboard-api
   ```

2. **Install Dependencies**
   Make sure you have Python and pip installed. Then run:
   ```bash
   pip install -r requirements.txt
   ```

3. **Run the API Server**
   You can run the API server locally using:
   ```bash
   python api_server.py
   ```

4. **Deployment**
   To deploy the API server on Vercel, ensure that your `vercel.json` is correctly configured and then run:
   ```bash
   vercel
   ```

## Usage

Once the API server is running, you can access the endpoints to retrieve model performance metrics and other data. Refer to the API documentation for specific endpoints and their usage.

## License

This project is licensed under the MIT License. See the LICENSE file for details.