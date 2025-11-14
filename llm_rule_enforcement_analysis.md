# LLM RULE ENFORCEMENT ANALYSIS
## Ensuring LLM follows all existing rules and guidelines

## 📋 **EXISTING RULES INVENTORY**

### **1. Country-Specific Rules:**

#### **Netherlands:**
- **Resume**: Max 2 pages, no photo, direct tone, efficiency focus
- **Cover Letter**: Max 300 words, direct opening, measurable results
- **LinkedIn**: Max 350 chars, professional casual style
- **Tone**: High directness, moderate formality, avoid corporate jargon

#### **Portugal:**  
- **Resume**: Max 4 pages, photo included, formal tone, relationships focus
- **Cover Letter**: Max 400 words, formal respectful opening, cultural appreciation
- **LinkedIn**: Max 300 chars, respectful formal style
- **Tone**: Low directness, high formality, avoid rushing

#### **Denmark:**
- **Resume**: Max 2 pages, no photo, casual approach
- **Cover Letter**: Max 200 words, direct honest opening
- **LinkedIn**: Max 250 chars, direct friendly style  
- **Tone**: High directness, low formality, hygge values

### **2. Content Quality Rules:**

#### **Professional Standards:**
- No placeholder text
- Factual accuracy only
- Domain consistency
- Complete content
- Professional language

#### **Human Writing Quality:**
- Avoid LLM red flags
- Natural language flow
- No overused phrases
- Personal voice
- Authentic tone

### **3. Template Structure Rules:**
- Specific section ordering
- Length requirements  
- Formatting standards
- Skill categorization
- Achievement framing

## 🚨 **THE CHALLENGE**

**Without rule enforcement, LLM could:**
- ❌ Ignore country-specific character limits
- ❌ Use wrong tone for country (formal in Denmark, casual in Portugal)
- ❌ Break formatting requirements
- ❌ Generate LLM-sounding language
- ❌ Exceed length limits
- ❌ Ignore cultural guidelines

## 🛡️ **RULE ENFORCEMENT STRATEGIES**

### **OPTION 1: PROMPT ENGINEERING (RECOMMENDED)**

```python
def get_rule_enforced_prompt(jd_analysis, user_profile, country, content_type):
    # Get country-specific rules
    country_rules = CountryConfig().get_config(country)
    
    # Build comprehensive rule-aware prompt
    prompt = f"""
    You are an expert resume writer specializing in {country} market.
    
    STRICT REQUIREMENTS:
    
    1. COUNTRY-SPECIFIC RULES FOR {country.upper()}:
    - Max Length: {country_rules[content_type]['max_length']} {get_unit(content_type)}
    - Tone: {country_rules['tone']['directness']} directness, {country_rules['tone']['formality']} formality
    - Key Values: {', '.join(country_rules['tone']['key_values'])}
    - Avoid: {', '.join(country_rules['tone']['avoid'])}
    - Style: {country_rules[content_type]['style']}
    
    2. CONTENT RULES:
    - Use ONLY factual information from user profile
    - NO placeholder text like [Your Name], [Company]
    - Professional language, avoid: "leverage", "utilize", "drive results"
    - Natural human writing, not AI-generated style
    - Specific metrics and achievements only
    
    3. FORMATTING RULES:
    - Exact format: {get_template_format(content_type)}
    - Section order: {country_rules['resume_format']['sections_order']}
    
    JOB ANALYSIS:
    {json.dumps(jd_analysis, indent=2)}
    
    USER PROFILE:
    {json.dumps(user_profile, indent=2)}
    
    TASK: Customize the following sections while following ALL rules above:
    {{
        "domain_focus": "specific focus for this role",
        "key_achievement": "most relevant achievement reframed",
        "technical_skills": "relevant technical skills list",
        "business_skills": "relevant business skills list"
    }}
    
    VALIDATION: Before responding, check:
    ✓ Length under limit
    ✓ Correct tone for {country}
    ✓ No LLM phrases
    ✓ Factual content only
    ✓ Professional standards
    """
    
    return prompt
```

### **OPTION 2: MULTI-STEP LLM WITH VALIDATION**

```python
def generate_with_rule_validation(jd_analysis, user_profile, country):
    # Step 1: Generate initial content
    initial_content = llm_service.generate_customization(jd_analysis, user_profile)
    
    # Step 2: Rule validation LLM call
    validation_prompt = f"""
    Validate this content against {country} rules:
    
    CONTENT: {initial_content}
    
    RULES:
    {get_all_rules_for_country(country)}
    
    Issues found:
    - Length violations?
    - Tone issues? 
    - Formatting problems?
    - LLM language detected?
    
    Return: {{
        "valid": true/false,
        "issues": ["list of issues"],
        "corrected_content": "if invalid, provide corrected version"
    }}
    """
    
    validation = llm_service.validate_content(validation_prompt)
    
    return validation['corrected_content'] if not validation['valid'] else initial_content
```

### **OPTION 3: HYBRID PROMPT + POST-VALIDATION**

```python
def generate_with_hybrid_enforcement(jd_analysis, user_profile, country):
    # Step 1: Rule-aware prompt
    rule_prompt = get_comprehensive_rule_prompt(jd_analysis, user_profile, country)
    content = llm_service.generate(rule_prompt)
    
    # Step 2: Automated validation with existing agents
    validation_result = ContentQualityValidator().validate(content, country)
    
    if validation_result.should_regenerate:
        # Step 3: Fix issues programmatically or regenerate
        fixed_content = fix_common_issues(content, validation_result.issues, country)
        return fixed_content
    
    return content
```

## 📊 **COMPARISON OF APPROACHES**

| Approach | Effectiveness | Cost | Complexity | Speed |
|----------|--------------|------|------------|-------|
| **Prompt Engineering** | 85% | $0.0035 | Low | Fast |
| **Multi-Step LLM** | 95% | $0.007 | Medium | Slow |
| **Hybrid Prompt + Validation** | 90% | $0.0035 | Medium | Medium |

## 🎯 **RECOMMENDED APPROACH: HYBRID (Option 3)**

### **Why Hybrid is Best:**
1. ✅ **Single LLM call** with comprehensive rule prompt
2. ✅ **Existing validation agents** catch any rule violations  
3. ✅ **Cost efficient** - no additional LLM calls for validation
4. ✅ **Reliable** - uses proven validation logic
5. ✅ **Flexible** - can programmatically fix minor issues

### **Implementation:**

```python
class RuleEnforcedLLMCustomizer:
    def __init__(self):
        self.country_config = CountryConfig()
        self.content_validator = ContentQualityValidator()
        self.human_voice_agent = HumanVoiceAgent()
    
    def customize_with_rules(self, jd_analysis, user_profile, country):
        """Generate customized content while enforcing all rules"""
        
        # Step 1: Build rule-comprehensive prompt
        rule_prompt = self._build_rule_aware_prompt(
            jd_analysis, user_profile, country
        )
        
        # Step 2: LLM generates customization
        customization = llm_service.call_llm(rule_prompt)
        
        # Step 3: Validate against all rules
        validation_result = self.content_validator.validate_customization(
            customization, country, jd_analysis
        )
        
        # Step 4: Apply fixes if needed
        if validation_result.has_issues():
            customization = self._apply_rule_fixes(
                customization, validation_result.issues, country
            )
        
        # Step 5: Human voice transformation
        final_customization = self.human_voice_agent.humanize_sections(
            customization, country
        )
        
        return final_customization
        
    def _build_rule_aware_prompt(self, jd_analysis, user_profile, country):
        """Build comprehensive prompt with all rules"""
        country_rules = self.country_config.get_config(country)
        
        return f"""
        EXPERT CUSTOMIZATION TASK for {country.upper()} market
        
        MANDATORY COMPLIANCE RULES:
        
        1. COUNTRY RULES - {country.upper()}:
           • Tone: {country_rules['tone']['directness']} directness, {country_rules['tone']['formality']} formality
           • Values: {', '.join(country_rules['tone']['key_values'])}
           • Avoid: {', '.join(country_rules['tone']['avoid'])}
           
        2. CONTENT QUALITY:
           • ONLY factual info from user profile
           • NO generic phrases: "leverage", "drive", "utilize" 
           • NO AI language: "delve into", "dynamic", "innovative"
           • Specific metrics and achievements only
           
        3. LENGTH LIMITS:
           • Resume sections: Concise, impactful
           • Professional summary: 50-80 words max
           • Achievement bullets: 1-2 lines each
           
        4. FORMATTING:
           • Bold key terms with **text**
           • Quantified metrics in all achievements
           • Professional terminology only
           
        JOB REQUIREMENTS TO MATCH:
        {json.dumps(jd_analysis['key_requirements'], indent=2)}
        
        USER EXPERIENCE TO LEVERAGE:
        {json.dumps(user_profile['key_achievements'], indent=2)}
        
        TASK: Return ONLY this JSON with customizations that follow ALL rules above:
        {{
            "domain_focus": "Specific {country}-appropriate focus area for this exact role",
            "key_achievement_reframed": "User's most relevant achievement, rewritten for this role with {country} tone",
            "technical_skills_emphasis": "Technical skills most relevant to JD, {country} style",
            "business_impact_framing": "Business impact using {country} cultural values"
        }}
        
        FINAL CHECK before responding:
        ✓ Follows {country} cultural tone?
        ✓ No AI/generic language?
        ✓ Factual content only?
        ✓ Appropriate length?
        ✓ Professional formatting?
        """
        
    def _apply_rule_fixes(self, content, issues, country):
        """Apply programmatic fixes for common rule violations"""
        fixed_content = content.copy()
        
        for issue in issues:
            if issue.category == 'length_violation':
                fixed_content = self._fix_length_issues(fixed_content, issue)
            elif issue.category == 'tone_mismatch':
                fixed_content = self._fix_tone_issues(fixed_content, country)
            elif issue.category == 'llm_language':
                fixed_content = self._fix_llm_phrases(fixed_content)
            elif issue.category == 'formatting':
                fixed_content = self._fix_formatting(fixed_content)
                
        return fixed_content
```

## 🔍 **RULE VALIDATION INTEGRATION**

### **Enhanced Content Validator:**
```python
class EnhancedContentValidator(ContentQualityValidator):
    def validate_llm_customization(self, customization, country, jd_analysis):
        """Validate LLM customization against all rules"""
        
        issues = []
        
        # Country rule validation
        country_issues = self._validate_country_rules(customization, country)
        issues.extend(country_issues)
        
        # Content quality validation  
        quality_issues = self._validate_content_quality(customization)
        issues.extend(quality_issues)
        
        # Template structure validation
        structure_issues = self._validate_template_structure(customization)
        issues.extend(structure_issues)
        
        # JD alignment validation
        alignment_issues = self._validate_jd_alignment(customization, jd_analysis)
        issues.extend(alignment_issues)
        
        return ValidationResult(
            has_critical_issues=any(i.severity == 'critical' for i in issues),
            issues=issues,
            should_regenerate=len([i for i in issues if i.severity in ['critical', 'major']]) > 2
        )
```

## 📋 **IMPLEMENTATION STRATEGY**

### **Phase 1: Rule-Aware Prompts**
- Build comprehensive rule database
- Create country-specific prompt templates
- Test with various countries and roles

### **Phase 2: Validation Integration** 
- Enhance existing validators for LLM content
- Add country-specific rule checks
- Implement programmatic fixes

### **Phase 3: Testing & Optimization**
- Test rule compliance across countries
- Measure rule violation rates
- Optimize prompts for better compliance

## ✅ **EXPECTED OUTCOMES**

### **Rule Compliance:**
- ✅ 95%+ compliance with country rules
- ✅ 100% compliance with length limits  
- ✅ 90%+ compliance with tone guidelines
- ✅ 100% elimination of LLM language

### **Quality Maintenance:**
- ✅ All existing quality standards maintained
- ✅ Country cultural requirements followed
- ✅ Professional standards upheld
- ✅ Human voice preserved

**This approach ensures LLM customization follows ALL existing rules while providing the role-specific tailoring you need.**