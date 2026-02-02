"""
Rule-based scoring system for student resumes
Scores are student-centric, focusing on academic relevance
"""

class ScoringEngine:
    """Scoring logic for resume analysis"""
    
    def __init__(self):
        self.skill_database = self._load_skill_database()
        self.section_weights = {
            'education': 20,
            'skills': 25,
            'projects': 20,
            'experience': 15,
            'internships': 15,
            'certifications': 5
        }
    
    def _load_skill_database(self):
        """Load relevant skills for students"""
        return {
            'in_demand': [
                'Python', 'Java', 'JavaScript', 'SQL', 'React', 'Django',
                'AWS', 'Git', 'Docker', 'REST API', 'MongoDB', 'Node.js',
                'TypeScript', 'Angular', 'Vue.js', 'C++', 'Machine Learning',
                'Data Analysis', 'HTML', 'CSS', 'Linux'
            ],
            'academic_focus': [
                'Data Structures', 'Algorithms', 'OOP', 'DBMS', 'Web Development',
                'Mobile Development', 'Cloud Computing', 'AI/ML', 'Cybersecurity',
                'Networking', 'Operating Systems', 'Software Engineering'
            ]
        }
    
    def calculate_scores(self, parsed_resume):
        """
        Calculate section-wise scores (0-100) based on student-centric criteria
        """
        scores = {
            'education': self._score_education(parsed_resume['education']),
            'skills': self._score_skills(parsed_resume['skills']),
            'projects': self._score_projects(parsed_resume['projects']),
            'experience': self._score_experience(parsed_resume['experience']),
            'internships': self._score_internships(parsed_resume['internships']),
            'certifications': self._score_certifications(parsed_resume['certifications']),
            'contact_info': self._score_contact_info(parsed_resume['contact_info'])
        }
        
        # Calculate weighted total score
        total_score = 0
        for section, weight in self.section_weights.items():
            total_score += scores[section] * (weight / 100)
        
        scores['total_score'] = round(total_score, 2)
        scores['grade'] = self._get_grade(total_score)
        
        return scores
    
    def _score_education(self, education):
        """
        Score education section (0-100)
        Criteria:
        - Has degree information (40 points)
        - Has institution name (30 points)
        - Has graduation year (30 points)
        """
        score = 0
        
        if education['found']:
            score += 30  # Has education section
        
        if education['degrees']:
            score += 40
        
        if education['institutions']:
            score += 20
        
        if education['years']:
            score += 10
        
        return min(score, 100)
    
    def _score_skills(self, skills):
        """
        Score skills section (0-100)
        Criteria:
        - Has technical skills (40 points)
        - Has programming languages (20 points)
        - Has frameworks/tools (20 points)
        - Has soft skills (20 points)
        """
        score = 0
        
        if skills['technical']:
            in_demand_count = sum(
                1 for skill in skills['technical'] 
                if skill in self.skill_database['in_demand']
            )
            score += min(len(skills['technical']) * 3, 40)
            score += min(in_demand_count * 5, 15)
        
        if skills['programming_languages']:
            score += min(len(skills['programming_languages']) * 5, 20)
        
        if skills['frameworks']:
            score += min(len(skills['frameworks']) * 4, 20)
        
        if skills['soft']:
            score += min(len(skills['soft']) * 3, 20)
        
        return min(score, 100)
    
    def _score_projects(self, projects):
        """
        Score projects section (0-100)
        Criteria:
        - Has projects section (30 points)
        - 1-2 projects (40 points)
        - 3+ projects (30 points)
        """
        score = 0
        
        if projects['found']:
            score += 30
            
            if projects['count'] == 1:
                score += 40
            elif projects['count'] >= 2:
                score += 30
                score += min(projects['count'] * 2, 10)
        
        return min(score, 100)
    
    def _score_experience(self, experience):
        """
        Score work experience (0-100)
        Criteria:
        - Has experience (30 points)
        - Multiple positions (40 points)
        - Job titles present (30 points)
        """
        score = 0
        
        if experience['found']:
            score += 30
        
        if experience['total_entries'] >= 1:
            score += 40
        
        if experience['positions']:
            score += min(len(experience['positions']) * 10, 30)
        
        return min(score, 100)
    
    def _score_internships(self, internships):
        """
        Score internships (0-100)
        Criteria:
        - Has internship (50 points)
        - Multiple internships (50 points)
        """
        score = 0
        
        if internships['found']:
            score += 50
            if internships['count'] >= 2:
                score += 50
            else:
                score += 30
        
        return min(score, 100)
    
    def _score_certifications(self, certifications):
        """
        Score certifications (0-100)
        Criteria:
        - Has certifications (40 points)
        - Multiple certifications (30 points)
        - Relevant certs (30 points)
        """
        score = 0
        
        if certifications['found']:
            score += 40
            if certifications['count'] >= 2:
                score += 30
            score += min(certifications['count'] * 10, 30)
        
        return min(score, 100)
    
    def _score_contact_info(self, contact_info):
        """
        Score contact information (0-100)
        Criteria:
        - Has email (40 points)
        - Has phone (30 points)
        - Has LinkedIn (30 points)
        """
        score = 0
        
        if contact_info['email']:
            score += 40
        
        if contact_info['phone']:
            score += 30
        
        if contact_info['linkedin']:
            score += 30
        
        return min(score, 100)
    
    def _get_grade(self, score):
        """Convert score to letter grade"""
        if score >= 85:
            return 'A'
        elif score >= 75:
            return 'B'
        elif score >= 65:
            return 'C'
        elif score >= 50:
            return 'D'
        else:
            return 'F'
    
    def identify_missing_areas(self, parsed_resume):
        """Identify areas missing from resume"""
        missing = []
        
        if not parsed_resume['education']['found']:
            missing.append('Education details')
        
        if len(parsed_resume['skills']['technical']) < 3:
            missing.append('More technical skills')
        
        if len(parsed_resume['skills']['programming_languages']) == 0:
            missing.append('Programming languages')
        
        if not parsed_resume['projects']['found']:
            missing.append('Academic/personal projects')
        
        if not parsed_resume['internships']['found']:
            missing.append('Internship experience')
        
        if not parsed_resume['certifications']['found']:
            missing.append('Professional certifications')
        
        if not parsed_resume['contact_info']['email']:
            missing.append('Email address')
        
        if len(parsed_resume['skills']['soft']) < 3:
            missing.append('Soft skills section')
        
        return missing
    
    def generate_recommendations(self, parsed_resume, scores):
        """
        Generate improvement strategies based on resume analysis
        """
        recommendations = {
            'immediate_actions': [],
            'medium_term': [],
            'long_term': []
        }
        
        # Immediate actions (high priority)
        if scores['education'] < 50:
            recommendations['immediate_actions'].append(
                'Add your degree, college name, and graduation year to the education section'
            )
        
        if not parsed_resume['contact_info']['email']:
            recommendations['immediate_actions'].append(
                'Include your professional email address'
            )
        
        if scores['skills'] < 60:
            recommendations['immediate_actions'].append(
                'List technical skills like programming languages, frameworks, and tools you have learned'
            )
        
        if len(parsed_resume['skills']['programming_languages']) == 0:
            recommendations['immediate_actions'].append(
                'Highlight at least 2-3 programming languages you are familiar with'
            )
        
        # Medium-term (3-6 months)
        if not parsed_resume['projects']['found']:
            recommendations['medium_term'].append(
                'Build and showcase 2-3 academic or personal projects with descriptions and technologies used'
            )
        elif parsed_resume['projects']['count'] < 2:
            recommendations['medium_term'].append(
                'Add at least one more project to demonstrate your practical skills'
            )
        
        if not parsed_resume['internships']['found']:
            recommendations['medium_term'].append(
                'Secure an internship to gain real-world experience and add to your resume'
            )
        
        if scores['skills'] < 80:
            recommendations['medium_term'].append(
                'Learn additional in-demand skills: ' + 
                ', '.join(self.skill_database['in_demand'][:5])
            )
        
        # Long-term (6+ months)
        if not parsed_resume['certifications']['found']:
            recommendations['long_term'].append(
                'Complete relevant certifications (AWS, Google Cloud, CompTIA, etc.)'
            )
        
        if parsed_resume['experience']['total_entries'] == 0:
            recommendations['long_term'].append(
                'Aim for multiple internships or part-time work experiences before graduation'
            )
        
        recommendations['long_term'].append(
            'Continuously update your resume with new projects, skills, and experiences'
        )
        
        return recommendations
    
    def recommend_skills(self, current_skills, academic_year):
        """
        Recommend skills based on current skills and academic year
        """
        recommended = {
            'must_have': [],
            'good_to_have': [],
            'advanced': []
        }
        
        all_skills = self.skill_database['in_demand']
        missing_skills = [s for s in all_skills if s not in current_skills]
        
        if academic_year in ['first_year', 'second_year']:
            # Basics for beginners
            recommended['must_have'] = [
                'Python', 'Java', 'Data Structures',
                'HTML', 'CSS', 'SQL'
            ]
            recommended['good_to_have'] = missing_skills[:5]
            recommended['advanced'] = []
        
        elif academic_year == 'third_year':
            # Intermediate skills
            recommended['must_have'] = [
                'Python', 'JavaScript', 'React/Angular', 'SQL',
                'Git', 'REST API'
            ]
            recommended['good_to_have'] = missing_skills[:8]
            recommended['advanced'] = ['Docker', 'AWS']
        
        else:  # final_year or beyond
            # Advanced skills
            recommended['must_have'] = [
                'Full-stack development', 'Git', 'REST APIs',
                'Databases', '2+ Programming Languages'
            ]
            recommended['good_to_have'] = missing_skills[:10]
            recommended['advanced'] = [
                'Cloud platforms (AWS/Azure)', 'DevOps',
                'Microservices', 'CI/CD', 'System Design'
            ]
        
        return recommended
