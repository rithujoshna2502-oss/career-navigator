import re
from datetime import datetime

# Try to use spaCy when available for improved entity/token extraction
try:
    import spacy
    _SPACY_AVAILABLE = True
    try:
        _NLP = spacy.load('en_core_web_sm')
    except Exception:
        # Model not installed; fallback to None
        _NLP = None
except Exception:
    _SPACY_AVAILABLE = False
    _NLP = None

def extract_skills_from_text(text):
    """Extract common tech skills from resume text. Uses spaCy if available, otherwise regex lookup."""
    text_lower = (text or '').lower()

    # Base keyword list for matching (extendable)
    skill_keywords = [
        'python', 'javascript', 'java', 'c++', 'sql', 'html', 'css', 'react', 'django', 'flask',
        'nodejs', 'node.js', 'tensorflow', 'tf', 'pytorch', 'pandas', 'aws', 'docker', 'kubernetes',
        'git', 'linux', 'machine learning', 'deep learning', 'data analysis'
    ]

    found = set()

    # If spaCy is available and model loaded, use noun chunks and entities to find skill-like tokens
    if _SPACY_AVAILABLE and _NLP is not None:
        try:
            doc = _NLP(text)
            # Check named entities and noun chunks
            for ent in list(doc.ents) + list(doc.noun_chunks):
                token_text = ent.text.lower()
                for kw in skill_keywords:
                    if kw in token_text:
                        found.add(kw)
            # Also check individual tokens for exact matches
            for token in doc:
                tok = token.text.lower()
                for kw in skill_keywords:
                    if tok == kw or tok.replace('.', '') == kw.replace('.', ''):
                        found.add(kw)
        except Exception:
            pass

    # Fallback / additional regex matching
    for kw in skill_keywords:
        pattern = re.escape(kw)
        if re.search(r'\b' + pattern + r'\b', text_lower):
            found.add(kw)

    # Normalize and title-case results
    return [s.title().replace('Node.Js', 'Node.js').replace('Tf', 'TF').replace('C++', 'C++') for s in sorted(found)]


def estimate_experience_level(text, years=0):
    """Estimate experience level based on content and years"""
    if years >= 5:
        return 'advanced'
    elif years >= 2:
        return 'intermediate'
    else:
        return 'beginner'


def extract_years_of_experience(text):
    """Extract years of experience from text"""
    patterns = [
        r'(\d+)\s*(?:years?|yrs?)\s+(?:of\s+)?(?:experience|exp)',
        r'(?:experience|exp).*?(\d+)\s*(?:years?|yrs?)',
        r'total experience.*?(\d+)\s*(?:year|yrs?)'
    ]
    
    text_lower = text.lower()
    for pattern in patterns:
        match = re.search(pattern, text_lower)
        if match:
            try:
                return float(match.group(1))
            except:
                pass
    
    return 0.0


def parse_resume_text(resume_text):
    """
    Parse resume text and extract key information
    Returns: dict with extracted data
    """
    
    result = {
        'skills': extract_skills_from_text(resume_text),
        'years_of_experience': extract_years_of_experience(resume_text),
        'education': extract_education(resume_text),
        'current_role': extract_role(resume_text)
    }
    
    result['experience_level'] = estimate_experience_level(
        resume_text, 
        result['years_of_experience']
    )
    
    return result


def extract_education(text):
    """Extract education from resume"""
    patterns = [
        r'(?:bachelor|b\.?s\.?|bs)',
        r'(?:master|m\.?s\.?|ms)',
        r'(?:phd|ph\.?d\.?)',
        r'(?:diploma|certification)',
    ]
    
    text_lower = text.lower()
    for pattern in patterns:
        if re.search(pattern, text_lower):
            # Extract the degree and possible field
            section = re.search(pattern + r'[^,\n]*(?:in|of)?[^,\n]*', text_lower)
            if section:
                return section.group(0).title()
    
    return "Not specified"


def extract_role(text):
    """Extract current/last role from resume"""
    # Look for common job titles
    titles = [
        'software engineer', 'data scientist', 'web developer', 'devops engineer',
        'cloud engineer', 'ai engineer', 'machine learning engineer', 'senior developer',
        'junior developer', 'full stack developer', 'frontend developer', 'backend developer'
    ]
    
    text_lower = text.lower()
    for title in titles:
        if title in text_lower:
            return title.title()
    
    return "Not specified"


def parse_pdf_resume(file_path):
    """
    Parse PDF resume (requires pdfplumber or PyPDF2)
    For now, returns empty - can be enhanced later
    """
    # Prefer pdfplumber for better layout extraction, fallback to PyPDF2
    try:
        import pdfplumber
        with pdfplumber.open(file_path) as pdf:
            text = ''
            for page in pdf.pages:
                page_text = page.extract_text() or ''
                text += page_text + '\n'
            return parse_resume_text(text)
    except Exception:
        try:
            from PyPDF2 import PdfReader
            reader = PdfReader(file_path)
            text = ''
            for page in reader.pages:
                page_text = page.extract_text() or ''
                text += page_text + '\n'
            return parse_resume_text(text)
        except Exception:
            return {'skills': [], 'years_of_experience': 0, 'education': 'Not available', 'current_role': 'Not available', 'experience_level': 'beginner'}


def parse_txt_resume(file_path):
    """Parse plain text resume"""
    try:
        with open(file_path, 'r', encoding='utf-8') as f:
            text = f.read()
        return parse_resume_text(text)
    except Exception as e:
        # Return consistent schema on error
        return {
            'skills': [],
            'years_of_experience': 0,
            'education': 'Not available',
            'current_role': 'Not available',
            'experience_level': 'beginner',
            'error': str(e)
        }
