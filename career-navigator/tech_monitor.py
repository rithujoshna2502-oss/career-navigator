import requests
from datetime import datetime, timedelta
import re

# Trending technologies database with relevance scores
TRENDING_TECHNOLOGIES = {
    # LLMs & AI
    'GPT-4': {'category': 'LLM', 'relevance': 95, 'professions': ['AI Engineer', 'Machine Learning Engineer']},
    'Claude 3': {'category': 'LLM', 'relevance': 92, 'professions': ['AI Engineer', 'Machine Learning Engineer']},
    'Gemini': {'category': 'LLM', 'relevance': 90, 'professions': ['AI Engineer', 'Machine Learning Engineer']},
    'Llama 2': {'category': 'LLM', 'relevance': 88, 'professions': ['AI Engineer', 'Machine Learning Engineer']},
    'Mistral': {'category': 'LLM', 'relevance': 85, 'professions': ['AI Engineer', 'Machine Learning Engineer']},
    
    # AI/ML Frameworks
    'Hugging Face': {'category': 'AI Framework', 'relevance': 90, 'professions': ['AI Engineer', 'Machine Learning Engineer', 'Data Scientist']},
    'TensorFlow 2.14': {'category': 'ML Framework', 'relevance': 85, 'professions': ['Machine Learning Engineer', 'AI Engineer']},
    'PyTorch 2.0': {'category': 'ML Framework', 'relevance': 92, 'professions': ['Machine Learning Engineer', 'AI Engineer']},
    'JAX': {'category': 'ML Framework', 'relevance': 80, 'professions': ['Machine Learning Engineer', 'Data Scientist']},
    
    # AI Tools & Platforms
    'Prompt Engineering': {'category': 'AI Skill', 'relevance': 95, 'professions': ['AI Engineer', 'Data Scientist']},
    'RAG Systems': {'category': 'AI Technique', 'relevance': 90, 'professions': ['AI Engineer']},
    'Fine-tuning': {'category': 'AI Skill', 'relevance': 88, 'professions': ['AI Engineer', 'Machine Learning Engineer']},
    'CrewAI': {'category': 'AI Framework', 'relevance': 85, 'professions': ['AI Engineer']},
    'LangChain': {'category': 'AI Framework', 'relevance': 88, 'professions': ['AI Engineer']},
    
    # Frontend
    'React 18': {'category': 'Frontend', 'relevance': 90, 'professions': ['Web Developer', 'Frontend Developer']},
    'Vue 3': {'category': 'Frontend', 'relevance': 82, 'professions': ['Web Developer', 'Frontend Developer']},
    'Next.js 14': {'category': 'Frontend', 'relevance': 92, 'professions': ['Web Developer', 'Frontend Developer', 'Full Stack Developer']},
    'Svelte': {'category': 'Frontend', 'relevance': 80, 'professions': ['Frontend Developer', 'Web Developer']},
    'Astro': {'category': 'Frontend', 'relevance': 78, 'professions': ['Frontend Developer', 'Web Developer']},
    'Tailwind CSS': {'category': 'CSS Framework', 'relevance': 88, 'professions': ['Frontend Developer', 'Web Developer', 'UI/UX Developer']},
    
    # Backend
    'FastAPI': {'category': 'Backend', 'relevance': 85, 'professions': ['Backend Engineer', 'Web Developer', 'Software Engineer']},
    'Django 5': {'category': 'Backend', 'relevance': 80, 'professions': ['Backend Engineer', 'Web Developer', 'Software Engineer']},
    'Rust': {'category': 'Language', 'relevance': 85, 'professions': ['Systems Engineer', 'Backend Engineer', 'Software Engineer']},
    'Go 1.21': {'category': 'Language', 'relevance': 82, 'professions': ['Backend Engineer', 'Cloud Engineer', 'DevOps Engineer']},
    
    # Cloud & DevOps
    'Kubernetes 1.28': {'category': 'Orchestration', 'relevance': 90, 'professions': ['DevOps Engineer', 'Cloud Engineer']},
    'Docker': {'category': 'Containerization', 'relevance': 92, 'professions': ['DevOps Engineer', 'Cloud Engineer', 'Backend Engineer']},
    'AWS': {'category': 'Cloud', 'relevance': 95, 'professions': ['Cloud Engineer', 'DevOps Engineer', 'Backend Engineer']},
    'Azure': {'category': 'Cloud', 'relevance': 90, 'professions': ['Cloud Engineer', 'DevOps Engineer']},
    'Google Cloud': {'category': 'Cloud', 'relevance': 88, 'professions': ['Cloud Engineer', 'DevOps Engineer', 'Data Engineer']},
    'Terraform': {'category': 'IaC', 'relevance': 88, 'professions': ['DevOps Engineer', 'Cloud Engineer']},
    'Ansible': {'category': 'IaC', 'relevance': 82, 'professions': ['DevOps Engineer', 'Systems Administrator']},
    
    # Data & Analytics
    'Apache Spark': {'category': 'Big Data', 'relevance': 85, 'professions': ['Data Engineer', 'Data Scientist']},
    'Dbt': {'category': 'Data Tools', 'relevance': 80, 'professions': ['Data Engineer', 'Analytics Engineer']},
    'Postgres 16': {'category': 'Database', 'relevance': 85, 'professions': ['Database Administrator', 'Data Engineer', 'Backend Engineer']},
    'MongoDB': {'category': 'Database', 'relevance': 82, 'professions': ['Backend Engineer', 'Database Administrator', 'Data Engineer']},
    
    # Mobile
    'Flutter': {'category': 'Mobile', 'relevance': 85, 'professions': ['Mobile Developer']},
    'React Native': {'category': 'Mobile', 'relevance': 88, 'professions': ['Mobile Developer']},
    'Swift': {'category': 'Language', 'relevance': 85, 'professions': ['iOS Developer', 'Mobile Developer']},
    'Kotlin': {'category': 'Language', 'relevance': 85, 'professions': ['Android Developer', 'Mobile Developer']},
    
    # Other Trending
    'TypeScript': {'category': 'Language', 'relevance': 90, 'professions': ['Web Developer', 'Frontend Developer', 'Backend Engineer']},
    'GraphQL': {'category': 'API', 'relevance': 85, 'professions': ['Backend Engineer', 'Web Developer', 'Full Stack Developer']},
    'WebAssembly': {'category': 'Web', 'relevance': 78, 'professions': ['Frontend Developer', 'Software Engineer']},
    'Blockchain': {'category': 'Emerging', 'relevance': 75, 'professions': ['Blockchain Developer', 'Software Engineer']},
    'Web3': {'category': 'Emerging', 'relevance': 72, 'professions': ['Blockchain Developer']},
}


def get_trending_technologies(profession=None, min_relevance=75):
    """
    Get trending technologies filtered by profession and minimum relevance score
    
    Args:
        profession: str - Filter by profession (optional)
        min_relevance: int - Minimum relevance score (0-100)
    
    Returns:
        list - Sorted list of trending technologies
    """
    
    trending = []
    for tech, data in TRENDING_TECHNOLOGIES.items():
        if data['relevance'] >= min_relevance:
            if profession is None or profession.lower() in [p.lower() for p in data.get('professions', [])]:
                trending.append({
                    'name': tech,
                    'category': data['category'],
                    'relevance': data['relevance'],
                    'professions': data.get('professions', [])
                })
    
    # Sort by relevance score
    trending.sort(key=lambda x: x['relevance'], reverse=True)
    return trending


def detect_new_technologies(current_skills, profession, threshold=80):
    """
    Detect new technologies that emerged for a profession
    
    Args:
        current_skills: list - Skills currently in the user's plan
        profession: str - User's target profession
        threshold: int - Relevance threshold for "new" tech
    
    Returns:
        dict - Contains new_technologies, deprecated_technologies, recommendations
    """
    
    trending = get_trending_technologies(profession, min_relevance=threshold)
    
    # Skills in the plan
    current_skills_lower = [skill.lower() for skill in current_skills]
    
    new_technologies = []
    for tech_data in trending:
        tech_lower = tech_data['name'].lower()
        # Check if technology is not in current skills
        if not any(skill in tech_lower or tech_lower in skill for skill in current_skills_lower):
            new_technologies.append(tech_data)
    
    # Sort by relevance
    new_technologies.sort(key=lambda x: x['relevance'], reverse=True)
    
    return {
        'new_technologies': new_technologies[:5],  # Top 5 new tech
        'all_trending': trending,
        'total_new': len(new_technologies),
        'updated_at': datetime.now().isoformat()
    }


def should_update_plan(plan_technologies, profession, days_since_creation=30):
    """
    Determine if a plan should be updated based on new tech emergence
    
    Args:
        plan_technologies: list - Technologies in current plan
        profession: str - User's target profession
        days_since_creation: int - Days since plan was created
    
    Returns:
        dict - Update recommendation with details
    """
    
    # Only check for updates after at least 7 days
    if days_since_creation < 7:
        return {'should_update': False, 'reason': 'Plan too new to check for updates'}
    
    # Get new technologies
    new_tech_data = detect_new_technologies(plan_technologies, profession, threshold=85)
    
    if len(new_tech_data['new_technologies']) >= 2:
        return {
            'should_update': True,
            'reason': f"{len(new_tech_data['new_technologies'])} new high-relevance technologies detected",
            'new_technologies': new_tech_data['new_technologies'],
            'urgency': 'high' if len(new_tech_data['new_technologies']) >= 3 else 'medium'
        }
    else:
        return {
            'should_update': False,
            'reason': 'No significant new technologies detected',
            'new_technologies': new_tech_data['new_technologies']
        }


def generate_tech_recommendations(profession, current_technologies):
    """
    Generate personalized tech recommendations for a profession
    
    Args:
        profession: str - Target profession
        current_technologies: list - Technologies already in plan
    
    Returns:
        dict - Recommendations with details
    """
    
    trending = get_trending_technologies(profession, min_relevance=75)
    
    recommendations = {
        'must_learn': [],      # Core technologies (85+ relevance)
        'good_to_learn': [],   # Secondary technologies (75-84 relevance)
        'emerging': []         # Emerging tech (new but rising)
    }
    
    current_lower = [t.lower() for t in current_technologies]
    
    for tech_data in trending:
        tech_lower = tech_data['name'].lower()
        
        # Skip if already in plan
        if any(skill in tech_lower or tech_lower in skill for skill in current_lower):
            continue
        
        if tech_data['relevance'] >= 85:
            recommendations['must_learn'].append(tech_data)
        elif tech_data['relevance'] >= 75:
            recommendations['good_to_learn'].append(tech_data)
        else:
            recommendations['emerging'].append(tech_data)
    
    return recommendations


def get_technology_update_summary(old_technologies, new_technologies):
    """
    Generate a summary of what changed in the technology stack
    
    Args:
        old_technologies: list - Previous technology list
        new_technologies: list - Updated technology list
    
    Returns:
        dict - Summary of changes
    """
    
    old_set = set([t.lower() for t in old_technologies])
    new_set = set([t.lower() for t in new_technologies])
    
    added = new_set - old_set
    removed = old_set - new_set
    
    return {
        'added_technologies': list(added),
        'removed_technologies': list(removed),
        'added_count': len(added),
        'removed_count': len(removed),
        'timestamp': datetime.now().isoformat()
    }
