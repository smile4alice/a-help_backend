def test_feedback_schema_validation_failure_name(feedback_schema):
    data = {
        "name": "T",
        "mail": "test@example.com",
    }
    errors = feedback_schema.validate(data)
    assert "name" in errors


def test_feedback_schema_validation_failure_mail(feedback_schema):
    data = {
        "name": "Test User",
        "mail": "notanemail",
    }
    errors = feedback_schema.validate(data)
    assert "mail" in errors


def test_feedback_schema_validation_failure_number(feedback_schema):
    data = {"name": "Test User", "mail": "test@example.com", "number": "1", "message": "Testing number"}
    errors = feedback_schema.validate(data)
    assert "number" in errors


def test_feedback_schema_validation_failure_message(feedback_schema):
    data = {
        "name": "Test User",
        "mail": "test@example.com",
        "message": "T" * 1001,
    }
    errors = feedback_schema.validate(data)
    assert "message" in errors


def test_valid_feedback_schema(feedback_schema):
    data = {"name": "Test User", "number": "+12345678", "mail": "test@example.com", "message": "Testing number"}
    errors = feedback_schema.validate(data)
    assert not errors
