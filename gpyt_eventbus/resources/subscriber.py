from flask import request
from flask_restful import Resource
from pydantic.error_wrappers import ValidationError
from sqlalchemy.exc import IntegrityError
from sqlalchemy.orm import Session

from gpyt_eventbus.model.subscriber import Subscriber as SubscriberORM


class Subscriber(Resource):
    def __init__(self, **kwargs):
        self.logger = kwargs["logger"]
        self.session: Session = kwargs["session"]

    def verify_request(self, request_json):
        self.logger.trace(f"Request json: {request_json}")
        try:
            return SubscriberORM(**request_json)
        except (ValidationError, TypeError) as validation_error:
            self.handle_invalid_request(validation_error)

    def persist_subscriber(self, subscriber: SubscriberORM):
        new_subscriber = SubscriberORM(**subscriber.dict())
        self.session.add(new_subscriber)
        self.session.commit()

    @staticmethod
    def handle_not_found():
        return {"message": "Subscriber not found"}, 404

    @staticmethod
    def handle_invalid_request(error):
        return {"message": f"Invalid request: {error}"}, 400

    def handle_error(self, error):
        self.logger.error(f"Error: {type(error)}")
        return {"message": "Error"}, 500

    def post(self):
        request_json = request.get_json(force=True)
        self.logger.trace(f"Request json: {request_json}")
        try:
            subscriber_model = self.verify_request(request_json)
            if not subscriber_model:
                return {"message": "Invalid request"}, 400
            self.persist_subscriber(subscriber_model)
            return subscriber_model.dict(), 201
        except IntegrityError as integrity_error:
            self.logger.error(f"Error: {integrity_error}")
            self.session.rollback()
            return {"message": "Subscriber already exists"}, 409
        except Exception as exception:  # pylint: disable=broad-except
            return self.handle_error(exception)

    def delete(self):
        request_json = request.get_json(force=True)
        self.logger.trace(f"Request json: {request_json}")
        # use session to retrieve subscriber, if not found return 404

        try:
            subscriber_model = (
                self.session.query(SubscriberORM).filter_by(**request_json).first()
            )
            if not subscriber_model:
                return self.handle_not_found()
            self.session.delete(subscriber_model)
            self.session.commit()
            return subscriber_model.dict(), 200
        except Exception as exception:  # pylint: disable=broad-except
            return self.handle_error(exception)
