def test_invalid_payment_details_schema_currency(payment_details_schema):
    invalid_data = {
        "currency": "RUB",
        "company_name": "company name",
    }
    errors = payment_details_schema.validate(invalid_data)
    assert "currency" in errors


def test_invalid_payment_details_schema_company_name(payment_details_schema):
    invalid_data = {
        "currency": "UAH",
        "company_name": "name",
    }
    errors = payment_details_schema.validate(invalid_data)
    assert "company_name" in errors


def test_invalid_payment_details_schema_iban_code(payment_details_schema):
    invalid_data = {
        "currency": "UAH",
        "company_name": "company name",
        "iban_code": "123456789",
    }
    errors = payment_details_schema.validate(invalid_data)
    assert "iban_code" in errors


def test_invalid_payment_details_schema_name_of_bank(payment_details_schema):
    invalid_data = {
        "currency": "UAH",
        "company_name": "company name",
        "iban_code": "12345678901234567890123456789",
        "name_of_bank": "name",
    }
    errors = payment_details_schema.validate(invalid_data)
    assert "name_of_bank" in errors


def test_invalid_payment_details_schema_bank_address(payment_details_schema):
    invalid_data = {
        "currency": "UAH",
        "company_name": "company name",
        "iban_code": "12345678901234567890123456789",
        "name_of_bank": "name of bank",
        "bank_address": "bank",
    }
    errors = payment_details_schema.validate(invalid_data)
    assert "bank_address" in errors


def test_invalid_payment_details_schema_edrpou_code(payment_details_schema):
    invalid_data = {
        "currency": "UAH",
        "company_name": "company name",
        "iban_code": "12345678901234567890123456789",
        "name_of_bank": "name of bank",
        "bank_address": "bank address",
        "edrpou_code": "12345",
    }
    errors = payment_details_schema.validate(invalid_data)
    assert "edrpou_code" in errors


def test_invalid_payment_details_schema_swift_code(payment_details_schema):
    invalid_data = {
        "currency": "UAH",
        "company_name": "company name",
        "iban_code": "12345678901234567890123456789",
        "name_of_bank": "name of bank",
        "bank_address": "bank address",
        "edrpou_code": "12345678",
        "swift_code": "12345",
    }
    errors = payment_details_schema.validate(invalid_data)
    assert "swift_code" in errors


def test_invalid_payment_details_schema_company_address(payment_details_schema):
    invalid_data = {
        "currency": "UAH",
        "company_name": "company name",
        "iban_code": "12345678901234567890123456789",
        "name_of_bank": "name of bank",
        "bank_address": "bank address",
        "edrpou_code": "12345678",
        "swift_code": "123456789",
        "company_address": "com",
    }
    errors = payment_details_schema.validate(invalid_data)
    assert "company_address" in errors


def test_invalid_payment_details_schema_correspondent_bank(payment_details_schema):
    invalid_data = {
        "currency": "UAH",
        "company_name": "company name",
        "iban_code": "12345678901234567890123456789",
        "name_of_bank": "name of bank",
        "bank_address": "bank address",
        "edrpou_code": "12345678",
        "swift_code": "123456789",
        "company_address": "company address",
        "correspondent_bank": "cor",
    }
    errors = payment_details_schema.validate(invalid_data)
    assert "correspondent_bank" in errors


def test_invalid_payment_details_schema_address_of_correspondent_bank(payment_details_schema):
    invalid_data = {
        "currency": "UAH",
        "company_name": "company name",
        "iban_code": "12345678901234567890123456789",
        "name_of_bank": "name of bank",
        "bank_address": "bank address",
        "edrpou_code": "12345678",
        "swift_code": "123456789",
        "company_address": "company address",
        "correspondent_bank": "correspondent bank",
        "address_of_correspondent_bank": "bank",
    }
    errors = payment_details_schema.validate(invalid_data)
    assert "address_of_correspondent_bank" in errors


def test_invalid_payment_details_schema_account_of_the_correspondent_bank(payment_details_schema):
    invalid_data = {
        "currency": "UAH",
        "company_name": "company name",
        "iban_code": "12345678901234567890123456789",
        "name_of_bank": "name of bank",
        "bank_address": "bank address",
        "edrpou_code": "12345678",
        "swift_code": "123456789",
        "company_address": "company address",
        "correspondent_bank": "correspondent bank",
        "address_of_correspondent_bank": "address of correspondent bank",
        "account_of_the_correspondent_bank": "bank",
    }
    errors = payment_details_schema.validate(invalid_data)
    assert "account_of_the_correspondent_bank" in errors


def test_invalid_payment_details_schema_swift_code_of_the_correspondent_bank(payment_details_schema):
    invalid_data = {
        "currency": "UAH",
        "company_name": "company name",
        "iban_code": "12345678901234567890123456789",
        "name_of_bank": "name of bank",
        "bank_address": "bank address",
        "edrpou_code": "12345678",
        "swift_code": "123456789",
        "company_address": "company address",
        "correspondent_bank": "correspondent bank",
        "address_of_correspondent_bank": "address of correspondent bank",
        "account_of_the_correspondent_bank": "account of the correspondent bank",
        "swift_code_of_the_correspondent_bank": "12345",
    }
    errors = payment_details_schema.validate(invalid_data)
    assert "swift_code_of_the_correspondent_bank" in errors


def test_valid_payment_details_schema(payment_details_schema):
    valid_data = {
        "currency": "UAH",
        "company_name": "company name",
        "iban_code": "12345678901234567890123456789",
        "name_of_bank": "name of bank",
        "bank_address": "bank address",
        "edrpou_code": "12345678",
        "swift_code": "123456789",
        "company_address": "company address",
        "correspondent_bank": "correspondent bank",
        "address_of_correspondent_bank": "address of correspondent bank",
        "account_of_the_correspondent_bank": "account of the correspondent bank",
        "swift_code_of_the_correspondent_bank": "123456789",
    }
    errors = payment_details_schema.validate(valid_data)
    assert not errors
