"""Email notification service for daily reminders and tech updates"""
from flask_mail import Mail, Message
from flask import current_app, render_template_string
from datetime import datetime
import logging

mail = Mail()

logger = logging.getLogger(__name__)


def send_daily_reminder_email(user_email, user_name, plan_goal, today_task, duration_months=None):
    """Send daily learning reminder to user. Optionally include plan duration."""
    try:
        subject = f"🎯 Daily Learning Reminder - {plan_goal}"

        # Format duration if provided
        formatted_duration = None
        if duration_months is not None:
            try:
                m = int(duration_months)
                weeks = round(m * 4.345)
                years = m / 12
                years_str = f"{years:.2f}" if (years % 1) else f"{int(years)}"
                month_label = 'month' if m == 1 else 'months'
                formatted_duration = f"{m} {month_label} (≈{weeks} weeks, {years_str} years)"
            except Exception:
                formatted_duration = str(duration_months)

        duration_section = f"<p style=\"color:#666;\"><strong>Plan duration:</strong> {formatted_duration}</p>" if formatted_duration else ""

        html_body = f"""
        <html>
        <body style="font-family: Arial, sans-serif; line-height: 1.6; color: #333;">
            <div style="max-width: 600px; margin: 0 auto; background: linear-gradient(135deg, #667eea 0%, #764ba2 100%); padding: 20px; border-radius: 10px;">
                <h2 style="color: white; margin: 0;">Good morning, {user_name}! 👋</h2>
            </div>
            
            <div style="max-width: 600px; margin: 20px auto; padding: 20px; background: #f5f7fa; border-radius: 10px;">
                <h3 style="color: #667eea;">Today's Task</h3>
                <p style="font-size: 16px; padding: 15px; background: white; border-left: 4px solid #667eea; border-radius: 4px;">
                    <strong>{today_task}</strong>
                </p>
                
                <p style="color: #666; margin-top: 20px;">
                    You're on your journey to become a <strong>{plan_goal}</strong>. Keep up the momentum! 🚀
                </p>
                {duration_section}
                
                <a href="http://careernavigator.app/dashboard" style="display: inline-block; background: linear-gradient(135deg, #667eea, #764ba2); color: white; padding: 12px 30px; text-decoration: none; border-radius: 6px; margin-top: 15px; font-weight: bold;">
                    View Your Plan
                </a>
            </div>
            
            <div style="max-width: 600px; margin: 20px auto; text-align: center; color: #999; font-size: 12px;">
                <p>Career Navigator - Your AI-powered learning companion</p>
            </div>
        </body>
        </html>
        """

        msg = Message(
            subject=subject,
            recipients=[user_email],
            html=html_body,
            sender=current_app.config['MAIL_DEFAULT_SENDER']
        )
        mail.send(msg)
        logger.info(f"Daily reminder sent to {user_email}")
        return True
    except Exception as e:
        logger.error(f"Failed to send daily reminder to {user_email}: {str(e)}")
        return False


def send_tech_update_alert_email(user_email, user_name, plan_goal, new_technologies):
    """Alert user about new industry-standard technologies"""
    try:
        subject = f"⚡ New Tech Alert for {plan_goal} - Update Your Plan!"
        
        tech_list = "".join([
            f"<li><strong>{tech['name']}</strong> ({tech.get('category', 'Other')}) - Relevance: {tech.get('relevance', 'Unknown')}%</li>"
            for tech in new_technologies
        ])
        
        html_body = f"""
        <html>
        <body style="font-family: Arial, sans-serif; line-height: 1.6; color: #333;">
            <div style="max-width: 600px; margin: 0 auto; background: linear-gradient(135deg, #ff6b6b 0%, #ff8c42 100%); padding: 20px; border-radius: 10px;">
                <h2 style="color: white; margin: 0;">⚡ New Technologies Emerged!</h2>
            </div>
            
            <div style="max-width: 600px; margin: 20px auto; padding: 20px; background: #f5f7fa; border-radius: 10px;">
                <p>Hi {user_name},</p>
                
                <p>We detected new industry-standard technologies relevant to your goal of becoming a <strong>{plan_goal}</strong>:</p>
                
                <ul style="background: white; padding: 20px; border-radius: 6px; border-left: 4px solid #ff8c42;">
                    {tech_list}
                </ul>
                
                <p style="color: #666;">
                    Your learning plan can be updated to include these technologies. This will help you stay ahead of industry trends!
                </p>
                
                <a href="http://careernavigator.app/dashboard" style="display: inline-block; background: linear-gradient(135deg, #ff6b6b, #ff8c42); color: white; padding: 12px 30px; text-decoration: none; border-radius: 6px; margin-top: 15px; font-weight: bold;">
                    Review & Update Plan
                </a>
            </div>
            
            <div style="max-width: 600px; margin: 20px auto; text-align: center; color: #999; font-size: 12px;">
                <p>Career Navigator - Adaptive Learning for AI Engineers</p>
            </div>
        </body>
        </html>
        """
        
        msg = Message(
            subject=subject,
            recipients=[user_email],
            html=html_body,
            sender=current_app.config['MAIL_DEFAULT_SENDER']
        )
        mail.send(msg)
        logger.info(f"Tech update alert sent to {user_email}")
        return True
    except Exception as e:
        logger.error(f"Failed to send tech alert to {user_email}: {str(e)}")
        return False


def send_plan_update_confirmation_email(user_email, user_name, plan_goal, changes_summary):
    """Confirm that plan was updated with new technologies"""
    try:
        subject = f"✅ Your {plan_goal} Plan Has Been Updated"
        
        html_body = f"""
        <html>
        <body style="font-family: Arial, sans-serif; line-height: 1.6; color: #333;">
            <div style="max-width: 600px; margin: 0 auto; background: linear-gradient(135deg, #4ade80 0%, #22c55e 100%); padding: 20px; border-radius: 10px;">
                <h2 style="color: white; margin: 0;">✅ Plan Updated Successfully!</h2>
            </div>
            
            <div style="max-width: 600px; margin: 20px auto; padding: 20px; background: #f5f7fa; border-radius: 10px;">
                <p>Hi {user_name},</p>
                
                <p>Your learning plan has been updated with the latest industry standards!</p>
                
                <div style="background: white; padding: 15px; border-radius: 6px; border-left: 4px solid #4ade80; margin: 15px 0;">
                    <p><strong>Changes made:</strong></p>
                    <ul>
                        <li>Added {changes_summary.get('added_count', 0)} new technologies</li>
                        <li>Removed {changes_summary.get('removed_count', 0)} outdated technologies</li>
                        <li>Plan version: {changes_summary.get('version', 1)}</li>
                    </ul>
                </div>
                
                <a href="http://careernavigator.app/dashboard" style="display: inline-block; background: linear-gradient(135deg, #4ade80, #22c55e); color: white; padding: 12px 30px; text-decoration: none; border-radius: 6px; margin-top: 15px; font-weight: bold;">
                    View Updated Plan
                </a>
            </div>
        </body>
        </html>
        """
        
        msg = Message(
            subject=subject,
            recipients=[user_email],
            html=html_body,
            sender=current_app.config['MAIL_DEFAULT_SENDER']
        )
        mail.send(msg)
        logger.info(f"Plan update confirmation sent to {user_email}")
        return True
    except Exception as e:
        logger.error(f"Failed to send plan update confirmation to {user_email}: {str(e)}")
        return False
