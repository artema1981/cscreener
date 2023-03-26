# Application: Tracking Large Limit Orders on Binance using Python Django #
*This Python Django-based application displays large limit orders on spot and perpetual futures with a size of 250000, 500000, 750000, and 1000000 USD and their distance from the spread in percentages for all perpetual futures on the Binance exchange.*

## Installation ##
### To install the application, follow these steps: ###

1. Create a Python virtual environment and activate it.
2. Clone the repository from Github.
3. Navigate to the directory where the repository was cloned.
4. Install the required packages using the command: pip install -r requirements.txt.
5. after install requirements.txt rename folder binance (venv/Lib/site-packages/)
7. comand pip install binance-connector==3.0.0rc1
8. Start the server using the command: python manage.py runserver.

## Usage ##
*To use the application, follow these steps:*

1. Open your web browser and go to http://localhost:8000/orders.
2. The application will display a table of large limit orders on spot and perpetual futures with a size of 250000, 500000, 750000, and 1000000 USD and their distance from the spread in percentages for all perpetual futures on the Binance exchange.

## Development ##
*To further develop the application, follow these steps:*

1. Create a Python virtual environment and activate it.
2. Clone the repository from Github.
3. Navigate to the directory where the repository was cloned.
4. Install the required packages using the command: pip install -r requirements.txt.
5. Make the necessary changes to the code.
6. Deploy the changes to a production server.
