import os
import unittest
import json

from app import APP
from models import setup_db, Movie, Actor

CASTING_ASSISTANT = os.environ["ASSISTANT"]
CASTING_DIRECTOR = os.environ["DIRECTOR"]
EXECUTIVE_PRODUCER = os.environ["PRODUCER"]


class CastingAgencyTest(unittest.TestCase):
    def setUp(self):
        self.app = APP
        self.client = self.app.test_client
        self.test_movie = {
            "title": "Mr and Mrs Smith",
            "release_date": "8-4-2021",
        }
        self.test_actor = {
            "name": "Jhon Smith",
            "age": 55,
            "gender": "male"
        }
        self.database_path = os.environ["DATABASE_URL"]

        setup_db(self.app, self.database_path)


# I will use this func later to test the endpoints 


    def post_actor(self, token):
        response = self.client().post(
            "/actors",
            json=self.test_actor,
            headers={"Authorization": f"Bearer {token}"},
        )
        return response

    def post_movie(self, token):
        response = self.client().post(
            "/movies",
            json=self.test_movie,
            headers={"Authorization": f"Bearer {token}"},
        )
        return response

    def patch_actor(self, actor_id, token):
        response = self.client().patch(
            f"/actors/{actor_id}",
            json={
                "name": "Jhone",
                "age": "30",
                "gender": "male"
            },
            headers={"Authorization": f"Bearer {token}"},
        )
        return response

    def patch_movie(self, movie_id, token):
        response = self.client().patch(
            f"/movies/{movie_id}",
            json={
                "title": "Wanted",
                "release_date": "2020-12-15"
            },
            headers={"Authorization": f"Bearer {token}"},
        )
        return response

    def delete_actor(self, actor_id, token):
        response = self.client().delete(
            f"/actors/{actor_id}", headers={"Authorization": f"Bearer {token}"}
        )
        return response

    def delete_movie(self, movie_id, token):
        response = self.client().delete(
            f"/movies/{movie_id}", headers={"Authorization": f"Bearer {token}"}
        )
        return response







# test the endpoints

################################# movies ##############################


    # test Movies endpoint 
    def test_get_all_movies(self): # test get all the movies
        response = self.client().get(
            "/movies",
            headers={"Authorization": f"Bearer {EXECUTIVE_PRODUCER}"}
        )
        data = json.loads(response.data)
        self.assertEqual(data["success"], True)
        self.assertEqual(response.status_code, 200)

    def test_get_movie_by_id(self): # test get the movie by id 
        response = self.client().get(
            "/movies/158", # make sure you have a movie with id = 1 or you can change it 
            headers={
                "Authorization": f"Bearer {EXECUTIVE_PRODUCER}"
            }
        )
        data = json.loads(response.data)
        self.assertEqual(response.status_code, 200)
        self.assertEqual(data['success'], True)
        self.assertTrue(data['movie'])


    def test_404_get_movie_by_id(self): # the movie not found 
        response = self.client().get(
            f"/movies/{2345}",
            headers={"Authorization": f"Bearer {EXECUTIVE_PRODUCER}"}
        )
        data = json.loads(response.data)

        self.assertEqual(response.status_code, 404)
        self.assertEqual(data["success"], False)

    def test_post_movie(self): # post the movie 
        response = self.post_movie(EXECUTIVE_PRODUCER)
        data = json.loads(response.data)
        movie = data["created_movie"]
        self.assertEqual(data["success"], True)
        self.assertEqual(response.status_code, 201)
        self.assertEqual(movie, movie)

        self.delete_movie(movie["id"], EXECUTIVE_PRODUCER)

    def test_401_post_movie(self): # unauthorized
        response = self.post_movie(CASTING_ASSISTANT)
        data = json.loads(response.data)
        self.assertEqual(data["success"], False)
        self.assertEqual(response.status_code, 401)

    def test_patch_movie(self): # patch the movie 
        post_movie = self.post_movie(EXECUTIVE_PRODUCER)
        movie = json.loads(post_movie.data)["created_movie"]

        response = self.patch_movie(movie["id"], EXECUTIVE_PRODUCER)
        data = json.loads(response.data)

        self.assertEqual(data["success"], True)
        self.assertNotEqual(movie, data["patched_movie"])

        self.delete_movie(movie["id"], EXECUTIVE_PRODUCER)

    def test_404_patch_movie(self): # the movie not found to patch it 
        response = self.patch_movie(1234, EXECUTIVE_PRODUCER)
        data = json.loads(response.data)

        self.assertEqual(response.status_code, 404)
        self.assertEqual(data["success"], False)

    def test_delete_movie(self): # delete the movie 
        post_movie = self.post_movie(EXECUTIVE_PRODUCER)
        movie = json.loads(post_movie.data)["created_movie"]

        response = self.delete_movie(movie["id"], EXECUTIVE_PRODUCER)
        data = json.loads(response.data)

        self.assertEqual(response.status_code, 200)
        self.assertEqual(data["success"], True)

    def test_404_delete_movie(self): # the movie not dound to delete it 
        response = self.delete_movie(5134, EXECUTIVE_PRODUCER)
        data = json.loads(response.data)
        self.assertEqual(data["success"], False)




############################# ACTORS ###################################

    def test_get_all_actors(self):
        response = self.client().get(  # get all the actors detail 
            "/actors",
            headers={
                "Authorization": f"Bearer {EXECUTIVE_PRODUCER}"  # I will use the produecer token and permission to do that 
                }
        )
        data = json.loads(response.data)
        self.assertEqual(data["success"], True)
        self.assertEqual(response.status_code, 200) # it must return 200 and True 

    def test_get_actor_by_id(self): # get the actors by Id 
        post_actor = self.post_actor(EXECUTIVE_PRODUCER) # I will use the post_actor func (I setup it above)
        actor = json.loads(post_actor.data)["created_actor"]
        actor_id = actor["id"] # I will create an actor first and I get the id of that actor

        response = self.client().get(
            f"/actors/{actor_id}", # I used that Id to get it 
            headers={"Authorization": f"Bearer {EXECUTIVE_PRODUCER}"}, # I used the producer permission 
        )
        data = json.loads(response.data)

        self.assertEqual(data["success"], True)
        self.assertEqual(data["actor"], actor)

        self.delete_actor(actor_id, EXECUTIVE_PRODUCER) # delete the actor

    def test_404_get_actor_by_id(self): # if the actor does not exist
        response = self.client().get(
            f"/actors/{2345}",
            headers={
                "Authorization": f"Bearer {EXECUTIVE_PRODUCER}"
                }
        )
        data = json.loads(response.data)

        self.assertEqual(response.status_code, 404)
        self.assertEqual(data["success"], False)

    def test_post_actor(self):
        response = self.post_actor(EXECUTIVE_PRODUCER) # test post actor 
        data = json.loads(response.data)
        actor = data["created_actor"] 
        self.assertEqual(data["success"], True)
        self.assertEqual(response.status_code, 201)
        self.assertEqual(actor, actor)

        self.delete_actor(actor["id"], EXECUTIVE_PRODUCER) # delete the actor 

    def test_401_post_actor(self): # 401 unaothorized 
        response = self.post_actor(CASTING_ASSISTANT) # I will use assistant permission to post (it must raise error ) 
        data = json.loads(response.data)
        self.assertEqual(data["success"], False)
        self.assertEqual(response.status_code, 401)

    def test_patch_actor(self): # I will test patch actor 
        post_actor = self.post_actor(EXECUTIVE_PRODUCER) # I used the producer again to post actor to patch it later 
        actor = json.loads(post_actor.data)["created_actor"]

        response = self.patch_actor(actor["id"], EXECUTIVE_PRODUCER)
        data = json.loads(response.data)

        self.assertEqual(data["success"], True)
        self.assertNotEqual(actor, data["patched_actor"])

        self.delete_actor(actor["id"], EXECUTIVE_PRODUCER)

    def test_404_patch_actor(self): # if the actor does not exist 
        response = self.patch_actor(1234, EXECUTIVE_PRODUCER)
        data = json.loads(response.data)

        self.assertEqual(response.status_code, 404)
        self.assertEqual(data["success"], False)

    def test_delete_actor(self): # test delete the actor
        # I will post actor first to delete it later  
        post_actor = self.post_actor(EXECUTIVE_PRODUCER)
        actor = json.loads(post_actor.data)

        response = self.delete_actor(
            actor["created_actor"]["id"],
            EXECUTIVE_PRODUCER
            )
        data = json.loads(response.data)
        self.assertEqual(response.status_code, 200)
        self.assertEqual(data["success"], True)

    def test_404_delete_actor(self): # 404 delete actor (not found)
        response = self.delete_actor(5134, EXECUTIVE_PRODUCER)
        data = json.loads(response.data)
        self.assertEqual(data["success"], False)

if __name__ == "__main__":
    unittest.main()
