from fastapi.testclient import TestClient

from day_2.endpoints import check_safety_with_leveller
from main import app
from utils import read_file

client = TestClient(app)

day = 2


class TestDay2:
    example_input = read_file("example_input.txt")

    test_input = read_file("test_input.txt")

    def test_task_1_example(self):
        expected_output = 2

        response = client.post(f"/{day}/1", json={"data": self.example_input})
        assert response.status_code == 200
        assert response.json() == {"answer": expected_output}

    def test_task_1_test(self):
        expected_output = 356

        response = client.post(f"/{day}/1", json={"data": self.test_input})
        assert response.status_code == 200
        assert response.json() == {"answer": expected_output}

    def test_task_2_example(self):
        expected_output = 4

        response = client.post(f"/{day}/2", json={"data": self.example_input})
        assert response.status_code == 200
        assert response.json() == {"answer": expected_output}

    def test_task_2_wrong_ordering_first_element(self):
        """
        What if the first item is the one that will cause the problem?
        :return:
        """
        expected_output = 1

        actual_output = check_safety_with_leveller([2, 4, 3, 2, 1])

        assert actual_output == expected_output

    def test_task_2_wrong_ordering_second_element(self):
        """
        What if the second item is the one that will cause the problem?
        :return:
        """
        expected_output = 1

        actual_output = check_safety_with_leveller([4, 2, 3, 2, 1])

        assert actual_output == expected_output

    def test_task_2_gap_too_big(self):
        """
        What if the second item is the one that will cause the problem?
        :return:
        """
        expected_output = 1

        actual_output = check_safety_with_leveller([7, 3, 5, 3, 1])

        assert actual_output == expected_output

    def test_task_2_test(self):
        expected_output = 413

        response = client.post(f"/{day}/2", json={"data": self.test_input})
        assert response.status_code == 200
        assert response.json() == {"answer": expected_output}
