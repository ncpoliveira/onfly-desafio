"""Teste de regressão para a leitura de todas as reservas do CSV."""

from helpers import run_cli


def test_reads_all_reservations_from_csv(tmp_path):
    rows = [{"reservation_id": f"R-{number}"} for number in range(1, 201)]
    rows.append({"reservation_id": "R-201", "status": "CANCELLED"})

    summary = run_cli(tmp_path, rows)["summary"]

    assert summary["total_reservations"] == 201
    assert summary["cancelled_reservations"] == 1
