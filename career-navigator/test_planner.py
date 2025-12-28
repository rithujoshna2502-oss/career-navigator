import pytest
from planner import generate_daily_plan


def test_generate_daily_plan_day_indexing_and_length():
    # Use a known profession and short duration to validate indexing
    profession = 'Web Developer'
    duration_months = 1
    current_skills = []
    experience_level = 'beginner'

    plan = generate_daily_plan(profession, duration_months, current_skills, experience_level)

    total_days = duration_months * 30
    assert plan['total_days'] == total_days
    daily_tasks = plan['daily_tasks']

    # Ensure we have at least total_days tasks (or trimmed to total_days)
    assert len(daily_tasks) == total_days

    # Ensure day numbering starts at 1 and increments properly
    assert daily_tasks[0]['day'] == 1
    for i, task in enumerate(daily_tasks, start=1):
        assert task['day'] == i
