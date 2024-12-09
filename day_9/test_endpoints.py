from pathlib import Path

from fastapi.testclient import TestClient

from day_9.endpoints import (
    parse_input,
    find_free_block,
    sort_file_blocks_method_1,
    sort_file_blocks_method_2,
)
from main import app
from utils import read_file

client = TestClient(app)

day = 9


class TestDay9:
    example_input = read_file(
        Path(__file__).parent.joinpath("example_input.txt").absolute()
    )

    test_input = read_file(Path(__file__).parent.joinpath("test_input.txt").absolute())

    def test_filesystem_builder(self):
        test_filesystem = "12345"
        expected_output = [
            {"id": 0, "length": 1, "free_space": 2},
            {"id": 1, "length": 3, "free_space": 4},
            {"id": 2, "length": 5, "free_space": 0},
        ]

        actual_output = parse_input(test_filesystem)

        assert actual_output == expected_output

    def test_filesystem_builder_2(self):
        test_filesystem = "90909"
        expected_output = [
            {"id": 0, "length": 9, "free_space": 0},
            {"id": 1, "length": 9, "free_space": 0},
            {"id": 2, "length": 9, "free_space": 0},
        ]

        actual_output = parse_input(test_filesystem)

        assert actual_output == expected_output

    def test_find_free_block_first_free(self):
        test_input = [
            {"id": 0, "length": 1, "free_space": 2},
            {"id": 1, "length": 3, "free_space": 4},
            {"id": 2, "length": 5, "free_space": 0},
        ]
        expected = 0
        actual = find_free_block(test_input)

        assert actual == expected

    def test_find_free_block_next_free(self):
        test_input = [
            {"id": 0, "length": 1, "free_space": 0},
            {"id": 1, "length": 3, "free_space": 4},
            {"id": 2, "length": 5, "free_space": 2},
        ]
        expected = 1
        actual = find_free_block(test_input)

        assert actual == expected

    def test_find_free_block_last_free(self):
        test_input = [
            {"id": 0, "length": 1, "free_space": 0},
            {"id": 1, "length": 3, "free_space": 0},
            {"id": 0, "length": 5, "free_space": 6},
        ]
        expected = 2
        actual = find_free_block(test_input)

        assert actual == expected

    def test_rearrange_blocks_1(self):
        test_input = [
            {"id": 0, "length": 1, "free_space": 2},
            {"id": 1, "length": 3, "free_space": 4},
            {"id": 2, "length": 5, "free_space": 0},
        ]

        expected_output = [
            {"id": 0, "length": 1, "free_space": 0},
            {"id": 2, "length": 2, "free_space": 0},
            {"id": 1, "length": 3, "free_space": 0},
            {"id": 2, "length": 3, "free_space": 6},
        ]

        assert expected_output == sort_file_blocks_method_1(test_input)

    def test_rearrange_blocks_2(self):
        test_input = [
            {"id": 0, "length": 2, "free_space": 3},
            {"id": 1, "length": 3, "free_space": 3},
            {"id": 2, "length": 1, "free_space": 3},
            {"id": 3, "length": 3, "free_space": 1},
            {"id": 4, "length": 2, "free_space": 1},
            {"id": 5, "length": 4, "free_space": 1},
            {"id": 6, "length": 4, "free_space": 1},
            {"id": 7, "length": 3, "free_space": 1},
            {"id": 8, "length": 4, "free_space": 0},
            {"id": 9, "length": 2, "free_space": 0},
        ]

        expected_output = [
            {"id": 0, "length": 2, "free_space": 0},
            {"id": 9, "length": 2, "free_space": 0},
            {"id": 2, "length": 1, "free_space": 0},
            {"id": 1, "length": 3, "free_space": 0},
            {"id": 7, "length": 3, "free_space": 1},
            {"id": 4, "length": 2, "free_space": 1},
            {"id": 3, "length": 3, "free_space": 4},
            {"id": 5, "length": 4, "free_space": 1},
            {"id": 6, "length": 4, "free_space": 5},
            {"id": 8, "length": 4, "free_space": 2},
        ]

        assert sort_file_blocks_method_2(test_input) == expected_output

    def test_rearrange_blocks_2_more_than_one_move_per_pass(self):
        """
        0..1..2..3..4..5
        054132..........
        """
        test_input = [
            {"id": 0, "length": 1, "free_space": 2},
            {"id": 1, "length": 1, "free_space": 2},
            {"id": 2, "length": 1, "free_space": 2},
            {"id": 3, "length": 1, "free_space": 2},
            {"id": 4, "length": 1, "free_space": 2},
            {"id": 5, "length": 1, "free_space": 0},
        ]

        expected_output = [
            {"id": 0, "length": 1, "free_space": 0},
            {"id": 5, "length": 1, "free_space": 0},
            {"id": 4, "length": 1, "free_space": 0},
            {"id": 1, "length": 1, "free_space": 0},
            {"id": 3, "length": 1, "free_space": 0},
            {"id": 2, "length": 1, "free_space": 10},
        ]

        assert sort_file_blocks_method_2(test_input) == expected_output

    def test_task_1_example(self):
        expected_output = 1928

        response = client.post(f"/{day}/1", json={"data": self.example_input})
        assert response.status_code == 200
        assert response.json() == {"answer": expected_output}

    def test_task_1_test(self):
        expected_output = 6401092019345

        response = client.post(f"/{day}/1", json={"data": self.test_input})
        assert response.status_code == 200
        assert response.json() == {"answer": expected_output}

    def test_task_2_example(self):
        expected_output = 2858

        response = client.post(f"/{day}/2", json={"data": self.example_input})
        assert response.status_code == 200
        assert response.json() == {"answer": expected_output}

    def test_task_2_test(self):
        expected_output = 6431472344710

        response = client.post(f"/{day}/2", json={"data": self.test_input})
        assert response.status_code == 200
        assert response.json() == {"answer": expected_output}
