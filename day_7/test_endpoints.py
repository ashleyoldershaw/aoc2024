from pathlib import Path

from fastapi.testclient import TestClient

from day_7.endpoints import concatenate_numbers, format_number_in_base
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

    def test_number_concatenation(self):
        expected = 567
        actual = concatenate_numbers(56, 7)
        assert actual == expected

    def test_number_formatting_base_3(self):
        expected = "010"
        actual = format_number_in_base(3, 3, 3)
        assert actual == expected

    def test_number_formatting_base_3_with_2s(self):
        expected = "012"
        actual = format_number_in_base(3, 5, 3)
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
