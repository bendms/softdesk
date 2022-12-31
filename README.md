# SOFTDESK

This is my fifth Python project for Openclassrooms courses.

In this scenario, I have joined a software company named SoftDesk as a back-end developer.

SoftDesk has created a new team for their latest project. This project is an application for reporting and monitoring technical problems (issue tracking system).

- The application will be available on all three platforms (website, android applications, and iOS)
- The app will basically allow users to create various projects, add users to specific projects, create issues within projects and assign labels to those issues based on their priorities, tags, etc.
- All three apps will leverage the API endpoints that will serve the data.

The first step in this project is to create a standard way to process data, which can be done by developing a RESTful API.

I will be using Django Rest Framework to create this API.

On the app you will be able to create your own account and create your projects, issues and comments.

You can find full documentation via Postman link : https://documenter.getpostman.com/view/23127724/2s8Z6yWYPu

This app follows OWASP security recommandations.

## Installation

This script needs Python installed and some packages detailled in requirements.txt.

1. Clone the repo with your terminal

```
  git clone https://github.com/bendms/softdesk.git
```

## Configuration 

1. Start virtual environment from the terminal : 
```
    source/env/bin/activate
```

2. Install packages from requirements.txt

```
  pip install -r requirements.txt
```

3. Go to softdesk directory 

```
  cd softdesk
```

4. Launch local server on your machine

```
  python manage.py runserver
```

5. Your URL will be https://127.0.0.1:8000/ 

6. Create your personnal account to access (see documentation)

## How to contribute 

Feel free to implement monitoring tool, interface and Throttling system.