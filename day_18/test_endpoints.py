from pathlib import Path

from fastapi.testclient import TestClient

from main import app
from utils import read_file

client = TestClient(app)

day = 18


class TestDay18:
    example_input = read_file(
        Path(__file__).parent.joinpath("example_input.txt").absolute()
    )

    test_input = read_file(Path(__file__).parent.joinpath("test_input.txt").absolute())

    def test_task_1_example(self):
        expected_output = 22

        response = client.post(
            f"/{day}/1",
            json={"data": self.example_input, "rows": 7, "cols": 7, "first": 12},
        )
        assert response.status_code == 200
        assert response.json() == {"answer": expected_output}

    def test_task_1_test(self):
        expected_output = 318

        response = client.post(
            f"/{day}/1",
            json={"data": self.test_input, "rows": 71, "cols": 71, "first": 1024},
        )
        assert response.status_code == 200
        assert response.json() == {"answer": expected_output}

    def test_task_2_example(self):
        expected_output = "6,1"

        response = client.post(
            f"/{day}/2", json={"data": self.example_input, "rows": 7, "cols": 7}
        )
        assert response.status_code == 200
        assert response.json() == {"answer": expected_output}

    def test_task_2_test(self):
        expected_output = "56,29"

        response = client.post(
            f"/{day}/2", json={"data": self.test_input, "rows": 71, "cols": 71}
        )
        assert response.status_code == 200
        assert response.json() == {"answer": expected_output}
