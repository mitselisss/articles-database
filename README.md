# Articles Database
**Junior Back-end Engineer Technical  Assignment Articles database**

A simple article management API built with Django, DRF and PostgreSQL.

## How to run
```sudo docker compose run --build```

After this command the web app is ready at:

[127.0.0.1:8000/api/docs/](127.0.0.1:8000/api/docs/)

[127.0.0.1:8000/admin/](127.0.0.1:8000/admin/)

To use the admin panel a superuser must be made via the command:

```sudo docker compose run --rm sh -c "python manage.py createsuperuser"```

and following the instructions.

The [127.0.0.1:8000/api/docs/](127.0.0.1:8000/api/docs/) page is the swagger where a user can interact with the app.

From this swagger someone must create a user via the POST /api/user/create/ and giving a username (required), an email, and a password (required).
After the succesfull user creation the user must log in to use all the features of the app. To log in use the POST /api/user/token/ and fill in
the credentials. A token will be generated. Copy and paste it at Authorize (upper right corner) as: Token <your_token> and hit authorize.

## How to use
Now that you are authorized you can use the features.

### Features about article:
- List all articles in the database or filter and then list based on author's id, tag, date, or keyword via the **GET /api​/article​/** (You dont have to be authorized for this feature)
- Create an article via the **POST ​/api​/article​/**
- Get an article by its id via the **GET ​/api​/article​/{id}​/**
- Update your article by its id via **PUT ​/api​/article​/{id}​/** (you can not change others articles)
- Partially update your own article by its id via **PATCH /api​/article​/{id}​/** (you can not change others articles)
- Delete your own article by its id via the **DELETE ​/api​/article​/{id}​/** (you can not delete others articles)
- Download articles in a csv format after filtering them via the **GET ​/api​/article​/download​/**

### Features about comments:
- List all comments on the database via the **GET /api​/comment​/** (You dont have to be authorized for this feature)
- Create a comment for an article via the **POST /api​/comment​/**
- Get a comment by its id via the **GET /api​/comment​/{id}​/**
- Update your own comment by its id via the **PUT /api​/comment​/{id}​/** (you can not change others comments)
- Partially update your own coment by its id via the **PATCH /api​/comment​/{id}​/** (you can not change others comments)
- Delete your own comment by its id via the **DELETE /api​/comment​/{id}​/** (you can not delete others comments)


### Features about tags:
Regarding the tags there are two ways to crete them. The first is through the creation of an article where you can also include tag(s) and the second is via the POST /api​/tag​/ where you create a tag and link it to an article's id.
- Get all tags in the database via the **GET /api​/tag​/** (You dont have to be authorized for this feature)
- Create a tag via the **POST /api​/tag​/**
- Get a tag by its id via the **GET /api​/tag​/{id}​/**
- Update your own tag by its id via the **PUT ​/api​/tag​/{id}​/** (you can not change others tags)
- Partially update your own tag by its id via the **PATCH /api​/tag​/{id}​/** (you can not change others tags)
- Delete your own tag by its id via the **DELETE /api​/tag​/{id}​/** (you can not delete others tags)

### Features about the user:
- Create a user via the **POST /api​/user​/create​/**
- Check which user is logged in via the **GET /api​/user​/me​/**
- Update your user via the **PUT /api​/user​/me​/**
- Partially update your user via the **PATCH /api​/user​/me​/**
- Generate a token for your user via the **POST /api​/user​/token​/**