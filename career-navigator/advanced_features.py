"""
Advanced Features Module
- AI-powered study recommendations
- Learning leaderboard
- Analytics dashboard
- Achievement badges
"""

def get_learning_recommendations(user_skills, goal, performance_data):
    """
    Generate personalized study recommendations based on:
    - Current skills
    - Career goal
    - Learning progress & velocity
    """
    recommendations = {
        'focus_areas': [],
        'recommended_resources': [],
        'challenge_level': 'intermediate',
        'estimated_hours_remaining': 0
    }
    
    # Calculate skill gaps
    required_skills = {
        'AI Engineer': ['Python', 'Machine Learning', 'TensorFlow', 'PyTorch', 'NLP', 'Deep Learning'],
        'Data Scientist': ['Python', 'Statistics', 'SQL', 'Pandas', 'Scikit-learn', 'Data Visualization'],
        'Software Engineer': ['Python', 'JavaScript', 'System Design', 'Databases', 'Git'],
    }
    
    goal_skills = required_skills.get(goal, [])
    current_skills = set(skill.lower() for skill in (user_skills or []))
    missing_skills = [s for s in goal_skills if s.lower() not in current_skills]
    
    recommendations['focus_areas'] = missing_skills[:3]  # Top 3 to focus on
    
    # Recommend resources based on missing skills
    resources_map = {
        'machine learning': 'Andrew Ng\'s Machine Learning Course (Coursera)',
        'tensorflow': 'TensorFlow Official Tutorials',
        'nlp': 'Hugging Face NLP Course',
        'deep learning': 'Fast.ai Deep Learning',
        'system design': 'System Design Interview Prep',
    }
    
    recommendations['recommended_resources'] = [
        resources_map.get(skill.lower(), f'{skill} Official Docs')
        for skill in missing_skills[:3]
    ]
    
    # Calculate estimated hours (rough estimate)
    recommendations['estimated_hours_remaining'] = len(missing_skills) * 40
    
    return recommendations


def calculate_learning_velocity(progress_data):
    """
    Calculate learning velocity:
    - Tasks completed per week
    - Consistency score
    - Acceleration/deceleration
    """
    if not progress_data or len(progress_data) < 7:
        return {
            'velocity': 0,
            'consistency': 0,
            'trend': 'insufficient_data',
            'tasks_per_week': 0
        }
    
    completed_tasks = sum(1 for p in progress_data if p.get('completed'))
    days_active = len(progress_data)
    weeks_active = max(1, days_active / 7)
    
    return {
        'velocity': round(completed_tasks / weeks_active, 2),
        'consistency': round((completed_tasks / len(progress_data)) * 100, 1),
        'trend': 'accelerating' if completed_tasks > (len(progress_data) / 2) else 'steady',
        'tasks_per_week': round(completed_tasks / weeks_active, 1)
    }


def get_achievement_badges(user_data, progress_data):
    """
    Award achievement badges for milestones
    """
    badges = []
    completed_count = sum(1 for p in progress_data if p.get('completed'))
    
    # Calculate current streak (consecutive days up to most recent completed date)
    def _parse_date(d):
        import datetime
        if not d:
            return None
        if isinstance(d, datetime.date) or isinstance(d, datetime.datetime):
            return d.date() if isinstance(d, datetime.datetime) else d
        for key in ['date', 'completed_date']:
            if isinstance(d, dict) and key in d:
                try:
                    return datetime.datetime.fromisoformat(d[key]).date()
                except Exception:
                    pass
        return None

    completed_dates = []
    for p in progress_data:
        if p.get('completed'):
            d = _parse_date(p)
            if d:
                completed_dates.append(d)

    current_streak = 0
    if completed_dates:
        completed_dates = sorted(set(completed_dates))
        from datetime import timedelta
        today = completed_dates[-1]
        day = today
        while day in completed_dates:
            current_streak += 1
            day = day - timedelta(days=1)

    badge_thresholds = {
        'early_bird': {'condition': completed_count >= 7, 'emoji': '🌅', 'name': 'Early Bird'},
        'consistent_learner': {'condition': completed_count >= 30, 'emoji': '📚', 'name': 'Consistent Learner'},
        'momentum': {'condition': completed_count >= 50, 'emoji': '🚀', 'name': 'Momentum'},
        'master': {'condition': completed_count >= 100, 'emoji': '👑', 'name': 'Master'},
        'streak_7': {'condition': current_streak >= 7, 'emoji': '🔥', 'name': '7-Day Streak'},
    }
    
    for badge_id, badge_info in badge_thresholds.items():
        if badge_info['condition']:
            badges.append({
                'id': badge_id,
                'emoji': badge_info['emoji'],
                'name': badge_info['name'],
            })
    
    return badges


def generate_analytics_summary(user_id, plan_data, progress_data):
    """
    Generate analytics dashboard data
    """
    completed_tasks = sum(1 for p in progress_data if p.get('completed'))
    total_tasks = len(progress_data)
    completion_rate = (completed_tasks / total_tasks * 100) if total_tasks > 0 else 0
    
    # user_id may be a user_data dict in some callers; normalize
    if isinstance(user_id, dict):
        user_data = user_id
    else:
        user_data = {'skills': []}

    return {
        'total_tasks': total_tasks,
        'completed_tasks': completed_tasks,
        'completion_rate': round(completion_rate, 1),
        'remaining_tasks': total_tasks - completed_tasks,
        'estimated_days_left': max(0, (total_tasks - completed_tasks) / 1.5),  # Assume 1.5 tasks/day
        'velocity': calculate_learning_velocity(progress_data),
        'badges': get_achievement_badges(user_data, progress_data),
        'recommendations': get_learning_recommendations(
            user_data.get('skills', []),
            plan_data.get('goal', ''),
            progress_data
        )
    }
