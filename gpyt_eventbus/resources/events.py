from flask import request
from flask_restful import Resource
from sqlalchemy.orm import Session

from gpyt_eventbus.model.event import Event as EventORM


class Events(Resource):
    def __init__(self, **kwargs):
        self.logger = kwargs["logger"]
        self.session: Session = kwargs["session"]

    @staticmethod
    def handle_invalid_request(error):
        return {"error": f"Invalid request: {error}"}, 400

    def return_events(self, events):
        self.logger.debug(f"Events: {events}")
        return [event.dict() for event in events], 200

    def get_by_aggregate_id(self, aggregate_id):
        events = self.session.query(EventORM).filter_by(aggregate_id=aggregate_id).all()
        if not events:
            return {"message": "Events not found"}, 404
        return self.return_events(events)

    def get_by_aggregate_name(self, aggregate_name):
        events = (
            self.session.query(EventORM).filter_by(aggregate_name=aggregate_name).all()
        )
        if not events:
            return {"message": "Events not found"}, 404
        return self.return_events(events)

    def get(self):
        request_json = request.get_json(force=True)
        self.logger.trace(f"Request json: {request_json}")
        if request_json.get("aggregate_id"):
            return self.get_by_aggregate_id(request_json["aggregate_id"])
        elif request_json.get("aggregate_name"):
            return self.get_by_aggregate_name(request_json["aggregate_name"])
        else:
            return self.handle_invalid_request("Missing aggregate_id or aggregate_name")
