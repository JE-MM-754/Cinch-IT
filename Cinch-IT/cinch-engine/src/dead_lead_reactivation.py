"""
CinchIT AI Sales Engine - Dead Lead Reactivation Module
AI-powered system to identify and re-engage dormant prospects
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

# Configure logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

class LeadStatus(Enum):
    COLD = "cold"
    WARM = "warm"
    HOT = "hot"
    DEAD = "dead"
    REACTIVATED = "reactivated"
    UNQUALIFIED = "unqualified"

class ReactivationReason(Enum):
    TIMING_CHANGE = "timing_change"
    NEW_DECISION_MAKER = "new_decision_maker"
    COMPANY_GROWTH = "company_growth"
    NEW_FUNDING = "new_funding"
    INDUSTRY_TRIGGER = "industry_trigger"
    COMPETITIVE_PRESSURE = "competitive_pressure"
    TECHNOLOGY_EVOLUTION = "technology_evolution"
    SEASONAL_OPPORTUNITY = "seasonal_opportunity"

@dataclass
class LeadProfile:
    """Comprehensive lead profile for reactivation analysis"""
    lead_id: str
    company_name: str
    contact_name: str
    email: str
    phone: Optional[str]
    title: str
    industry: str
    company_size: str
    last_contact_date: str
    last_interaction_type: str
    original_pain_points: List[str]
    decision_timeline: str
    budget_range: str
    stakeholders: List[str]
    competitor_mentions: List[str]
    engagement_history: List[Dict]
    lead_source: str
    current_status: str
    notes: str

@dataclass
class ReactivationSignal:
    """Data structure for reactivation opportunity signals"""
    signal_type: ReactivationReason
    signal_strength: float  # 0-1 confidence score
    detected_date: str
    source: str
    description: str
    actionable_insight: str
    recommended_approach: str
    urgency_score: int  # 1-10 scale

@dataclass
class ReactivationCampaign:
    """Reactivation campaign configuration"""
    campaign_id: str
    lead_id: str
    signals: List[ReactivationSignal]
    personalization_data: Dict
    message_sequence: List[Dict]
    timing_strategy: str
    success_metrics: Dict
    status: str
    created_date: str

class DeadLeadReactivation:
    """AI-powered dead lead reactivation system"""
    
    def __init__(self):
        self.openai_api_key = os.getenv('OPENAI_API_KEY')
        self.crunchbase_api_key = os.getenv('CRUNCHBASE_API_KEY')
        self.news_api_key = os.getenv('NEWS_API_KEY')
        
        # Scoring weights for different signals
        self.signal_weights = {
            ReactivationReason.NEW_FUNDING: 0.9,
            ReactivationReason.NEW_DECISION_MAKER: 0.8,
            ReactivationReason.COMPANY_GROWTH: 0.7,
            ReactivationReason.COMPETITIVE_PRESSURE: 0.6,
            ReactivationReason.INDUSTRY_TRIGGER: 0.5,
            ReactivationReason.TIMING_CHANGE: 0.4,
            ReactivationReason.TECHNOLOGY_EVOLUTION: 0.4,
            ReactivationReason.SEASONAL_OPPORTUNITY: 0.3
        }
    
    def analyze_dead_leads(self, leads: List[LeadProfile]) -> List[Tuple[LeadProfile, List[ReactivationSignal]]]:
        """Analyze dead leads for reactivation opportunities"""
        logger.info(f"Analyzing {len(leads)} dead leads for reactivation signals")
        
        reactivation_opportunities = []
        
        for lead in leads:
            signals = self._detect_reactivation_signals(lead)
            
            # Filter for high-confidence signals
            high_confidence_signals = [s for s in signals if s.signal_strength >= 0.6]
            
            if high_confidence_signals:
                reactivation_opportunities.append((lead, high_confidence_signals))
                logger.info(f"Found {len(high_confidence_signals)} signals for {lead.company_name}")
        
        # Sort by total signal strength
        reactivation_opportunities.sort(
            key=lambda x: sum(s.signal_strength for s in x[1]), 
            reverse=True
        )
        
        return reactivation_opportunities
    
    def _detect_reactivation_signals(self, lead: LeadProfile) -> List[ReactivationSignal]:
        """Detect various reactivation signals for a lead"""
        signals = []
        
        # Check for funding announcements
        funding_signal = self._check_funding_signals(lead)
        if funding_signal:
            signals.append(funding_signal)
        
        # Check for leadership changes
        leadership_signal = self._check_leadership_changes(lead)
        if leadership_signal:
            signals.append(leadership_signal)
        
        # Check for company growth indicators
        growth_signal = self._check_growth_signals(lead)
        if growth_signal:
            signals.append(growth_signal)
        
        # Check for industry/market triggers
        industry_signal = self._check_industry_triggers(lead)
        if industry_signal:
            signals.append(industry_signal)
        
        # Check for timing-based opportunities
        timing_signal = self._check_timing_opportunities(lead)
        if timing_signal:
            signals.append(timing_signal)
        
        # Check for competitive pressure
        competitive_signal = self._check_competitive_pressure(lead)
        if competitive_signal:
            signals.append(competitive_signal)
        
        return signals
    
    def _check_funding_signals(self, lead: LeadProfile) -> Optional[ReactivationSignal]:
        """Check for recent funding announcements"""
        try:
            # Mock implementation - would integrate with Crunchbase API
            # In real implementation, query funding databases
            
            # Simulate funding check
            company_keywords = [lead.company_name.lower(), lead.company_name.replace(' ', '').lower()]
            
            # This would be replaced with actual Crunchbase API call
            recent_funding = self._mock_funding_check(lead.company_name)
            
            if recent_funding:
                return ReactivationSignal(
                    signal_type=ReactivationReason.NEW_FUNDING,
                    signal_strength=0.85,
                    detected_date=datetime.now().isoformat(),
                    source="funding_database",
                    description=f"{lead.company_name} secured {recent_funding['amount']} in {recent_funding['round']} funding",
                    actionable_insight="New funding indicates budget availability and growth plans",
                    recommended_approach="Congratulate on funding and position solution for scaling needs",
                    urgency_score=8
                )
        except Exception as e:
            logger.error(f"Error checking funding signals for {lead.company_name}: {e}")
        
        return None
    
    def _check_leadership_changes(self, lead: LeadProfile) -> Optional[ReactivationSignal]:
        """Check for leadership changes that might affect decision making"""
        try:
            # Mock implementation - would integrate with LinkedIn or news APIs
            leadership_change = self._mock_leadership_check(lead.company_name, lead.title)
            
            if leadership_change:
                return ReactivationSignal(
                    signal_type=ReactivationReason.NEW_DECISION_MAKER,
                    signal_strength=0.75,
                    detected_date=datetime.now().isoformat(),
                    source="leadership_tracking",
                    description=f"New {leadership_change['role']} appointed at {lead.company_name}",
                    actionable_insight="New leadership may reassess existing vendor relationships",
                    recommended_approach="Introduce solution to new decision maker",
                    urgency_score=7
                )
        except Exception as e:
            logger.error(f"Error checking leadership changes for {lead.company_name}: {e}")
        
        return None
    
    def _check_growth_signals(self, lead: LeadProfile) -> Optional[ReactivationSignal]:
        """Check for company growth indicators"""
        try:
            # Check for growth indicators (headcount, office expansion, etc.)
            growth_indicators = self._mock_growth_check(lead.company_name)
            
            if growth_indicators and growth_indicators['growth_score'] > 0.6:
                return ReactivationSignal(
                    signal_type=ReactivationReason.COMPANY_GROWTH,
                    signal_strength=growth_indicators['growth_score'],
                    detected_date=datetime.now().isoformat(),
                    source="growth_tracking",
                    description=growth_indicators['description'],
                    actionable_insight="Company growth creates new operational challenges",
                    recommended_approach="Focus on scalability benefits of solution",
                    urgency_score=6
                )
        except Exception as e:
            logger.error(f"Error checking growth signals for {lead.company_name}: {e}")
        
        return None
    
    def _check_industry_triggers(self, lead: LeadProfile) -> Optional[ReactivationSignal]:
        """Check for industry-wide events that could create urgency"""
        try:
            # Check for industry-specific triggers
            industry_events = self._mock_industry_check(lead.industry)
            
            if industry_events and industry_events['relevance_score'] > 0.5:
                return ReactivationSignal(
                    signal_type=ReactivationReason.INDUSTRY_TRIGGER,
                    signal_strength=industry_events['relevance_score'],
                    detected_date=datetime.now().isoformat(),
                    source="industry_monitoring",
                    description=industry_events['description'],
                    actionable_insight=industry_events['business_impact'],
                    recommended_approach="Connect industry trends to solution value",
                    urgency_score=5
                )
        except Exception as e:
            logger.error(f"Error checking industry triggers for {lead.industry}: {e}")
        
        return None
    
    def _check_timing_opportunities(self, lead: LeadProfile) -> Optional[ReactivationSignal]:
        """Check for timing-based reactivation opportunities"""
        try:
            last_contact = datetime.fromisoformat(lead.last_contact_date.replace('Z', '+00:00'))
            months_since_contact = (datetime.now() - last_contact).days / 30
            
            # Different timing strategies based on original context
            if lead.decision_timeline == "next_quarter" and months_since_contact >= 3:
                return ReactivationSignal(
                    signal_type=ReactivationReason.TIMING_CHANGE,
                    signal_strength=0.6,
                    detected_date=datetime.now().isoformat(),
                    source="timing_analysis",
                    description=f"Original timeline of 'next quarter' has passed ({months_since_contact:.1f} months ago)",
                    actionable_insight="Decision timeline may have shifted, new budget cycle",
                    recommended_approach="Check if circumstances have changed since original conversation",
                    urgency_score=4
                )
            
            elif lead.decision_timeline == "next_year" and months_since_contact >= 12:
                return ReactivationSignal(
                    signal_type=ReactivationReason.TIMING_CHANGE,
                    signal_strength=0.7,
                    detected_date=datetime.now().isoformat(),
                    source="timing_analysis",
                    description="Original 'next year' timeline has arrived",
                    actionable_insight="Previously discussed timeline has arrived",
                    recommended_approach="Follow up on previously discussed implementation plans",
                    urgency_score=6
                )
        except Exception as e:
            logger.error(f"Error checking timing opportunities for {lead.company_name}: {e}")
        
        return None
    
    def _check_competitive_pressure(self, lead: LeadProfile) -> Optional[ReactivationSignal]:
        """Check for competitive pressure that might create urgency"""
        try:
            # Check news for competitor mentions and market pressure
            competitive_events = self._mock_competitive_check(lead.industry, lead.competitor_mentions)
            
            if competitive_events and competitive_events['pressure_score'] > 0.6:
                return ReactivationSignal(
                    signal_type=ReactivationReason.COMPETITIVE_PRESSURE,
                    signal_strength=competitive_events['pressure_score'],
                    detected_date=datetime.now().isoformat(),
                    source="competitive_intelligence",
                    description=competitive_events['description'],
                    actionable_insight="Competitive pressure may create urgency for solution adoption",
                    recommended_approach="Highlight competitive advantages and speed to value",
                    urgency_score=7
                )
        except Exception as e:
            logger.error(f"Error checking competitive pressure for {lead.company_name}: {e}")
        
        return None
    
    def create_reactivation_campaign(self, lead: LeadProfile, signals: List[ReactivationSignal]) -> ReactivationCampaign:
        """Create personalized reactivation campaign based on signals"""
        campaign_id = f"reactivation_{lead.lead_id}_{int(time.time())}"
        
        # Sort signals by strength and urgency
        signals.sort(key=lambda x: (x.signal_strength, x.urgency_score), reverse=True)
        primary_signal = signals[0]
        
        # Generate personalized messaging
        personalization_data = {
            'contact_name': lead.contact_name,
            'company_name': lead.company_name,
            'title': lead.title,
            'primary_signal': primary_signal.description,
            'original_pain_points': lead.original_pain_points,
            'last_interaction': lead.last_interaction_type,
            'industry': lead.industry
        }
        
        # Create message sequence based on primary signal
        message_sequence = self._generate_message_sequence(lead, primary_signal, signals)
        
        # Determine timing strategy
        timing_strategy = self._determine_timing_strategy(primary_signal, signals)
        
        return ReactivationCampaign(
            campaign_id=campaign_id,
            lead_id=lead.lead_id,
            signals=signals,
            personalization_data=personalization_data,
            message_sequence=message_sequence,
            timing_strategy=timing_strategy,
            success_metrics={
                'target_response_rate': 0.15,
                'target_meeting_rate': 0.08,
                'target_pipeline_value': 50000
            },
            status="ready_to_launch",
            created_date=datetime.now().isoformat()
        )
    
    def _generate_message_sequence(self, lead: LeadProfile, primary_signal: ReactivationSignal, all_signals: List[ReactivationSignal]) -> List[Dict]:
        """Generate personalized message sequence for reactivation"""
        
        # Base templates for different signal types
        templates = {
            ReactivationReason.NEW_FUNDING: [
                {
                    "sequence": 1,
                    "channel": "email",
                    "timing": "immediate",
                    "subject": "Congratulations on the funding, {contact_name}!",
                    "template": "funding_congratulations",
                    "personalization": ["funding_amount", "growth_plans"]
                },
                {
                    "sequence": 2,
                    "channel": "linkedin",
                    "timing": "3_days",
                    "template": "scaling_challenges",
                    "personalization": ["original_pain_points", "scaling_context"]
                }
            ],
            ReactivationReason.NEW_DECISION_MAKER: [
                {
                    "sequence": 1,
                    "channel": "email",
                    "timing": "immediate",
                    "subject": "Introduction and our previous conversation",
                    "template": "new_stakeholder_intro",
                    "personalization": ["previous_discussion", "company_context"]
                }
            ],
            ReactivationReason.TIMING_CHANGE: [
                {
                    "sequence": 1,
                    "channel": "email",
                    "timing": "immediate",
                    "subject": "Following up on {company_name}'s {original_timeline}",
                    "template": "timing_follow_up",
                    "personalization": ["original_timeline", "current_priorities"]
                }
            ]
        }
        
        # Get template for primary signal type
        base_sequence = templates.get(primary_signal.signal_type, templates[ReactivationReason.TIMING_CHANGE])
        
        # Add personalization data to each message
        for message in base_sequence:
            message['signal_context'] = primary_signal.actionable_insight
            message['recommended_approach'] = primary_signal.recommended_approach
            message['urgency_score'] = primary_signal.urgency_score
        
        return base_sequence
    
    def _determine_timing_strategy(self, primary_signal: ReactivationSignal, all_signals: List[ReactivationSignal]) -> str:
        """Determine optimal timing strategy based on signal urgency"""
        max_urgency = max(signal.urgency_score for signal in all_signals)
        
        if max_urgency >= 8:
            return "immediate_outreach"
        elif max_urgency >= 6:
            return "within_24_hours"
        elif max_urgency >= 4:
            return "within_week"
        else:
            return "monthly_nurture"
    
    def score_reactivation_opportunity(self, lead: LeadProfile, signals: List[ReactivationSignal]) -> float:
        """Score the overall reactivation opportunity for prioritization"""
        if not signals:
            return 0.0
        
        # Weighted signal score
        signal_score = sum(
            signal.signal_strength * self.signal_weights.get(signal.signal_type, 0.5)
            for signal in signals
        ) / len(signals)
        
        # Urgency multiplier
        max_urgency = max(signal.urgency_score for signal in signals) / 10
        
        # Lead quality factors
        lead_quality_factors = {
            'enterprise': 1.2,
            'mid-market': 1.0,
            'smb': 0.8
        }
        size_multiplier = lead_quality_factors.get(lead.company_size.lower(), 1.0)
        
        # Engagement history factor
        engagement_factor = min(1.5, len(lead.engagement_history) / 10 + 0.5)
        
        final_score = signal_score * max_urgency * size_multiplier * engagement_factor
        return min(1.0, final_score)  # Cap at 1.0
    
    # Mock functions for external data sources (replace with real integrations)
    def _mock_funding_check(self, company_name: str) -> Optional[Dict]:
        """Mock funding check - replace with Crunchbase API"""
        # Simulate 15% chance of recent funding
        import random
        if random.random() < 0.15:
            return {
                'amount': '$10M',
                'round': 'Series B',
                'date': '2026-01-15'
            }
        return None
    
    def _mock_leadership_check(self, company_name: str, title: str) -> Optional[Dict]:
        """Mock leadership change check"""
        import random
        if random.random() < 0.10:  # 10% chance
            return {
                'role': 'Chief Technology Officer',
                'name': 'Jane Smith',
                'date': '2026-02-01'
            }
        return None
    
    def _mock_growth_check(self, company_name: str) -> Optional[Dict]:
        """Mock growth indicators check"""
        import random
        growth_score = random.random()
        if growth_score > 0.6:
            return {
                'growth_score': growth_score,
                'description': f"{company_name} expanded team by 25% in Q4",
                'indicators': ['headcount_growth', 'office_expansion']
            }
        return None
    
    def _mock_industry_check(self, industry: str) -> Optional[Dict]:
        """Mock industry trigger check"""
        import random
        relevance = random.random()
        if relevance > 0.5:
            return {
                'relevance_score': relevance,
                'description': f"New regulations affecting {industry} industry",
                'business_impact': 'Companies need to update compliance systems'
            }
        return None
    
    def _mock_competitive_check(self, industry: str, competitors: List[str]) -> Optional[Dict]:
        """Mock competitive pressure check"""
        import random
        pressure_score = random.random()
        if pressure_score > 0.6:
            return {
                'pressure_score': pressure_score,
                'description': f"Major competitor launched new product in {industry} space",
                'urgency_factor': 'high'
            }
        return None

# Utility functions for sales teams
def quick_dead_lead_analysis(leads_data: List[Dict]) -> Dict:
    """Quick analysis for sales managers to prioritize dead leads"""
    try:
        reactivator = DeadLeadReactivation()
        
        # Convert dict data to LeadProfile objects
        leads = []
        for lead_data in leads_data:
            lead = LeadProfile(**lead_data)
            leads.append(lead)
        
        # Analyze for reactivation opportunities
        opportunities = reactivator.analyze_dead_leads(leads)
        
        # Generate summary report
        total_leads = len(leads)
        reactivatable_leads = len(opportunities)
        
        # Priority scoring
        scored_opportunities = []
        for lead, signals in opportunities:
            score = reactivator.score_reactivation_opportunity(lead, signals)
            scored_opportunities.append({
                'lead_id': lead.lead_id,
                'company_name': lead.company_name,
                'contact_name': lead.contact_name,
                'reactivation_score': round(score, 3),
                'signal_count': len(signals),
                'top_signal': signals[0].signal_type.value if signals else None,
                'urgency': max(s.urgency_score for s in signals) if signals else 0,
                'recommended_timing': reactivator._determine_timing_strategy(signals[0], signals) if signals else 'low_priority'
            })
        
        return {
            'summary': {
                'total_dead_leads': total_leads,
                'reactivatable_leads': reactivatable_leads,
                'reactivation_rate': round(reactivatable_leads / total_leads * 100, 1) if total_leads > 0 else 0
            },
            'priority_leads': sorted(scored_opportunities, key=lambda x: x['reactivation_score'], reverse=True)[:10],
            'signal_distribution': {
                signal.value: sum(1 for _, signals in opportunities for signal in signals if signal.signal_type == signal)
                for signal in ReactivationReason
            },
            'urgency_breakdown': {
                'immediate': len([o for o in scored_opportunities if o['urgency'] >= 8]),
                'high': len([o for o in scored_opportunities if 6 <= o['urgency'] < 8]),
                'medium': len([o for o in scored_opportunities if 4 <= o['urgency'] < 6]),
                'low': len([o for o in scored_opportunities if o['urgency'] < 4])
            }
        }
    except Exception as e:
        logger.error(f"Error in quick dead lead analysis: {e}")
        return {
            'error': str(e),
            'summary': {'total_dead_leads': 0, 'reactivatable_leads': 0}
        }

if __name__ == "__main__":
    # Example usage
    sample_leads = [
        {
            'lead_id': 'L001',
            'company_name': 'TechCorp',
            'contact_name': 'John Smith',
            'email': 'john.smith@techcorp.com',
            'phone': '+1-555-0123',
            'title': 'VP Engineering',
            'industry': 'Software',
            'company_size': 'mid-market',
            'last_contact_date': '2025-08-15T10:00:00Z',
            'last_interaction_type': 'demo_call',
            'original_pain_points': ['manual_processes', 'scalability'],
            'decision_timeline': 'next_quarter',
            'budget_range': '$50k-100k',
            'stakeholders': ['VP Engineering', 'CTO'],
            'competitor_mentions': ['CompetitorX'],
            'engagement_history': [
                {'date': '2025-08-01', 'type': 'email_open'},
                {'date': '2025-08-15', 'type': 'demo_attended'}
            ],
            'lead_source': 'webinar',
            'current_status': 'dead',
            'notes': 'Timing not right, revisit in Q1'
        }
    ]
    
    result = quick_dead_lead_analysis(sample_leads)
    print(json.dumps(result, indent=2))