from flask import request, current_app
from flask_restful import Resource, abort
from flask_mail import Message, Mail
from flask_jwt_extended import jwt_required
from marshmallow import ValidationError
from sqlalchemy.exc import SQLAlchemyError

from ahelp.api.schemas import FeedbackSchema
from ahelp.extensions import db


class FeedbackResource(Resource):
    """To send feedback to an email and save the feedback data in the database

    ---
    post:
      tags:
        - api
      summary: Send a feedback
      description: Send a new feedback message
      requestBody:
        content:
          application/json:
            schema:
              type: object
              properties:
                name:
                  type: string
                  description: sender name.
                  example: John Doe
                mail:
                  type: string
                  format: mail
                  description: sender mail.
                  example: ukrsearch@inter.ua
                number:
                  type: string
                  description: sender phone number.(optional)
                  example: +380444952488
                message:
                  type: string
                  description: message from the sender with an alternative method of help
                  example: I have 100500 watermelons. I would like to give you some watermelons.
      responses:
        200:
          content:
            application/json:
              schema:
                type: object
                properties:
                  message:
                    type: string
                    example: Feedback sent successfully!
        400:
            description: Failed to validate feedback or missing required field
        500:
            description: Failed to save feedback to the database or Unexpected error
    """

    method_decorators = [jwt_required()]

    def post(self):
        try:
            json_data = request.get_json()
            name = json_data.get("name", None)
            email = json_data.get("mail", None)
            number = json_data.get("number", None)
            message = json_data.get("message", None)
        except KeyError as e:
            abort(400, error=f"Missing required field: {e.args[0]}")

        try:
            msg = Message(
                subject=f"New feedback from {email} ({name})",
                sender=email,
                recipients=current_app.config.get("MAIL_RECIPIENTS"),
                body=f"{message}\n\nMy phone number - {number}",
                reply_to=email,
            )
            Mail().send(msg)
        except Exception as e:
            abort(500, message=f"Failed to send email: {e}")
        try:
            schema = FeedbackSchema()
            feedback = schema.load(request.json)
            schema.dump(feedback)
            db.session.add(feedback)
            db.session.commit()
        except ValidationError as e:
            abort(400, error=f"Failed to validate feedback: {e}")
        except SQLAlchemyError as e:
            abort(500, error=f"Failed to save feedback to the database: {e}")
        except Exception as e:
            abort(500, error=f"Unexpected error: {e}")
        return {"message": "Feedback sent successfully!"}, 200
