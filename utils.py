"""
Utility functions and validators for the resume analyzer
"""

import os
import re
from datetime import datetime

class TextValidator:
    """Text validation utilities"""
    
    @staticmethod
    def is_valid_email(email):
        """Validate email format"""
        pattern = r'^[a-zA-Z0-9._%+-]+@[a-zA-Z0-9.-]+\.[a-zA-Z]{2,}$'
        return re.match(pattern, email) is not None
    
    @staticmethod
    def is_valid_phone(phone):
        """Validate phone number format"""
        pattern = r'^(?:\+\d{1,3})?[-.\s]?\d{3}[-.\s]?\d{3}[-.\s]?\d{4}$'
        return re.match(pattern, phone) is not None
    
    @staticmethod
    def extract_words(text):
        """Extract words from text"""
        return re.findall(r'\b\w+\b', text.lower())
    
    @staticmethod
    def count_words(text):
        """Count words in text"""
        return len(TextValidator.extract_words(text))


class FileManager:
    """File management utilities"""
    
    @staticmethod
    def get_file_size_mb(filepath):
        """Get file size in MB"""
        return os.path.getsize(filepath) / (1024 * 1024)
    
    @staticmethod
    def file_exists(filepath):
        """Check if file exists"""
        return os.path.isfile(filepath)
    
    @staticmethod
    def create_directory(directory_path):
        """Create directory if it doesn't exist"""
        os.makedirs(directory_path, exist_ok=True)


class DateUtils:
    """Date utility functions"""
    
    @staticmethod
    def get_current_timestamp():
        """Get current timestamp"""
        return datetime.now().isoformat()
    
    @staticmethod
    def get_year_difference(start_year, end_year):
        """Calculate year difference"""
        try:
            return int(end_year) - int(start_year)
        except:
            return 0


class SkillMatcher:
    """Utility for matching skills"""
    
    SKILL_DATABASE = {
        'languages': [
            'Python', 'Java', 'JavaScript', 'C++', 'C#', 'PHP',
            'Ruby', 'Go', 'Rust', 'TypeScript', 'Kotlin', 'Swift'
        ],
        'web_frameworks': [
            'React', 'Angular', 'Vue', 'Django', 'Flask', 'Spring',
            'Node.js', 'Express', 'ASP.NET', 'Laravel', 'Rails'
        ],
        'databases': [
            'MySQL', 'PostgreSQL', 'MongoDB', 'Firebase', 'Redis',
            'Oracle', 'SQL Server', 'Cassandra', 'DynamoDB'
        ],
        'cloud_platforms': [
            'AWS', 'Google Cloud', 'Azure', 'Heroku', 'DigitalOcean',
            'IBM Cloud', 'Oracle Cloud'
        ],
        'devops': [
            'Docker', 'Kubernetes', 'Jenkins', 'Git', 'GitHub',
            'GitLab', 'Ansible', 'Terraform', 'CI/CD'
        ],
        'data_science': [
            'Machine Learning', 'TensorFlow', 'PyTorch', 'Scikit-learn',
            'Pandas', 'NumPy', 'Data Analysis', 'Statistics',
            'Deep Learning', 'NLP'
        ]
    }
    
    @classmethod
    def categorize_skill(cls, skill):
        """Categorize a skill"""
        skill_lower = skill.lower()
        
        for category, skills in cls.SKILL_DATABASE.items():
            if any(skill_lower in s.lower() or s.lower() in skill_lower 
                   for s in skills):
                return category
        
        return 'other'
    
    @classmethod
    def get_skills_by_category(cls, skills_list):
        """Categorize multiple skills"""
        categorized = {
            'languages': [],
            'web_frameworks': [],
            'databases': [],
            'cloud_platforms': [],
            'devops': [],
            'data_science': [],
            'other': []
        }
        
        for skill in skills_list:
            category = cls.categorize_skill(skill)
            categorized[category].append(skill)
        
        return categorized


class ReportGenerator:
    """Generate analysis reports"""
    
    @staticmethod
    def generate_text_report(analysis_result):
        """Generate text format report"""
        report = f"""
{'='*60}
RESUME ANALYSIS REPORT
{'='*60}

Student Name: {analysis_result.get('student_name', 'N/A')}
Analysis Date: {analysis_result.get('timestamp', 'N/A')}

{'='*60}
OVERALL SCORE
{'='*60}

Total Score: {analysis_result['scores']['total_score']}/100
Grade: {analysis_result['scores']['grade']}

{'='*60}
SECTION-WISE BREAKDOWN
{'='*60}

Education:       {analysis_result['scores']['education']}/100
Skills:          {analysis_result['scores']['skills']}/100
Projects:        {analysis_result['scores']['projects']}/100
Experience:      {analysis_result['scores']['experience']}/100
Internships:     {analysis_result['scores']['internships']}/100
Certifications:  {analysis_result['scores']['certifications']}/100

{'='*60}
MISSING AREAS
{'='*60}

"""
        for i, area in enumerate(analysis_result['missing_areas'], 1):
            report += f"{i}. {area}\n"
        
        report += f"\n{'='*60}\nRECOMMENDATIONS\n{'='*60}\n\n"
        
        recommendations = analysis_result['recommendations']
        
        report += "IMMEDIATE ACTIONS:\n"
        for i, rec in enumerate(recommendations['immediate_actions'], 1):
            report += f"{i}. {rec}\n"
        
        report += "\nMEDIUM-TERM (3-6 months):\n"
        for i, rec in enumerate(recommendations['medium_term'], 1):
            report += f"{i}. {rec}\n"
        
        report += "\nLONG-TERM (6+ months):\n"
        for i, rec in enumerate(recommendations['long_term'], 1):
            report += f"{i}. {rec}\n"
        
        report += f"\n{'='*60}\nEnd of Report\n{'='*60}"
        
        return report
    
    @staticmethod
    def generate_json_report(analysis_result):
        """Generate JSON format report"""
        import json
        return json.dumps(analysis_result, indent=2, default=str)


class Logger:
    """Simple logging utility"""
    
    @staticmethod
    def log_error(message, error_type="ERROR"):
        """Log error message"""
        timestamp = datetime.now().isoformat()
        print(f"[{timestamp}] {error_type}: {message}")
    
    @staticmethod
    def log_info(message):
        """Log info message"""
        timestamp = datetime.now().isoformat()
        print(f"[{timestamp}] INFO: {message}")
    
    @staticmethod
    def log_warning(message):
        """Log warning message"""
        timestamp = datetime.now().isoformat()
        print(f"[{timestamp}] WARNING: {message}")
