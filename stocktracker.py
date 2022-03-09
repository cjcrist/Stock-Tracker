#!/usr/bin/env python3

# standard library
import urllib3
import sys
import json

# 3rd party imports
import click
from pyaml_env import parse_config

# local imports
from stock_tracker.utils.logger import Logger
from stock_tracker.core.core import Stock
from stock_tracker.utils.dot import Dot

urllib3.disable_warnings(urllib3.exceptions.InsecureRequestWarning)


@click.group()
@click.option('-c', '--config', type=click.Path(exists=True), default='stocktracker.yaml', help="Configuration File")
@click.option('-d', '--debug', is_flag=True, help="Print Debug output to STDERR")
@click.option('-v', '--verbose', is_flag=True, help="Print ALL logging modules to output")
@click.pass_context
def cli(ctx, config, debug, verbose):
    """
    Simple app to retrieve stock data from AlphaVantage.co

    Function documentation can be found at:\nhttps://www.alphavantage.co/documentation/#
    """
    # Setup logging
    LOGGER = Logger('stocktracker.main')
    LOGGER.set_loggers(['stocktracker.core'])
    LOGGER.setup_logging(debug=debug, verbose=verbose)
    try:
        conf = parse_config(config)
    except IOError as e:
        LOGGER.error(str(e))
        sys.exit(1)

    ctx.ensure_object(dict)
    ctx.obj['Logger'] = LOGGER
    ctx.obj['config'] = conf


@cli.command()
@click.option('-r', '--raw', is_flag=True, help="Raw printout of response for parsing with jq")
@click.option('-f', '--fields', multiple=True, help="Required fields to validate the request")
@click.option('-c', '--command', default="TIME_SERIES_DAILY", help="Stock function to call. Must be listed in config.")
@click.pass_obj
def fetch(ctx, raw, fields, command):
    """
    Currently fetches the function being sent to the API

    Pass --command to call a new function.

    Function and parameters must be listed in the config file.
    path: tracker.query.function

    View README for details.
    """
    LOGGER = ctx['Logger']
    config = Dot(ctx['config'])
    stock = Stock(config)
    # Fetch response from API
    try:
        for query in config.tracker.query:
            if command == query['function']:
                if fields:
                    stock.validate_fields(query, fields)
                    stock.validated = True
                stock.fetch(query)
        if raw:
            LOGGER.debug(stock.response)
            print(json.dumps(stock.response))
        else:
            LOGGER.info(stock.response)
    except Exception as e:
        LOGGER.error(str(e))
        sys.exit(1)


if __name__ == "__main__":
    cli()
