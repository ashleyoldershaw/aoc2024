from fastapi import APIRouter

from aoc_types import TaskInput

day_5_routes = APIRouter()


def generate_rule_set(raw_rules):
    rules = [line.split("|") for line in raw_rules.split("\n")]
    rule_set = {}
    # key is a page, value is a set of pages that will not be allowed anymore after it's been seen
    for rule in rules:
        if rule[1] not in rule_set:
            rule_set[rule[1]] = set()
        rule_set[rule[1]].add(rule[0])
    return rule_set


def generate_order_set(raw_rules):
    rules = [line.split("|") for line in raw_rules.split("\n")]
    rule_set = {}
    # key is a page, value is a set of pages that should be after the current page
    for rule in rules:
        if rule[0] not in rule_set:
            rule_set[rule[0]] = set()
        rule_set[rule[0]].add(rule[1])
    return rule_set


def get_new_page_location(manual, ordering_set, page_number):
    new_location = len(manual)
    for previous_page in ordering_set[page_number]:
        if previous_page in manual:
            new_location = min(manual.index(previous_page), new_location)
    return new_location


@day_5_routes.post("/1")
async def task_1(task_input: TaskInput):
    total = 0
    raw_rules, raw_manuals = task_input.data.split("\n\n")
    rule_set = generate_rule_set(raw_rules)

    for manual in [raw_manual.split(",") for raw_manual in raw_manuals.split("\n")]:
        page_valid = True
        banned_list = set()
        for page_number in manual:
            if page_number in banned_list:
                page_valid = False
            elif page_number in rule_set:
                # ban all values that should come before the page number
                banned_list = banned_list.union(rule_set[page_number])

        if page_valid:
            total += int(manual[len(manual) // 2])

    return {"answer": total}


@day_5_routes.post("/2")
async def task_2(task_input: TaskInput):
    total = 0
    raw_rules, raw_manuals = task_input.data.split("\n\n")
    rule_set = generate_rule_set(raw_rules)
    ordering_set = generate_order_set(raw_rules)

    for manual in [raw_manual.split(",") for raw_manual in raw_manuals.split("\n")]:
        page_valid = True
        banned_list = set()
        for i in range(len(manual)):
            page_number = manual[i]
            if page_number in banned_list:
                # if the page is banned, we need to find the new location to move it to
                page_valid = False

                new_location = get_new_page_location(manual, ordering_set, page_number)

                # remove the offending page and slide it behind the new one we need
                manual.pop(i)
                manual.insert(new_location, page_number)

            if page_number in rule_set:
                # ban all values that should come before the page number
                banned_list = banned_list.union(rule_set[page_number])

        if not page_valid:
            total += int(manual[len(manual) // 2])
    return {"answer": total}
