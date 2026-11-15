"""Teste de exatidão monetária no relatório."""

from helpers import run_cli


def test_currency_preserves_precision_until_serialization(tmp_path):
    report = run_cli(
        tmp_path,
        [
            {"reservation_id": "R-1", "currency": "USD", "amount": "0.75"},
            {"reservation_id": "R-2", "currency": "USD", "amount": "0.75"},
        ],
    )

    summary = report["summary"]
    assert summary["total_amount_brl"] == "8.13"
    assert summary["average_nightly_rate_brl"] == "4.07"
