from typing import List, Dict, Any
from datetime import datetime, timedelta


class SkillAssessor:
    """Assess user skills from resume and progress data."""

    def assess_user(self, user_id: int) -> Dict[str, Any]:
        """Assess user skills from resume and recent progress.
        
        Returns: dict with 'current_skills', 'skill_gaps', 'proficiency_estimate'
        """
        try:
            from models import db, User, Resume, Plan, DailyProgress
            
            user = User.query.get(user_id)
            if not user:
                return {'current_skills': [], 'skill_gaps': [], 'proficiency_estimate': 'unknown'}
            
            # Get latest resume
            resume = Resume.query.filter_by(user_id=user_id).order_by(Resume.uploaded_at.desc()).first()
            current_skills = resume.skills if resume else []
            experience_level = resume.experience_level if resume else 'beginner'
            
            # Get active plan and assess progress
            plan = Plan.query.filter_by(user_id=user_id, status='active').first()
            plan_goal = plan.goal if plan else 'Unknown'
            plan_skills = plan.technologies if plan else []
            
            # Calculate progress velocity (tasks completed in last 30 days)
            thirty_days_ago = datetime.utcnow() - timedelta(days=30)
            recent_progress = 0
            if plan:
                recent_progress = DailyProgress.query.filter(
                    DailyProgress.plan_id == plan.id,
                    DailyProgress.is_completed == True,
                    DailyProgress.completed_date >= thirty_days_ago
                ).count()
            
            # Assess skill gaps (what's in plan but not yet mastered)
            skill_gaps = [s for s in plan_skills if s.lower() not in [cs.lower() for cs in current_skills]]
            
            return {
                'current_skills': current_skills,
                'plan_skills': plan_skills,
                'skill_gaps': skill_gaps[:5],  # Top 5 gaps
                'proficiency_estimate': experience_level,
                'plan_goal': plan_goal,
                'recent_tasks_completed': recent_progress
            }
        except Exception as e:
            return {'current_skills': [], 'skill_gaps': [], 'proficiency_estimate': 'error', 'error': str(e)}
