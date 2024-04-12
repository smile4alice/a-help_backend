def test_invalid_goals_foundation_schema_photo_path(goals_foundation):
    invalid_data = {
        "photo_path": "photo.txt",
        "title": "Title for goals foundation",
    }
    errors = goals_foundation.validate(invalid_data)
    assert "photo_path" in errors


def test_invalid_goals_foundation_schema_title(goals_foundation):
    invalid_data = {
        "photo_path": "photo.png",
        "title": "T",
    }
    errors = goals_foundation.validate(invalid_data)
    assert "title" in errors


def test_invalid_goals_foundation_schema_title_en(goals_foundation):
    invalid_data = {
        "photo_path": "photo.png",
        "title": "Title for goals foundation",
        "title_en": "T",
    }
    errors = goals_foundation.validate(invalid_data)
    assert "title_en" in errors


def test_invalid_goals_foundation_schema_description(goals_foundation):
    invalid_data = {
        "photo_path": "photo.png",
        "title": "Title for goals foundation",
        "title_en": "Title for goals foundation",
        "description": "Desc",
    }
    errors = goals_foundation.validate(invalid_data)
    assert "description" in errors


def test_invalid_goals_foundation_schema_description_en(goals_foundation):
    invalid_data = {
        "photo_path": "photo.png",
        "title": "Title for goals foundation",
        "title_en": "Title for goals foundation",
        "description": "Description for goals foundation",
        "description_en": "Desc",
    }
    errors = goals_foundation.validate(invalid_data)
    assert "description_en" in errors


def test_valid_goals_foundation_schema(goals_foundation):
    valid_data = {
        "photo_path": "photo.png",
        "title": "Title for goals foundation",
        "title_en": "title for goals foundation",
        "description": "description for goals foundation",
        "description_en": "description for goals foundation",
    }
    errors = goals_foundation.validate(valid_data)
    assert not errors
