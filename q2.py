import datetime
# to import the library datetime which will help in calculating time
# taken from sending the request until we receive the response
import requests  # to import the library requests

while True:  # infinite loop
    url = input("Enter The Link: <enter -1 to exit>\t")  # to print a statment to help the user know what should he do
    if url == "-1":  # end the loop when the user enters -1
        break
    if not url.startswith('http'):  # this will check if the entered link starts with http or not
        # if it did not start with http, it will add <http://> at the beginning of the link to avoid problems
        url = 'http://' + url
        # for example:==>       http://amazon.com/ or amazon.com

    dt_started = datetime.datetime.utcnow()  # started time will be the time we send the request at

    url = requests.head(url)
    # using head method  to request the headers that would be returned if
    # the head request's url was instead requested with the http get method

    dt_ended = datetime.datetime.utcnow()  # ended time will be the time receive the response at
    # We used <print(f""{})> to print statements and variables values at the same line with the same print <statement>
    print(f"The Header File: {url.headers}")
    print(f"Started Time: {dt_started}")
    print(f"Finished Time: {dt_ended}")
    print(f"Time Taken: {(dt_ended - dt_started).total_seconds()}")
