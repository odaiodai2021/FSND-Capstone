import os
import unittest
import json
from flask_sqlalchemy import SQLAlchemy
from flask import Flask
from app import app
from models import setup_db, Movie, Actor, database_path
from flask import request, _request_ctx_stack, abort


CASTING_ASSISTANT = os.environ["ASSISTANT"]
CASTING_DIRECTOR = os.environ["DIRECTOR"]
EXECUTIVE_PRODUCER = os.environ["PRODUCER"]


class CastingAgencyTestCase(unittest.TestCase):
    """This class represents the casting agency test case"""

    def setUp(self):
        """Define test variables and initialize app."""
        self.app = app
        self.client = self.app.test_client
        self.database_path = os.environ["DATABASE_URL"]
        self.app.config['TESTING'] = True

        self.new_movie = {
            "title": "Wanted",
            "release_date": "2008"
        }
        self.update_movie = {
            "title": "This movie is updated"
        }
        self.new_actor = {
            "name": "James McAvoy",
            "age": "42",
            "gender": "male"
        }
        self.update_actor = {
            "name": "Name-Updated"
        }

    def tearDown(self):
        """Executed after reach test"""
        pass

    def test_get_movies(self):
        res = self.client().get(
            '/movies',
            headers={
                "Authorization": f"Bearer {EXECUTIVE_PRODUCER}"
            }
        )
        data = json.loads(res.data)
        self.assertEqual(res.status_code, 200)
        self.assertTrue(data['success'])

    def test_create_new_movie(self):
        res = self.client().post(
            '/movies',
            headers={
                "Authorization": f"Bearer {EXECUTIVE_PRODUCER}"
            },
            json=self.new_movie
        )
        data = json.loads(res.data)
        self.assertEqual(res.status_code, 200)
        self.assertEqual(data['success'], True)

    def test_delete_movie(self):
        create_movie = {
            'title': 'This is a delete test movie',
            'release_date': '2000'
        }
        res = self.client().post(
            '/movies',
            headers={
                "Authorization": f"Bearer {EXECUTIVE_PRODUCER}"
            },
            json=create_movie
        )
        data = json.loads(res.data)
        movie_id = data['movie']['id']
        res = self.client().delete(
            '/movies/{}'.format(movie_id),
            headers={
                "Authorization": f"Bearer {EXECUTIVE_PRODUCER}"
            }
        )
        data = json.loads(res.data)
        self.assertEqual(res.status_code, 200)
        self.assertEqual(data['success'], True)

    def test_update_movie(self):
        create_movie = {
            'title': 'This an update test movie',
            'release_date': '1990'
                        }
        res = self.client().post(
            '/movies',
            headers={"Authorization": f"Bearer {EXECUTIVE_PRODUCER}"},
            json=create_movie
        )
        data = json.loads(res.data)
        movie_id = data['movie']['id']
        update_movie = self.update_movie
        res = self.client().patch(
            '/movies/{}'.format(movie_id),
            headers={
                "Authorization": f"Bearer {EXECUTIVE_PRODUCER}"
            },
            json=update_movie
        )
        data = json.loads(res.data)
        self.assertEqual(res.status_code, 200)
        self.assertEqual(data['success'], True)

    def test_get_actors(self):
        res = self.client().get(
            '/actors',
            headers={
                "Authorization": f"Bearer {EXECUTIVE_PRODUCER}"
            }
        )
        data = json.loads(res.data)
        self.assertEqual(res.status_code, 200)
        self.assertEqual(data['success'], True)

    def test_create_new_actor(self):
        res = self.client().post(
            '/actors',
            headers={
                "Authorization": f"Bearer {EXECUTIVE_PRODUCER}"
            }, json=self.new_actor
        )
        data = json.loads(res.data)
        self.assertEqual(res.status_code, 200)
        self.assertEqual(data['success'], True)

    def test_delete_actor(self):
        create_actor = {
            'name': 'Tom Cruise',
            'age': '30',
            'gender': 'Male'
        }
        res = self.client().post(
            '/actors',
            headers={
                "Authorization": f"Bearer {EXECUTIVE_PRODUCER}"
            },
            json=create_actor
        )
        data = json.loads(res.data)
        actor_id = data['actor']['id']
        res = self.client().delete(
            '/actors/{}'.format(actor_id),
            headers={
                "Authorization": f"Bearer {EXECUTIVE_PRODUCER}"
            }
        )
        data = json.loads(res.data)
        self.assertEqual(res.status_code, 200)
        self.assertEqual(data['success'], True)

    def test_update_actor(self):
        create_actor = {
            'name': 'Angelina Jolie',
            'age': '45',
            'gender': 'female'
        }
        res = self.client().post(
            '/actors',
            headers={
                "Authorization": f"Bearer {EXECUTIVE_PRODUCER}"
            },
            json=create_actor
        )
        data = json.loads(res.data)
        actor_id = data['actor']['id']
        update_actor = self.update_actor
        res = self.client().patch(
            '/actors/{}'.format(actor_id),
            headers={
                "Authorization": f"Bearer {EXECUTIVE_PRODUCER}"
            },
            json=update_actor
        )
        data = json.loads(res.data)
        self.assertEqual(res.status_code, 200)
        self.assertEqual(data['success'], True)

    def test_get_actors_without_permessions(self):
        res = self.client().get('/actors')
        data = json.loads(res.data)
        self.assertEqual(res.status_code, 401)
        self.assertFalse(data['success'])

if __name__ == "__main__":
    unittest.main()
