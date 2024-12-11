from pathlib import Path

from fastapi.testclient import TestClient

from main import app
from utils import read_file

client = TestClient(app)

day = 6


class TestDay6:
    example_input = read_file(
        Path(__file__).parent.joinpath("example_input.txt").absolute()
    )

    test_input = read_file(Path(__file__).parent.joinpath("test_input.txt").absolute())

    def test_task_1_example(self):
        expected_output = 41

        response = client.post(f"/{day}/1", json={"data": self.example_input})
        assert response.status_code == 200
        assert response.json() == {"answer": expected_output}

    def test_task_1_test(self):
        expected_output = 5444

        response = client.post(f"/{day}/1", json={"data": self.test_input})
        assert response.status_code == 200
        assert response.json() == {"answer": expected_output}

    def test_task_2_example(self):
        expected_output = 6

        response = client.post(f"/{day}/2", json={"data": self.example_input})
        assert response.status_code == 200
        assert response.json() == {"answer": expected_output}

    def test_task_2_test(self):
        expected_output = 1946

        response = client.post(f"/{day}/2", json={"data": self.test_input})
        assert response.status_code == 200
        assert response.json() == {"answer": expected_output}

    def test_task_2_small_loop(self):
        expected_output = 1
        test_input = ".#.\n" ".^#\n" ".#."

        response = client.post(f"/{day}/2", json={"data": test_input})
        assert response.status_code == 200
        assert response.json() == {"answer": expected_output}

    def test_task_2_small_loop_look_ahead(self):
        expected_output = 1
        test_input = "...\n" "#^#\n" ".#."

        response = client.post(f"/{day}/2", json={"data": test_input})
        assert response.status_code == 200
        assert response.json() == {"answer": expected_output}
