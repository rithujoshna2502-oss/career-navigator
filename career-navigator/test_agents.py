import pytest
from agents.orchestrator import Orchestrator
from agents.skill_assessor import SkillAssessor
from agents.recommender import Recommender
from agents.monitor import Monitor


def test_orchestrator_initialization():
    """Test that orchestrator initializes all agents."""
    orch = Orchestrator(poll_interval=30)
    assert orch.skill_assessor is not None
    assert orch.recommender is not None
    assert orch.monitor is not None
    assert orch.poll_interval == 30


def test_orchestrator_start_stop():
    """Test that orchestrator can start and stop its background thread."""
    orch = Orchestrator(poll_interval=5)
    orch.start()
    assert orch._thread is not None
    assert orch._thread.is_alive()
    orch.stop()
    # Give it a moment to join
    orch._thread.join(timeout=2)
    assert not orch._thread.is_alive()


def test_skill_assessor_no_user():
    """Test skill assessor returns empty for nonexistent user."""
    assessor = SkillAssessor()
    result = assessor.assess_user(99999)
    assert result['current_skills'] == []
    # Will be 'unknown' if DB access fails gracefully, 'error' if exception occurred
    assert result['proficiency_estimate'] in ['unknown', 'error']


def test_monitor_get_trends():
    """Test monitor can retrieve trending technologies."""
    monitor = Monitor()
    result = monitor.check_trends()
    assert 'trending' in result
    assert isinstance(result['trending'], list)


def test_recommender_empty_assessment():
    """Test recommender handles empty assessment gracefully."""
    recommender = Recommender()
    assessment = {
        'plan_goal': 'Software Engineer',
        'current_skills': [],
        'skill_gaps': [],
        'plan_skills': []
    }
    result = recommender.recommend_for_user(1, assessment)
    assert 'skill_gaps' in result
    assert 'must_learn' in result
