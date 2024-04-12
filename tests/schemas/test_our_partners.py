def test_invalid_our_partners_schema_photo_format(our_partners_schema):
    invalid_data = {
        "photo_path": "test@example.com",
    }
    errors = our_partners_schema.validate(invalid_data)
    assert "photo_path" in errors


def test_invalid_our_partners_schema_name(our_partners_schema):
    invalid_data = {
        "photo_path": "something.png",
        "name": "1",
    }
    errors = our_partners_schema.validate(invalid_data)
    assert "name" in errors


def test_invalid_our_partners_schema_name_en(our_partners_schema):
    invalid_data = {
        "photo_path": "something.png",
        "name": "Bob",
        "name_en": "1",
    }
    errors = our_partners_schema.validate(invalid_data)
    assert "name_en" in errors


def test_invalid_our_partners_schema_description(our_partners_schema):
    invalid_data = {
        "photo_path": "something.png",
        "name": "John Doe",
        "name_en": "John Doe",
        "description": "a litle",
    }
    errors = our_partners_schema.validate(invalid_data)
    assert "description" in errors


def test_invalid_our_partners_schema_description_en(our_partners_schema):
    invalid_data = {
        "photo_path": "something.png",
        "name": "John Doe",
        "name_en": "John Doe",
        "description": "Description for our team schema",
        "description_en": "a litle",
    }
    errors = our_partners_schema.validate(invalid_data)
    assert "description_en" in errors


def test_valid_our_partners_schema(our_partners_schema):
    valid_data = {
        "photo_path": "something.png",
        "name": "John Doe",
        "name_en": "John Doe",
        "description": "Description for our team schema",
        "description_en": "Description for our team schema",
    }
    errors = our_partners_schema.validate(valid_data)
    assert not errors
