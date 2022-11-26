from queue import Queue
import threading
import requests
import pandas as pd
from .email_scrape import get_email
from tqdm import tqdm
from datetime import datetime
import os
from dotenv import load_dotenv, find_dotenv
load_dotenv(find_dotenv())

GITHUB_PAT = os.environ['GITHUB_PAT'] if 'GITHUB_PAT' in os.environ else ""
now = datetime.now()
timestamp = datetime.timestamp(now)

headers = {
    "authorization": f"Bearer {GITHUB_PAT}"
}

URL = "https://api.github.com/search/users?q={}&per_page=20"

queue = Queue()


def create_query(query_params):
    """ Constructs the query from given parameters """

    if not any(query_params.values()):
        print("Insufficient search parameters given")
        print("Please input atleast one parameter")
        return ""

    query = ""
    for key in query_params.keys():
        if query_params[key]:
            if key == "keyword":
                query += query_params[key]
            else:
                query += f"{key}:{query_params[key]}"
            query += "+"

    return query


def get_user_list(query):
    """ API request for searching the users with given parameters """

    response = requests.get(URL.format(query), headers=headers)
    if response.status_code != 200:
        print("{} Bad Request".format(response.status_code))
        print(URL.format(query))
        print(response.json())
        return [], -1

    user_response = response.json()
    user_list = user_response["items"]
    user_count = user_response["total_count"]
    return user_list, user_count


def get_user_info(idx, user_url, user_info):
    """ Populates the user information """

    # Get data of all users
    user_info_params = ["name", "login",
                        "bio", "location", "email", "html_url"]

    data = []
    resp = requests.get(user_url, headers=headers)
    user = resp.json()

    for param in user_info_params:
        if param == "bio" and user["bio"] is not None:
            data.append(user[param].strip())
        elif param == "email" and user["email"] is None:
            email = get_email(user["html_url"])
            data.append(email)
        else:
            data.append(user[param])

    user_info[idx] = data


def convert_to_csv(data):
    """ Writes the user data obtained to a csv file """

    user_df = pd.DataFrame(data, columns=[
        "Name", "Github Handle", "Bio", "Location", "Email", "Github Link"])

    if data:
        filename = f'../results/user_info_{timestamp}.csv'
        os.makedirs(os.path.dirname(filename), exist_ok=True)
        user_df.to_csv(filename, index=False)
        print("Saved the results to resutls/{}".format(filename))


def main(query_params):
    """ The main function """

    query = create_query(query_params)
    user_list, user_count = get_user_list(query)
    print(f"Found {user_count} users")
    user_info = get_user_info(user_list)
    # convert_to_csv(user_info)

    return user_info


def fill_queue_and_list(user_list):
    # Get API url of all users
    user_urls = []
    for idx, user in enumerate(user_list):
        user_urls.append(user["url"])
        queue.put([idx, user["url"]])

    return user_urls


def worker(user_info):
    while not queue.empty():
        user = queue.get()
        get_user_info(user[0], user[1], user_info)


def multi_threading(user_urls):

    user_info = [[]]*len(user_urls)

    thread_list = []

    # Creating 5 threads
    threads = 5
    for t in range(threads):
        thread = threading.Thread(target=worker, args=(user_info,))
        thread_list.append(thread)

    for thread in thread_list:
        thread.start()

    for thread in tqdm(thread_list):
        thread.join()

    print("Query Completed")

    return user_info

