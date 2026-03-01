"""
CinchIT AI Sales Engine - Competitor Analysis Module
Comprehensive competitive intelligence gathering and analysis
"""

import os
import json
import time
from typing import Dict, List, Optional, Any, Tuple
from dataclasses import dataclass, asdict
from datetime import datetime, timedelta
from enum import Enum
import logging
import requests
from urllib.parse import urlencode, quote

# Configure logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

class CompetitorSize(Enum):
    STARTUP = "startup"
    GROWTH = "growth"
    ESTABLISHED = "established"
    ENTERPRISE = "enterprise"

class ThreatLevel(Enum):
    LOW = "low"
    MEDIUM = "medium"
    HIGH = "high"
    CRITICAL = "critical"

@dataclass
class CompetitorProfile:
    """Comprehensive competitor profile"""
    competitor_id: str
    company_name: str
    website: str
    industry: str
    size: CompetitorSize
    funding_stage: str
    total_funding: str
    employee_count: int
    headquarters: str
    founded_year: int
    key_executives: List[Dict]
    product_portfolio: List[Dict]
    pricing_model: str
    target_market: List[str]
    value_proposition: str
    strengths: List[str]
    weaknesses: List[str]
    threat_level: ThreatLevel
    market_share: float
    last_updated: str

@dataclass
class CompetitiveIntelligence:
    """Competitive intelligence data point"""
    intel_id: str
    competitor_id: str
    intel_type: str
    source: str
    date_collected: str
    title: str
    summary: str
    business_impact: str
    confidence_score: float
    url: Optional[str]
    tags: List[str]

@dataclass
class MarketPosition:
    """Market positioning analysis"""
    competitor_id: str
    positioning_statement: str
    differentiation_factors: List[str]
    competitive_advantages: List[str]
    market_positioning: str  # "leader", "challenger", "follower", "niche"
    customer_segment_focus: List[str]
    pricing_strategy: str
    go_to_market_strategy: str

@dataclass
class BattleCard:
    """Sales battle card for competitive situations"""
    competitor_name: str
    last_updated: str
    quick_facts: Dict
    win_strategies: List[str]
    common_objections: List[Dict]  # objection + response
    competitive_advantages: List[str]
    price_comparison: Dict
    customer_references: List[str]
    sales_plays: List[str]

class CompetitorAnalysis:
    """Comprehensive competitor analysis and intelligence system"""
    
    def __init__(self):
        self.crunchbase_api_key = os.getenv('CRUNCHBASE_API_KEY')
        self.clearbit_api_key = os.getenv('CLEARBIT_API_KEY')
        self.news_api_key = os.getenv('NEWS_API_KEY')
        self.alpha_vantage_api_key = os.getenv('ALPHA_VANTAGE_API_KEY')
        
        # Intelligence sources configuration
        self.intelligence_sources = {
            'news': {'weight': 0.3, 'freshness_weight': 0.4},
            'funding': {'weight': 0.25, 'freshness_weight': 0.3},
            'hiring': {'weight': 0.2, 'freshness_weight': 0.5},
            'product_updates': {'weight': 0.15, 'freshness_weight': 0.6},
            'social_sentiment': {'weight': 0.1, 'freshness_weight': 0.2}
        }
    
    def analyze_competitor(self, company_name: str, deep_analysis: bool = True) -> CompetitorProfile:
        """Comprehensive competitor analysis"""
        logger.info(f"Starting competitor analysis for: {company_name}")
        
        try:
            # Basic company information
            basic_info = self._get_basic_company_info(company_name)
            
            # Funding and financial information
            funding_info = self._get_funding_information(company_name)
            
            # Leadership and team analysis
            leadership_info = self._get_leadership_information(company_name)
            
            # Product and service analysis
            product_info = self._analyze_product_portfolio(company_name)
            
            # Market positioning analysis
            positioning = self._analyze_market_positioning(company_name)
            
            # Threat assessment
            threat_level = self._assess_threat_level(basic_info, funding_info, product_info)
            
            # Determine competitor size
            size = self._determine_competitor_size(funding_info, basic_info.get('employee_count', 0))
            
            return CompetitorProfile(
                competitor_id=f"comp_{company_name.lower().replace(' ', '_')}_{int(time.time())}",
                company_name=company_name,
                website=basic_info.get('website', ''),
                industry=basic_info.get('industry', ''),
                size=size,
                funding_stage=funding_info.get('stage', 'unknown'),
                total_funding=funding_info.get('total_funding', ''),
                employee_count=basic_info.get('employee_count', 0),
                headquarters=basic_info.get('headquarters', ''),
                founded_year=basic_info.get('founded_year', 0),
                key_executives=leadership_info,
                product_portfolio=product_info,
                pricing_model=positioning.get('pricing_strategy', 'unknown'),
                target_market=positioning.get('target_markets', []),
                value_proposition=positioning.get('value_proposition', ''),
                strengths=positioning.get('strengths', []),
                weaknesses=positioning.get('weaknesses', []),
                threat_level=threat_level,
                market_share=self._estimate_market_share(company_name, basic_info),
                last_updated=datetime.now().isoformat()
            )
            
        except Exception as e:
            logger.error(f"Error analyzing competitor {company_name}: {e}")
            return self._create_minimal_profile(company_name, str(e))
    
    def gather_competitive_intelligence(self, competitor_id: str, company_name: str, days_back: int = 30) -> List[CompetitiveIntelligence]:
        """Gather recent competitive intelligence"""
        logger.info(f"Gathering intelligence for {company_name} over last {days_back} days")
        
        intelligence = []
        
        # News and media mentions
        news_intel = self._gather_news_intelligence(company_name, days_back)
        intelligence.extend(news_intel)
        
        # Funding and investment activity
        funding_intel = self._gather_funding_intelligence(company_name, days_back)
        intelligence.extend(funding_intel)
        
        # Hiring and team changes
        hiring_intel = self._gather_hiring_intelligence(company_name, days_back)
        intelligence.extend(hiring_intel)
        
        # Product updates and releases
        product_intel = self._gather_product_intelligence(company_name, days_back)
        intelligence.extend(product_intel)
        
        # Social media sentiment
        social_intel = self._gather_social_intelligence(company_name, days_back)
        intelligence.extend(social_intel)
        
        # Sort by date and confidence
        intelligence.sort(key=lambda x: (x.date_collected, x.confidence_score), reverse=True)
        
        return intelligence
    
    def create_battle_card(self, competitor_profile: CompetitorProfile, intelligence: List[CompetitiveIntelligence]) -> BattleCard:
        """Create sales battle card for competitive situations"""
        logger.info(f"Creating battle card for {competitor_profile.company_name}")
        
        # Extract key information
        quick_facts = {
            'founded': competitor_profile.founded_year,
            'employees': competitor_profile.employee_count,
            'funding': competitor_profile.total_funding,
            'headquarters': competitor_profile.headquarters,
            'threat_level': competitor_profile.threat_level.value
        }
        
        # Generate win strategies based on weaknesses
        win_strategies = self._generate_win_strategies(competitor_profile)
        
        # Common objections and responses
        objections = self._generate_objection_responses(competitor_profile)
        
        # Competitive advantages
        advantages = self._identify_our_advantages(competitor_profile)
        
        # Price comparison (mock - would need actual pricing data)
        price_comparison = self._generate_price_comparison(competitor_profile)
        
        # Sales plays
        sales_plays = self._generate_sales_plays(competitor_profile, intelligence)
        
        return BattleCard(
            competitor_name=competitor_profile.company_name,
            last_updated=datetime.now().isoformat(),
            quick_facts=quick_facts,
            win_strategies=win_strategies,
            common_objections=objections,
            competitive_advantages=advantages,
            price_comparison=price_comparison,
            customer_references=self._get_competitive_references(competitor_profile),
            sales_plays=sales_plays
        )
    
    def track_competitor_movements(self, competitors: List[str], alert_thresholds: Dict) -> List[Dict]:
        """Track and alert on significant competitor movements"""
        logger.info(f"Tracking movements for {len(competitors)} competitors")
        
        alerts = []
        
        for competitor in competitors:
            try:
                # Get recent intelligence
                recent_intel = self.gather_competitive_intelligence(
                    f"comp_{competitor.lower().replace(' ', '_')}", 
                    competitor, 
                    days_back=7
                )
                
                # Check for significant events
                significant_events = self._identify_significant_events(recent_intel, alert_thresholds)
                
                for event in significant_events:
                    alerts.append({
                        'competitor': competitor,
                        'event_type': event['type'],
                        'significance': event['significance'],
                        'description': event['description'],
                        'business_impact': event['business_impact'],
                        'recommended_action': event['recommended_action'],
                        'urgency': event['urgency'],
                        'detected_date': datetime.now().isoformat()
                    })
                    
            except Exception as e:
                logger.error(f"Error tracking {competitor}: {e}")
        
        # Sort by urgency and significance
        alerts.sort(key=lambda x: (x['urgency'], x['significance']), reverse=True)
        
        return alerts
    
    # Intelligence gathering methods
    def _gather_news_intelligence(self, company_name: str, days_back: int) -> List[CompetitiveIntelligence]:
        """Gather news-based competitive intelligence"""
        intelligence = []
        
        try:
            # Mock implementation - would use News API or similar
            news_items = self._mock_news_search(company_name, days_back)
            
            for item in news_items:
                intel = CompetitiveIntelligence(
                    intel_id=f"news_{int(time.time())}_{item['id']}",
                    competitor_id=f"comp_{company_name.lower().replace(' ', '_')}",
                    intel_type="news",
                    source=item['source'],
                    date_collected=item['date'],
                    title=item['title'],
                    summary=item['summary'],
                    business_impact=item['business_impact'],
                    confidence_score=item['confidence'],
                    url=item.get('url'),
                    tags=item['tags']
                )
                intelligence.append(intel)
                
        except Exception as e:
            logger.error(f"Error gathering news intelligence for {company_name}: {e}")
        
        return intelligence
    
    def _gather_funding_intelligence(self, company_name: str, days_back: int) -> List[CompetitiveIntelligence]:
        """Gather funding-related intelligence"""
        intelligence = []
        
        try:
            # Mock implementation - would use Crunchbase API
            funding_events = self._mock_funding_search(company_name, days_back)
            
            for event in funding_events:
                intel = CompetitiveIntelligence(
                    intel_id=f"funding_{int(time.time())}_{event['id']}",
                    competitor_id=f"comp_{company_name.lower().replace(' ', '_')}",
                    intel_type="funding",
                    source="funding_database",
                    date_collected=event['date'],
                    title=f"{company_name} {event['round']} funding",
                    summary=f"Raised {event['amount']} in {event['round']} round",
                    business_impact=event['business_impact'],
                    confidence_score=0.9,
                    url=event.get('url'),
                    tags=['funding', event['round'].lower()]
                )
                intelligence.append(intel)
                
        except Exception as e:
            logger.error(f"Error gathering funding intelligence for {company_name}: {e}")
        
        return intelligence
    
    def _gather_hiring_intelligence(self, company_name: str, days_back: int) -> List[CompetitiveIntelligence]:
        """Gather hiring and team expansion intelligence"""
        intelligence = []
        
        try:
            # Mock implementation - would scrape LinkedIn or use APIs
            hiring_data = self._mock_hiring_search(company_name, days_back)
            
            for hire in hiring_data:
                intel = CompetitiveIntelligence(
                    intel_id=f"hiring_{int(time.time())}_{hire['id']}",
                    competitor_id=f"comp_{company_name.lower().replace(' ', '_')}",
                    intel_type="hiring",
                    source="job_boards",
                    date_collected=hire['date'],
                    title=f"New {hire['role']} hire at {company_name}",
                    summary=hire['summary'],
                    business_impact=hire['business_impact'],
                    confidence_score=0.7,
                    url=hire.get('url'),
                    tags=['hiring', hire['department'].lower()]
                )
                intelligence.append(intel)
                
        except Exception as e:
            logger.error(f"Error gathering hiring intelligence for {company_name}: {e}")
        
        return intelligence
    
    def _gather_product_intelligence(self, company_name: str, days_back: int) -> List[CompetitiveIntelligence]:
        """Gather product updates and releases"""
        intelligence = []
        
        try:
            # Mock implementation - would monitor product blogs, release notes
            product_updates = self._mock_product_search(company_name, days_back)
            
            for update in product_updates:
                intel = CompetitiveIntelligence(
                    intel_id=f"product_{int(time.time())}_{update['id']}",
                    competitor_id=f"comp_{company_name.lower().replace(' ', '_')}",
                    intel_type="product_update",
                    source="product_blog",
                    date_collected=update['date'],
                    title=update['title'],
                    summary=update['summary'],
                    business_impact=update['business_impact'],
                    confidence_score=0.8,
                    url=update.get('url'),
                    tags=update['tags']
                )
                intelligence.append(intel)
                
        except Exception as e:
            logger.error(f"Error gathering product intelligence for {company_name}: {e}")
        
        return intelligence
    
    def _gather_social_intelligence(self, company_name: str, days_back: int) -> List[CompetitiveIntelligence]:
        """Gather social media sentiment and mentions"""
        intelligence = []
        
        try:
            # Mock implementation - would use social media APIs
            social_data = self._mock_social_search(company_name, days_back)
            
            for mention in social_data:
                intel = CompetitiveIntelligence(
                    intel_id=f"social_{int(time.time())}_{mention['id']}",
                    competitor_id=f"comp_{company_name.lower().replace(' ', '_')}",
                    intel_type="social_mention",
                    source=mention['platform'],
                    date_collected=mention['date'],
                    title=f"Social mention on {mention['platform']}",
                    summary=mention['summary'],
                    business_impact=mention['business_impact'],
                    confidence_score=mention['confidence'],
                    url=mention.get('url'),
                    tags=['social', mention['sentiment']]
                )
                intelligence.append(intel)
                
        except Exception as e:
            logger.error(f"Error gathering social intelligence for {company_name}: {e}")
        
        return intelligence
    
    # Analysis and utility methods
    def _assess_threat_level(self, basic_info: Dict, funding_info: Dict, product_info: List) -> ThreatLevel:
        """Assess competitive threat level"""
        threat_score = 0
        
        # Size factor
        employee_count = basic_info.get('employee_count', 0)
        if employee_count > 1000:
            threat_score += 30
        elif employee_count > 100:
            threat_score += 20
        elif employee_count > 20:
            threat_score += 10
        
        # Funding factor
        funding_stage = funding_info.get('stage', 'unknown')
        funding_scores = {
            'series_c': 25, 'series_b': 20, 'series_a': 15, 
            'seed': 10, 'pre_seed': 5
        }
        threat_score += funding_scores.get(funding_stage.lower(), 0)
        
        # Product portfolio breadth
        threat_score += min(25, len(product_info) * 5)
        
        # Market presence
        if basic_info.get('market_presence', 'low') == 'high':
            threat_score += 20
        
        # Determine threat level
        if threat_score >= 80:
            return ThreatLevel.CRITICAL
        elif threat_score >= 60:
            return ThreatLevel.HIGH
        elif threat_score >= 40:
            return ThreatLevel.MEDIUM
        else:
            return ThreatLevel.LOW
    
    def _determine_competitor_size(self, funding_info: Dict, employee_count: int) -> CompetitorSize:
        """Determine competitor size category"""
        funding_stage = funding_info.get('stage', 'unknown').lower()
        
        if employee_count > 500 or funding_stage in ['series_c', 'series_d', 'ipo']:
            return CompetitorSize.ENTERPRISE
        elif employee_count > 100 or funding_stage == 'series_b':
            return CompetitorSize.ESTABLISHED
        elif employee_count > 20 or funding_stage == 'series_a':
            return CompetitorSize.GROWTH
        else:
            return CompetitorSize.STARTUP
    
    def _generate_win_strategies(self, competitor: CompetitorProfile) -> List[str]:
        """Generate strategies to win against this competitor"""
        strategies = []
        
        # Size-based strategies
        if competitor.size == CompetitorSize.STARTUP:
            strategies.extend([
                "Emphasize stability and proven track record",
                "Highlight enterprise-grade security and compliance",
                "Focus on comprehensive support and services"
            ])
        elif competitor.size == CompetitorSize.ENTERPRISE:
            strategies.extend([
                "Emphasize agility and faster implementation",
                "Highlight personalized service and attention",
                "Focus on competitive pricing and value"
            ])
        
        # Weakness-based strategies
        for weakness in competitor.weaknesses:
            if 'pricing' in weakness.lower():
                strategies.append("Lead with cost-effectiveness and ROI")
            elif 'support' in weakness.lower():
                strategies.append("Emphasize superior customer support")
            elif 'integration' in weakness.lower():
                strategies.append("Highlight seamless integration capabilities")
        
        return strategies[:5]  # Top 5 strategies
    
    def _generate_objection_responses(self, competitor: CompetitorProfile) -> List[Dict]:
        """Generate common objections and responses"""
        objections = []
        
        # Standard competitive objections
        if competitor.threat_level in [ThreatLevel.HIGH, ThreatLevel.CRITICAL]:
            objections.append({
                'objection': f"We're already considering {competitor.company_name}",
                'response': f"That's great! {competitor.company_name} is a solid choice. Let me show you how we differentiate...",
                'talking_points': ['unique_value_prop', 'customer_success_story', 'competitive_advantage']
            })
        
        if competitor.size == CompetitorSize.ENTERPRISE:
            objections.append({
                'objection': f"{competitor.company_name} is the market leader",
                'response': "Market leadership doesn't always mean the best fit for your specific needs...",
                'talking_points': ['agility', 'innovation', 'personalized_service']
            })
        
        # Price-related objections
        objections.append({
            'objection': f"{competitor.company_name} has better pricing",
            'response': "Price is important, but total cost of ownership includes implementation, support, and results...",
            'talking_points': ['tco_analysis', 'faster_roi', 'hidden_costs']
        })
        
        return objections
    
    def _identify_our_advantages(self, competitor: CompetitorProfile) -> List[str]:
        """Identify our competitive advantages against this competitor"""
        # This would be customized based on your actual product
        advantages = [
            "Faster implementation time (30% faster setup)",
            "Superior customer support (24/7 availability)",
            "Better ROI (average 40% cost savings)",
            "More flexible pricing models",
            "Stronger integration capabilities"
        ]
        
        # Customize based on competitor weaknesses
        for weakness in competitor.weaknesses:
            if 'slow' in weakness.lower():
                advantages.insert(0, "Rapid deployment and quick time-to-value")
            elif 'complex' in weakness.lower():
                advantages.insert(0, "Intuitive, easy-to-use interface")
        
        return advantages[:5]
    
    # Mock implementations (replace with real integrations)
    def _get_basic_company_info(self, company_name: str) -> Dict:
        """Mock basic company information gathering"""
        return {
            'website': f"www.{company_name.lower().replace(' ', '')}.com",
            'industry': 'Technology',
            'employee_count': 150,
            'headquarters': 'San Francisco, CA',
            'founded_year': 2018,
            'market_presence': 'medium'
        }
    
    def _get_funding_information(self, company_name: str) -> Dict:
        """Mock funding information"""
        return {
            'stage': 'Series_B',
            'total_funding': '$25M',
            'last_round': '$10M',
            'last_round_date': '2025-09-15',
            'investors': ['Acme Ventures', 'Tech Capital']
        }
    
    def _get_leadership_information(self, company_name: str) -> List[Dict]:
        """Mock leadership information"""
        return [
            {'name': 'John CEO', 'title': 'CEO', 'background': 'Former VP at BigTech'},
            {'name': 'Jane CTO', 'title': 'CTO', 'background': 'Ex-Google engineer'}
        ]
    
    def _analyze_product_portfolio(self, company_name: str) -> List[Dict]:
        """Mock product portfolio analysis"""
        return [
            {
                'product': 'Core Platform',
                'category': 'SaaS',
                'target_market': 'Mid-market',
                'pricing_tier': 'premium'
            }
        ]
    
    def _analyze_market_positioning(self, company_name: str) -> Dict:
        """Mock market positioning analysis"""
        return {
            'value_proposition': 'AI-powered automation for modern businesses',
            'target_markets': ['mid-market', 'enterprise'],
            'pricing_strategy': 'value-based',
            'strengths': ['Innovation', 'User experience'],
            'weaknesses': ['Limited integrations', 'Higher price point']
        }
    
    def _estimate_market_share(self, company_name: str, basic_info: Dict) -> float:
        """Mock market share estimation"""
        import random
        return round(random.uniform(0.1, 5.0), 2)
    
    def _mock_news_search(self, company_name: str, days_back: int) -> List[Dict]:
        """Mock news search results"""
        import random
        if random.random() < 0.7:  # 70% chance of news
            return [{
                'id': f"news_{random.randint(1000, 9999)}",
                'title': f"{company_name} announces new product features",
                'summary': f"Recent product update from {company_name} includes new AI capabilities",
                'source': 'TechCrunch',
                'date': (datetime.now() - timedelta(days=random.randint(1, days_back))).isoformat(),
                'business_impact': 'Product enhancement may attract new customers',
                'confidence': 0.8,
                'tags': ['product', 'ai', 'announcement']
            }]
        return []
    
    def _mock_funding_search(self, company_name: str, days_back: int) -> List[Dict]:
        """Mock funding search results"""
        import random
        if random.random() < 0.2:  # 20% chance of funding news
            return [{
                'id': f"funding_{random.randint(1000, 9999)}",
                'round': 'Series B',
                'amount': '$15M',
                'date': (datetime.now() - timedelta(days=random.randint(1, days_back))).isoformat(),
                'business_impact': 'Increased funding will accelerate growth and market expansion',
                'investors': ['VC Firm A', 'VC Firm B']
            }]
        return []
    
    def _mock_hiring_search(self, company_name: str, days_back: int) -> List[Dict]:
        """Mock hiring intelligence"""
        import random
        if random.random() < 0.5:  # 50% chance of hiring activity
            return [{
                'id': f"hire_{random.randint(1000, 9999)}",
                'role': 'VP of Sales',
                'department': 'Sales',
                'date': (datetime.now() - timedelta(days=random.randint(1, days_back))).isoformat(),
                'summary': f"{company_name} hired experienced VP of Sales from competitor",
                'business_impact': 'Sales leadership hire indicates aggressive growth plans'
            }]
        return []
    
    def _mock_product_search(self, company_name: str, days_back: int) -> List[Dict]:
        """Mock product update intelligence"""
        import random
        if random.random() < 0.4:  # 40% chance of product updates
            return [{
                'id': f"product_{random.randint(1000, 9999)}",
                'title': f"{company_name} releases version 2.0",
                'date': (datetime.now() - timedelta(days=random.randint(1, days_back))).isoformat(),
                'summary': 'Major product update with new features and improvements',
                'business_impact': 'Product enhancement may improve competitive position',
                'tags': ['product', 'update', 'features']
            }]
        return []
    
    def _mock_social_search(self, company_name: str, days_back: int) -> List[Dict]:
        """Mock social media intelligence"""
        import random
        if random.random() < 0.6:  # 60% chance of social mentions
            sentiment = random.choice(['positive', 'neutral', 'negative'])
            return [{
                'id': f"social_{random.randint(1000, 9999)}",
                'platform': 'Twitter',
                'date': (datetime.now() - timedelta(days=random.randint(1, days_back))).isoformat(),
                'summary': f"{sentiment.title()} customer feedback about {company_name}",
                'sentiment': sentiment,
                'business_impact': f"{sentiment.title()} sentiment may impact brand perception",
                'confidence': 0.6
            }]
        return []
    
    def _create_minimal_profile(self, company_name: str, error: str) -> CompetitorProfile:
        """Create minimal profile when analysis fails"""
        return CompetitorProfile(
            competitor_id=f"comp_{company_name.lower().replace(' ', '_')}_minimal",
            company_name=company_name,
            website="",
            industry="Unknown",
            size=CompetitorSize.STARTUP,
            funding_stage="unknown",
            total_funding="",
            employee_count=0,
            headquarters="",
            founded_year=0,
            key_executives=[],
            product_portfolio=[],
            pricing_model="unknown",
            target_market=[],
            value_proposition="",
            strengths=[],
            weaknesses=[],
            threat_level=ThreatLevel.LOW,
            market_share=0.0,
            last_updated=datetime.now().isoformat()
        )
    
    def _identify_significant_events(self, intelligence: List[CompetitiveIntelligence], thresholds: Dict) -> List[Dict]:
        """Identify significant competitive events"""
        significant_events = []
        
        for intel in intelligence:
            significance = 0
            
            # Funding events are always significant
            if intel.intel_type == "funding":
                significance = 9
                event = {
                    'type': 'funding_announcement',
                    'significance': significance,
                    'description': intel.summary,
                    'business_impact': intel.business_impact,
                    'recommended_action': 'Review pricing strategy and value proposition',
                    'urgency': 8
                }
                significant_events.append(event)
            
            # High-confidence product updates
            elif intel.intel_type == "product_update" and intel.confidence_score >= 0.8:
                significance = 7
                event = {
                    'type': 'product_release',
                    'significance': significance,
                    'description': intel.summary,
                    'business_impact': intel.business_impact,
                    'recommended_action': 'Analyze new features and update battle cards',
                    'urgency': 6
                }
                significant_events.append(event)
            
            # Key hiring decisions
            elif intel.intel_type == "hiring" and any(role in intel.title.lower() for role in ['ceo', 'cto', 'vp']):
                significance = 6
                event = {
                    'type': 'executive_hire',
                    'significance': significance,
                    'description': intel.summary,
                    'business_impact': intel.business_impact,
                    'recommended_action': 'Research new executive background and strategy changes',
                    'urgency': 5
                }
                significant_events.append(event)
        
        return significant_events
    
    def _generate_price_comparison(self, competitor: CompetitorProfile) -> Dict:
        """Generate price comparison (mock)"""
        return {
            'our_price': '$99/month',
            'competitor_price': '$129/month',
            'value_advantage': 'Lower cost with more features',
            'tco_comparison': '25% lower total cost of ownership'
        }
    
    def _get_competitive_references(self, competitor: CompetitorProfile) -> List[str]:
        """Get customer references for competitive situations"""
        return [
            'Customer A - switched from competitor and saw 30% efficiency gain',
            'Customer B - chose us over competitor for better ROI'
        ]
    
    def _generate_sales_plays(self, competitor: CompetitorProfile, intelligence: List[CompetitiveIntelligence]) -> List[str]:
        """Generate sales plays based on competitive analysis"""
        plays = [
            'Lead with unique value proposition and differentiation',
            'Use customer success stories from competitive wins',
            'Highlight total cost of ownership advantages'
        ]
        
        # Add intelligence-based plays
        for intel in intelligence[:3]:  # Top 3 recent intelligence items
            if intel.intel_type == "product_update":
                plays.append('Position our mature features against their new/unproven ones')
            elif intel.intel_type == "funding":
                plays.append('Emphasize stability vs their need to prove ROI to investors')
        
        return plays

# Utility functions for sales teams
def quick_competitive_overview(competitor_names: List[str]) -> Dict:
    """Quick competitive landscape overview"""
    try:
        analyzer = CompetitorAnalysis()
        
        competitor_profiles = []
        for name in competitor_names:
            profile = analyzer.analyze_competitor(name, deep_analysis=False)
            competitor_profiles.append({
                'name': profile.company_name,
                'threat_level': profile.threat_level.value,
                'size': profile.size.value,
                'funding_stage': profile.funding_stage,
                'employee_count': profile.employee_count,
                'strengths': profile.strengths[:3],  # Top 3
                'weaknesses': profile.weaknesses[:3]  # Top 3
            })
        
        # Threat level distribution
        threat_levels = [p['threat_level'] for p in competitor_profiles]
        threat_distribution = {level: threat_levels.count(level) for level in set(threat_levels)}
        
        return {
            'total_competitors': len(competitor_profiles),
            'threat_distribution': threat_distribution,
            'competitors': sorted(competitor_profiles, key=lambda x: ['low', 'medium', 'high', 'critical'].index(x['threat_level']), reverse=True),
            'analysis_date': datetime.now().isoformat()
        }
    except Exception as e:
        logger.error(f"Error in competitive overview: {e}")
        return {
            'error': str(e),
            'total_competitors': 0
        }

if __name__ == "__main__":
    # Example usage
    competitors = ["Salesforce", "HubSpot", "Pipedrive"]
    overview = quick_competitive_overview(competitors)
    print(json.dumps(overview, indent=2))