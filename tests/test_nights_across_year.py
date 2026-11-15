"""Teste de regressão para noites de quarto na virada de ano."""

from helpers import run_cli


def test_nights_across_year_boundary_with_multiple_rooms(tmp_path):
    report = run_cli(
        tmp_path,
        [
            {
                "checkin_date": "2025-12-31",
                "checkout_date": "2026-01-02",
                "rooms": "2",
            },
        ],
    )

    assert report["summary"]["total_room_nights"] == 4
    monthly_nights = [(month["month"], month["room_nights"]) for month in report["by_month"]]
    assert monthly_nights == [("2025-12", 4)]
