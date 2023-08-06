import unittest
from unittest.mock import MagicMock

from flask import Flask
from flask_restful import Api
from loguru import logger
from sqlalchemy.orm import Session

from gpyt_eventbus.resources.event import Event


class EventTestCase(unittest.TestCase):
    def setUp(self):
        self.app = Flask(__name__)
        self.api = Api(self.app)
        self.session = MagicMock(spec=Session)
        self.api.add_resource(
            Event,
            "/event",
            resource_class_kwargs={"logger": logger, "session": self.session},
        )
        self.client = self.app.test_client()

    def test_verify_request_raises_error(self):
        event_data = {
            "aggregate_id": "some_id",
            "data": {
                "some_key": "some_value",
                "some_other_key": 1,
                "some_other_other_key": True,
                "some_other_other_other_key": ["some", "list"],
                "some_other_other_other_other_key": {"some": "dict"},
            },
            "meta_data": {},
            "revision": 0,
            "some_other_key": "some_value",
        }
        event = Event(logger=logger, session=self.session)
        result = event.verify_request(event_data)
        response, code = result.error
        assert code == 400
        assert response == {"error": "Invalid request: Unexpected key 'some_other_key'"}

    def test_post_event_valid_request(self):
        self.session.query.return_value.filter_by.return_value.first.return_value = None
        event_data = {
            "aggregate_id": "some_id",
            "data": {
                "some_key": "some_value",
                "some_other_key": 1,
                "some_other_other_key": True,
                "some_other_other_other_key": ["some", "list"],
                "some_other_other_other_other_key": {"some": "dict"},
            },
            "meta_data": {},
            "timestamp": "2023-08-02 20:01:45.819383",
            "aggregate_name": "example",
            "revision": 0,
        }
        response = self.client.post("/event", json=event_data)
        self.assertEqual(response.status_code, 201)

        # Verify that the EventORM object was created and added to the session correctly
        self.session.add.assert_called_once()
        self.session.commit.assert_called_once()

        # Verify that the response data matches the expected response
        response_data = response.get_json()
        expected_response = {"message": "Event created successfully"}
        self.assertEqual(response_data, expected_response)

    def test_post_event_invalid_request(self):
        event_data = {
            "data": {},
            "timestamp": "2023-08-02 20:01:45.819383",
            "aggregate_name": "example",
            "revision": 0,
        }
        response = self.client.post("/event", json=event_data)
        self.assertEqual(response.status_code, 400)

        # Verify that the error message is returned
        response_data = response.get_json()
        self.assertEqual(
            response_data,
            {
                "error": "Invalid request: Missing one or more of ['aggregate_id', 'aggregate_name', 'revision', 'data', 'meta_data']"
            },
        )

        # Verify that the session methods were not called
        self.session.add.assert_not_called()
        self.session.commit.assert_not_called()

    def test_post_event_duplicate_event(self):
        self.session.query.return_value.filter_by.return_value.first.return_value = True
        event_data = {
            "aggregate_id": "some_id",
            "data": {
                "some_key": "some_value",
                "some_other_key": 1,
                "some_other_other_key": True,
                "some_other_other_other_key": ["some", "list"],
                "some_other_other_other_other_key": {"some": "dict"},
            },
            "meta_data": {},
            "timestamp": "2023-08-02 20:01:45.819383",
            "aggregate_name": "example",
            "revision": 0,
        }
        response = self.client.post("/event", json=event_data)
        self.assertEqual(response.status_code, 409)

        # Verify that the error message is returned
        response_data = response.get_json()
        self.assertEqual(
            response_data,
            {
                "error": "Conflict. Event with same aggregate_id and revision already exists"
            },
        )

        # Verify that the session methods were not called
        self.session.add.assert_not_called()
        self.session.commit.assert_not_called()
