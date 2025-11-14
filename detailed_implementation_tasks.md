# DETAILED MICRO-TASK BREAKDOWN

## 🎯 **PHASE 1: CORE LLM INTEGRATION (Day 1-2)**

### **Task 1.1: JD Parser LLM Integration (2 hours)**
**File: `modules/jd_parser.py`**

#### Subtask 1.1.1: Import LLM Service (15 mins)
```python
# Add to imports at top of jd_parser.py
from .llm_service import LLMService
```

#### Subtask 1.1.2: Add LLM Analysis Method (45 mins)
```python
def _analyze_with_llm(self, jd_text: str) -> Dict:
    """Use LLM to analyze job description and determine role domain"""
    
    prompt = f"""
Analyze this job description and identify the role domain:

JOB DESCRIPTION:
{jd_text}

Return JSON only:
{{
    "role_domain": "specific domain like Communication Platforms, Fintech, Healthcare Tech, etc",
    "template_recommendation": "communication|fintech|healthcare|security|b2b|b2c|aiml",
    "confidence": 0.95
}}
"""

    try:
        llm_service = LLMService()
        response = llm_service.call_llm(
            prompt=prompt,
            task_type="analysis", 
            max_tokens=500
        )
        
        if response.success:
            import json
            return json.loads(response.content)
        else:
            return self._fallback_analysis()
            
    except Exception as e:
        print(f"LLM analysis failed: {e}")
        return self._fallback_analysis()

def _fallback_analysis(self) -> Dict:
    """Fallback if LLM fails"""
    return {
        'role_domain': 'General Product Management',
        'template_recommendation': 'b2b',
        'confidence': 0.5
    }
```

#### Subtask 1.1.3: Modify Main Parse Method (30 mins)
```python
# In parse() method, add after existing parsing
def parse(self, job_description: str) -> Dict:
    # Existing parsing logic...
    jd_lower = job_description.lower()
    
    base_data = {
        'company': self._extract_company(job_description),
        'role_title': self._extract_role_title(job_description),
        # ... existing fields ...
    }
    
    # NEW: Add LLM analysis
    llm_analysis = self._analyze_with_llm(job_description)
    
    # Merge results
    return {
        **base_data,
        **llm_analysis,
        'llm_enhanced': True
    }
```

#### Subtask 1.1.4: Test JD Parser (30 mins)
```python
# Create test_jd_parser_llm.py
from modules.jd_parser import JobDescriptionParser

squarespace_jd = """At Squarespace..."""
parser = JobDescriptionParser()
result = parser.parse(squarespace_jd)

print(f"Role Domain: {result['role_domain']}")
print(f"Template Rec: {result['template_recommendation']}")
```

### **Task 1.2: Resume Generator Template Logic (1.5 hours)**
**File: `modules/resume_generator.py`**

#### Subtask 1.2.1: Update Variant Determination (30 mins)
```python
# Replace _determine_resume_variant method
def _determine_resume_variant(self, ai_ml_focus: float, business_model: str, required_skills: List[str]) -> str:
    """Enhanced variant selection using LLM analysis if available"""
    
    # Check if we have LLM enhancement
    if hasattr(self, 'current_jd_data') and self.current_jd_data.get('llm_enhanced'):
        template_rec = self.current_jd_data.get('template_recommendation', 'b2b')
        
        # Map LLM recommendations to existing variants
        variant_mapping = {
            'communication': 'communication',
            'fintech': 'fintech', 
            'healthcare': 'healthcare',
            'security': 'security',
            'aiml': 'aiml',
            'b2b': 'b2b',
            'b2c': 'b2c'
        }
        
        mapped_variant = variant_mapping.get(template_rec, 'b2b')
        print(f"LLM recommended template: {template_rec} → {mapped_variant}")
        return mapped_variant
    
    # Original logic as fallback
    ai_ml_keywords = ['ai', 'ml', 'machine learning', 'artificial intelligence', 'rag', 'llm']
    ai_ml_in_requirements = any(skill.lower() in ' '.join(required_skills).lower() 
                               for skill in ai_ml_keywords)
    
    if ai_ml_focus > 0.3 or ai_ml_in_requirements:
        return 'aiml'
    elif business_model == 'b2b':
        return 'b2b'
    elif business_model == 'b2c':
        return 'b2c'
    else:
        return 'b2b'
```

#### Subtask 1.2.2: Store JD Data in Generator (15 mins)
```python
# In generate() method, store jd_data for variant determination
def generate(self, jd_data: Dict, country: str) -> Tuple[str, List[str]]:
    self.current_jd_data = jd_data  # Store for variant determination
    
    changes_made = []
    # ... rest of existing logic
```

#### Subtask 1.2.3: Add Communication Template (45 mins)
```python
# In _generate_optimized_summary method, add new elif block
def _generate_optimized_summary(self, jd_data: Dict, variant: str, country: str) -> str:
    base_summary = self.user_profile['summary']
    
    if variant == 'communication':
        summary = f"""Senior Product Manager with 7+ years specializing in **communication platforms, messaging infrastructure, and API-driven systems** serving enterprise customers. Built automated messaging workflows processing **2M+ notifications monthly**, integrated with external communication partners (Twilio, SendGrid), and managed **scalable messaging platforms** serving 600K+ users with 99.9% delivery reliability. Expert in **email/SMS systems, lifecycle messaging automation, external partner integrations**, cross-functional collaboration to deliver compliant, resilient communication tools."""
    
    elif variant == 'aiml':
        # Existing AI/ML template...
    
    elif variant == 'b2b':
        # Existing B2B template...
    
    # ... rest of existing logic
```

### **Task 1.3: Testing & Validation (1 hour)**

#### Subtask 1.3.1: Create Comprehensive Test (30 mins)
```python
# Create test_llm_integration.py
def test_squarespace_classification():
    squarespace_jd = """At Squarespace, we empower product teams..."""
    
    # Test JD Parser
    parser = JobDescriptionParser()
    jd_data = parser.parse(squarespace_jd)
    
    assert jd_data['llm_enhanced'] == True
    assert 'communication' in jd_data['role_domain'].lower()
    assert jd_data['template_recommendation'] == 'communication'
    
    # Test Resume Generator
    generator = ResumeGenerator()  
    resume, changes = generator.generate(jd_data, 'portugal')
    
    assert 'communication platforms' in resume.lower()
    assert 'messaging infrastructure' in resume.lower()
    
    print("✅ Squarespace test passed!")

def test_ai_ml_classification():
    ai_jd = """We're looking for a Product Manager to lead our AI/ML initiatives..."""
    # Similar test for AI/ML role
    
def test_fallback_logic():
    # Test what happens when LLM fails
    pass
```

#### Subtask 1.3.2: Manual Verification (30 mins)
```bash
# Run tests
python test_llm_integration.py

# Generate actual application
python main.py
# Input: Squarespace JD
# Verify: Should now generate communication-focused resume
```

## 🎯 **PHASE 2: TEMPLATE EXPANSION (Day 3-4)**

### **Task 2.1: Add Fintech Template (1 hour)**
```python
elif variant == 'fintech':
    summary = f"""Senior Product Manager with 7+ years specializing in **payment systems, financial infrastructure, and fintech platforms**. Built automated payment workflows processing **$2M+ in transactions**, integrated with financial partners and payment gateways, and managed **scalable payment platforms** serving 600K+ users with 99.9% uptime. Expert in **payment processing, financial compliance, API integrations**, cross-functional collaboration to deliver secure, compliant financial products."""
```

### **Task 2.2: Add Healthcare Template (1 hour)**
### **Task 2.3: Add Security Template (1 hour)**
### **Task 2.4: Add Developer Tools Template (1 hour)**

## 🎯 **PHASE 3: OPTIMIZATION (Day 5)**

### **Task 3.1: Add Response Caching (1 hour)**
```python
def _analyze_with_llm(self, jd_text: str) -> Dict:
    # Generate cache key
    import hashlib
    cache_key = hashlib.md5(jd_text.encode()).hexdigest()[:16]
    
    # Check cache
    cache_file = Path("cache/jd_analysis.json")
    if cache_file.exists():
        with open(cache_file) as f:
            cache = json.load(f)
            if cache_key in cache:
                return cache[cache_key]
    
    # Call LLM
    result = self._call_llm_analysis(jd_text)
    
    # Save to cache
    cache[cache_key] = result
    cache_file.parent.mkdir(exist_ok=True)
    with open(cache_file, 'w') as f:
        json.dump(cache, f)
        
    return result
```

### **Task 3.2: Add Cost Monitoring (30 mins)**
```python
def track_llm_usage(self, tokens_used: int, cost: float):
    usage_file = Path("logs/llm_usage.json")
    # Track usage and costs
```

### **Task 3.3: Add Error Handling & Logging (30 mins)**

## 🚨 **AGENTS & ARCHITECTURE**

### **No Additional Agents Needed** ❌
- Current system already has agent framework (simulated)
- We're only adding ONE real LLM call to JD parser
- Keep existing agent simulation for content generation

### **Why No Additional Agents:**
1. **Cost Control**: Each agent = additional LLM calls = higher costs
2. **Simplicity**: One targeted fix is easier to debug/maintain  
3. **Risk Mitigation**: Minimal changes reduce chance of breaking existing functionality
4. **Existing Templates Work**: Your predefined templates are good quality

## ⏱️ **TIMELINE SUMMARY**
- **Day 1-2**: Core LLM integration (4 hours)
- **Day 3-4**: Template expansion (4 hours) 
- **Day 5**: Optimization & testing (2 hours)
- **Total**: 10 hours of focused work

## 🎯 **SUCCESS CRITERIA**
1. ✅ Squarespace JD correctly identifies as "Communication Platforms"
2. ✅ Generates communication-focused resume (not AI/ML)
3. ✅ Cost under $0.01 per application  
4. ✅ No breaking changes to existing API
5. ✅ Graceful fallback when LLM fails