"""Teste da regra de status nos agrupamentos do relatório."""

from helpers import run_cli


def test_only_confirmed_reservations_appear_in_report_groups(tmp_path):
    report = run_cli(
        tmp_path,
        [
            {"reservation_id": "R-1", "status": "CONFIRMED", "hotel_id": "H01"},
            {
                "reservation_id": "R-2",
                "status": "CANCELLED",
                "hotel_id": "H02",
                "checkin_date": "2025-02-10",
                "checkout_date": "2025-02-11",
            },
            {
                "reservation_id": "R-3",
                "status": "NO_SHOW",
                "hotel_id": "H03",
                "checkin_date": "2025-03-10",
                "checkout_date": "2025-03-11",
            },
        ],
    )

    assert [month["month"] for month in report["by_month"]] == ["2025-01"]
    assert [hotel["hotel_id"] for hotel in report["top_hotels"]] == ["H01"]
