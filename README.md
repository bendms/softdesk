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

You can find full documentation via Postman link : 

This app follows OWASP security recommandations.

## Installation

This script needs Python installed and some packages detailled in requirements.txt.

1. Clone the repo with your terminal

```
  git clone https://github.com/bendms/softdesk.git
```

## Configuration 

1. Go to litreview directory

```
  cd softdesk
```

2. Start virtual environment from the terminal : 
```
    source/env/bin/activate
```

3. Install packages from requirements.txt

```
  pip install -r requirements.txt
```

4. Go to softdesk directory 

```
  cd softdesk
```

5. Launch local server on your machine

```
  python manage.py runserver
```

6. Your URL will be https://127.0.0.1:8000/ 

7. Create your personnal account to access (see documentation)

## How to contribute 

This project is a MVP and specifications requests simple and minimal UI. Feel free to imagine a design and add CSS for it. It will be great to have some animations with JavaScript too. 