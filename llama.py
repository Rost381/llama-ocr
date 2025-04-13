#!/usr/bin/env python3
import argparse
import json
from dotenv import load_dotenv
import os
from typing import Optional
from base import ocr


def get_api_key(cli_api_key: Optional[str] = None) -> str:
    """Gets API key in priority order: .env > argument > input"""
    load_dotenv()
    env_key = os.getenv("TOGETHER_API_KEY")
    if env_key:
        return env_key
    if cli_api_key:
        return cli_api_key
    return input("Input Together AI API key: ").strip()


def main():
    parser = argparse.ArgumentParser(
        description="Converting Images to Markdown/JSON with Llama Vision",
        formatter_class=argparse.RawTextHelpFormatter
    )
    parser.add_argument("file_path", help="Image path or URL")
    parser.add_argument("--api-key", help="Together AI API key")
    parser.add_argument(
        "--model",
        choices=["Llama-Vision-Free", "Llama-3.2-11B-Vision", "Llama-3.2-90B-Vision"],
        default="Llama-Vision-Free",
        help="""Model:
- Llama-Vision-Free (Free)
- Llama-3.2-11B-Vision (paid)
- Llama-3.2-90B-Vision (paid, the most accurate)"""
    )
    parser.add_argument(
        "--markdown",
        action="store_true",
        help="Only Markdown (JSON default)"
    )
    parser.add_argument(
        "--pretty",
        action="store_true",
        help="Formatting JSON"
    )

    args = parser.parse_args()

    try:
        result = ocr(
            file_path=args.file_path,
            api_key=get_api_key(args.api_key),
            model=args.model,
            return_markdown=args.markdown
        )

        if args.markdown:
            print(result)
        else:
            print(json.dumps(result, indent=2 if args.pretty else None, ensure_ascii=False))

    except Exception as e:
        print(f"Error: {str(e)}", file=sys.stderr)
        sys.exit(1)

if __name__ == "__main__":
    import sys

    main()