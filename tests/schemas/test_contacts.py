def test_invalid_contacts_schema_number(contacts_schema):
    invalid_data = {"number": "123", "email": "test@example.com"}
    errors = contacts_schema.validate(invalid_data)
    assert "number" in errors


def test_invalid_contacts_schema_email(contacts_schema):
    invalid_data = {"number": "1234567", "email": "example.com"}
    errors = contacts_schema.validate(invalid_data)
    assert "email" in errors


def test_invalid_contacts_schema_address(contacts_schema):
    invalid_data = {"number": "1234567", "email": "test@example.com", "address": "1"}
    errors = contacts_schema.validate(invalid_data)
    assert "address" in errors


def test_invalid_contacts_schema_address_en(contacts_schema):
    invalid_data = {
        "number": "1234567",
        "email": "test@example.com",
        "address": "123 Main St.",
        "address_en": "1",
    }
    errors = contacts_schema.validate(invalid_data)
    assert "address_en" in errors


def test_invalid_contacts_schema_facebook(contacts_schema):
    invalid_data = {
        "number": "1234567",
        "email": "test@example.com",
        "address": "123 Main St.",
        "address_en": "123 Main St.",
        "facebook": "1",
    }
    errors = contacts_schema.validate(invalid_data)
    assert "facebook" in errors


def test_invalid_contacts_schema_instagram(contacts_schema):
    invalid_data = {
        "number": "1234567",
        "email": "test@example.com",
        "address": "123 Main St.",
        "address_en": "123 Main St.",
        "facebook": "facebook",
        "instagram": "1",
    }
    errors = contacts_schema.validate(invalid_data)
    assert "instagram" in errors


def test_invalid_contacts_schema_telegram(contacts_schema):
    invalid_data = {
        "number": "1234567",
        "email": "test@example.com",
        "address": "123 Main St.",
        "address_en": "123 Main St.",
        "facebook": "facebook",
        "instagram": "instagram",
        "telegram": "1",
    }
    errors = contacts_schema.validate(invalid_data)
    assert "telegram" in errors


def test_invalid_contacts_schema_viber(contacts_schema):
    invalid_data = {
        "number": "1234567",
        "email": "test@example.com",
        "address": "123 Main St.",
        "address_en": "123 Main St.",
        "facebook": "facebook",
        "instagram": "instagram",
        "telegram": "telegram",
        "viber": "1",
    }
    errors = contacts_schema.validate(invalid_data)
    assert "viber" in errors


def test_invalid_contacts_schema_photo_format(contacts_schema):
    invalid_data = {
        "number": "1234567",
        "email": "test@example.com",
        "address": "123 Main St.",
        "address_en": "123 Main St.",
        "facebook": "facebook",
        "instagram": "instagram",
        "telegram": "telegram",
        "viber": "viber",
        "photo_path": "test.txt",
    }
    errors = contacts_schema.validate(invalid_data)
    assert "photo_path" in errors


def test_invalid_contacts_schema_google_maps(contacts_schema):
    invalid_data = {
        "number": "1234567",
        "email": "test@example.com",
        "address": "123 Main St.",
        "address_en": "123 Main St.",
        "facebook": "facebook",
        "instagram": "instagram",
        "telegram": "telegram",
        "viber": "viber",
        "photo_path": "test.jpg",
        "google_maps": "not url or HTML",
    }
    errors = contacts_schema.validate(invalid_data)
    assert "google_maps" in errors


def test_valid_contacts_schema(contacts_schema):
    valid_data = {
        "number": "1234567",
        "email": "test@example.com",
        "address": "123 Main St.",
        "address_en": "123 Main St.",
        "facebook": "facebook",
        "instagram": "instagram",
        "telegram": "telegram",
        "viber": "viber",
        "photo_path": "test.jpg",
        "google_maps": "https://www.google.com/maps",
    }
    errors = contacts_schema.validate(valid_data)
    assert not errors
