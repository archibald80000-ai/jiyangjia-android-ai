from __future__ import annotations

from getpass import getpass
import secrets

from gateway.app.public_access import hash_public_access_password


def main() -> int:
    password = getpass("Public gate password: ")
    confirmation = getpass("Confirm password: ")
    if not password:
        raise SystemExit("Password must not be empty.")
    if password != confirmation:
        raise SystemExit("Passwords do not match.")
    print(f"JIYANGJIA_PUBLIC_GATE_PASSWORD_HASH={hash_public_access_password(password)}")
    print(f"JIYANGJIA_PUBLIC_GATE_SESSION_SECRET={secrets.token_urlsafe(48)}")
    print("JIYANGJIA_PUBLIC_GATE_SESSION_TTL_SECONDS=86400")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
