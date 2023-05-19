# # Create an API that connects to a database and implements the following Endpoints (very similar to SWAPI.dev or SWAPI.tech):

# [GET] /people Get a list of all the people in the database
# [GET] /people/<int:people_id> Get a one single people information
# [GET] /planets Get a list of all the planets in the database
# [GET] /planets/<int:planet_id> Get one single planet information
# Additionally create the following endpoints to allow your StartWars blog to have users and favorites:

# [GET] /users Get a list of all the blog post users
# [GET] /users/favorites Get all the favorites that belong to the current user.
# [POST] /favorite/planet/<int:planet_id> Add a new favorite planet to the current user with the planet id = planet_id.
# [POST] /favorite/people/<int:people_id> Add new favorite people to the current user with the people id = people_id.
# [DELETE] /favorite/planet/<int:planet_id> Delete favorite planet with the id = planet_id.
# [DELETE] /favorite/people/<int:people_id> Delete favorite people with the id = people_id.
# Your current API does not have an authentication system (yet), which is why the only way to create users is directly on the database using the flask admin.