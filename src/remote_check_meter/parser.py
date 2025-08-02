"""HTML parser for meter data."""

import re
from typing import Any, Dict, List, Optional

from bs4 import BeautifulSoup


class MeterDataParser:
    """Parser for meter data HTML tables."""

    def parse_meter_table(self, html: str) -> List[Dict[str, Any]]:
        """Parse meter data from HTML table."""
        soup = BeautifulSoup(html, "html.parser")

        # 테이블 찾기
        table = None
        for t in soup.find_all("table", width="520"):
            if t.get("bgcolor") == "#cccccc":
                table = t
                break

        if not table:
            return []

        # 데이터 추출
        data = []
        rows = table.find_all("tr")

        for row in rows[1:]:  # 헤더 행 제외
            cols = row.find_all("td")
            if len(cols) >= 3:
                record = self._parse_row(cols)
                if record:
                    data.append(record)

        return data

    def _parse_row(self, cols: Any) -> Optional[Dict[str, Any]]:
        """Parse a single table row."""
        try:
            # 날짜 파싱
            date_text = cols[0].get_text(strip=True)
            date_match = re.search(r"(\d{4})년\s*(\d{2})월\s*(\d{2})일", date_text)

            # 사용량 파싱
            cumulative_text = cols[1].get_text(strip=True)
            daily_text = cols[2].get_text(strip=True)

            cumulative_match = re.search(r"([\d.]+)", cumulative_text)
            daily_match = re.search(r"([\d.]+)", daily_text)

            if date_match and cumulative_match and daily_match:
                return {
                    "date": f"{date_match.group(1)}-{date_match.group(2)}-{date_match.group(3)}",
                    "cumulative_usage_kwh": float(cumulative_match.group(1)),
                    "daily_usage_kwh": float(daily_match.group(1)),
                }
        except (ValueError, AttributeError):
            pass

        return None
