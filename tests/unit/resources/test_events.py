import unittest
from unittest.mock import MagicMock

from flask import Flask
from flask_restful import Api
from loguru import logger
from sqlalchemy.orm import Session

from gpyt_eventbus.resources.events import Events


class EventsTestCase(unittest.TestCase):
    def setUp(self):
        self.app = Flask(__name__)
        self.api = Api(self.app)
        self.session = MagicMock(spec=Session)
        self.api.add_resource(
            Events,
            "/events",
            resource_class_kwargs={"logger": logger, "session": self.session},
        )
        self.client = self.app.test_client()

    def test_get_events_by_aggregate_id(self):
        event_mock = MagicMock()
        event_mock.dict.return_value = {"some": "event"}
        self.session.query.return_value.filter_by.return_value.all.return_value = [
            event_mock
        ]
        response = self.client.get(
            "/events", json={"aggregate_id": "some_aggregate_id"}
        )
        assert response.status_code == 200
        assert response.json == [{"some": "event"}]

    def test_get_events_by_aggregate_name(self):
        event_mock = MagicMock()
        event_mock.dict.return_value = {"some": "event"}
        self.session.query.return_value.filter_by.return_value.all.return_value = [
            event_mock
        ]
        response = self.client.get(
            "/events", json={"aggregate_name": "some_aggregate_name"}
        )
        assert response.status_code == 200
        assert response.json == [{"some": "event"}]
