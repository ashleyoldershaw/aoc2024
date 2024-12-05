from pathlib import Path

from fastapi.testclient import TestClient

from day_4.endpoints import (
    half_rotate,
    square_rotate,
    calculate_ending_location,
    calculate_starting_location,
)
from main import app
from utils import read_file

client = TestClient(app)

day = 4


class TestDay4:
    example_input = read_file(
        Path(__file__).parent.joinpath("example_input.txt").absolute()
    )

    test_input = read_file(Path(__file__).parent.joinpath("test_input.txt").absolute())

    def test_calculate_starting_position_1x1_line_1(self):
        expected = (0, 0)
        actual = calculate_ending_location(1, 1, 0)
        assert actual == expected

    def test_calculate_ending_position_1x1_line_1(self):
        expected = (0, 0)
        actual = calculate_starting_location(1, 1, 0)
        assert actual == expected

    def test_calculate_starting_position_1x2_line_1(self):
        expected = (0, 1)
        actual = calculate_ending_location(1, 2, 0)
        assert actual == expected

    def test_calculate_ending_position_1x2_line_1(self):
        expected = (0, 1)
        actual = calculate_starting_location(1, 2, 0)
        assert actual == expected

    def test_calculate_starting_position_1x2_line_2(self):
        expected = (0, 0)
        actual = calculate_ending_location(1, 2, 1)
        assert actual == expected

    def test_calculate_ending_position_1x2_line_2(self):
        expected = (0, 0)
        actual = calculate_starting_location(1, 2, 1)
        assert actual == expected

    def test_calculate_starting_position_2x1_line_1(self):
        expected = (0, 0)
        actual = calculate_ending_location(2, 1, 0)
        assert actual == expected

    def test_calculate_ending_position_2x1_line_1(self):
        expected = (0, 0)
        actual = calculate_starting_location(2, 1, 0)
        assert actual == expected

    def test_calculate_starting_position_2x1_line_2(self):
        expected = (1, 0)
        actual = calculate_ending_location(2, 1, 1)
        assert actual == expected

    def test_calculate_ending_position_2x1_line_2(self):
        expected = (1, 0)
        actual = calculate_starting_location(2, 1, 1)
        assert actual == expected

    def test_calculate_starting_position_2x2_line_1(self):
        expected = (0, 1)
        actual = calculate_ending_location(2, 2, 0)
        assert actual == expected

    def test_calculate_ending_position_2x2_line_1(self):
        expected = (0, 1)
        actual = calculate_starting_location(2, 2, 0)
        assert actual == expected

    def test_calculate_starting_position_2x2_line_2(self):
        expected = (1, 1)
        actual = calculate_ending_location(2, 2, 1)
        assert actual == expected

    def test_calculate_ending_position_2x2_line_2(self):
        expected = (0, 0)
        actual = calculate_starting_location(2, 2, 1)
        assert actual == expected

    def test_calculate_starting_position_2x2_line_3(self):
        expected = (1, 0)
        actual = calculate_ending_location(2, 2, 2)
        assert actual == expected

    def test_calculate_ending_position_2x2_line_3(self):
        expected = (1, 0)
        actual = calculate_starting_location(2, 2, 2)
        assert actual == expected

    def test_calculate_starting_position_3x3_line_1(self):
        expected = (0, 2)
        actual = calculate_ending_location(3, 3, 0)
        assert actual == expected

    def test_calculate_ending_position_3x3_line_1(self):
        expected = (0, 2)
        actual = calculate_starting_location(3, 3, 0)
        assert actual == expected

    def test_calculate_starting_position_3x3_line_2(self):
        expected = (1, 2)
        actual = calculate_ending_location(3, 3, 1)
        assert actual == expected

    def test_calculate_ending_position_3x3_line_2(self):
        expected = (0, 1)
        actual = calculate_starting_location(3, 3, 1)
        assert actual == expected

    def test_calculate_starting_position_3x3_line_3(self):
        expected = (2, 2)
        actual = calculate_ending_location(3, 3, 2)
        assert actual == expected

    def test_calculate_ending_position_3x3_line_3(self):
        expected = (0, 0)
        actual = calculate_starting_location(3, 3, 2)
        assert actual == expected

    def test_calculate_starting_position_3x3_line_4(self):
        expected = (2, 1)
        actual = calculate_ending_location(3, 3, 3)
        assert actual == expected

    def test_calculate_ending_position_3x3_line_4(self):
        expected = (1, 0)
        actual = calculate_starting_location(3, 3, 3)
        assert actual == expected

    def test_calculate_starting_position_3x3_line_5(self):
        expected = (2, 0)
        actual = calculate_ending_location(3, 3, 4)
        assert actual == expected

    def test_calculate_ending_position_3x3_line_5(self):
        expected = (2, 0)
        actual = calculate_starting_location(3, 3, 4)
        assert actual == expected

    def test_rotate_90_one(self):
        input = "A"
        expected_output = "A"
        actual_output = square_rotate(input)
        assert actual_output == expected_output

    def test_rotate_90_linear(self):
        input = "AB"
        expected_output = "B\n" "A"
        actual_output = square_rotate(input)
        assert actual_output == expected_output

    def test_rotate_90_square(self):
        input = "AB\n" "CD"
        expected_output = "BD\n" "AC"
        actual_output = square_rotate(input)
        assert actual_output == expected_output

    def test_rotate_45_square_2x2(self):
        input = "AB\n" "CD"
        expected_output = "B\n" "AD\n" "C"
        actual_output = half_rotate(input)
        assert actual_output == expected_output

    def test_rotate_45_square_3x3(self):
        input = "ABC\n" "DEF\n" "GHI"
        expected_output = "C\n" "BF\n" "AEI\n" "DH\n" "G"
        actual_output = half_rotate(input)
        assert actual_output == expected_output

    def test_rotate_45_rect_long(self):
        input = "ABC\n" "DEF"
        expected_output = "C\n" "BF\n" "AE\n" "D"
        actual_output = half_rotate(input)
        assert actual_output == expected_output

    def test_rotate_45_rect_tall(self):
        input = "AB\n" "CD\n" "EF"
        expected_output = "B\n" "AD\n" "CF\n" "E"
        actual_output = half_rotate(input)
        assert actual_output == expected_output

    def test_task_1_example(self):
        expected_output = 18

        response = client.post(f"/{day}/1", json={"data": self.example_input})
        assert response.status_code == 200
        assert response.json() == {"answer": expected_output}

    def test_task_1_test(self):
        expected_output = 2593

        response = client.post(f"/{day}/1", json={"data": self.test_input})
        assert response.status_code == 200
        assert response.json() == {"answer": expected_output}

    def test_task_2_example(self):
        expected_output = 9

        response = client.post(f"/{day}/2", json={"data": self.example_input})
        assert response.status_code == 200
        assert response.json() == {"answer": expected_output}

    def test_task_2_test(self):
        expected_output = 1950

        response = client.post(f"/{day}/2", json={"data": self.test_input})
        assert response.status_code == 200
        assert response.json() == {"answer": expected_output}
