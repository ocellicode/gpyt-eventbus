import datetime

import backoff
import requests
from flask import request
from flask_restful import Resource
from pydantic.error_wrappers import ValidationError
from sqlalchemy.orm import Session

from gpyt_eventbus.model.event import Event as EventORM
from gpyt_eventbus.model.subscriber import Subscriber as SubscriberORM


class Event(Resource):
    def __init__(self, **kwargs):
        self.logger = kwargs["logger"]
        self.session: Session = kwargs["session"]

    def verify_request(self, request_json):
        self.logger.trace(f"Request json: {request_json}")
        try:
            return EventORM(**request_json)
        except (ValidationError, TypeError) as validation_error:
            return self.handle_invalid_request(validation_error)

    def persist_event(self, event: EventORM):
        new_event = EventORM(**event.dict())
        self.session.add(new_event)
        self.session.commit()

    @staticmethod
    def handle_invalid_request(error):
        return {"error": f"Invalid request: {error}"}, 400

    def post(self):
        try:
            request_json = request.get_json(force=True)
            if "timestamp" in request_json:
                request_json["timestamp"] = datetime.datetime.strptime(
                    request_json.pop("timestamp"), "%Y-%m-%d %H:%M:%S.%f"
                )
            self.logger.trace(f"Request json: {request_json}")
            aggregate_id = request_json.get("aggregate_id")
            revision = request_json.get("revision")

            if not aggregate_id or revision is None:
                return {"error": "Missing aggregate_id or revision"}, 400

            existing_event = (
                self.session.query(EventORM)
                .filter_by(aggregate_id=aggregate_id, revision=revision)
                .first()
            )
            if existing_event:
                return {
                    "error": "Conflict. Event with same aggregate_id and revision already exists"
                }, 409

            if revision > 0:
                last_event = (
                    self.session.query(EventORM)
                    .filter_by(aggregate_id=aggregate_id)
                    .order_by(EventORM.revision.desc())
                    .first()
                )
                if not last_event or last_event.revision != revision - 1:
                    return {"error": "Conflict. Invalid revision number"}, 409

            event = self.verify_request(request_json)
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
