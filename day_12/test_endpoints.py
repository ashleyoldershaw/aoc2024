from pathlib import Path

from fastapi.testclient import TestClient

from main import app
from utils import read_file

client = TestClient(app)

day = 12


class TestDay12:
    example_input = read_file(
        Path(__file__).parent.joinpath("example_input.txt").absolute()
    )

    test_input = read_file(Path(__file__).parent.joinpath("test_input.txt").absolute())

    def test_task_1_example(self):
        expected_output = 1930

        response = client.post(f"/{day}/1", json={"data": self.example_input})
        assert response.status_code == 200
        assert response.json() == {"answer": expected_output}

    def test_task_1_test(self):
        expected_output = 1465112

        response = client.post(f"/{day}/1", json={"data": self.test_input})
        assert response.status_code == 200
        assert response.json() == {"answer": expected_output}

    def test_task_2_example(self):
        expected_output = 1206

        response = client.post(f"/{day}/2", json={"data": self.example_input})
        assert response.status_code == 200
        assert response.json() == {"answer": expected_output}

    def test_task_2_test(self):
        expected_output = 893790

        response = client.post(f"/{day}/2", json={"data": self.test_input})
        assert response.status_code == 200
        assert response.json() == {"answer": expected_output}