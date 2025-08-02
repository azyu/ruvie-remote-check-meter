"""Tests for MeterDataParser."""

from remote_check_meter.parser import MeterDataParser


class TestMeterDataParser:
    """Test cases for MeterDataParser."""

    def test_parse_meter_table(self):
        """Test parsing meter data table."""
        parser = MeterDataParser()

        html = """
        <table width="520" bgcolor="#cccccc">
            <tr><th>날짜</th><th>누적</th><th>일일</th></tr>
            <tr bgcolor="#ffffff">
                <td>2025년 08월 01일</td>
                <td>37129.9 KWh</td>
                <td>32.6 KWh</td>
            </tr>
        </table>
        """

        result = parser.parse_meter_table(html)

        assert len(result) == 1
        assert result[0]["date"] == "2025-08-01"
        assert result[0]["cumulative_usage_kwh"] == 37129.9
        assert result[0]["daily_usage_kwh"] == 32.6
