import mysql.connector
from mysql.connector import Error
from datetime import datetime
import json
import uuid

class Database:
    """Database management class"""
    
    def __init__(self, app):
        self.app = app
        self.connection = None
        self.config = {
            'host': app.config['MYSQL_HOST'],
            'user': app.config['MYSQL_USER'],
            'password': app.config['MYSQL_PASSWORD'],
            'database': app.config['MYSQL_DATABASE'],
            'port': app.config['MYSQL_PORT']
        }
    
    def connect(self):
        """Establish database connection"""
        try:
            self.connection = mysql.connector.connect(**self.config)
            return self.connection
        except Error as e:
            print(f"Database connection error: {e}")
            return None
    
    def init_tables(self):
        """Initialize database tables"""
        try:
            conn = self.connect()
            cursor = conn.cursor()
            
            # Create resumes table
            cursor.execute("""
                CREATE TABLE IF NOT EXISTS resumes (
                    id VARCHAR(36) PRIMARY KEY,
                    student_id VARCHAR(100),
                    student_name VARCHAR(255),
                    filename VARCHAR(255),
                    filepath VARCHAR(500),
                    raw_text LONGTEXT,
                    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
                    updated_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP ON UPDATE CURRENT_TIMESTAMP,
                    INDEX idx_student_id (student_id),
                    INDEX idx_created_at (created_at)
                )
            """)
            
            # Create analyses table
            cursor.execute("""
                CREATE TABLE IF NOT EXISTS analyses (
                    id VARCHAR(36) PRIMARY KEY,
                    resume_id VARCHAR(36),
                    parsed_data JSON,
                    scores JSON,
                    recommendations JSON,
                    missing_areas JSON,
                    total_score INT,
                    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
                    FOREIGN KEY (resume_id) REFERENCES resumes(id) ON DELETE CASCADE,
                    INDEX idx_resume_id (resume_id)
                )
            """)
            
            # Create skill library table
            cursor.execute("""
                CREATE TABLE IF NOT EXISTS skill_library (
                    id INT AUTO_INCREMENT PRIMARY KEY,
                    skill_name VARCHAR(100) UNIQUE,
                    category VARCHAR(50),
                    academic_relevance INT,
                    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
                )
            """)
            
            conn.commit()
            cursor.close()
            conn.close()
            print("Database tables initialized successfully")
            
        except Error as e:
            print(f"Error initializing tables: {e}")
    
    def save_resume(self, student_id, student_name, filename, filepath, raw_text):
        """Save resume to database"""
        try:
            conn = self.connect()
            cursor = conn.cursor()
            
            resume_id = str(uuid.uuid4())
            
            cursor.execute("""
                INSERT INTO resumes 
                (id, student_id, student_name, filename, filepath, raw_text)
                VALUES (%s, %s, %s, %s, %s, %s)
            """, (resume_id, student_id, student_name, filename, filepath, raw_text))
            
            conn.commit()
            cursor.close()
            conn.close()
            
            return resume_id
            
        except Error as e:
            print(f"Error saving resume: {e}")
            return None
    
    def get_resume(self, resume_id):
        """Get resume data from database"""
        try:
            conn = self.connect()
            cursor = conn.cursor(dictionary=True)
            
            cursor.execute("SELECT * FROM resumes WHERE id = %s", (resume_id,))
            resume = cursor.fetchone()
            
            cursor.close()
            conn.close()
            
            return resume
            
        except Error as e:
            print(f"Error retrieving resume: {e}")
            return None
    
    def save_analysis(self, resume_id, analysis_result):
        """Save analysis results to database"""
        try:
            conn = self.connect()
            cursor = conn.cursor()
            
            analysis_id = str(uuid.uuid4())
            
            cursor.execute("""
                INSERT INTO analyses 
                (id, resume_id, parsed_data, scores, recommendations, missing_areas, total_score)
                VALUES (%s, %s, %s, %s, %s, %s, %s)
            """, (
                analysis_id,
                resume_id,
                json.dumps(analysis_result.get('parsed_resume', {})),
                json.dumps(analysis_result.get('scores', {})),
                json.dumps(analysis_result.get('recommendations', {})),
                json.dumps(analysis_result.get('missing_areas', {})),
                analysis_result.get('scores', {}).get('total_score', 0)
            ))
            
            conn.commit()
            cursor.close()
            conn.close()
            
            return analysis_id
            
        except Error as e:
            print(f"Error saving analysis: {e}")
            return None
    
    def get_analysis(self, analysis_id):
        """Get analysis result from database"""
        try:
            conn = self.connect()
            cursor = conn.cursor(dictionary=True)
            
            cursor.execute("SELECT * FROM analyses WHERE id = %s", (analysis_id,))
            analysis = cursor.fetchone()
            
            cursor.close()
            conn.close()
            
            if analysis:
                analysis['parsed_data'] = json.loads(analysis['parsed_data'])
                analysis['scores'] = json.loads(analysis['scores'])
                analysis['recommendations'] = json.loads(analysis['recommendations'])
                analysis['missing_areas'] = json.loads(analysis['missing_areas'])
            
            return analysis
            
        except Error as e:
            print(f"Error retrieving analysis: {e}")
            return None
    
    def get_student_history(self, student_id):
        """Get all analyses for a student"""
        try:
            conn = self.connect()
            cursor = conn.cursor(dictionary=True)
            
            cursor.execute("""
                SELECT r.id, r.student_name, r.created_at, a.total_score, a.id as analysis_id
                FROM resumes r
                LEFT JOIN analyses a ON r.id = a.resume_id
                WHERE r.student_id = %s
                ORDER BY r.created_at DESC
            """, (student_id,))
            
            history = cursor.fetchall()
            cursor.close()
            conn.close()
            
            return history
            
        except Error as e:
            print(f"Error retrieving history: {e}")
            return []
