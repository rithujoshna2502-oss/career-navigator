"""Background task scheduler for agent orchestrator.

Runs agent tasks periodically (tech monitoring, plan updates).
In production, replace with Celery + Redis.
"""
import threading
import time
from datetime import datetime, timedelta
import logging

logger = logging.getLogger(__name__)


class TaskScheduler:
    """Simple scheduler to run agent background tasks."""

    def __init__(self, app=None, interval=3600):
        self.app = app
        self.interval = interval
        self._thread = None
        self._stop_event = threading.Event()

    def start(self):
        """Start the background task scheduler."""
        if self._thread and self._thread.is_alive():
            return
        self._stop_event.clear()
        self._thread = threading.Thread(target=self._run, daemon=True)
        self._thread.start()
        logger.info(f"Task scheduler started with interval={self.interval}s")

    def stop(self):
        """Stop the background task scheduler."""
        self._stop_event.set()
        if self._thread:
            self._thread.join(timeout=5)
        logger.info("Task scheduler stopped")

    def _run(self):
        """Main scheduler loop."""
        while not self._stop_event.is_set():
            try:
                self._check_and_update_plans()
                time.sleep(0.5)
            except Exception as e:
                logger.error(f"Scheduler error: {e}")
            self._stop_event.wait(self.interval)

    def _check_and_update_plans(self):
        """Check for plans that need tech updates."""
        try:
            if not self.app:
                return

            with self.app.app_context():
                from models import db, Plan
                from tech_monitor import should_update_plan
                from datetime import datetime

                # Find plans that haven't been checked in 7+ days
                week_ago = datetime.utcnow() - timedelta(days=7)
                plans = Plan.query.filter(
                    Plan.status == 'active',
                    (Plan.last_updated < week_ago) | (Plan.last_updated.is_(None))
                ).all()

                for plan in plans:
                    days_old = (datetime.utcnow() - plan.created_at).days
                    update_needed = should_update_plan(
                        plan.technologies or [],
                        plan.goal,
                        days_old
                    )

                    if update_needed.get('should_update'):
                        plan.status = 'update_available'
                        plan.last_updated = datetime.utcnow()
                        db.session.commit()
                        logger.info(f"Plan {plan.id} marked for update review")

        except Exception as e:
            logger.error(f"Error checking plans: {e}")
