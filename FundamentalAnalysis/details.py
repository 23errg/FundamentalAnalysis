from urllib.request import urlopen
import json
import pandas as pd


def available_companies(api_key):
    """
    Description
    ----
    Gives all tickers, company names, current price and stock exchange that are available
    for retrieval for financial statements, ratios and extended stock data. General stock
    data can be retrieved for any company or financial instrument.

    Input
    ----
    api_key (string)
        The API Key obtained from https://financialmodelingprep.com/developer/docs/

    Output
    ----
    data (dataframe)
        Data with the ticker as the index and the company name, price and
        stock exchange in the columns.
    """
    response = urlopen("https://financialmodelingprep.com/api/v3/company/stock/list?apikey=" + api_key)
    data = response.read().decode("utf-8")
    data_json = json.loads(data)['symbolsList']

    df = pd.DataFrame(data_json)
    df.loc[df["name"].isna(), "name"] = df["symbol"]
    df = df.set_index("symbol")

    return df


def profile(ticker, api_key):
    """
    Description
    ----
    Gives information about the profile of a company which includes
    i.a. beta, company description, industry and sector.

    Input
    ----
    ticker (string)
        The company ticker (for example: "AAPL")
    api_key (string)
        The API Key obtained from https://financialmodelingprep.com/developer/docs/

    Output
    ----
    data (dataframe)
        Data with variables in rows and the period in columns.
    """
    response = urlopen("https://financialmodelingprep.com/api/v3/company/profile/" + ticker + "?apikey=" + api_key)
    data = response.read().decode("utf-8")
    data_formatted = pd.DataFrame(json.loads(data)['profile'], index=['profile']).T

    return data_formatted


def quote(ticker, api_key):
    """
    Description
    ----
    Gives information about the quote of a company which includes i.a.
    high/low close prices, price-to-earning ratio and shares outstanding.

    Input
    ----
    ticker (string)
        The company ticker (for example: "AMD")
    api_key (string)
        The API Key obtained from https://financialmodelingprep.com/developer/docs/

    Output
    ----
    data (dataframe)
        Data with variables in rows and the period in columns.
    """
    response = urlopen("https://financialmodelingprep.com/api/v3/quote/" + ticker + "?apikey=" + api_key)
    data = response.read().decode("utf-8")
    data_formatted = pd.DataFrame(json.loads(data)[0], index=["quote"]).T

    return data_formatted


def enterprise(ticker, api_key, period="annual"):
    """
    Description
    ----
    Gives information about the enterprise value of a company which includes
    i.a. market capitalisation, Cash & Cash Equivalents, total debt and enterprise value.

    Input
    ----
    ticker (string)
        The company ticker (for example: "TSLA")
    api_key (string)
        The API Key obtained from https://financialmodelingprep.com/developer/docs/
    period (string)
        Data period, this can be "annual" or "quarter".

    Output
    ----
    data (dataframe)
        Data with variables in rows and the period in columns.
    """
    response = urlopen("https://financialmodelingprep.com/api/v3/enterprise-value/" +
                       ticker + "?period=" + period + "&apikey=" + api_key)
    data = response.read().decode("utf-8")
    data_json = json.loads(data)['enterpriseValues']

    data_formatted = {}
    for data in data_json:
        if period == "quarter":
            date = data['date'][:7]
        else:
            date = data['date'][:4]
        del data['date']
        data_formatted[date] = data

    return pd.DataFrame(data_formatted)


def rating(ticker, api_key):
    """
     Description
     ----
     Gives information about the rating of a company which includes i.a. the company
     rating and recommendation as well as ratings based on a variety of ratios.

     Input
     ----
     ticker (string)
        The company ticker (for example: "MSFT")
     api_key (string)
        The API Key obtained from https://financialmodelingprep.com/developer/docs/

     Output
     ----
     data (dataframe)
        Data with variables in rows and the period in columns..
     """
    response = urlopen("https://financialmodelingprep.com/api/v3/company/rating/" +
                       ticker + "?apikey=" + api_key)
    data = response.read().decode("utf-8")
    data_json = json.loads(data)
    data_formatted = pd.DataFrame(data_json["ratingDetails"]).T

    return data_formatted


def discounted_cash_flow(ticker, api_key, period="annual"):
    """
    Description
    ----
    Gives information about the discounted cash flow (DCF) of a company which includes
    i.a. the (current) stock price and DCF and over time.

    Input
    ----
    ticker (string)
        The company ticker (for example: "UBER")
    api_key (string)
        The API Key obtained from https://financialmodelingprep.com/developer/docs/
    period (string)
        Data period, this can be "annual" or "quarter".

    Output
    ----
    data (dataframe)
        Data with variables in rows and the period in columns.
    """
    response = urlopen("https://financialmodelingprep.com/api/v3/company/discounted-cash-flow/" +
                       ticker + "?period=" + period + "&apikey=" + api_key)
    data = response.read().decode("utf-8")
    data_json_current = json.loads(data)

    try:
        del data_json_current['symbol']
        data_json_current['DCF'] = data_json_current.pop('dcf')
    except KeyError:
        pass

    response = urlopen("https://financialmodelingprep.com/api/v3/company/historical-discounted-cash-flow/" +
                       ticker + "?period=" + period + "&apikey=" + api_key)
    data = response.read().decode("utf-8")
    data_json = json.loads(data)['historicalDCF']

    data_formatted = {}

    if period == "quarter":
        current_year = data_json_current['date'][:7]
    else:
        current_year = data_json_current['date'][:4]
    data_formatted[current_year] = data_json_current

    for data in data_json:
        if period == "quarter":
            date = data['date'][:7]
        else:
            date = data['date'][:4]
        data_formatted[date] = data

    return pd.DataFrame(data_formatted)


def earnings_calendar(api_key):
    """
    Description
    ----
    Gives information about the discounted cash flow (DCF) of a company which includes
    i.a. the (current) stock price and DCF and over time.

    Input
    ----
    ticker (string)
        The company ticker (for example: "UBER")
    period (string)
        Data period, this can be "annual" or "quarter".

    Output
    ----
    data (dataframe)
        Data with variables in rows and the period in columns.
    """
    response = urlopen("https://financialmodelingprep.com/api/v3/earning_calendar/" +
                       "?apikey=" + api_key)
    data = response.read().decode("utf-8")
    data_json_current = json.loads(data)

    return pd.DataFrame(data_json_current).set_index("date")
