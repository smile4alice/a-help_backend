def test_invalid_docs_and_reports_schema_statutes(docs_and_reports_schema):
    invalid_data = {
        "statutes": "document.com",
        "ownership_structure": "document.txt",
    }
    errors = docs_and_reports_schema.validate(invalid_data)
    assert "statutes" in errors


def test_invalid_docs_and_reports_schema_statutes_ownership_structure(docs_and_reports_schema):
    invalid_data = {
        "statutes": "document.pdf",
        "ownership_structure": "document.com",
    }
    errors = docs_and_reports_schema.validate(invalid_data)
    assert "ownership_structure" in errors


def test_invalid_docs_and_reports_schema_statutes_photo_path(docs_and_reports_schema):
    invalid_data = {
        "statutes": "document.pdf",
        "ownership_structure": "document.txt",
        "photo_path": "document",
    }
    errors = docs_and_reports_schema.validate(invalid_data)
    assert "photo_path" in errors


def test_invalid_docs_and_reports_schema_statutes_bank_account_holder_certificate(docs_and_reports_schema):
    invalid_data = {
        "statutes": "document.pdf",
        "ownership_structure": "document.txt",
        "photo_path": "document.png",
        "bank_account_holder_certificate": "document.com",
    }
    errors = docs_and_reports_schema.validate(invalid_data)
    assert "bank_account_holder_certificate" in errors


def test_invalid_docs_and_reports_schema_statutes_certificate_of_nonprofit_organization(docs_and_reports_schema):
    invalid_data = {
        "statutes": "document.pdf",
        "ownership_structure": "document.txt",
        "photo_path": "document.png",
        "bank_account_holder_certificate": "document.jpeg",
        "certificate_of_nonprofit_organization": "document",
    }
    errors = docs_and_reports_schema.validate(invalid_data)
    assert "certificate_of_nonprofit_organization" in errors


def test_invalid_docs_and_reports_schema_statutes_extract_from_unified_state_register(docs_and_reports_schema):
    invalid_data = {
        "statutes": "document.pdf",
        "ownership_structure": "document.txt",
        "photo_path": "document.png",
        "bank_account_holder_certificate": "document.jpeg",
        "certificate_of_nonprofit_organization": "document.bmp",
        "extract_from_unified_state_register": "document.com",
    }
    errors = docs_and_reports_schema.validate(invalid_data)
    assert "extract_from_unified_state_register" in errors


def test_invalid_docs_and_reports_schema_statutes_annual_report(docs_and_reports_schema):
    invalid_data = {
        "statutes": "document.pdf",
        "ownership_structure": "document.txt",
        "photo_path": "document.png",
        "bank_account_holder_certificate": "document.jpeg",
        "certificate_of_nonprofit_organization": "document.bmp",
        "extract_from_unified_state_register": "document.csv",
        "annual_report": "document.com",
    }
    errors = docs_and_reports_schema.validate(invalid_data)
    assert "annual_report" in errors


def test_invalid_docs_and_reports_schema_statutes_privacy_policy(docs_and_reports_schema):
    invalid_data = {
        "statutes": "document.pdf",
        "ownership_structure": "document.txt",
        "photo_path": "document.png",
        "bank_account_holder_certificate": "document.jpeg",
        "certificate_of_nonprofit_organization": "document.bmp",
        "extract_from_unified_state_register": "document.csv",
        "annual_report": "document.tiff",
        "privacy_policy": "document",
    }
    errors = docs_and_reports_schema.validate(invalid_data)
    assert "privacy_policy" in errors


def test_invalid_docs_and_reports_schema_statutes_privacy_policy_en(docs_and_reports_schema):
    invalid_data = {
        "statutes": "document.pdf",
        "ownership_structure": "document.txt",
        "photo_path": "document.png",
        "bank_account_holder_certificate": "document.jpeg",
        "certificate_of_nonprofit_organization": "document.bmp",
        "extract_from_unified_state_register": "document.csv",
        "annual_report": "document.tiff",
        "privacy_policy": "document.pdf",
        "privacy_policy_en": "document",
    }
    errors = docs_and_reports_schema.validate(invalid_data)
    assert "privacy_policy_en" in errors


def test_valid_docs_and_reports_schema(docs_and_reports_schema):
    valid_data = {
        "statutes": "document.pdf",
        "ownership_structure": "document.txt",
        "photo_path": "document.png",
        "bank_account_holder_certificate": "document.jpeg",
        "certificate_of_nonprofit_organization": "document.bmp",
        "extract_from_unified_state_register": "document.csv",
        "annual_report": "document.tiff",
        "privacy_policy": "document.txt",
        "privacy_policy_en": "document.pdf",
    }
    errors = docs_and_reports_schema.validate(valid_data)
    assert not errors
