# tools/log_settings.py

import settings


def mask_secret(secret: str | None) -> str:
    if not secret:
        return "None"
    return secret[:5] + "*" * 5


def print_section(title: str, section: object, mask_keys: tuple[str, ...] = ("password", "secret", "key")) -> None:
    print(f"\n[{title}]")
    for attr in dir(section):
        if attr.startswith("_"):
            continue
        value = getattr(section, attr)
        is_masked = any(mask in attr.lower() for mask in mask_keys)
        display_value = mask_secret(str(value)) if is_masked else value
        print(f"{attr.replace('_', ' ').capitalize():25} {display_value}")


def print_settings() -> None:
    print("\n" + "=" * 50)
    print("APPLICATION CONFIGURATION")
    print("=" * 50)

    print_section("General",   settings.General)
    print_section("AI",        settings.AI)
    print_section("Database",  settings.Database)
    print_section("Auth",      settings.Auth)

    print("\n" + "=" * 50 + "\n")