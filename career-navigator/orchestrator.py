import threading
import time
from typing import Any, Dict

from .skill_assessor import SkillAssessor
from .recommender import Recommender
from .monitor import Monitor


class Orchestrator:
    """Orchestrator to coordinate agents and manage real-time skill evolution.

    - Runs a periodic loop to check for tech trends and suggest updates
    - Provides API to get suggestions and apply updates
    """

    def __init__(self, poll_interval: int = 60):
        self.poll_interval = poll_interval
        self._thread = None
        self._stop_event = threading.Event()

        self.skill_assessor = SkillAssessor()
        self.recommender = Recommender()
        self.monitor = Monitor()

    def _run_loop(self):
        while not self._stop_event.is_set():
            try:
                # Check for tech trends periodically
                trends = self.monitor.check_trends()
                # Real-time logic: could fetch active users and update suggestions
                time.sleep(0.1)
            except Exception:
                pass
            self._stop_event.wait(self.poll_interval)

    def start(self):
        """Start the orchestrator background thread."""
        if self._thread and self._thread.is_alive():
            return
        self._stop_event.clear()
        self._thread = threading.Thread(target=self._run_loop, daemon=True)
        self._thread.start()

    def stop(self):
        """Stop the orchestrator background thread."""
        self._stop_event.set()
        if self._thread:
            self._thread.join(timeout=5)

    def get_suggestions_for_user(self, user_id: int) -> Dict[str, Any]:
        """Get personalized learning suggestions for a user.
        
        Orchestrates: Skill Assessment -> Recommendations
        """
        try:
            # Assess current skills
            assessment = self.skill_assessor.assess_user(user_id)
            
            # Generate recommendations
            recommendations = self.recommender.recommend_for_user(user_id, assessment)
            
            return {
                'assessment': assessment,
                'recommendations': recommendations
            }
        except Exception as e:
            return {'error': str(e)}

    def apply_update(self, user_id: int, update_payload: Dict[str, Any]) -> Dict[str, Any]:
        """Apply an update to the user's plan.
        
        In production, this would create a new plan version and notify the user.
        """
        try:
            from models import db, Plan
            
            # For now, just log the intent
            # In production: create new plan version, update DB, send email
            plan_id = update_payload.get('plan_id')
            new_technologies = update_payload.get('new_technologies', [])
            
            if plan_id:
                plan = Plan.query.get(plan_id)
                if plan and plan.user_id == user_id:
                    # Mark plan as needing update review
                    plan.status = 'update_pending'
                    plan.version += 1
                    plan.last_updated = db.func.now()
                    db.session.commit()
                    
                    return {
                        'applied': True,
                        'plan_id': plan_id,
                        'new_version': plan.version,
                        'new_technologies_count': len(new_technologies)
                    }
            
            return {'applied': False, 'reason': 'Plan not found'}
        except Exception as e:
            return {'error': str(e)}
