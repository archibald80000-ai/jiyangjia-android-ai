from __future__ import annotations

import argparse


def main() -> None:
    parser = argparse.ArgumentParser(description="Jiyangjia FastAPI Gateway")
    parser.add_argument("--host", default="0.0.0.0")
    parser.add_argument("--port", type=int, default=8080)
    parser.add_argument("--print-config", action="store_true")
    args = parser.parse_args()

    if args.print_config:
        from gateway.app.config import load_settings

        settings = load_settings()
        print(settings.safe_summary())
        return

    import uvicorn

    uvicorn.run("gateway.app.main:app", host=args.host, port=args.port)


if __name__ == "__main__":
    main()
