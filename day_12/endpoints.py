from typing import List, Set

from fastapi import APIRouter

from aoc_types import TaskInput, Coordinates
from day_6.endpoints import out_of_bounds

day_12_routes = APIRouter()


def create_region_with_perimeter(
    plot_map: List[str], start_position: Coordinates, explored_plots: Set[Coordinates]
):
    """
    create a region around a cell, calculating its perimeter and area as we go
    :param plot_map: the map of the farm you are adding fencing to
    :param start_position: the initial location of the region you want to fence
    :param explored_plots: all the regions you have already explored
    :return: the area multiplied by the perimeter
    """
    rows = len(plot_map)
    cols = len(plot_map[0])

    perimeter = 0
    area = 0

    plot_type = plot_map[start_position[0]][start_position[1]]

    to_explore = {start_position}

    while to_explore:
        explored = to_explore.pop()
        area += 1
        explored_plots.add(explored)

        potential_new_plots = [
            (explored[0] - 1, explored[1]),
            (explored[0] + 1, explored[1]),
            (explored[0], explored[1] + 1),
            (explored[0], explored[1] - 1),
        ]

        for potential_plot in potential_new_plots:
            if out_of_bounds(potential_plot, rows, cols):
                perimeter += 1
                continue

            if plot_map[potential_plot[0]][potential_plot[1]] == plot_type:
                if potential_plot in explored_plots:
                    continue
                to_explore.add(potential_plot)
            else:
                perimeter += 1

    return area * perimeter


def create_region_with_sides(
    plot_map: List[str], start_position: Coordinates, explored_plots: Set[Coordinates]
):
    """
    create a region around a cell, calculating the number of sides and area as we go
    :param plot_map: the map of the farm you are adding fencing to
    :param start_position: the initial location of the region you want to fence
    :param explored_plots: all the regions you have already explored
    :return: the area multiplied by the number of sides
    """
    rows = len(plot_map)
    cols = len(plot_map[0])

    area = 0

    plot_type = plot_map[start_position[0]][start_position[1]]

    to_explore = {start_position}

    region_plots = set()

    while to_explore:
        explored = to_explore.pop()
        area += 1
        explored_plots.add(explored)
        region_plots.add(explored)

        potential_new_plots = [
            (explored[0] - 1, explored[1]),
            (explored[0] + 1, explored[1]),
            (explored[0], explored[1] + 1),
            (explored[0], explored[1] - 1),
        ]

        for potential_plot in potential_new_plots:
            if out_of_bounds(potential_plot, rows, cols):
                continue

            if plot_map[potential_plot[0]][potential_plot[1]] == plot_type:
                if potential_plot in explored_plots:
                    continue
                to_explore.add(potential_plot)

    corners = 0
    # find corners, and use to calculate edges
    for plot in region_plots:
        north_plot = (plot[0] - 1, plot[1])
        south_plot = (plot[0] + 1, plot[1])
        east_plot = (plot[0], plot[1] + 1)
        west_plot = (plot[0], plot[1] - 1)

        northeast_plot = (plot[0] - 1, plot[1] + 1)
        northwest_plot = (plot[0] - 1, plot[1] - 1)
        southeast_plot = (plot[0] + 1, plot[1] + 1)
        southwest_plot = (plot[0] + 1, plot[1] - 1)

        if north_plot not in region_plots:
            if east_plot not in region_plots:
                corners += 1
            if west_plot not in region_plots:
                corners += 1

        if south_plot not in region_plots:
            if east_plot not in region_plots:
                corners += 1
            if west_plot not in region_plots:
                corners += 1

        if north_plot in region_plots:
            if east_plot in region_plots and northeast_plot not in region_plots:
                corners += 1
            if west_plot in region_plots and northwest_plot not in region_plots:
                corners += 1

        if south_plot in region_plots:
            if east_plot in region_plots and southeast_plot not in region_plots:
                corners += 1
            if west_plot in region_plots and southwest_plot not in region_plots:
                corners += 1

    edges = corners

    return area * edges


@day_12_routes.post("/1")
async def task_1(task_input: TaskInput):
    total = 0
    plot_map = task_input.data.splitlines()
    explored_plots = set()
    for i in range(len(plot_map)):
        for j in range(len(plot_map[0])):
            if (new_region_start := (i, j)) not in explored_plots:
                total += create_region_with_perimeter(
                    plot_map, new_region_start, explored_plots
                )

    return {"answer": total}


@day_12_routes.post("/2")
async def task_2(task_input: TaskInput):
    total = 0
    plot_map = task_input.data.splitlines()
    explored_plots = set()
    for i in range(len(plot_map)):
        for j in range(len(plot_map[0])):
            if (new_region_start := (i, j)) not in explored_plots:
                total += create_region_with_sides(
                    plot_map, new_region_start, explored_plots
                )

    return {"answer": total}
