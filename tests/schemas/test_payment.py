def test_invalid_payment_schema_header(payment_schema):
    invalid_data = {
        "header": "H",
        "header_en": "Header for payment schema",
    }
    errors = payment_schema.validate(invalid_data)
    assert "header" in errors


def test_invalid_payment_schema_header_en(payment_schema):
    invalid_data = {
        "header": "Header for payment schema",
        "header_en": "H",
    }
    errors = payment_schema.validate(invalid_data)
    assert "header_en" in errors


def test_invalid_payment_schema_body(payment_schema):
    invalid_data = {
        "header": "Header for payment schema",
        "header_en": "Header for payment schema",
        "body": "Body",
    }
    errors = payment_schema.validate(invalid_data)
    assert "body" in errors


def test_invalid_payment_schema_body_en(payment_schema):
    invalid_data = {
        "header": "Header for payment schema",
        "header_en": "Header for payment schema",
        "body": "Body for payment schema",
        "body_en": "Body",
    }
    errors = payment_schema.validate(invalid_data)
    assert "body_en" in errors


def test_invalid_payment_schema_photo_path(payment_schema):
    invalid_data = {
        "header": "Header for payment schema",
        "header_en": "Header for payment schema",
        "body": "Body for payment schema",
        "body_en": "Body for payment schema",
        "photo_path": "Description.txt",
    }
    errors = payment_schema.validate(invalid_data)
    assert "photo_path" in errors


def test_invalid_payment_schema_title(payment_schema):
    invalid_data = {
        "header": "Header for payment schema",
        "header_en": "Header for payment schema",
        "body": "Body for payment schema",
        "body_en": "Body for payment schema",
        "photo_path": "Description.png",
        "title": "T",
    }
    errors = payment_schema.validate(invalid_data)
    assert "title" in errors


def test_invalid_payment_schema_title_en(payment_schema):
    invalid_data = {
        "header": "Header for payment schema",
        "header_en": "Header for payment schema",
        "body": "Body for payment schema",
        "body_en": "Body for payment schema",
        "photo_path": "Description.png",
        "title": "Title for payment schema",
        "title_en": "T",
    }
    errors = payment_schema.validate(invalid_data)
    assert "title_en" in errors


def test_invalid_payment_schema_description(payment_schema):
    invalid_data = {
        "header": "Header for payment schema",
        "header_en": "Header for payment schema",
        "body": "Body for payment schema",
        "body_en": "Body for payment schema",
        "photo_path": "Description.png",
        "title": "Title for payment schema",
        "title_en": "Title for payment schema",
        "description": "Description",
    }
    errors = payment_schema.validate(invalid_data)
    assert "description" in errors


def test_invalid_payment_schema_description_en(payment_schema):
    invalid_data = {
        "header": "Header for payment schema",
        "header_en": "Header for payment schema",
        "body": "Body for payment schema",
        "body_en": "Body for payment schema",
        "photo_path": "Description.png",
        "title": "Title for payment schema",
        "title_en": "Title for payment schema",
        "description": "Description for payment schema",
        "description_en": "Description",
    }
    errors = payment_schema.validate(invalid_data)
    assert "description_en" in errors


def test_valid_payment_schema(payment_schema):
    valid_data = {
        "header": "Header for payment schema",
        "header_en": "Header for payment schema",
        "body": "Body for payment schema",
        "body_en": "Body for payment schema",
        "photo_path": "Description.png",
        "title": "Title for payment schema",
        "title_en": "Title for payment schema",
        "description": "Description for payment schema",
        "description_en": "Description for payment schema",
    }
    errors = payment_schema.validate(valid_data)
    assert not errors
