from flask_restful import Resource
from flask import request, current_app
from flask_jwt_extended import jwt_required

from ahelp.models import CounterModel


class CounterResource(Resource):
    """Counter Resource

    ---
    get:
        tags:
            - api
        summary: Get the current counter value
        description: Returns the current counter value for the user locale based on the Accept-Language header.
        parameters:
            - in: path
              name: language
              schema:
                type: string
              description: The preferred language of the user
              default: empty
              example: en
            - in: header
              name: Accept-Language
              type: string
              example: en-US
              required: false
        responses:
            200:
                description: OK
                content:
                    application/json:
                        schema:
                            type: object
                            properties:
                                counter:
                                    type: integer
                                    example: 1000
                                currency_symbol: 
                                    type: string
                                    example: USD
            404:
                description: No counter data was found
    """

    method_decorators = [jwt_required()]

    def get(self, language=None):
        """Returns the user locale based on the Accept-Language header."""
        user_locales = request.accept_languages
        default_locale = current_app.config["BABEL_DEFAULT_LOCALE"]
        if not user_locales:
            user_locales = "en_US" if language == "en" else default_locale
        else:
            user_locales = user_locales.best_match(["en_US", "en_EU", "uk_UA"]) or user_locales
        counter_data = CounterModel.query.filter(CounterModel.locale == user_locales).first_or_404(description="No counter data was found")
        return {
            "counter": counter_data.amount if counter_data else 0,
            "currency_symbol": counter_data.currency_symbol if counter_data else None,
        }
