
# Github User Search API


#### A REST API made w/ Django which generates a csv formatted response of user information retrieved from given search query parameters as input.


## Tech Stack

- Python 3.10
- Django 4.1.3


## API Reference

#### Search users with given parameters

```https
  GET /user/?keyword={}&location={}&followers={}&repos={}&language={}
```

| Parameter | Type     | Description                       |
| :-------- | :------- | :-------------------------------- |
| `keyword`      | `string` |   Name, Keyword in Bio of the user |
| `location`      | `string` |   Location of the user |
| `followers`      | `string` |  No. of followers of user \| Ex: >10, <30  |
| `repos`      | `string` |   No. of public repositories \| Ex: >4, <60
| `language`      | `string` | Most used programming language by the user |

Atleast one of the following parameters is **Required** for a successful request



#### API Demo using Postman

[![Run in Postman](https://run.pstmn.io/button.svg)](https://app.getpostman.com/run-collection/23153797-d82383c7-eda5-4e3d-81a3-638aa4388e93?action=collection%2Ffork&collection-url=entityId%3D23153797-d82383c7-eda5-4e3d-81a3-638aa4388e93%26entityType%3Dcollection%26workspaceId%3D6a2e7cfa-b21d-4b0c-b9e7-388fd99d4e25)

### Result

Example Query: ```user/?keyword=hackathon&location=india&followers=>2&repos=>5&language=python```

Result for the above query can be seen in the file [user_info.csv](user_info.csv)


## What's The Code ?
-   Processes input parameters (keyword, location etc. of user) to search users, then from the search result retrieves the user
    info(name, email etc.) of all users using the GitHub API.
- Implemented asynchronous programming to make multiple
     http requests concurrently which increases the speed of
    the program significantly
## Run Locally

Clone the project

```bash
  git clone https://github.com/rogdex24/github-user-search-api.git
```

Go to the project directory

```bash
  cd github-user-search-api
```

Create a virtual environment

```bash
  python -m venv .venv
```

Activate the virtual environment

```bash
  . .venv/Scripts/activate
```

Add the environment variables: 
(create the '.env' file and add the variables)

```bash
  GITHUB_PAT=<YourGithubPAT>
```

Install the dependencies:

```bash
  pip install -r requirements.txt
```

Create a superuser

```bash
  python manage.py createsuperuser
```

Migrate the databse

```bash
  python manage.py migrate
```

Run the Server

```bash
  python manage.py runserver
```
