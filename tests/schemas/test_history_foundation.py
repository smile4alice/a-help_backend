def test_invalid_history_foundation_schema_title(history_foundation_schema):
    invalid_data = {
        "title": "t",
        "title_en": "title for history foundation schema",
    }
    errors = history_foundation_schema.validate(invalid_data)
    assert "title" in errors


def test_invalid_history_foundation_schema_title_en(history_foundation_schema):
    invalid_data = {
        "title": "title for history foundation schema",
        "title_en": "t",
    }
    errors = history_foundation_schema.validate(invalid_data)
    assert "title_en" in errors


def test_invalid_history_foundation_schema_description(history_foundation_schema):
    invalid_data = {
        "title": "title for history foundation schema",
        "title_en": "title for history foundation schema",
        "description": "desc",
    }
    errors = history_foundation_schema.validate(invalid_data)
    assert "description" in errors


def test_invalid_history_foundation_schema_description_en(history_foundation_schema):
    invalid_data = {
        "title": "title for history foundation schema",
        "title_en": "title for history foundation schema",
        "description": "Description for history foundation schema",
        "description_en": "desc",
    }
    errors = history_foundation_schema.validate(invalid_data)
    assert "description_en" in errors


def test_invalid_history_foundation_schema_media_path(history_foundation_schema):
    invalid_data = {
        "title": "title for history foundation schema",
        "title_en": "title for history foundation schema",
        "description": "Description for history foundation schema",
        "description_en": "Description for history foundation schema",
        "media_path": "title.txt",
    }
    errors = history_foundation_schema.validate(invalid_data)
    assert "media_path" in errors


def test_valid_history_foundation_schema(history_foundation_schema):
    valid_data = {
        "title": "title for history foundation schema",
        "title_en": "title for history foundation schema",
        "description": "Description for history foundation schema",
        "description_en": "Description for history foundation schema",
        "media_path": ["title.png", "path.jpg"],
    }
    errors = history_foundation_schema.validate(valid_data)
    assert not errors
