from pathlib import Path

from fastapi.testclient import TestClient

from day_10.endpoints import find_trailheads
from main import app
from utils import read_file

client = TestClient(app)

day = 10


class TestDay10:
    example_input = read_file(
        Path(__file__).parent.joinpath("example_input.txt").absolute()
    )

    test_input = read_file(Path(__file__).parent.joinpath("test_input.txt").absolute())

    def test_path_finder(self):
        test_input = (
            "...0...\n"
            "...1...\n"
            "...2...\n"
            "6543456\n"
            "7.....7\n"
            "8.....8\n"
            "9.....9\n".splitlines()
        )
        expected_output = 2
        trailheads = set()
        find_trailheads(test_input, 0, 3, trailheads, 0)
        assert len(trailheads) == expected_output

    def test_task_1_example(self):
        expected_output = 36

        response = client.post(f"/{day}/1", json={"data": self.example_input})
        assert response.status_code == 200
        assert response.json() == {"answer": expected_output}

    def test_task_1_test(self):
        expected_output = 737

        response = client.post(f"/{day}/1", json={"data": self.test_input})
        assert response.status_code == 200
        assert response.json() == {"answer": expected_output}

    def test_task_2_example(self):
        expected_output = 81

        response = client.post(f"/{day}/2", json={"data": self.example_input})
        assert response.status_code == 200
        assert response.json() == {"answer": expected_output}

    def test_task_2_test(self):
        expected_output = 1619

        response = client.post(f"/{day}/2", json={"data": self.test_input})
        assert response.status_code == 200
        assert response.json() == {"answer": expected_output}
