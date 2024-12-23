from pathlib import Path

from fastapi.testclient import TestClient

from main import app
from utils import read_file

client = TestClient(app)

day = 17


class TestDay17:
    example_input = read_file(
        Path(__file__).parent.joinpath("example_input.txt").absolute()
    )

    example_input_part_2 = read_file(
        Path(__file__).parent.joinpath("example_input_part_2.txt").absolute()
    )

    test_input = read_file(Path(__file__).parent.joinpath("test_input.txt").absolute())

    def test_task_1_example(self):
        expected_output = "4,6,3,5,6,3,5,2,1,0"

        response = client.post(f"/{day}/1", json={"data": self.example_input})
        assert response.status_code == 200
        assert response.json() == {"answer": expected_output}

    def test_task_1_test(self):
        expected_output = "7,1,3,7,5,1,0,3,4"

        response = client.post(f"/{day}/1", json={"data": self.test_input})
        assert response.status_code == 200
        assert response.json() == {"answer": expected_output}

    def test_task_2_example(self):
        expected_output = 117440

        response = client.post(f"/{day}/2", json={"data": self.example_input_part_2})
        assert response.status_code == 200
        assert response.json() == {"answer": expected_output}

    def test_task_2_test(self):
        expected_output = 190384113204239

        response = client.post(f"/{day}/2", json={"data": self.test_input})
        assert response.status_code == 200
        assert response.json() == {"answer": expected_output}
