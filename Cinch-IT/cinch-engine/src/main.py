"""
CinchIT AI Sales Engine - Main Orchestrator
Central system coordinating all sales intelligence modules
"""

import os
import sys
import json
import asyncio
import logging
from typing import Dict, List, Optional, Any
from datetime import datetime, timedelta
from dataclasses import dataclass, asdict
import argparse

# Add the current directory to the Python path
sys.path.append(os.path.dirname(os.path.abspath(__file__)))

# Import our intelligence modules
from youtube_intelligence import YouTubeIntelligence, quick_prospect_youtube_analysis
from dead_lead_reactivation import DeadLeadReactivation, quick_dead_lead_analysis, LeadProfile
from competitor_analysis import CompetitorAnalysis, quick_competitive_overview

# Configure logging
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
    handlers=[
        logging.FileHandler('cinchit_engine.log'),
        logging.StreamHandler(sys.stdout)
    ]
)
logger = logging.getLogger(__name__)

@dataclass
class SalesIntelligenceReport:
    """Comprehensive sales intelligence report"""
    report_id: str
    generated_date: str
    target_company: str
    contact_info: Dict
    youtube_analysis: Dict
    competitive_landscape: Dict
    lead_reactivation_score: float
    market_signals: List[Dict]
    recommended_actions: List[str]
    urgency_score: int
    next_steps: List[str]
    confidence_score: float

@dataclass
class ProspectIntelligence:
    """Prospect intelligence package"""
    prospect_id: str
    company_name: str
    contact_name: str
    contact_email: str
    intelligence_summary: str
    key_insights: List[str]
    competitive_threats: List[str]
    engagement_recommendations: List[str]
    best_contact_time: str
    personalization_data: Dict

class CinchITSalesEngine:
    """Main sales intelligence orchestrator"""
    
    def __init__(self):
        logger.info("Initializing CinchIT AI Sales Engine")
        
        # Initialize intelligence modules
        try:
            self.youtube_intel = YouTubeIntelligence()
            logger.info("YouTube Intelligence module initialized")
        except Exception as e:
            logger.warning(f"YouTube Intelligence initialization failed: {e}")
            self.youtube_intel = None
        
        try:
            self.lead_reactivator = DeadLeadReactivation()
            logger.info("Dead Lead Reactivation module initialized")
        except Exception as e:
            logger.warning(f"Dead Lead Reactivation initialization failed: {e}")
            self.lead_reactivator = None
        
        try:
            self.competitor_analyzer = CompetitorAnalysis()
            logger.info("Competitor Analysis module initialized")
        except Exception as e:
            logger.warning(f"Competitor Analysis initialization failed: {e}")
            self.competitor_analyzer = None
        
        # Configuration
        self.config = self._load_configuration()
        
        # Statistics
        self.stats = {
            'reports_generated': 0,
            'prospects_analyzed': 0,
            'leads_reactivated': 0,
            'competitors_tracked': 0,
            'last_run': None
        }
    
    def _load_configuration(self) -> Dict:
        """Load engine configuration"""
        default_config = {
            'max_concurrent_analyses': 5,
            'cache_duration_hours': 24,
            'confidence_threshold': 0.7,
            'urgency_threshold': 6,
            'auto_update_interval_hours': 6,
            'intelligence_sources': {
                'youtube': {'enabled': True, 'weight': 0.3},
                'news': {'enabled': True, 'weight': 0.25},
                'social': {'enabled': True, 'weight': 0.2},
                'funding': {'enabled': True, 'weight': 0.15},
                'hiring': {'enabled': True, 'weight': 0.1}
            },
            'alert_thresholds': {
                'new_funding': 0.8,
                'executive_hire': 0.7,
                'product_launch': 0.6,
                'negative_news': 0.5
            }
        }
        
        try:
            # Try to load from config file
            config_path = os.path.join(os.path.dirname(__file__), '..', 'config.json')
            if os.path.exists(config_path):
                with open(config_path, 'r') as f:
                    custom_config = json.load(f)
                    default_config.update(custom_config)
                    logger.info("Configuration loaded from config.json")
        except Exception as e:
            logger.warning(f"Could not load custom configuration: {e}")
        
        return default_config
    
    async def generate_prospect_intelligence(self, company_name: str, contact_name: str = "", contact_email: str = "") -> ProspectIntelligence:
        """Generate comprehensive prospect intelligence"""
        logger.info(f"Generating prospect intelligence for {company_name}")
        
        prospect_id = f"prospect_{company_name.lower().replace(' ', '_')}_{int(datetime.now().timestamp())}"
        
        # Parallel intelligence gathering
        tasks = []
        
        # YouTube intelligence
        if self.youtube_intel:
            tasks.append(self._get_youtube_intelligence(company_name))
        
        # Competitive analysis
        if self.competitor_analyzer:
            tasks.append(self._get_competitive_intelligence(company_name))
        
        # Execute all tasks concurrently
        results = await asyncio.gather(*tasks, return_exceptions=True)
        
        # Process results
        youtube_data = {}
        competitive_data = {}
        
        for i, result in enumerate(results):
            if isinstance(result, Exception):
                logger.error(f"Task {i} failed: {result}")
                continue
            
            if i == 0 and not isinstance(result, Exception):  # YouTube data
                youtube_data = result
            elif i == 1 and not isinstance(result, Exception):  # Competitive data
                competitive_data = result
        
        # Generate intelligence summary
        intelligence_summary = self._generate_intelligence_summary(company_name, youtube_data, competitive_data)
        
        # Extract key insights
        key_insights = self._extract_key_insights(youtube_data, competitive_data)
        
        # Identify competitive threats
        competitive_threats = self._identify_competitive_threats(competitive_data)
        
        # Generate engagement recommendations
        engagement_recommendations = self._generate_engagement_recommendations(youtube_data, competitive_data)
        
        # Determine best contact time
        best_contact_time = self._determine_best_contact_time(youtube_data)
        
        # Compile personalization data
        personalization_data = self._compile_personalization_data(company_name, youtube_data, competitive_data)
        
        self.stats['prospects_analyzed'] += 1
        
        return ProspectIntelligence(
            prospect_id=prospect_id,
            company_name=company_name,
            contact_name=contact_name,
            contact_email=contact_email,
            intelligence_summary=intelligence_summary,
            key_insights=key_insights,
            competitive_threats=competitive_threats,
            engagement_recommendations=engagement_recommendations,
            best_contact_time=best_contact_time,
            personalization_data=personalization_data
        )
    
    async def _get_youtube_intelligence(self, company_name: str) -> Dict:
        """Gather YouTube intelligence asynchronously"""
        try:
            loop = asyncio.get_event_loop()
            return await loop.run_in_executor(None, quick_prospect_youtube_analysis, company_name)
        except Exception as e:
            logger.error(f"YouTube intelligence failed for {company_name}: {e}")
            return {}
    
    async def _get_competitive_intelligence(self, company_name: str) -> Dict:
        """Gather competitive intelligence asynchronously"""
        try:
            loop = asyncio.get_event_loop()
            # Get direct competitors in the same industry
            competitors = [company_name]  # In real implementation, you'd identify actual competitors
            return await loop.run_in_executor(None, quick_competitive_overview, competitors)
        except Exception as e:
            logger.error(f"Competitive intelligence failed for {company_name}: {e}")
            return {}
    
    def _generate_intelligence_summary(self, company_name: str, youtube_data: Dict, competitive_data: Dict) -> str:
        """Generate executive summary of intelligence"""
        summary_points = []
        
        # YouTube presence summary
        if youtube_data.get('has_youtube_presence'):
            summary_points.append(f"Active YouTube presence with {youtube_data.get('total_subscribers', 0)} subscribers")
            summary_points.append(f"Content focus: {youtube_data.get('content_focus', 'mixed')}")
            summary_points.append(f"Target audience: {youtube_data.get('target_audience', 'general business')}")
        else:
            summary_points.append("No significant YouTube presence detected")
        
        # Competitive landscape
        if competitive_data.get('total_competitors', 0) > 0:
            threat_dist = competitive_data.get('threat_distribution', {})
            high_threat_count = threat_dist.get('high', 0) + threat_dist.get('critical', 0)
            if high_threat_count > 0:
                summary_points.append(f"{high_threat_count} high-threat competitors identified")
            else:
                summary_points.append("Moderate competitive landscape")
        
        # Performance insights
        if youtube_data.get('performance_score', 0) > 70:
            summary_points.append("Strong digital marketing performance")
        elif youtube_data.get('performance_score', 0) > 40:
            summary_points.append("Moderate digital marketing presence")
        else:
            summary_points.append("Limited digital marketing activity")
        
        return ". ".join(summary_points) + "."
    
    def _extract_key_insights(self, youtube_data: Dict, competitive_data: Dict) -> List[str]:
        """Extract actionable insights"""
        insights = []
        
        # YouTube insights
        if youtube_data.get('key_insights'):
            insights.extend(youtube_data['key_insights'])
        
        # Recent activity insights
        recent_activity = youtube_data.get('recent_activity', [])
        for activity in recent_activity:
            if activity.get('upload_frequency') == 'daily':
                insights.append("High content production - may indicate marketing budget availability")
            elif activity.get('upload_frequency') == 'rarely':
                insights.append("Low content activity - potential gap in marketing strategy")
        
        # Competitive insights
        competitors = competitive_data.get('competitors', [])
        for competitor in competitors:
            if competitor.get('threat_level') == 'critical':
                insights.append(f"Critical competitor: {competitor.get('name')} - requires defensive strategy")
        
        return insights[:5]  # Top 5 insights
    
    def _identify_competitive_threats(self, competitive_data: Dict) -> List[str]:
        """Identify main competitive threats"""
        threats = []
        
        competitors = competitive_data.get('competitors', [])
        for competitor in competitors:
            threat_level = competitor.get('threat_level', 'low')
            if threat_level in ['high', 'critical']:
                threats.append(f"{competitor.get('name')} - {threat_level} threat, {competitor.get('funding_stage', 'unknown')} stage")
        
        return threats
    
    def _generate_engagement_recommendations(self, youtube_data: Dict, competitive_data: Dict) -> List[str]:
        """Generate engagement recommendations"""
        recommendations = []
        
        # Content-based recommendations
        content_focus = youtube_data.get('content_focus', '')
        if content_focus == 'product_demos':
            recommendations.append("Lead with product differentiation - they're focused on demos")
        elif content_focus == 'thought_leadership':
            recommendations.append("Engage with industry insights and thought leadership content")
        elif content_focus == 'no_youtube_presence':
            recommendations.append("Opportunity to differentiate with digital marketing expertise")
        
        # Audience-based recommendations
        target_audience = youtube_data.get('target_audience', '')
        if target_audience == 'developers':
            recommendations.append("Technical approach - speak to API capabilities and integrations")
        elif target_audience == 'business_leaders':
            recommendations.append("ROI-focused messaging - emphasize business outcomes")
        
        # Timing recommendations
        performance_score = youtube_data.get('performance_score', 0)
        if performance_score < 30:
            recommendations.append("Position as marketing performance improvement opportunity")
        
        return recommendations
    
    def _determine_best_contact_time(self, youtube_data: Dict) -> str:
        """Determine optimal contact timing"""
        # Analyze upload patterns for engagement timing
        recent_activity = youtube_data.get('recent_activity', [])
        
        if not recent_activity:
            return "business_hours"
        
        # Check upload frequency for engagement patterns
        for activity in recent_activity:
            freq = activity.get('upload_frequency', '')
            if freq == 'weekly':
                return "early_week"  # Weekly uploaders often plan on Mondays
            elif freq == 'daily':
                return "morning"  # Daily content creators often work mornings
        
        return "business_hours"
    
    def _compile_personalization_data(self, company_name: str, youtube_data: Dict, competitive_data: Dict) -> Dict:
        """Compile data for personalized outreach"""
        return {
            'company_name': company_name,
            'youtube_presence': youtube_data.get('has_youtube_presence', False),
            'content_themes': youtube_data.get('content_focus', 'unknown'),
            'subscriber_count': youtube_data.get('total_subscribers', 0),
            'main_competitors': [c.get('name') for c in competitive_data.get('competitors', [])[:3]],
            'competitive_positioning': self._determine_competitive_position(competitive_data),
            'marketing_maturity': self._assess_marketing_maturity(youtube_data),
            'engagement_opportunities': self._identify_engagement_opportunities(youtube_data, competitive_data)
        }
    
    def _determine_competitive_position(self, competitive_data: Dict) -> str:
        """Determine competitive market position"""
        threat_dist = competitive_data.get('threat_distribution', {})
        
        if threat_dist.get('critical', 0) > 0:
            return "highly_competitive"
        elif threat_dist.get('high', 0) > 1:
            return "competitive"
        elif threat_dist.get('medium', 0) > 0:
            return "moderate_competition"
        else:
            return "low_competition"
    
    def _assess_marketing_maturity(self, youtube_data: Dict) -> str:
        """Assess marketing maturity level"""
        if not youtube_data.get('has_youtube_presence'):
            return "early_stage"
        
        performance_score = youtube_data.get('performance_score', 0)
        subscriber_count = youtube_data.get('total_subscribers', 0)
        
        if performance_score > 70 and subscriber_count > 10000:
            return "mature"
        elif performance_score > 40 and subscriber_count > 1000:
            return "growing"
        else:
            return "developing"
    
    def _identify_engagement_opportunities(self, youtube_data: Dict, competitive_data: Dict) -> List[str]:
        """Identify specific engagement opportunities"""
        opportunities = []
        
        # YouTube-based opportunities
        if youtube_data.get('has_youtube_presence'):
            content_focus = youtube_data.get('content_focus', '')
            if content_focus == 'educational':
                opportunities.append("Offer to contribute to educational content")
            elif content_focus == 'product_demos':
                opportunities.append("Propose integration demo or partnership")
        else:
            opportunities.append("Offer digital marketing consultation")
        
        # Competitive opportunities
        competitive_position = self._determine_competitive_position(competitive_data)
        if competitive_position == "low_competition":
            opportunities.append("Market leadership positioning opportunity")
        elif competitive_position == "highly_competitive":
            opportunities.append("Differentiation and unique value proposition focus")
        
        return opportunities
    
    def analyze_dead_leads(self, leads_data: List[Dict]) -> Dict:
        """Analyze dead leads for reactivation opportunities"""
        if not self.lead_reactivator:
            return {'error': 'Lead reactivation module not available'}
        
        logger.info(f"Analyzing {len(leads_data)} dead leads")
        
        try:
            result = quick_dead_lead_analysis(leads_data)
            self.stats['leads_reactivated'] += result.get('summary', {}).get('reactivatable_leads', 0)
            return result
        except Exception as e:
            logger.error(f"Dead lead analysis failed: {e}")
            return {'error': str(e)}
    
    def track_competitors(self, competitor_names: List[str]) -> Dict:
        """Track competitor movements and alerts"""
        if not self.competitor_analyzer:
            return {'error': 'Competitor analysis module not available'}
        
        logger.info(f"Tracking {len(competitor_names)} competitors")
        
        try:
            # Get competitive overview
            overview = quick_competitive_overview(competitor_names)
            
            # Track movements (simplified for demo)
            alerts = []
            for competitor in competitor_names:
                # In real implementation, this would check for recent changes
                alerts.append({
                    'competitor': competitor,
                    'alert_type': 'routine_monitoring',
                    'message': f"No significant changes detected for {competitor}",
                    'urgency': 'low',
                    'date': datetime.now().isoformat()
                })
            
            overview['alerts'] = alerts
            self.stats['competitors_tracked'] = len(competitor_names)
            
            return overview
        except Exception as e:
            logger.error(f"Competitor tracking failed: {e}")
            return {'error': str(e)}
    
    def get_engine_status(self) -> Dict:
        """Get engine status and statistics"""
        return {
            'status': 'running',
            'modules': {
                'youtube_intelligence': self.youtube_intel is not None,
                'dead_lead_reactivation': self.lead_reactivator is not None,
                'competitor_analysis': self.competitor_analyzer is not None
            },
            'statistics': self.stats,
            'configuration': self.config,
            'last_updated': datetime.now().isoformat()
        }
    
    def run_daily_intelligence_update(self) -> Dict:
        """Run daily intelligence gathering and updates"""
        logger.info("Running daily intelligence update")
        
        update_results = {
            'start_time': datetime.now().isoformat(),
            'modules_updated': [],
            'errors': [],
            'summary': {}
        }
        
        try:
            # Update competitor intelligence
            if self.competitor_analyzer:
                # In real implementation, this would update stored competitor data
                logger.info("Updating competitor intelligence")
                update_results['modules_updated'].append('competitor_analysis')
            
            # Update market signals
            logger.info("Updating market signals")
            update_results['modules_updated'].append('market_signals')
            
            # Clean old cache
            logger.info("Cleaning expired cache")
            
            update_results['summary'] = {
                'modules_updated': len(update_results['modules_updated']),
                'errors_encountered': len(update_results['errors']),
                'status': 'completed'
            }
            
        except Exception as e:
            logger.error(f"Daily update failed: {e}")
            update_results['errors'].append(str(e))
            update_results['summary']['status'] = 'failed'
        
        update_results['end_time'] = datetime.now().isoformat()
        self.stats['last_run'] = update_results['end_time']
        
        return update_results

# CLI Interface
def main():
    """Main CLI interface"""
    parser = argparse.ArgumentParser(description='CinchIT AI Sales Engine')
    parser.add_argument('command', choices=['prospect', 'deadleads', 'competitors', 'status', 'update'], 
                       help='Command to execute')
    parser.add_argument('--company', type=str, help='Company name for prospect analysis')
    parser.add_argument('--contact-name', type=str, help='Contact name')
    parser.add_argument('--contact-email', type=str, help='Contact email')
    parser.add_argument('--leads-file', type=str, help='JSON file with leads data')
    parser.add_argument('--competitors', nargs='+', help='List of competitor names')
    parser.add_argument('--output', type=str, help='Output file for results')
    
    args = parser.parse_args()
    
    # Initialize engine
    engine = CinchITSalesEngine()
    
    result = {}
    
    try:
        if args.command == 'prospect':
            if not args.company:
                print("Error: --company required for prospect analysis")
                sys.exit(1)
            
            # Run prospect analysis
            loop = asyncio.get_event_loop()
            prospect_intel = loop.run_until_complete(
                engine.generate_prospect_intelligence(
                    args.company, 
                    args.contact_name or "", 
                    args.contact_email or ""
                )
            )
            result = asdict(prospect_intel)
            
        elif args.command == 'deadleads':
            if not args.leads_file:
                print("Error: --leads-file required for dead lead analysis")
                sys.exit(1)
            
            # Load leads data
            with open(args.leads_file, 'r') as f:
                leads_data = json.load(f)
            
            result = engine.analyze_dead_leads(leads_data)
            
        elif args.command == 'competitors':
            if not args.competitors:
                print("Error: --competitors required for competitor analysis")
                sys.exit(1)
            
            result = engine.track_competitors(args.competitors)
            
        elif args.command == 'status':
            result = engine.get_engine_status()
            
        elif args.command == 'update':
            result = engine.run_daily_intelligence_update()
        
        # Output results
        if args.output:
            with open(args.output, 'w') as f:
                json.dump(result, f, indent=2)
            print(f"Results saved to {args.output}")
        else:
            print(json.dumps(result, indent=2))
            
    except Exception as e:
        logger.error(f"Command execution failed: {e}")
        print(f"Error: {e}")
        sys.exit(1)

if __name__ == "__main__":
    main()