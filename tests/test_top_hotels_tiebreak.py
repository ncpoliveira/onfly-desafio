"""Teste do desempate na última vaga do ranking de hotéis."""

from helpers import run_cli


def test_top_hotels_breaks_ties_by_ascending_hotel_id(tmp_path):
    report = run_cli(
        tmp_path,
        [
            {"reservation_id": "R-1", "hotel_id": "H03", "amount": "900.00"},
            {"reservation_id": "R-2", "hotel_id": "H01", "amount": "1000.00"},
            {"reservation_id": "R-3", "hotel_id": "H02", "amount": "900.00"},
        ],
        top=2,
    )

    assert [hotel["hotel_id"] for hotel in report["top_hotels"]] == ["H01", "H02"]
