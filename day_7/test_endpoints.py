from pathlib import Path

from fastapi.testclient import TestClient

from day_7.endpoints import check_for_deconcatenation, deconcatenate_numbers
from main import app
from utils import read_file

client = TestClient(app)

day = 7


class TestDay7:
    example_input = read_file(
        Path(__file__).parent.joinpath("example_input.txt").absolute()
    )

    test_input = read_file(Path(__file__).parent.joinpath("test_input.txt").absolute())

    def test_task_1_example(self):
        expected_output = 3749

        response = client.post(f"/{day}/1", json={"data": self.example_input})
        assert response.status_code == 200
        assert response.json() == {"answer": expected_output}

    def test_task_1_test(self):
        expected_output = 2654749936343

        response = client.post(f"/{day}/1", json={"data": self.test_input})
        assert response.status_code == 200
        assert response.json() == {"answer": expected_output}

    def test_check_for_deconcatenation_true(self):
        expected = True
        actual = check_for_deconcatenation(12345, 45)

        assert actual == expected

    def test_check_for_deconcatenation_false(self):
        expected = False
        actual = check_for_deconcatenation(12345, 44)

        assert actual == expected

    def test_check_for_deconcatenation_too_big(self):
        expected = False
        actual = check_for_deconcatenation(12, 123)

        assert actual == expected

    def test_deconcatenation(self):
        expected = 123
        actual = deconcatenate_numbers(12345, 45)

        assert actual == expected

    def test_deconcatenation_leaving_0(self):
        expected = 0
        actual = deconcatenate_numbers(123, 123)

        assert actual == expected

    def test_task_2_example(self):
        expected_output = 11387

        response = client.post(f"/{day}/2", json={"data": self.example_input})
        assert response.status_code == 200
        assert response.json() == {"answer": expected_output}

    def test_task_2_test(self):
        expected_output = 124060392153684

        response = client.post(f"/{day}/2", json={"data": self.test_input})
        assert response.status_code == 200
        assert response.json() == {"answer": expected_output}
