from pathlib import Path

from fastapi.testclient import TestClient

from day_21.endpoints import get_keypad_path, get_complexity
from main import app
from utils import read_file

client = TestClient(app)

day = 21


class TestDay21:
    example_input = read_file(
        Path(__file__).parent.joinpath("example_input.txt").absolute()
    )

    test_input = read_file(Path(__file__).parent.joinpath("test_input.txt").absolute())

    def test_keypad_path(self):
        expected = "<A^A^^>AvvvA"
        actual = get_keypad_path("029A")
        assert actual == expected

    def test_get_complexity(self):
        inputs = ["029A", "980A", "179A", "456A", "379A"]
        actual = [get_complexity(i, 2) for i in inputs]
        expected = [68 * 29, 60 * 980, 68 * 179, 64 * 456, 64 * 379]
        assert actual == expected

    def test_task_1_example(self):
        expected_output = 126384

        response = client.post(
            f"/{day}/1",
            json={"data": self.example_input},
        )
        assert response.status_code == 200
        assert response.json() == {"answer": expected_output}

    def test_task_1_test(self):
        expected_output = 176870

        response = client.post(
            f"/{day}/1",
            json={"data": self.test_input},
        )
        assert response.status_code == 200
        assert response.json() == {"answer": expected_output}

    def test_task_2_test(self):
        expected_output = 223902935165512

        response = client.post(f"/{day}/2", json={"data": self.test_input})
        assert response.status_code == 200
        assert response.json() == {"answer": expected_output}
