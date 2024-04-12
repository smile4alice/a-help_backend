def test_invalid_our_team_schema_founder(our_team_schema):
    invalid_data = {
        "founder": None,
        "photo_path": "payment.png",
    }
    errors = our_team_schema.validate(invalid_data)
    assert "founder" in errors


def test_invalid_our_team_schema_photo_format(our_team_schema):
    invalid_data = {
        "founder": False,
        "photo_path": "test@example.com",
    }
    errors = our_team_schema.validate(invalid_data)
    assert "photo_path" in errors


def test_invalid_our_team_schema_name(our_team_schema):
    invalid_data = {
        "founder": False,
        "photo_path": "something.png",
        "name": "1",
    }
    errors = our_team_schema.validate(invalid_data)
    assert "name" in errors


def test_invalid_our_team_schema_name_en(our_team_schema):
    invalid_data = {
        "founder": False,
        "photo_path": "something.png",
        "name": "Bob",
        "name_en": "1",
    }
    errors = our_team_schema.validate(invalid_data)
    assert "name_en" in errors


def test_invalid_our_team_schema_description(our_team_schema):
    invalid_data = {
        "founder": False,
        "photo_path": "something.png",
        "name": "John Doe",
        "name_en": "John Doe",
        "description": "a litle description",
    }
    errors = our_team_schema.validate(invalid_data)
    assert "description" in errors


def test_invalid_our_team_schema_description_en(our_team_schema):
    invalid_data = {
        "founder": True,
        "photo_path": "something.png",
        "name": "John Doe",
        "name_en": "John Doe",
        "description": "Description for our team schema",
        "description_en": "a litle description",
    }
    errors = our_team_schema.validate(invalid_data)
    assert "description_en" in errors


def test_valid_our_team_schema(our_team_schema):
    valid_data = {
        "founder": True,
        "photo_path": "something.png",
        "name": "John Doe",
        "name_en": "John Doe",
        "description": "Description for our team schema",
        "description_en": "Description for our team schema",
    }
    errors = our_team_schema.validate(valid_data)
    assert not errors
