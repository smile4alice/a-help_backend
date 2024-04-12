def test_invalid_hero_schema_active(hero_schema):
    invalid_data = {
        "active": None,
        "media_path": "path.png",
    }
    errors = hero_schema.validate(invalid_data)
    assert "active" in errors


def test_invalid_hero_schema_media_path(hero_schema):
    invalid_data = {
        "active": True,
        "media_path": "path.txt",
    }
    errors = hero_schema.validate(invalid_data)
    assert "description_en" in errors


def test_invalid_hero_schema_slogan(hero_schema):
    invalid_data = {
        "active": True,
        "media_path": "path.png",
        "slogan": "s",
    }
    errors = hero_schema.validate(invalid_data)
    assert "slogan" in errors


def test_invalid_hero_schema_slogan_en(hero_schema):
    invalid_data = {
        "active": True,
        "media_path": "path.png",
        "slogan": "slogan for hero schema",
        "slogan_en": "s",
    }
    errors = hero_schema.validate(invalid_data)
    assert "slogan_en" in errors


def test_invalid_hero_schema_description(hero_schema):
    invalid_data = {
        "active": True,
        "media_path": "path.png",
        "slogan": "slogan for hero schema",
        "slogan_en": "slogan for hero schema",
        "description": "desc",
    }
    errors = hero_schema.validate(invalid_data)
    assert "description" in errors


def test_invalid_hero_schema_description_en(hero_schema):
    invalid_data = {
        "active": True,
        "media_path": "path.png",
        "slogan": "slogan for hero schema",
        "slogan_en": "slogan for hero schema",
        "description": "description for hero schema",
        "description_en": "desc",
    }
    errors = hero_schema.validate(invalid_data)
    assert "description_en" in errors


def test_invalid_hero_schema_call_to_action(hero_schema):
    invalid_data = {
        "active": True,
        "media_path": "path.png",
        "slogan": "slogan for hero schema",
        "slogan_en": "slogan for hero schema",
        "description": "description for hero schema",
        "description_en": "description for hero schema",
        "call_to_action": "call",
    }
    errors = hero_schema.validate(invalid_data)
    assert "call_to_action" in errors


def test_invalid_hero_schema_call_to_action_en(hero_schema):
    invalid_data = {
        "active": True,
        "media_path": "path.png",
        "slogan": "slogan for hero schema",
        "slogan_en": "slogan for hero schema",
        "description": "description for hero schema",
        "description_en": "description for hero schema",
        "call_to_action": "Call for hero schema",
        "call_to_action_en": "call",
    }
    errors = hero_schema.validate(invalid_data)
    assert "call_to_action_en" in errors


def test_valid_hero_schema(hero_schema):
    valid_data = {
        "active": True,
        "media_path": ["path.png", "scam.jpeg"],
        "slogan": "slogan for hero schema",
        "slogan_en": "slogan for hero schema",
        "description": "description for hero schema",
        "description_en": "description for hero schema",
        "call_to_action": "description for hero schema",
        "call_to_action_en": "description for hero schema",
    }
    errors = hero_schema.validate(valid_data)
    assert not errors
