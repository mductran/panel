import requests
from time import sleep

# change the name of file to correct manga page if needed
with open("nettruyen", "r") as file:
    proxies = file.read().split("\n")

sites_to_scrape = []
counter = 0

for site in sites_to_scrape:
    try:
        print(f"Using the proxy: {proxies[counter]}")
        res = requests.get(site, proxies={"http": proxies[counter], "https": proxies[counter]})
    #     continue scraping code....
    except requests.exceptions.RequestException as e:
        print(f"Failed: {proxies[counter]}")
    finally:
        counter += 1
        counter %= len(proxies)
        # if back to first proxy wait for 10 seconds
        if counter == 0:
            sleep(10)
