from datetime import datetime, timedelta
import json

# Profession-specific learning paths
PROFESSION_PATHS = {
    'software engineer': {
        'duration_months': 6,
        'skills_required': ['Python', 'JavaScript', 'HTML', 'CSS', 'SQL', 'Flask', 'React'],
        'daily_distribution': {
            'weeks_1_2': {'focus': 'Python Fundamentals', 'daily_hours': 3},
            'weeks_3_4': {'focus': 'Web Development Basics (HTML/CSS)', 'daily_hours': 3},
            'weeks_5_8': {'focus': 'JavaScript & Frontend', 'daily_hours': 4},
            'weeks_9_12': {'focus': 'Backend & Databases', 'daily_hours': 4},
            'weeks_13_20': {'focus': 'Full Stack Projects', 'daily_hours': 5},
            'weeks_21_26': {'focus': 'Portfolio & Interview Prep', 'daily_hours': 4}
        },
        'milestones': [
            {'week': 2, 'milestone': 'Complete Python basics (loops, functions, OOP)'},
            {'week': 4, 'milestone': 'Build first static website with HTML/CSS'},
            {'week': 8, 'milestone': 'Master JavaScript and start with React'},
            {'week': 12, 'milestone': 'Learn SQL and build backend with Flask'},
            {'week': 16, 'milestone': 'Complete 2-3 full stack mini-projects'},
            {'week': 20, 'milestone': 'Deploy projects on GitHub and cloud'},
            {'week': 26, 'milestone': 'Finish portfolio and practice interviews'}
        ]
    },
    'backend engineer': {
        'duration_months': 6,
        'skills_required': ['Python/Java', 'SQL', 'API Design', 'Database Design', 'Docker', 'Microservices'],
        'daily_distribution': {
            'weeks_1_2': {'focus': 'Server-side Fundamentals', 'daily_hours': 3},
            'weeks_3_4': {'focus': 'Database Design & SQL', 'daily_hours': 3},
            'weeks_5_8': {'focus': 'API Development', 'daily_hours': 4},
            'weeks_9_12': {'focus': 'Authentication & Security', 'daily_hours': 4},
            'weeks_13_20': {'focus': 'Microservices & Scaling', 'daily_hours': 5},
            'weeks_21_26': {'focus': 'DevOps & Deployment', 'daily_hours': 4}
        },
        'milestones': [
            {'week': 2, 'milestone': 'Master server-side language (Python/Java)'},
            {'week': 4, 'milestone': 'Design and manage databases'},
            {'week': 8, 'milestone': 'Build and deploy RESTful APIs'},
            {'week': 12, 'milestone': 'Implement authentication & authorization'},
            {'week': 16, 'milestone': 'Design microservices architecture'},
            {'week': 20, 'milestone': 'Deploy with Docker & orchestration'},
            {'week': 26, 'milestone': 'Build production-ready backend systems'}
        ]
    },
    'frontend developer': {
        'duration_months': 6,
        'skills_required': ['HTML', 'CSS', 'JavaScript', 'React/Vue', 'UI Design', 'Responsive Design'],
        'daily_distribution': {
            'weeks_1_2': {'focus': 'HTML & CSS Fundamentals', 'daily_hours': 3},
            'weeks_3_4': {'focus': 'JavaScript Mastery', 'daily_hours': 3},
            'weeks_5_8': {'focus': 'React/Vue Framework', 'daily_hours': 4},
            'weeks_9_12': {'focus': 'State Management & APIs', 'daily_hours': 4},
            'weeks_13_20': {'focus': 'Performance & Optimization', 'daily_hours': 5},
            'weeks_21_26': {'focus': 'UI/UX & Portfolio Projects', 'daily_hours': 4}
        },
        'milestones': [
            {'week': 2, 'milestone': 'Build semantic HTML & modern CSS'},
            {'week': 4, 'milestone': 'Master vanilla JavaScript'},
            {'week': 8, 'milestone': 'Build interactive components with React'},
            {'week': 12, 'milestone': 'Manage state with Redux/Context'},
            {'week': 16, 'milestone': 'Optimize performance & bundle size'},
            {'week': 20, 'milestone': 'Design beautiful, responsive UIs'},
            {'week': 26, 'milestone': 'Deploy full-stack applications'}
        ]
    },
    'web developer': {
        'duration_months': 6,
        'skills_required': ['HTML', 'CSS', 'JavaScript', 'Backend Language', 'SQL', 'Deployment'],
        'daily_distribution': {
            'weeks_1_2': {'focus': 'Web Fundamentals', 'daily_hours': 3},
            'weeks_3_4': {'focus': 'Frontend Basics', 'daily_hours': 3},
            'weeks_5_8': {'focus': 'JavaScript & Interactivity', 'daily_hours': 4},
            'weeks_9_12': {'focus': 'Backend & Databases', 'daily_hours': 4},
            'weeks_13_20': {'focus': 'Full Stack Integration', 'daily_hours': 5},
            'weeks_21_26': {'focus': 'Projects & Deployment', 'daily_hours': 4}
        },
        'milestones': [
            {'week': 2, 'milestone': 'Complete web fundamentals'},
            {'week': 4, 'milestone': 'Build responsive websites'},
            {'week': 8, 'milestone': 'Make interactive web applications'},
            {'week': 12, 'milestone': 'Build backend services'},
            {'week': 16, 'milestone': 'Integrate frontend & backend'},
            {'week': 20, 'milestone': 'Deploy to production'},
            {'week': 26, 'milestone': 'Complete full-stack projects'}
        ]
    },
    'mobile developer': {
        'duration_months': 6,
        'skills_required': ['React Native/Flutter', 'Mobile UI', 'APIs', 'State Management', 'Testing'],
        'daily_distribution': {
            'weeks_1_2': {'focus': 'Mobile Fundamentals', 'daily_hours': 3},
            'weeks_3_4': {'focus': 'React Native Basics', 'daily_hours': 3},
            'weeks_5_8': {'focus': 'Mobile UI & UX', 'daily_hours': 4},
            'weeks_9_12': {'focus': 'API Integration', 'daily_hours': 4},
            'weeks_13_20': {'focus': 'Advanced Features', 'daily_hours': 5},
            'weeks_21_26': {'focus': 'Testing & Deployment', 'daily_hours': 4}
        },
        'milestones': [
            {'week': 2, 'milestone': 'Learn mobile development basics'},
            {'week': 4, 'milestone': 'Build first mobile app'},
            {'week': 8, 'milestone': 'Master mobile UI components'},
            {'week': 12, 'milestone': 'Integrate backend APIs'},
            {'week': 16, 'milestone': 'Add complex features & state management'},
            {'week': 20, 'milestone': 'Test and optimize performance'},
            {'week': 26, 'milestone': 'Deploy apps to stores'}
        ]
    },
    'data scientist': {
        'duration_months': 6,
        'skills_required': ['Python', 'Pandas', 'NumPy', 'Machine Learning', 'SQL', 'Statistics'],
        'daily_distribution': {
            'weeks_1_2': {'focus': 'Python & Data Manipulation', 'daily_hours': 3},
            'weeks_3_4': {'focus': 'Statistics & Probability', 'daily_hours': 3},
            'weeks_5_8': {'focus': 'Pandas & Data Analysis', 'daily_hours': 4},
            'weeks_9_12': {'focus': 'Machine Learning Algorithms', 'daily_hours': 4},
            'weeks_13_20': {'focus': 'Real-world Projects & Kaggle', 'daily_hours': 5},
            'weeks_21_26': {'focus': 'Portfolio & Interview Prep', 'daily_hours': 4}
        },
        'milestones': [
            {'week': 2, 'milestone': 'Master Python basics and NumPy/Pandas'},
            {'week': 4, 'milestone': 'Understand statistics and probability'},
            {'week': 8, 'milestone': 'Complete exploratory data analysis projects'},
            {'week': 12, 'milestone': 'Master supervised and unsupervised learning'},
            {'week': 16, 'milestone': 'Complete 3-4 end-to-end ML projects'},
            {'week': 20, 'milestone': 'Top 500 on Kaggle competitions'},
            {'week': 26, 'milestone': 'Finish portfolio and case studies'}
        ]
    },
    'ai engineer': {
        'duration_months': 6,
        'skills_required': ['Python', 'PyTorch', 'Transformers', 'LLMs', 'Prompt Engineering'],
        'daily_distribution': {
            'weeks_1_2': {'focus': 'Python & Deep Learning Basics', 'daily_hours': 3},
            'weeks_3_4': {'focus': 'Neural Networks & PyTorch', 'daily_hours': 3},
            'weeks_5_8': {'focus': 'Transformers & NLP', 'daily_hours': 4},
            'weeks_9_12': {'focus': 'LLMs & Fine-tuning', 'daily_hours': 4},
            'weeks_13_20': {'focus': 'Prompt Engineering & Deployment', 'daily_hours': 5},
            'weeks_21_26': {'focus': 'AI Projects & Advanced Topics', 'daily_hours': 4}
        },
        'milestones': [
            {'week': 2, 'milestone': 'Deep learning fundamentals with PyTorch'},
            {'week': 4, 'milestone': 'Build and train neural networks'},
            {'week': 8, 'milestone': 'Understand transformers and attention'},
            {'week': 12, 'milestone': 'Fine-tune LLMs for specific tasks'},
            {'week': 16, 'milestone': 'Create RAG systems and AI applications'},
            {'week': 20, 'milestone': 'Deploy models with CrewAI or similar'},
            {'week': 26, 'milestone': 'Finish advanced AI projects'}
        ]
    },
    'machine learning engineer': {
        'duration_months': 6,
        'skills_required': ['Python', 'Scikit-learn', 'TensorFlow', 'Model Deployment', 'MLOps'],
        'daily_distribution': {
            'weeks_1_2': {'focus': 'Math Foundations', 'daily_hours': 3},
            'weeks_3_4': {'focus': 'ML Algorithms', 'daily_hours': 3},
            'weeks_5_8': {'focus': 'Deep Learning', 'daily_hours': 4},
            'weeks_9_12': {'focus': 'Model Optimization', 'daily_hours': 4},
            'weeks_13_20': {'focus': 'Production ML Systems', 'daily_hours': 5},
            'weeks_21_26': {'focus': 'MLOps & Scaling', 'daily_hours': 4}
        },
        'milestones': [
            {'week': 2, 'milestone': 'Understand linear algebra & statistics'},
            {'week': 4, 'milestone': 'Master supervised learning algorithms'},
            {'week': 8, 'milestone': 'Build neural networks'},
            {'week': 12, 'milestone': 'Optimize and tune models'},
            {'week': 16, 'milestone': 'Deploy ML models in production'},
            {'week': 20, 'milestone': 'Monitor and maintain models'},
            {'week': 26, 'milestone': 'Build end-to-end ML pipelines'}
        ]
    },
    'cloud engineer': {
        'duration_months': 6,
        'skills_required': ['AWS', 'Azure', 'Docker', 'Kubernetes', 'Linux', 'Terraform'],
        'daily_distribution': {
            'weeks_1_2': {'focus': 'Linux & Networking Basics', 'daily_hours': 3},
            'weeks_3_4': {'focus': 'Cloud Platform Fundamentals', 'daily_hours': 3},
            'weeks_5_8': {'focus': 'Docker & Containerization', 'daily_hours': 4},
            'weeks_9_12': {'focus': 'Kubernetes & Orchestration', 'daily_hours': 4},
            'weeks_13_20': {'focus': 'Infrastructure as Code', 'daily_hours': 5},
            'weeks_21_26': {'focus': 'Cloud Certifications & Projects', 'daily_hours': 4}
        },
        'milestones': [
            {'week': 2, 'milestone': 'Linux administration and networking basics'},
            {'week': 4, 'milestone': 'Complete Cloud Platform certification prep'},
            {'week': 8, 'milestone': 'Master Docker containerization'},
            {'week': 12, 'milestone': 'Learn Kubernetes for production'},
            {'week': 16, 'milestone': 'Implement Infrastructure as Code with Terraform'},
            {'week': 20, 'milestone': 'Deploy multi-tier applications'},
            {'week': 26, 'milestone': 'Complete cloud certification exams'}
        ]
    },
    'devops engineer': {
        'duration_months': 6,
        'skills_required': ['Linux', 'Docker', 'Kubernetes', 'CI/CD', 'Terraform', 'Monitoring'],
        'daily_distribution': {
            'weeks_1_2': {'focus': 'Linux & Scripting', 'daily_hours': 3},
            'weeks_3_4': {'focus': 'Git & Version Control', 'daily_hours': 3},
            'weeks_5_8': {'focus': 'Docker & Containerization', 'daily_hours': 4},
            'weeks_9_12': {'focus': 'Kubernetes & Orchestration', 'daily_hours': 4},
            'weeks_13_20': {'focus': 'CI/CD Pipelines', 'daily_hours': 5},
            'weeks_21_26': {'focus': 'IaC & Monitoring', 'daily_hours': 4}
        },
        'milestones': [
            {'week': 2, 'milestone': 'Master Linux and shell scripting'},
            {'week': 4, 'milestone': 'Learn Git and version control'},
            {'week': 8, 'milestone': 'Master Docker for containerization'},
            {'week': 12, 'milestone': 'Implement Kubernetes clusters'},
            {'week': 16, 'milestone': 'Build CI/CD pipelines'},
            {'week': 20, 'milestone': 'Implement Infrastructure as Code'},
            {'week': 26, 'milestone': 'Set up monitoring and logging'}
        ]
    },
    'security engineer': {
        'duration_months': 6,
        'skills_required': ['Networking', 'Cryptography', 'Penetration Testing', 'Security Tools', 'Compliance'],
        'daily_distribution': {
            'weeks_1_2': {'focus': 'Networking Fundamentals', 'daily_hours': 3},
            'weeks_3_4': {'focus': 'Security Basics', 'daily_hours': 3},
            'weeks_5_8': {'focus': 'Cryptography & Encryption', 'daily_hours': 4},
            'weeks_9_12': {'focus': 'Penetration Testing', 'daily_hours': 4},
            'weeks_13_20': {'focus': 'Security Tools & Techniques', 'daily_hours': 5},
            'weeks_21_26': {'focus': 'Compliance & Certifications', 'daily_hours': 4}
        },
        'milestones': [
            {'week': 2, 'milestone': 'Understand network security fundamentals'},
            {'week': 4, 'milestone': 'Learn OWASP top 10'},
            {'week': 8, 'milestone': 'Master cryptography concepts'},
            {'week': 12, 'milestone': 'Perform basic penetration tests'},
            {'week': 16, 'milestone': 'Master security tools and frameworks'},
            {'week': 20, 'milestone': 'Implement security measures'},
            {'week': 26, 'milestone': 'Prepare for security certifications'}
        ]
    },
    'data analyst': {
        'duration_months': 6,
        'skills_required': ['SQL', 'Excel', 'Python', 'Tableau/Power BI', 'Statistics', 'Business Acumen'],
        'daily_distribution': {
            'weeks_1_2': {'focus': 'SQL Fundamentals', 'daily_hours': 3},
            'weeks_3_4': {'focus': 'Excel & Data Tools', 'daily_hours': 3},
            'weeks_5_8': {'focus': 'Python for Data Analysis', 'daily_hours': 4},
            'weeks_9_12': {'focus': 'Data Visualization', 'daily_hours': 4},
            'weeks_13_20': {'focus': 'Analytics & Insights', 'daily_hours': 5},
            'weeks_21_26': {'focus': 'Portfolio & Case Studies', 'daily_hours': 4}
        },
        'milestones': [
            {'week': 2, 'milestone': 'Master SQL queries'},
            {'week': 4, 'milestone': 'Advanced Excel skills'},
            {'week': 8, 'milestone': 'Python data manipulation'},
            {'week': 12, 'milestone': 'Create dashboards & visualizations'},
            {'week': 16, 'milestone': 'Derive business insights'},
            {'week': 20, 'milestone': 'Complete end-to-end analyses'},
            {'week': 26, 'milestone': 'Build analytics portfolio'}
        ]
    },
    'game developer': {
        'duration_months': 6,
        'skills_required': ['Game Engine', 'C#/C++', 'Graphics', 'Physics', 'Game Design'],
        'daily_distribution': {
            'weeks_1_2': {'focus': 'Game Development Basics', 'daily_hours': 3},
            'weeks_3_4': {'focus': 'Game Engine Fundamentals', 'daily_hours': 3},
            'weeks_5_8': {'focus': '2D/3D Graphics', 'daily_hours': 4},
            'weeks_9_12': {'focus': 'Physics & Gameplay', 'daily_hours': 4},
            'weeks_13_20': {'focus': 'Game Development Tools', 'daily_hours': 5},
            'weeks_21_26': {'focus': 'Complete Game Projects', 'daily_hours': 4}
        },
        'milestones': [
            {'week': 2, 'milestone': 'Learn game development concepts'},
            {'week': 4, 'milestone': 'Create first game prototype'},
            {'week': 8, 'milestone': 'Master 2D/3D graphics'},
            {'week': 12, 'milestone': 'Implement game physics'},
            {'week': 16, 'milestone': 'Add gameplay mechanics'},
            {'week': 20, 'milestone': 'Optimize game performance'},
            {'week': 26, 'milestone': 'Release complete game projects'}
        ]
    },
    'database administrator': {
        'duration_months': 6,
        'skills_required': ['SQL', 'Database Design', 'Backup/Recovery', 'Performance Tuning', 'Security'],
        'daily_distribution': {
            'weeks_1_2': {'focus': 'Database Fundamentals', 'daily_hours': 3},
            'weeks_3_4': {'focus': 'SQL Advanced', 'daily_hours': 3},
            'weeks_5_8': {'focus': 'Database Design', 'daily_hours': 4},
            'weeks_9_12': {'focus': 'Maintenance & Backup', 'daily_hours': 4},
            'weeks_13_20': {'focus': 'Performance & Optimization', 'daily_hours': 5},
            'weeks_21_26': {'focus': 'Security & Compliance', 'daily_hours': 4}
        },
        'milestones': [
            {'week': 2, 'milestone': 'Master SQL queries and optimization'},
            {'week': 4, 'milestone': 'Learn database architecture'},
            {'week': 8, 'milestone': 'Design efficient schemas'},
            {'week': 12, 'milestone': 'Implement backup & recovery'},
            {'week': 16, 'milestone': 'Optimize database performance'},
            {'week': 20, 'milestone': 'Ensure database security'},
            {'week': 26, 'milestone': 'Manage production databases'}
        ]
    },
    'product manager': {
        'duration_months': 6,
        'skills_required': ['Product Strategy', 'User Research', 'Analytics', 'Roadmapping', 'Leadership'],
        'daily_distribution': {
            'weeks_1_2': {'focus': 'Product Management Basics', 'daily_hours': 3},
            'weeks_3_4': {'focus': 'User Research Methods', 'daily_hours': 3},
            'weeks_5_8': {'focus': 'Product Strategy', 'daily_hours': 4},
            'weeks_9_12': {'focus': 'Roadmapping & Planning', 'daily_hours': 4},
            'weeks_13_20': {'focus': 'Analytics & Metrics', 'daily_hours': 5},
            'weeks_21_26': {'focus': 'Leadership & Communication', 'daily_hours': 4}
        },
        'milestones': [
            {'week': 2, 'milestone': 'Understand product management framework'},
            {'week': 4, 'milestone': 'Conduct user research'},
            {'week': 8, 'milestone': 'Define product strategy'},
            {'week': 12, 'milestone': 'Create product roadmaps'},
            {'week': 16, 'milestone': 'Track metrics and KPIs'},
            {'week': 20, 'milestone': 'Lead cross-functional teams'},
            {'week': 26, 'milestone': 'Launch successful products'}
        ]
    },
    'technical writer': {
        'duration_months': 6,
        'skills_required': ['Writing', 'Technical Concepts', 'Documentation', 'Tools', 'User Experience'],
        'daily_distribution': {
            'weeks_1_2': {'focus': 'Technical Writing Basics', 'daily_hours': 3},
            'weeks_3_4': {'focus': 'Documentation Standards', 'daily_hours': 3},
            'weeks_5_8': {'focus': 'API Documentation', 'daily_hours': 4},
            'weeks_9_12': {'focus': 'User Guides & Tutorials', 'daily_hours': 4},
            'weeks_13_20': {'focus': 'Technical Tools & Platforms', 'daily_hours': 5},
            'weeks_21_26': {'focus': 'Portfolio & Publishing', 'daily_hours': 4}
        },
        'milestones': [
            {'week': 2, 'milestone': 'Learn technical writing principles'},
            {'week': 4, 'milestone': 'Create user documentation'},
            {'week': 8, 'milestone': 'Write API documentation'},
            {'week': 12, 'milestone': 'Develop comprehensive guides'},
            {'week': 16, 'milestone': 'Master documentation tools'},
            {'week': 20, 'milestone': 'Publish technical content'},
            {'week': 26, 'milestone': 'Build technical writing portfolio'}
        ]
    },
    'teacher': {
        'duration_months': 6,
        'skills_required': ['Subject Matter Expertise', 'Curriculum Design', 'Classroom Management', 'Student Assessment', 'Communication', 'Educational Technology'],
        'daily_distribution': {
            'weeks_1_2': {'focus': 'Teaching Fundamentals & Pedagogy', 'daily_hours': 3},
            'weeks_3_4': {'focus': 'Subject Matter Mastery', 'daily_hours': 3},
            'weeks_5_8': {'focus': 'Curriculum Development', 'daily_hours': 4},
            'weeks_9_12': {'focus': 'Instructional Strategies', 'daily_hours': 4},
            'weeks_13_20': {'focus': 'Assessment & Student Evaluation', 'daily_hours': 5},
            'weeks_21_26': {'focus': 'Classroom Management & EdTech', 'daily_hours': 4}
        },
        'milestones': [
            {'week': 2, 'milestone': 'Understand teaching principles and pedagogy'},
            {'week': 4, 'milestone': 'Master subject content deeply'},
            {'week': 8, 'milestone': 'Design engaging and effective curricula'},
            {'week': 12, 'milestone': 'Master diverse instructional methods'},
            {'week': 16, 'milestone': 'Create effective assessments and rubrics'},
            {'week': 20, 'milestone': 'Manage diverse classrooms effectively'},
            {'week': 26, 'milestone': 'Integrate technology and foster student growth'}
        ]
    },
    'professor': {
        'duration_months': 6,
        'skills_required': ['Advanced Subject Expertise', 'Research Methods', 'Academic Writing', 'Course Design', 'Mentoring', 'Grant Writing', 'Publishing'],
        'daily_distribution': {
            'weeks_1_2': {'focus': 'Academic Excellence Foundations', 'daily_hours': 3},
            'weeks_3_4': {'focus': 'Research Methods & Methodology', 'daily_hours': 3},
            'weeks_5_8': {'focus': 'Advanced Course Design', 'daily_hours': 4},
            'weeks_9_12': {'focus': 'Academic Writing & Publishing', 'daily_hours': 4},
            'weeks_13_20': {'focus': 'Research & Grant Writing', 'daily_hours': 5},
            'weeks_21_26': {'focus': 'Mentoring & Academic Leadership', 'daily_hours': 4}
        },
        'milestones': [
            {'week': 2, 'milestone': 'Develop expert-level subject knowledge'},
            {'week': 4, 'milestone': 'Learn rigorous research methods'},
            {'week': 8, 'milestone': 'Design graduate-level courses'},
            {'week': 12, 'milestone': 'Publish academic papers and research'},
            {'week': 16, 'milestone': 'Write and secure research grants'},
            {'week': 20, 'milestone': 'Mentor doctoral students and junior scholars'},
            {'week': 26, 'milestone': 'Establish independent research program'}
        ]
    },
    'business manager': {
        'duration_months': 6,
        'skills_required': ['Business Strategy', 'Financial Management', 'Leadership', 'Operations', 'Project Management', 'Decision Making', 'Communication'],
        'daily_distribution': {
            'weeks_1_2': {'focus': 'Business Fundamentals', 'daily_hours': 3},
            'weeks_3_4': {'focus': 'Financial Analysis & Accounting', 'daily_hours': 3},
            'weeks_5_8': {'focus': 'Strategic Business Planning', 'daily_hours': 4},
            'weeks_9_12': {'focus': 'Operations Management', 'daily_hours': 4},
            'weeks_13_20': {'focus': 'Leadership & Team Management', 'daily_hours': 5},
            'weeks_21_26': {'focus': 'Decision Making & Business Analytics', 'daily_hours': 4}
        },
        'milestones': [
            {'week': 2, 'milestone': 'Understand core business principles'},
            {'week': 4, 'milestone': 'Master financial management & accounting'},
            {'week': 8, 'milestone': 'Develop comprehensive strategic plans'},
            {'week': 12, 'milestone': 'Optimize business operations & efficiency'},
            {'week': 16, 'milestone': 'Lead high-performance teams'},
            {'week': 20, 'milestone': 'Make data-driven business decisions'},
            {'week': 26, 'milestone': 'Drive business growth & innovation'}
        ]
    }
}



def generate_daily_plan(profession, duration_months, current_skills, experience_level):
    """
    Generate a detailed day-by-day learning plan
    
    Args:
        profession: str - "Software Engineer", "Data Scientist", etc.
        duration_months: int - How many months (usually 6)
        current_skills: list - Skills user already has
        experience_level: str - "beginner", "intermediate", "advanced"
    
    Returns:
        dict - Contains daily_tasks, milestones, technologies
    """
    
    profession_key = profession.lower()
    if profession_key not in PROFESSION_PATHS:
        return generate_generic_plan(profession, duration_months)
    
    profession_data = PROFESSION_PATHS[profession_key]
    total_days = duration_months * 30  # Approximate
    
    daily_tasks = []
    technologies_to_learn = [
        skill for skill in profession_data['skills_required']
        if skill not in current_skills
    ]
    
    # Distribute tasks across days
    task_distribution = profession_data['daily_distribution']
    current_day = 0
    
    for week_range, week_data in task_distribution.items():
        # week_range format: 'weeks_1_2', 'weeks_3_4', etc.
        parts = week_range.split('_')
        try:
            start_week = int(parts[1])
            end_week = int(parts[2])
        except Exception:
            # fallback: assume single 2-week block
            start_week, end_week = 1, 2

        weeks = end_week - start_week + 1
        days_in_phase = weeks * 7
        focus = week_data['focus']
        daily_hours = week_data['daily_hours']

        for day in range(days_in_phase):
            current_day += 1

            # Generate specific task based on phase
            task = generate_specific_task(
                focus,
                day + 1,
                current_skills,
                experience_level
            )

            daily_tasks.append({
                'day': current_day,
                'task': task,
                'focus_area': focus,
                'recommended_hours': daily_hours,
                'difficulty': calculate_difficulty(current_day, total_days)
            })
    
    return {
        'total_days': total_days,
        'daily_tasks': daily_tasks[:total_days],  # Trim to exact duration
        'technologies': technologies_to_learn,
        'milestones': profession_data['milestones']
    }


def generate_specific_task(focus_area, day_in_phase, current_skills, experience_level):
    """Generate specific task based on focus area"""
    
    task_templates = {
        'Python Fundamentals': [
            'Learn variables, data types, and basic operations',
            'Practice control flow: if/else statements',
            'Master loops: for and while loops with exercises',
            'Build functions: definition, parameters, return values',
            'Work on list and dictionary operations',
            'Understand strings and string manipulation',
            'Practice with 5-10 small coding challenges',
            'Build a simple calculator program'
        ],
        'Web Development Basics (HTML/CSS)': [
            'Learn HTML semantic elements and structure',
            'Build a personal portfolio webpage',
            'Master CSS selectors and styling',
            'Create a multi-page website with navigation',
            'Practice CSS flexbox and grid layout',
            'Implement responsive design with media queries',
            'Build a landing page with animations'
        ],
        'JavaScript & Frontend': [
            'Learn JavaScript variables and data types',
            'Master JavaScript DOM manipulation',
            'Build interactive web components',
            'Learn event handling and callbacks',
            'Understand array methods and ES6 features',
            'Build a todo app with JavaScript',
            'Learn async/await and promises'
        ],
        'Backend & Databases': [
            'Learn SQL basics: SELECT, INSERT, UPDATE, DELETE',
            'Design database schemas and relationships',
            'Build REST APIs with Flask/Django',
            'Implement database migrations',
            'Learn about authentication and security',
            'Build a complete backend with user system'
        ],
        'Python & Data Manipulation': [
            'Master Python NumPy arrays and operations',
            'Learn Pandas data frames and series',
            'Practice data cleaning and preprocessing',
            'Work with CSV and JSON files',
            'Create data visualizations with Matplotlib'
        ],
        'Machine Learning Algorithms': [
            'Understand linear regression from scratch',
            'Learn logistic regression and classification',
            'Master decision trees and random forests',
            'Study neural networks basics',
            'Implement algorithms from scratch',
            'Use scikit-learn for practical ML'
        ]
    }
    
    if focus_area in task_templates:
        tasks = task_templates[focus_area]
        task_index = (day_in_phase - 1) % len(tasks)
        return tasks[task_index]
    else:
        # Try to match focus_area to a known template by fuzzy/substring matching
        lower_focus = focus_area.lower()
        for tmpl_key in task_templates:
            if tmpl_key.lower() in lower_focus or lower_focus in tmpl_key.lower():
                tasks = task_templates[tmpl_key]
                task_index = (day_in_phase - 1) % len(tasks)
                return tasks[task_index]

        return f"Work on {focus_area} - Day {day_in_phase}"


def calculate_difficulty(current_day, total_days):
    """Calculate difficulty level based on progression"""
    percentage = current_day / total_days
    
    if percentage < 0.2:
        return 'easy'
    elif percentage < 0.5:
        return 'medium'
    elif percentage < 0.8:
        return 'hard'
    else:
        return 'very hard'


def generate_generic_plan(profession, duration_months):
    """Generate a generic plan if profession not found"""
    total_days = duration_months * 30
    
    daily_tasks = []
    # Use a set of varied generic templates to avoid repeated identical tasks
    generic_templates = [
        'Read a system design article or blog and summarize key takeaways',
        'Study core principles: scalability, availability, consistency',
        'Practice designing a component (APIs, data model, storage) on paper',
        'Implement a small prototype or proof-of-concept for a subsystem',
        'Review distributed systems patterns (load balancing, sharding, caching)',
        'Analyze a real-world system case study and note trade-offs',
        'Do a mock system design interview: sketch architecture and justify choices',
        'Improve previous designs: add reliability and monitoring considerations',
        'Write tests/specs for a designed component and think about scaling',
        'Refactor a prototype to improve performance or simplicity'
    ]

    for day in range(1, total_days + 1):
        template = generic_templates[(day - 1) % len(generic_templates)]
        task_text = template
        # Add day-specific hint to keep clarity
        task_text = f"{task_text} (Day {day})"
        daily_tasks.append({
            'day': day,
            'task': task_text,
            'focus_area': profession,
            'recommended_hours': 3 + ((day - 1) % 3),
            'difficulty': calculate_difficulty(day, total_days)
        })
    
    return {
        'total_days': total_days,
        'daily_tasks': daily_tasks,
        'technologies': [],
        'milestones': [
            {'week': 2, 'milestone': f'Complete Week 2 of {profession} learning'},
            {'week': 13, 'milestone': f'Halfway through {profession} mastery'},
            {'week': 26, 'milestone': f'Complete {profession} learning plan'}
        ]
    }
