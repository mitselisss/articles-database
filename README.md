# Articles Database
**Junior Back-end Engineer Technical  Assignment Articles database**

A simple article management API built with Django and DRF.

## How to run
```bash sudo docker compose run --build```

After this command the web app is ready at 127.0.0.1:8000/api/docs/ or at 127.0.0.1:8000/admin/ but a superuser must be made via the command:
sudo docker compose run --rm sh -c "python manage.py createsuperuser" and follow the instructions.

The 127.0.0.1:8000/api/docs/ page is the swagger where a user can interact with the app.

From this swagger a user must create a user via the POST /api/user/create/ and giving a username (required), an email, and a password (required).
After the succesfull user creation the user must log in to use all the features of the app. To log in use the POST /api/user/token/ and fill in
the credentials. A token will be generated. Copy and past it at Authorize (upper right corner) as: Token <your_token> and hit authorize.
To check if the correct user is logged in go to GET ​/api​/user​/me​/ and you should see your username and email.

Now that you are authorized you can:
- List all articles in the databse or filter and then list based on author's id, tag, data, or keyword via the GET /api​/article​/ (You dont have to be authorized for this feature)
- Create an article via the POST ​/api​/article​/
- Get a specific article via the article's id via the GET ​/api​/article​/{id}​/
- Update your whole article(s) via their ids via PUT ​/api​/article​/{id}​/ (you can not change others articles)
- Partially update your own article(s) via PATCH /api​/article​/{id}​/ (you can not change others articles)
- Delete your own article(s) via the DELETE ​/api​/article​/{id}​/
- Download articles in a csv format after filtering them via the GET ​/api​/article​/download​/
- List all comments on the database via the GET /api​/comment​/ (You dont have to be authorized for this feature)
- Create a comment for an article via the POST /api​/comment​/
- Get a comment via the GET /api​/comment​/{id}​/
- Update your own comments via the PUT /api​/comment​/{id}​/
- Partially update your own coment via the PATCH /api​/comment​/{id}​/
- Delete your own comment via the DELETE /api​/comment​/{id}​/

Regarding the tags there are two ways to crete them. The first is through the creation of an article where you can also include tag(s) and the second is via the POST /api​/tag​/ where you create a tag and link it to an article's id. Additional features about tags:
- Get all tags in the database via the GET /api​/tag​/ (You dont have to be authorized for this feature)
- Get a tag by its id via the GET /api​/tag​/{id}​/
- Update your own tag by its id via the PUT ​/api​/tag​/{id}​/
- Partially update your own tag by its id via the PATCH /api​/tag​/{id}​/
- Delete your own tag by its id via the DELETE /api​/tag​/{id}​/

Additionally features about the user:
- Create a user via the POST /api​/user​/create​/
- Check which user is logged in via the GET /api​/user​/me​/
- Update your user via the PUT /api​/user​/me​/
- Partially update your user via the PATCH /api​/user​/me​/
- Generate a token for your user via the POST /api​/user​/token​/