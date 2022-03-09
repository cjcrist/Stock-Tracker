# Stock Tracker
### A simple application to retrieve stock data.

More commands and functionality will be added down the road.

The API documentation can be found: [here](https://www.alphavantage.co/documentation/#) .

### Usage:
<strong>main</strong>
```commandline
python3 stocktracker.py --help
Usage: stocktracker.py [OPTIONS] COMMAND [ARGS]...

      Simple app to retrieve stock data from AlphaVantage.co

      Function documentation can be found at:
      https://www.alphavantage.co/documentation/#

Options:
  -c, --config PATH  Configuration File
  -d, --debug        Print Debug output to STDERR
  -v, --verbose      Print ALL logging modules to output
  --help             Show this message and exit.

Commands:
  fetch  Currently fetches the function being sent to the API
```

<strong>fetch</strong>
```commandline
python3 stocktracker.py fetch --help
Usage: stocktracker.py fetch [OPTIONS]

  Currently fetches the function being sent to the API

  Pass --command to call a new function.

  Function and parameters must be listed in the config file. path:
  tracker.query.function

  View README for details.

Options:
  -r, --raw           Raw printout of response for parsing with jq
  -f, --fields TEXT   Required fields to validate the request
  -c, --command TEXT  Stock function to call. Must be listed in config.
  --help              Show this message and exit.
```

### Config
A basic configuration will have the:
* endpoint
* auth api key
  * can be set in environment variables with the !ENV tag.
* query parameters
  * The function names and parameters needed can be found on the API author's website.

Below is a basic configuration with 1 function listed
```yaml
---
tracker:
  endpoint: https://www.alphavantage.co/query
  auth: !ENV ${TOKEN}
  query:
    - function: TIME_SERIES_DAILY
      symbol: RIVN
      outputsize: full
```