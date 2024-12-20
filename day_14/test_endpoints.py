from pathlib import Path

from fastapi.testclient import TestClient

from main import app
from utils import read_file

client = TestClient(app)

day = 14


class TestDay14:
    example_input = read_file(
        Path(__file__).parent.joinpath("example_input.txt").absolute()
    )

    test_input = read_file(Path(__file__).parent.joinpath("test_input.txt").absolute())

    def test_task_1_example(self):
        expected_output = 12

        response = client.post(
            f"/{day}/1", json={"data": self.example_input, "rows": 7, "cols": 11}
        )
        assert response.status_code == 200
        assert response.json() == {"answer": expected_output}

    def test_task_1_test(self):
        expected_output = 219150360

        response = client.post(
            f"/{day}/1", json={"data": self.test_input, "rows": 103, "cols": 101}
        )
        assert response.status_code == 200
        assert response.json() == {"answer": expected_output}
