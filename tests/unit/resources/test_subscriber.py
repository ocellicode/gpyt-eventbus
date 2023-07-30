import unittest
from unittest.mock import MagicMock

from flask import Flask
from flask_restful import Api
from loguru import logger
from sqlalchemy.exc import IntegrityError
from sqlalchemy.orm import Session

from gpyt_eventbus.model.subscriber import Subscriber as SubscriberORM
from gpyt_eventbus.resources.subscriber import Subscriber


class SubscriberTestCase(unittest.TestCase):
    def setUp(self):
        self.app = Flask(__name__)
        self.api = Api(self.app)
        self.session = MagicMock(spec=Session)
        self.api.add_resource(
            Subscriber,
            "/subscriber",
            resource_class_kwargs={"logger": logger, "session": self.session},
        )
        self.client = self.app.test_client()

    def test_post_target_valid_request(self):
        subscriber_data = {"url": "http://example.com"}
        response = self.client.post("/subscriber", json=subscriber_data)
        self.assertEqual(response.status_code, 201)

        # Verify that the SubscriberModel object was created correctly
        expected_subscriber_model = SubscriberORM(**subscriber_data)

        # Verify that the SubscriberORM object was created and added to the session correctly
        self.session.add.assert_called_once()
        self.session.commit.assert_called_once()

        # Verify that the response data matches the SubscriberModel
        response_data = response.get_json()
        expected_data = expected_subscriber_model.dict()
        self.assertEqual(response_data, expected_data)

    def test_post_subscriber_invalid_request(self):
        subscriber_data = {"invalid_key": "http://example.com"}
        response = self.client.post("/subscriber", json=subscriber_data)
        self.assertEqual(response.status_code, 400)

        # Verify that the error message is returned
        response_data = response.get_json()
        self.assertEqual(response_data, {"message": "Invalid request"})

        # Verify that the session methods were not called
        self.session.add.assert_not_called()
        self.session.commit.assert_not_called()

    def test_post_target_error(self):
        subscriber_data = {"url": "http://example.com"}
        self.session.commit.side_effect = Exception("Test error")
        response = self.client.post("/subscriber", json=subscriber_data)
        self.assertEqual(response.status_code, 500)

        # Verify that the error message is returned
        response_data = response.get_json()
        self.assertEqual(response_data, {"message": "Error"})

        # Verify that the session methods were called
        self.session.add.assert_called_once()
        self.session.commit.assert_called_once()

    def test_post_target_duplicate(self):
        subscriber_data = {"url": "http://example.com"}
        self.session.add.side_effect = IntegrityError("Test error", None, None)
        response = self.client.post("/subscriber", json=subscriber_data)
        self.assertEqual(response.status_code, 409)

        # Verify that the error message is returned
        response_data = response.get_json()
        self.assertEqual(response_data, {"message": "Subscriber already exists"})

        # Verify that the session methods were called
        self.session.add.assert_called_once()
        self.session.commit.assert_not_called()

    def test_verify_request_valid(self):
        subscriber_data = {"url": "http://example.com"}
        target = Subscriber(logger=logger, session=self.session)
        result = target.verify_request(subscriber_data)
        self.assertIsInstance(result, SubscriberORM)

    def test_verify_request_invalid(self):
        subscriber_data = {"invalid_key": "http://example.com"}
        target = Subscriber(logger=logger, session=self.session)
        result = target.verify_request(subscriber_data)
        self.assertFalse(result)

    def test_post_target(self):
        subscriber_data = {"url": "http://example.com"}
        subscriber_model = SubscriberORM(**subscriber_data)
        target = Subscriber(logger=logger, session=self.session)

        target.persist_subscriber(subscriber_model)

        # Verify that the session add and commit methods were called
        self.session.add.assert_called_once()
        self.session.commit.assert_called_once()

        # Get the persisted SubscriberORM object from the session add call
        added_target_orm = self.session.add.call_args[0][0]

        # Verify that the persisted object's attribute values match the test object
        self.assertEqual(added_target_orm.url, subscriber_model.url)

    def test_subscriber_delete(self):
        the_dict = {"url": "http://example.com"}
        target_orm = SubscriberORM(**the_dict)
        self.session.query.return_value.filter_by.return_value.first.return_value = (
            target_orm
        )

        response = self.client.delete("/subscriber", json=the_dict)

        self.assertEqual(response.status_code, 200)
        self.assertEqual(response.get_json(), the_dict)

    def test_subscriber_delete_not_found(self):
        response_dict = {"message": "Subscriber not found"}

        self.session.query.return_value.filter_by.return_value.first.return_value = None

        response = self.client.delete("/subscriber", json={"url": "broken"})

        self.assertEqual(response.status_code, 404)
        self.assertEqual(response.get_json(), response_dict)

    def test_subscriber_delete_error(self):
        response_dict = {"message": "Error"}

        self.session.query.return_value.filter_by.return_value.first.side_effect = (
            Exception("Test error")
        )

        response = self.client.delete("/subscriber", json={"url": "broken"})

        self.assertEqual(response.status_code, 500)
        self.assertEqual(response.get_json(), response_dict)
