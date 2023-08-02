import unittest
from unittest.mock import MagicMock

from flask import Flask
from flask_restful import Api
from loguru import logger
from sqlalchemy.orm import Session

from gpyt_eventbus.model.event import Event as EventORM
from gpyt_eventbus.resources.event import (
    Event,
)  # Replace with the actual path to your Event class


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

    # Add your test methods here, similar to the SubscriberTestCase

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
