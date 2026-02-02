import PyPDF2
import re
from datetime import datetime

class ResumeProcessor:
    """Resume text extraction and parsing"""
    
    def __init__(self):
        self.common_sections = [
            'education', 'experience', 'skills', 'projects', 
            'certifications', 'internships', 'awards', 'languages',
            'achievements', 'summary', 'objective', 'technical'
        ]
    
    def extract_text_from_pdf(self, filepath):
        """Extract text from PDF file"""
        try:
            text = ""
            with open(filepath, 'rb') as file:
                pdf_reader = PyPDF2.PdfReader(file)
                num_pages = len(pdf_reader.pages)
                
                for page_num in range(num_pages):
                    page = pdf_reader.pages[page_num]
                    text += page.extract_text() or ""

            
            return text
            
        except Exception as e:
            print(f"Error extracting text from PDF: {e}")
            return None
    
    def parse_resume(self, text):
        """Parse resume text into structured sections"""
        parsed = {
            'raw_text': text,
            'education': self._extract_education(text),
            'skills': self._extract_skills(text),
            'experience': self._extract_experience(text),
            'projects': self._extract_projects(text),
            'internships': self._extract_internships(text),
            'certifications': self._extract_certifications(text),
            'contact_info': self._extract_contact_info(text),
            'summary': self._extract_summary(text)
        }
        return parsed
    
    def _extract_education(self, text):
        """Extract education details"""
        education = {
            'found': False,
            'degrees': [],
            'institutions': [],
            'years': []
        }
        
        # Look for degree keywords
        degree_keywords = [
            r'B\.?Tech|B\.?E\.?', r'Bachelor', 
            r'M\.?Tech|M\.?E\.?', r'Master', 
            r'B\.?Sc', r'B\.?A\.?', r'M\.?Sc', r'M\.?B\.?A\.?',
            r'D\.?M\.?', r'B\.?Pharm'
        ]
        
        for keyword in degree_keywords:
            matches = re.findall(f'{keyword}[\\s\\w\\.]*', text, re.IGNORECASE)
            if matches:
                education['degrees'].extend(matches)
                education['found'] = True
        
        # Look for institution names (common university patterns)
        institution_keywords = [
            r'[Uu]niversity', r'[Cc]ollege', r'[Ii]nstitute',
            r'[Ss]chool', r'[Aa]cademy', r'[Cc]enter'
        ]
        
        for line in text.split('\n'):
            for keyword in institution_keywords:
                if re.search(keyword, line):
                    institution = line.strip()
                    if len(institution) > 5 and len(institution) < 150:
                        education['institutions'].append(institution)
                        break
        
        # Extract years
        years = re.findall(r'(20\d{2}|19\d{2})', text)
        if years:
            education['years'] = sorted(list(set(years)))
        
        return education
    
    def _extract_skills(self, text):
        """Extract technical and soft skills"""
        skills = {
            'technical': [],
            'soft': [],
            'programming_languages': [],
            'frameworks': [],
            'tools': []
        }
        
        # Technical skills
        tech_keywords = {
            'programming': [
                'Python', 'Java', 'C\\+\\+', 'JavaScript', 'TypeScript', 
                'C#', 'PHP', 'Ruby', 'Go', 'Rust', 'Kotlin', 'Swift'
            ],
            'web': [
                'React', 'Angular', 'Vue\\.js', 'Node\\.js', 'Django', 
                'Flask', 'Express', 'Spring', 'ASP\\.NET'
            ],
            'databases': [
                'MySQL', 'PostgreSQL', 'MongoDB', 'Firebase', 'Redis',
                'Oracle', 'SQLServer', 'Cassandra'
            ],
            'tools': [
                'Git', 'Docker', 'Kubernetes', 'Jenkins', 'AWS', 'Azure',
                'Google Cloud', 'Linux', 'Jira', 'Figma', 'Photoshop'
            ]
        }
        
        for category, keywords in tech_keywords.items():
            for keyword in keywords:
                if re.search(keyword, text, re.IGNORECASE):
                    skills['technical'].append(keyword)
                    if category == 'programming':
                        skills['programming_languages'].append(keyword)
                    elif category == 'web':
                        skills['frameworks'].append(keyword)
                    elif category == 'tools':
                        skills['tools'].append(keyword)
        
        # Soft skills
        soft_skills = [
            'Communication', 'Leadership', 'Teamwork', 'Problem Solving',
            'Critical Thinking', 'Time Management', 'Project Management',
            'Collaboration', 'Creativity', 'Adaptability'
        ]
        
        for skill in soft_skills:
            if re.search(skill, text, re.IGNORECASE):
                skills['soft'].append(skill)
        
        skills['technical'] = list(set(skills['technical']))
        skills['soft'] = list(set(skills['soft']))
        
        return skills
    
    def _extract_experience(self, text):
        """Extract work experience"""
        experience = {
            'found': False,
            'total_entries': 0,
            'positions': [],
            'companies': [],
            'duration': []
        }
        
        # Look for job titles
        job_titles = [
            'Developer', 'Engineer', 'Manager', 'Analyst', 'Consultant',
            'Intern', 'Associate', 'Coordinator', 'Specialist', 'Lead',
            'Director', 'Architect', 'Administrator', 'Designer'
        ]
        
        for title in job_titles:
            matches = re.findall(f'[\\w\\s]*{title}[\\w\\s]*', text, re.IGNORECASE)
            if matches:
                experience['positions'].extend(matches[:3])
                experience['found'] = True
        
        # Extract years/duration
        duration_pattern = r'(20\d{2}|present|current)'
        durations = re.findall(duration_pattern, text, re.IGNORECASE)
        if durations:
            experience['duration'] = list(set(durations))
            experience['total_entries'] = len(durations) // 2
        
        experience['positions'] = list(set(experience['positions']))
        
        return experience
    
    def _extract_projects(self, text):
        """Extract projects information"""
        projects = {
            'found': False,
            'count': 0,
            'details': []
        }
        
        # Look for project keywords
        if re.search(r'project|capstone|thesis|portfolio', text, re.IGNORECASE):
            projects['found'] = True
            
            # Count project sections
            project_markers = re.findall(
                r'(project|capstone|thesis|portfolio)',
                text,
                re.IGNORECASE
            )
            projects['count'] = len(project_markers)
        
        return projects
    
    def _extract_internships(self, text):
        """Extract internship information"""
        internships = {
            'found': False,
            'count': 0,
            'companies': []
        }
        
        if re.search(r'intern|internship', text, re.IGNORECASE):
            internships['found'] = True
            internship_count = len(re.findall(r'intern', text, re.IGNORECASE))
            internships['count'] = internship_count // 2 if internship_count > 1 else 1
        
        return internships
    
    def _extract_certifications(self, text):
        """Extract certifications"""
        certifications = {
            'found': False,
            'count': 0,
            'certifications': []
        }
        
        cert_keywords = [
            'Certificate', 'Certified', 'AWS', 'Azure', 'Google Cloud',
            'CompTIA', 'CISNA', 'CCNA', 'CPA', 'PMP', 'Scrum', 'Six Sigma'
        ]
        
        for cert in cert_keywords:
            if re.search(cert, text, re.IGNORECASE):
                certifications['certifications'].append(cert)
                certifications['found'] = True
        
        certifications['count'] = len(certifications['certifications'])
        
        return certifications
    
    def _extract_contact_info(self, text):
        """Extract contact information"""
        contact = {
            'email': None,
            'phone': None,
            'linkedin': None
        }
        
        # Email
        email_pattern = r'[a-zA-Z0-9._%+-]+@[a-zA-Z0-9.-]+\.[a-zA-Z]{2,}'
        email_match = re.search(email_pattern, text)
        if email_match:
            contact['email'] = email_match.group()
        
        # Phone
        phone_pattern = r'(?:\+\d{1,3})?[-.\s]?\d{3}[-.\s]?\d{3}[-.\s]?\d{4}'
        phone_match = re.search(phone_pattern, text)
        if phone_match:
            contact['phone'] = phone_match.group()
        
        # LinkedIn
        linkedin_pattern = r'linkedin\.com/in/[^\s]+'
        linkedin_match = re.search(linkedin_pattern, text, re.IGNORECASE)
        if linkedin_match:
            contact['linkedin'] = linkedin_match.group()
        
        return contact
    
    def _extract_summary(self, text):
        """Extract summary/objective section"""
        summary = {
            'found': False,
            'text': None,
            'length': 0
        }
        
        # Look for summary/objective section
        summary_pattern = r'(?:summary|objective|professional summary|about me)[:\s]+([^.]*)\.?'
        match = re.search(summary_pattern, text, re.IGNORECASE)
        
        if match:
            summary['found'] = True
            summary['text'] = match.group(1).strip()
            summary['length'] = len(summary['text'].split())
        
        return summary
