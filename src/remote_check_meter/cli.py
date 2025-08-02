#!/usr/bin/env python3
"""Command line interface for remote meter data collection."""

import argparse
import json
import sys
from datetime import datetime
from getpass import getpass

from .client import RuvieMeterClient
from .config import load_config


def create_parser() -> argparse.ArgumentParser:
    """Create command line argument parser."""
    parser = argparse.ArgumentParser(
        description="Remote meter data parser",
        formatter_class=argparse.RawDescriptionHelpFormatter,
    )

    parser.add_argument(
        "year", type=int, nargs="?", help="Year to query (default: current year)"
    )
    parser.add_argument(
        "month", type=int, nargs="?", help="Month to query (default: current month)"
    )
    parser.add_argument("--username", "-u", help="Username for login")
    parser.add_argument("--password", "-p", help="Password for login")
    parser.add_argument("--output", "-o", help="Output file path")
    parser.add_argument(
        "--multi", "-m", action="store_true", help="Query multiple months"
    )

    return parser


def main() -> None:
    """Main CLI entry point."""
    parser = create_parser()
    args = parser.parse_args()

    # 설정 로드
    config = load_config()

    # 사용자 정보 가져오기
    username = args.username or config.get("username") or input("아이디: ")
    password = args.password or config.get("password") or getpass("비밀번호: ")

    # 년월 결정
    if args.year and args.month:
        year, month = args.year, args.month
    else:
        now = datetime.now()
        year, month = now.year, now.month

    # 클라이언트 생성 및 실행
    client = RuvieMeterClient()

    print("=== Ruvie 원격 검침 데이터 조회 ===")

    if client.login(username, password):
        result = client.fetch_meter_data(year, month)

        if result:
            # 출력
            print("\n=== 검침 데이터 ===")
            print(json.dumps(result, ensure_ascii=False, indent=2))

            # 파일 저장
            filename = args.output or f"meter_data_{year}_{month:02d}.json"
            with open(filename, "w", encoding="utf-8") as f:
                json.dump(result, f, ensure_ascii=False, indent=2)

            print(f"\n데이터가 {filename} 파일로 저장되었습니다.")
        else:
            print("데이터를 가져올 수 없습니다.")
            sys.exit(1)
    else:
        print("로그인에 실패했습니다.")
        sys.exit(1)


if __name__ == "__main__":
    main()
