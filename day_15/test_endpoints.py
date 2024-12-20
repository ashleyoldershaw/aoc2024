from pathlib import Path

from fastapi.testclient import TestClient

from day_15.endpoints import (
    puzzle_map_string,
    follow_instructions,
    follow_instructions_part_2,
)
from main import app
from utils import read_file

client = TestClient(app)

day = 15


class TestDay15:
    example_input = read_file(
        Path(__file__).parent.joinpath("example_input.txt").absolute()
    )

    test_input = read_file(Path(__file__).parent.joinpath("test_input.txt").absolute())

    def test_example_finishes_the_same(self):
        start = """########
#..O.O.#
##@.O..#
#...O..#
#.#.O..#
#...O..#
#......#
########

<^^>>>vv<v>>v<<"""
        expected_output = """########
#....OO#
##.....#
#.....O#
#.#O...#
#...O..#
#...O..#
########"""
        actual_output = puzzle_map_string(follow_instructions(start))

        assert actual_output == expected_output

    def test_task_1_map_finishes_the_same(self):
        expected_output = (
            "##########\n"
            "#.O.O.OOO#\n"
            "#........#\n"
            "#OO......#\n"
            "#OO......#\n"
            "#O#.....O#\n"
            "#O.....OO#\n"
            "#O.....OO#\n"
            "#OO....OO#\n"
            "##########"
        )
        actual_output = puzzle_map_string(follow_instructions(self.example_input))
        assert actual_output == expected_output

    def test_task_1_example(self):
        expected_output = 10092

        response = client.post(f"/{day}/1", json={"data": self.example_input})
        assert response.status_code == 200
        assert response.json() == {"answer": expected_output}

    def test_task_1_test(self):
        expected_output = 1509074

        response = client.post(f"/{day}/1", json={"data": self.test_input})
        assert response.status_code == 200
        assert response.json() == {"answer": expected_output}

    def test_task_2_mini_map_finishes_the_same(self):
        start = """#######
#...#.#
#.....#
#..OO@#
#..O..#
#.....#
#######

<vv<<^^<<^^"""
        expected_output = """##############
##...[].##..##
##...@.[]...##
##....[]....##
##..........##
##..........##
##############"""

        actual_output = puzzle_map_string(follow_instructions_part_2(start))

        assert actual_output == expected_output

    def test_task_2_hitting_wall(self):
        start = """#######
#...#.#
#.....#
#..OO@#
#..O..#
#.....#
#######

<vv<<^^^<<^^"""
        expected_output = """##############
##...[].##..##
##...@.[]...##
##....[]....##
##..........##
##..........##
##############"""

        actual_output = puzzle_map_string(follow_instructions_part_2(start))

        assert actual_output == expected_output

    def test_task_2_map_finishes_the_same(self):
        expected_output = (
            "####################\n"
            "##[].......[].[][]##\n"
            "##[]...........[].##\n"
            "##[]........[][][]##\n"
            "##[]......[]....[]##\n"
            "##..##......[]....##\n"
            "##..[]............##\n"
            "##..@......[].[][]##\n"
            "##......[][]..[]..##\n"
            "####################"
        )

        actual_output = puzzle_map_string(
            follow_instructions_part_2(self.example_input)
        )

        assert actual_output == expected_output

    def test_task_2_example(self):
        expected_output = 9021

        response = client.post(f"/{day}/2", json={"data": self.example_input})
        assert response.status_code == 200
        assert response.json() == {"answer": expected_output}

    def test_task_2_test(self):
        expected_output = 1521453

        response = client.post(f"/{day}/2", json={"data": self.test_input})
        assert response.status_code == 200
        assert response.json() == {"answer": expected_output}
