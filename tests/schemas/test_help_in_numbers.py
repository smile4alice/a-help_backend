def test_invalid_help_in_numbers_schema_photo_path(help_in_numbers_schema):
    invalid_data = {
        "photo_path": "document.txt",
        "photo_path_en": "document.jpg",
        "photo_path_adaptive": "document.gif",
        "photo_path_adaptive_en": "document.bmp",
    }
    errors = help_in_numbers_schema.validate(invalid_data)
    assert "photo_path" in errors


def test_invalid_help_in_numbers_schema_photo_path_en(help_in_numbers_schema):
    invalid_data = {
        "photo_path": "document.png",
        "photo_path_en": "document.txt",
        "photo_path_adaptive": "document.gif",
        "photo_path_adaptive_en": "document.bmp",
    }
    errors = help_in_numbers_schema.validate(invalid_data)
    assert "photo_path_en" in errors


def test_invalid_help_in_numbers_schema_photo_path_adaptive(help_in_numbers_schema):
    invalid_data = {
        "photo_path": "document.png",
        "photo_path_en": "document.jpg",
        "photo_path_adaptive": "document.txt",
        "photo_path_adaptive_en": "document.bmp",
    }
    errors = help_in_numbers_schema.validate(invalid_data)
    assert "photo_path_adaptive" in errors


def test_invalid_help_in_numbers_schema_photo_path_adaptive_en(help_in_numbers_schema):
    invalid_data = {
        "photo_path": "document.png",
        "photo_path_en": "document.jpg",
        "photo_path_adaptive": "document.gif",
        "photo_path_adaptive_en": "document",
    }
    errors = help_in_numbers_schema.validate(invalid_data)
    assert "photo_path_adaptive_en" in errors


def test_valid_help_in_numbers_schema(help_in_numbers_schema):
    valid_data = {
        "photo_path": "document.png",
        "photo_path_en": "document.jpg",
        "photo_path_adaptive": "document.gif",
        "photo_path_adaptive_en": "document.bmp",
    }
    errors = help_in_numbers_schema.validate(valid_data)
    assert not errors
