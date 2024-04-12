def test_invalid_needs_schema_active(needs_schema):
    invalid_data = {
        "active": None,
        "media_path": ["something.png", "something_else.jpg"],
    }
    errors = needs_schema.validate(invalid_data)
    assert "active" in errors


def test_invalid_needs_schema_media_path(needs_schema):
    invalid_data = {
        "active": True,
        "media_path": ["something.txt", "something_else.com"],
    }
    errors = needs_schema.validate(invalid_data)
    assert "media_path" in errors


def test_invalid_needs_schema_title(needs_schema):
    invalid_data = {
        "active": True,
        "media_path": ["something.png", "something_else.jpg"],
        "title": "T",
    }
    errors = needs_schema.validate(invalid_data)
    assert "title" in errors


def test_invalid_needs_schema_title_en(needs_schema):
    invalid_data = {
        "active": True,
        "media_path": ["something.png", "something_else.jpg"],
        "title": "Title",
        "title_en": "T",
    }
    errors = needs_schema.validate(invalid_data)
    assert "title_en" in errors


def test_invalid_needs_schema_total_amount(needs_schema):
    invalid_data = {
        "active": True,
        "media_path": ["something.png", "something_else.jpg"],
        "title": "Title",
        "title_en": "Title",
        "total_amount": -100500,
    }
    errors = needs_schema.validate(invalid_data)
    assert "total_amount" in errors


def test_invalid_needs_schema_description(needs_schema):
    invalid_data = {
        "active": True,
        "media_path": ["something.png", "something_else.jpg"],
        "title": "Title",
        "title_en": "Title",
        "total_amount": 100500,
        "description": "Descr",
        "description_en": "Description for needs schema",
    }
    errors = needs_schema.validate(invalid_data)
    assert "description" in errors


def test_invalid_needs_schema_description_en(needs_schema):
    invalid_data = {
        "active": True,
        "media_path": ["something.png", "something_else.jpg"],
        "title": "Title",
        "title_en": "Title",
        "total_amount": 100500,
        "description": "Description for needs schema",
        "description_en": "Descr",
    }
    errors = needs_schema.validate(invalid_data)
    assert "description_en" in errors


def test_valid_needs_schema(needs_schema):
    valid_data = {
        "active": True,
        "media_path": ["something.png", "something_else.jpg"],
        "title": "Title",
        "title_en": "Title",
        "total_amount": 100500,
        "description": "Description for needs schema",
        "description_en": "Description for needs schema",
    }
    errors = needs_schema.validate(valid_data)
    assert not errors
