import backoff
import requests
from flask import request
from flask_restful import Resource
from pydantic.error_wrappers import ValidationError
from sqlalchemy.orm import Session

from gpyt_eventbus.interface.result import Result
from gpyt_eventbus.model.event import Event as EventORM
from gpyt_eventbus.model.subscriber import Subscriber as SubscriberORM


class Event(Resource):
    def __init__(self, **kwargs):
        self.logger = kwargs["logger"]
        self.session: Session = kwargs["session"]

    def verify_request(self, request_json):
        self.logger.trace(f"Request json: {request_json}")
        expected_keys = [
            "aggregate_id",
            "aggregate_name",
            "revision",
            "data",
            "meta_data",
            "event_type",
        ]
        for key in request_json.keys():
            if key not in expected_keys + ["timestamp"]:
                return Result.fail(
                    self.handle_invalid_request(f"Unexpected key '{key}'")
                )
        if not all(key in request_json.keys() for key in expected_keys):
            return Result.fail(
                self.handle_invalid_request(f"Missing one or more of {expected_keys}")
            )
        try:
            return Result.ok(EventORM.from_dict(request_json))
        except (ValidationError, TypeError) as validation_error:
            return Result.fail(self.handle_invalid_request(validation_error))
        except KeyError as key_error:
            return Result.fail(self.handle_invalid_request(f"{key_error} is missing"))

    def persist_event(self, event: EventORM):
        self.session.add(event)
        self.session.commit()

    @staticmethod
    def handle_invalid_request(error):
        return {"error": f"Invalid request: {error}"}, 400

    def post(self):
        try:
            request_json = request.get_json(force=True)
            self.logger.trace(f"Request json: {request_json}")

            event_result = self.verify_request(request_json)
            if event_result.failure:
                return event_result.error
            else:
                event = event_result.value
            existing_event = (
                self.session.query(EventORM)
                .filter_by(aggregate_id=event.aggregate_id, revision=event.revision)
                .first()
            )
            if existing_event:
                return {
                    "error": "Conflict. Event with same aggregate_id and revision already exists"
                }, 409

            if event.revision > 0:
                last_event = (
                    self.session.query(EventORM)
                    .filter_by(aggregate_id=event.aggregate_id)
                    .order_by(EventORM.revision.desc())
                    .first()
                )
                if not last_event or last_event.revision != event.revision - 1:
                    return {"error": "Conflict. Invalid revision number"}, 409

            self.persist_event(event)
            self.publish_event(event)
            return {"message": "Event created successfully"}, 201

        except Exception as unknown_type:  # pylint: disable=broad-except
            self.logger.error(f"Error: {unknown_type}")
            return {"error": "An error occurred"}, 500

    @backoff.on_exception(
        backoff.expo, requests.exceptions.RequestException, max_time=60
    )
    def publish_event(self, event: EventORM):
        subscribers = self.session.query(SubscriberORM).all()
        for subscriber in subscribers:
            requests.post(subscriber.url, json=event.dict(), timeout=5)
            self.logger.info(f"Event published to {subscriber.url}")
