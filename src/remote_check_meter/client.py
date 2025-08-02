#!/usr/bin/env python3
"""Ruvie meter client for remote meter data collection."""

import re
import time
from typing import Any, Dict, List, Optional, cast

import requests
import urllib3
from bs4 import BeautifulSoup, Tag

from .config import load_config
from .parser import MeterDataParser

# SSL 경고 무시
urllib3.disable_warnings(urllib3.exceptions.InsecureRequestWarning)


class RuvieMeterClient:
    """Client for accessing Ruvie remote meter data."""

    def __init__(self, config: Optional[Dict[str, Any]] = None) -> None:
        self.session = requests.Session()

        # 설정 로드
        if config is None:
            config = load_config()

        self.base_url = config["base_url"]
        self.meter_base_url = config["meter_base_url"]
        self.timeout = config["timeout"]
        self.retries = config["retries"]
        self.debug = config["debug"]
        self.parser = MeterDataParser()

        # 기본 헤더 설정
        self.session.headers.update(
            {
                "User-Agent": "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/138.0.0.0 Safari/537.36",
                "Accept": "text/html,application/xhtml+xml,application/xml;q=0.9,image/avif,image/webp,image/apng,*/*;q=0.8",
                "Accept-Language": "ko;q=0.6",
                "Sec-GPC": "1",
                "Upgrade-Insecure-Requests": "1",
            }
        )

    def login(self, username: str, password: str) -> bool:
        """Login to ruvie.co.kr"""
        try:
            # 1. 먼저 메인 페이지에 접속하여 세션 쿠키 획득
            response = self.session.get(self.base_url)

            # 2. 로그인 요청
            login_url = f"{self.base_url}/login_set.html"

            login_data = {
                "uid": username,
                "upasswd": password,
                "x": "0",
                "y": "0",
            }

            login_headers = {
                "Content-Type": "application/x-www-form-urlencoded",
                "Origin": self.base_url,
                "Referer": f"{self.base_url}/",
                "Cache-Control": "max-age=0",
                "Sec-Fetch-Dest": "document",
                "Sec-Fetch-Mode": "navigate",
                "Sec-Fetch-Site": "same-origin",
                "Sec-Fetch-User": "?1",
            }

            response = self.session.post(
                login_url,
                data=login_data,
                headers=login_headers,
                allow_redirects=True,
                timeout=self.timeout,
            )

            # 로그인 성공 확인
            if response.status_code == 200:
                response_text = response.text

                # 로그인 성공 여부 확인
                success_patterns = [
                    "로그아웃",
                    "logout",
                    "마이페이지",
                    "mypage",
                    "님",
                    "회원정보",
                    "내정보",
                    "원격검침",
                ]

                for pattern in success_patterns:
                    if pattern in response_text.lower():
                        return True

                # 자동 폼 제출 확인 (두 번째 서버로의 전송)
                if "document.iform.submit()" in response_text:
                    # BeautifulSoup으로 폼 데이터 추출
                    soup = BeautifulSoup(response_text, "html.parser")
                    form = soup.find("form", {"name": "iform"})

                    if form:
                        form_tag = cast("Tag", form)
                        action = cast("str", form_tag.get("action"))

                        # 폼 데이터 수집
                        form_data = {}
                        for input_tag in form_tag.find_all("input", type="hidden"):
                            name = input_tag.get("name")
                            value = input_tag.get("value", "")
                            if name:
                                form_data[name] = value

                        # 두 번째 서버로 POST 요청
                        second_response = self.session.post(
                            action, data=form_data, verify=False
                        )

                        if second_response.status_code == 200:
                            # 쿠키 정리 - 중복된 PHPSESSID 처리
                            cookies_dict = {}
                            for cookie in self.session.cookies:
                                # meter server 도메인의 쿠키를 우선시
                                meter_host = self.meter_base_url.split("//")[1].split(
                                    ":"
                                )[0]
                                if (
                                    cookie.name == "PHPSESSID"
                                    and meter_host in cookie.domain
                                ):
                                    cookies_dict["PHPSESSID"] = cookie.value
                                elif cookie.name not in cookies_dict:
                                    cookies_dict[cookie.name] = cookie.value

                            return True

                # JavaScript 리다이렉트 확인
                if (
                    "location.href" in response_text
                    or "location.replace" in response_text
                ):
                    redirect_match = re.search(
                        r"location\.(href|replace)\s*[=\(]\s*[\"\']([^\"\']+)[\"\']",
                        response_text,
                    )
                    if redirect_match:
                        redirect_url = redirect_match.group(2)

                        # 리다이렉트 따라가기
                        if redirect_url.startswith("/"):
                            redirect_url = self.base_url + redirect_url

                        time.sleep(1)
                        redirect_response = self.session.get(redirect_url)

                        # 리다이렉트 후 로그인 확인
                        for pattern in success_patterns:
                            if pattern in redirect_response.text.lower():
                                return True

                return False
            else:
                return False

        except Exception:
            return False

    def fetch_meter_data(
        self, year: int, month: int, eg: int = 1
    ) -> Optional[Dict[str, Any]]:
        """Fetch remote meter data"""
        url = f"{self.meter_base_url}/center/remote_meter_sub.php"
        params: Dict[str, Any] = {
            "tag": "home_remote_meter",
            "yy": year,
            "mm": month,
            "eg": eg,
        }

        headers = {
            "Referer": f"{self.meter_base_url}/center/remote_meter_view.php?tag=home_remote_meter&eg={eg}&yy={year}",
            "Connection": "keep-alive",
        }

        try:
            response = self.session.get(
                url, params=params, headers=headers, verify=False
            )
            response.raise_for_status()

            # HTML 파싱을 위해 parser 사용
            data = self.parser.parse_meter_table(response.text)

            if not data:
                return None

            return {"year": year, "month": month, "data": data}

        except Exception:
            return None

    def fetch_multiple_months(
        self, start_year: int, start_month: int, end_year: int, end_month: int
    ) -> List[Dict[str, Any]]:
        """Fetch data for multiple months"""
        all_data = []

        current_year = start_year
        current_month = start_month

        while (current_year < end_year) or (
            current_year == end_year and current_month <= end_month
        ):
            result = self.fetch_meter_data(current_year, current_month)

            if result:
                all_data.append(result)
                time.sleep(1)  # 서버 부하 방지를 위한 딜레이

            # 다음 달로 이동
            current_month += 1
            if current_month > 12:
                current_month = 1
                current_year += 1

        return all_data
