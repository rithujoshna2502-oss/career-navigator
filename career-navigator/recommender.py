from typing import Any, Dict, List
import sys
import os
sys.path.insert(0, os.path.dirname(os.path.dirname(__file__)))

from tech_monitor import get_trending_technologies, detect_new_technologies, generate_tech_recommendations


class Recommender:
    """Produce incremental plan updates based on skill gaps."""

    def recommend_for_user(self, user_id: int, assessment: Dict[str, Any]) -> Dict[str, Any]:
        """Generate prioritized recommendations based on skill assessment.
        
        Args:
            user_id: User ID
            assessment: dict from SkillAssessor.assess_user()
        
        Returns: dict with prioritized learning recommendations
        """
        try:
            from models import Plan
            
            plan_goal = assessment.get('plan_goal', 'Unknown')
            current_skills = assessment.get('current_skills', [])
            skill_gaps = assessment.get('skill_gaps', [])
            plan_skills = assessment.get('plan_skills', [])
            
            # Get trending tech for the profession
            trending = get_trending_technologies(plan_goal, min_relevance=80)
            
            # Detect new technologies not in current plan
            new_tech = detect_new_technologies(plan_skills, plan_goal, threshold=80)
            
            # Generate detailed recommendations
            recs = generate_tech_recommendations(plan_goal, plan_skills)
            
            return {
                'skill_gaps': skill_gaps,
                'must_learn': recs.get('must_learn', [])[:3],
                'good_to_learn': recs.get('good_to_learn', [])[:3],
                'new_technologies': new_tech.get('new_technologies', [])[:3],
                'total_new_detected': new_tech.get('total_new', 0),
                'recommend_plan_update': new_tech.get('total_new', 0) >= 2
            }
        except Exception as e:
            return {
                'skill_gaps': assessment.get('skill_gaps', []),
                'must_learn': [],
                'good_to_learn': [],
                'error': str(e)
            }
