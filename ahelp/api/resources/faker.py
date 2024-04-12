from faker import Faker
from flask_restful import Resource

from ahelp.models import (
    CounterModel,
    ContactsModel,
    PaymentDetailsModel,
    PaymentModel,
    OurPartnersModel,
    HeroModel,
    DocsAndReportsModel,
    OurTeamModel,
    NeedsModel,
    GoalsFoundationModel,
    HistoryFoundationModel,
)
from ahelp.extensions import ma, db

fake = Faker()


class FakerResource(Resource):
    def get(cls):
        fake_contact = [
            {
                "number": "123456789",
                "viber": fake.ssn(),
                "instagram": fake.ssn(),
                "google_maps": """<iframe src="https://www.google.com/maps/embed?pb=!1m18!1m12!1m3!1d2849.159472391896!2d36.28652975146993!3d50.049323879321015!2m3!1f0!2f0!3f0!3m2!1i1024!2i768!4f13.1!3m3!1m2!1s0x4127a6fdc4284ae7%3A0x6b75b628164149b4!2z0JDRgNCx0YPQtw!5e1!3m2!1suk!2sua!4v1676901036201!5m2!1suk!2sua" width="800" height="500" style="border:0;" allowfullscreen="" loading="lazy" referrerpolicy="no-referrer-when-downgrade"></iframe>""",
                "facebook": fake.name(),
                "address": Faker("pl_PL").address(),
                "address_en": fake.address(),
                "photo_path": "ahelp/static/test/img1.jpg",
                "email": fake.email(),
                "telegram": fake.ssn(),
            }
        ]
        fake_bank = (
            [
                {
                    "currency": "USD",
                    "company_name": fake.company(),
                    "iban_code": fake.iban(),
                    "name_of_bank": fake.company(),
                    "bank_address": fake.street_address(),
                    "edrpou_code": fake.aba()[:8],
                    "swift_code": fake.swift(),
                    "company_address": fake.street_address(),
                    "correspondent_bank": fake.company(),
                    "address_of_correspondent_bank": fake.street_address(),
                    "account_of_the_correspondent_bank": fake.bban(),
                    "swift_code_of_the_correspondent_bank": fake.swift(length=11),
                }
            ]
            + [
                {
                    "currency": "EUR",
                    "company_name": fake.company(),
                    "iban_code": fake.iban(),
                    "name_of_bank": fake.company(),
                    "bank_address": fake.street_address(),
                    "edrpou_code": fake.aba()[:8],
                    "swift_code": fake.swift(),
                    "company_address": fake.company(),
                    "correspondent_bank": fake.company(),
                    "address_of_correspondent_bank": fake.street_address(),
                    "account_of_the_correspondent_bank": fake.bban(),
                    "swift_code_of_the_correspondent_bank": fake.swift(length=11),
                }
            ]
            + [
                {
                    "currency": "UAH",
                    "company_name": fake.company(),
                    "iban_code": fake.iban(),
                    "name_of_bank": fake.company(),
                    "bank_address": fake.street_address(),
                    "edrpou_code": fake.aba()[:8],
                    "swift_code": fake.swift(),
                    "company_address": fake.street_address(),
                }
            ]
        )
        fake_needs = [
            {
                "active": False,
                "media_path": "ahelp/static/test/img1.jpg ahelp/static/test/img2.jpg",
                "title": Faker("pl_PL").sentence(nb_words=2),
                "title_en": fake.sentence(nb_words=2),
                "total_amount": 100500,
                "description": Faker("pl_PL").text(),
                "description_en": fake.text(),
            }
            for _ in range(10)
        ] + [
            {
                "active": True,
                "media_path": "ahelp/static/test/img1.jpg ahelp/static/test/img1.jpg",
                "title": Faker("pl_PL").sentence(nb_words=2),
                "title_en": fake.sentence(nb_words=2),
                "total_amount": 100500,
                "description": Faker("pl_PL").catch_phrase(),
                "description_en": fake.catch_phrase(),
            }
            for _ in range(10)
        ]

        fake_team = [
            {
                "founder": False,
                "photo_path": "ahelp/static/test/img1.jpg",
                "name": Faker("uk_UA").name(),
                "name_en": fake.name(),
                "description": fake.catch_phrase(),
                "description_en": fake.catch_phrase(),
            }
            for _ in range(10)
        ] + [
            {
                "founder": True,
                "photo_path": "ahelp/static/test/img1.jpg",
                "name": Faker("uk_UA").name(),
                "name_en": fake.name(),
                "description": fake.catch_phrase(),
                "description_en": fake.catch_phrase(),
            }
        ]
        fake_partners = [
            {
                "photo_path": "ahelp/static/test/img1.jpg",
                "name": Faker("uk_UA").name(),
                "name_en": fake.name(),
                "description": Faker("pl_PL").catch_phrase(),
                "description_en": fake.catch_phrase(),
            }
            for _ in range(10)
        ]
        fake_hero = [
            {
                "media_path": "ahelp/static/test/img1.jpg ahelp/static/test/img2.jpg",
                "active": True,
                "slogan": Faker("pl_PL").catch_phrase(),
                "slogan_en": fake.catch_phrase(),
                "description": Faker("pl_PL").catch_phrase(),
                "description_en": fake.catch_phrase(),
                "call_to_action": Faker("pl_PL").text(),
                "call_to_action_en": fake.text(),
            }
            for _ in range(1)
        ]
        fake_docs = [
            {
                "photo_path": "ahelp/static/test/img1.jpg",
                "statutes": "ahelp/static/test/img2.jpg",
                "ownership_structure": "ahelp/static/test/img3.jpg",
                "bank_account_holder_certificate": "ahelp/static/test/img4.jpg",
                "certificate_of_nonprofit_organization": "ahelp/static/test/img5.jpg",
                "extract_from_unified_state_register": "ahelp/static/test/img6.jpg",
                "annual_report": "ahelp/static/test/img7.jpg",
                "privacy_policy": "ahelp/static/test/img8.jpg",
                "privacy_policy_en": "ahelp/static/test/img9.jpg",
            }
            for _ in range(1)
        ]
        fake_goals = [
            {
                "photo_path": "ahelp/static/test/img9.jpg",
                "title": Faker("pl_PL").catch_phrase(),
                "title_en": fake.catch_phrase(),
                "description": Faker("pl_PL").catch_phrase(),
                "description_en": fake.catch_phrase(),
            }
            for _ in range(3)
        ]
        fake_history = [
            {
                "media_path": "ahelp/static/test/img9.jpg ahelp/static/test/img10.jpg",
                "title": Faker("pl_PL").catch_phrase(),
                "title_en": fake.catch_phrase(),
                "description": Faker("pl_PL").catch_phrase(),
                "description_en": fake.catch_phrase(),
            }
            for _ in range(10)
        ]
        fake_payment = [
            {
                "photo_path": "ahelp/static/test/img9.jpg",
                "header": Faker("pl_PL").catch_phrase(),
                "header_en": fake.catch_phrase(),
                "body": Faker("pl_PL").catch_phrase(),
                "body_en": fake.catch_phrase(),
                "title": Faker("pl_PL").catch_phrase(),
                "title_en": fake.catch_phrase(),
                "description": Faker("pl_PL").catch_phrase(),
                "description_en": fake.catch_phrase(),
            }
            for _ in range(1)
        ]
        fake_counter = (
            [
                {
                    "currency_symbol": "USD",
                    "amount": 2222,
                    "locale": "en_US",
                }
                for _ in range(1)
            ]
            + [
                {
                    "currency_symbol": "EUR",
                    "amount": 3333,
                    "locale": "en_EU",
                }
                for _ in range(1)
            ]
            + [
                {
                    "currency_symbol": "UAH",
                    "amount": 1111,
                    "locale": "uk_UA",
                }
                for _ in range(1)
            ]
        )

        with db.session.begin():
            for row in fake_payment:
                pt = PaymentModel(**row)
                db.session.add(pt)
            for row in fake_counter:
                pt = CounterModel(**row)
                db.session.add(pt)
            for row in fake_history:
                pt = HistoryFoundationModel(**row)
                db.session.add(pt)
            for row in fake_goals:
                pt = GoalsFoundationModel(**row)
                db.session.add(pt)
            for row in fake_docs:
                pt = DocsAndReportsModel(**row)
                db.session.add(pt)
            for row in fake_team:
                tm = OurTeamModel(**row)
                db.session.add(tm)
            for row in fake_partners:
                pt = OurPartnersModel(**row)
                db.session.add(pt)
            for row in fake_hero:
                fh = HeroModel(**row)
                db.session.add(fh)
            for row in fake_contact:
                cont = ContactsModel(**row)
                db.session.add(cont)
            for row in fake_bank:
                usd = PaymentDetailsModel(**row)
                db.session.add(usd)
            for row in fake_needs:
                needs = NeedsModel(**row)
                db.session.add(needs)
