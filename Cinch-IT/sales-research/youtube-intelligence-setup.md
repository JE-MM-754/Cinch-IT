# YouTube Intelligence Setup Guide

## Overview
The YouTube Intelligence module leverages YouTube Data API v3 to gather sales intelligence and prospect research data from target companies' YouTube presence.

## API Key Setup

### 1. Google Cloud Console Setup
1. Go to [Google Cloud Console](https://console.cloud.google.com/)
2. Create a new project or select existing project
3. Enable the YouTube Data API v3
4. Create credentials (API Key)
5. Restrict the API key to YouTube Data API only
6. Add the API key to your `.env.local` file:

```bash
YOUTUBE_API_KEY=your_youtube_api_key_here
```

### 2. API Quota Management
- **Default quota:** 10,000 units per day
- **Typical usage per prospect:** 5-15 units
- **Daily capacity:** ~600-2000 prospects
- **Rate limiting:** 100 requests per 100 seconds

### 3. Required Scopes
- `https://www.googleapis.com/auth/youtube.readonly`
- `https://www.googleapis.com/auth/youtube.force-ssl`

## Intelligence Categories

### Content Strategy Analysis
- **Product Demos:** How-to videos, feature walkthroughs
- **Thought Leadership:** Industry insights, trend discussions
- **Customer Success:** Testimonials, case studies, reviews
- **Company Culture:** Behind-the-scenes, team videos
- **Educational:** Tutorials, training content
- **Events & Webinars:** Conference talks, product launches

### Engagement Metrics
- **Subscriber Growth:** Channel growth trajectory
- **View Patterns:** Average views per video, engagement trends
- **Content Frequency:** Upload schedule consistency
- **Audience Engagement:** Like/comment ratios, interaction quality

### Competitive Intelligence
- **Content Gaps:** Topics competitors aren't covering
- **Performance Benchmarks:** Subscriber counts, view metrics
- **Strategy Differences:** Content approach variations
- **Market Positioning:** How companies present themselves

## Sales Use Cases

### 1. Prospect Research
```python
# Example: Research a prospect's YouTube presence
from youtube_intelligence import quick_prospect_youtube_analysis

company_analysis = quick_prospect_youtube_analysis("TechCorp")
```

**Output includes:**
- YouTube presence assessment
- Content focus areas
- Target audience analysis
- Performance metrics
- Engagement recommendations

### 2. Competitive Analysis
```python
# Example: Analyze competitor YouTube strategies
from youtube_intelligence import YouTubeIntelligence

youtube_intel = YouTubeIntelligence()
competitor_analysis = youtube_intel.analyze_competitor("CompetitorCorp")
```

**Provides:**
- Channel performance metrics
- Content strategy breakdown
- Audience targeting insights
- Competitive positioning
- Content calendar patterns

### 3. Market Signal Detection
- **Product Launch Indicators:** New product demo videos
- **Growth Signals:** Increased content production, hiring videos
- **Market Expansion:** Content in new languages/regions
- **Partnership Signals:** Collaboration videos, guest appearances

## Sales Intelligence Insights

### Content Strategy Intelligence
- **Heavy Demo Focus:** May indicate product complexity, need for education
- **Thought Leadership:** Shows market positioning, industry expertise
- **Customer Success Content:** Indicates mature customer base
- **Educational Focus:** Suggests inbound marketing strategy

### Engagement Intelligence
- **High Engagement Rate:** Active, engaged audience
- **Low Subscriber-to-View Ratio:** Content reaches beyond subscriber base
- **Consistent Upload Schedule:** Professional marketing operation
- **Irregular Posting:** Potential marketing resource constraints

### Audience Intelligence
- **Developer-Focused:** Technical decision makers, API-first approach
- **Business Leader Content:** C-suite decision makers, ROI focus
- **Mixed Audience:** Broad market appeal, multiple buyer personas

## Implementation Examples

### Sales Rep Quick Research
```bash
# CLI usage for quick prospect research
python -m cinch-engine prospect --company "TechCorp" --output prospect_intel.json
```

### Batch Competitive Analysis
```python
# Analyze multiple competitors
competitors = ["Salesforce", "HubSpot", "Pipedrive"]
competitive_overview = quick_competitive_overview(competitors)
```

### Integration with CRM
```python
# Enrich CRM data with YouTube intelligence
def enrich_lead_with_youtube_data(lead):
    youtube_data = quick_prospect_youtube_analysis(lead.company_name)
    lead.youtube_presence = youtube_data.get('has_youtube_presence')
    lead.content_focus = youtube_data.get('content_focus')
    lead.engagement_score = youtube_data.get('performance_score')
    return lead
```

## Best Practices

### 1. Rate Limit Management
- Implement exponential backoff for API errors
- Cache results for 24 hours to reduce API calls
- Batch similar requests when possible
- Monitor quota usage daily

### 2. Data Quality
- Cross-verify channel ownership (official vs. fan channels)
- Filter out inactive channels (no uploads in 90+ days)
- Validate content relevance to business context
- Account for private/unlisted content limitations

### 3. Sales Application
- Use insights to personalize outreach messages
- Reference specific content in conversations
- Identify content collaboration opportunities
- Time outreach based on upload patterns

### 4. Privacy & Compliance
- Only analyze public YouTube data
- Respect channel privacy settings
- Comply with YouTube Terms of Service
- Maintain data retention policies

## Troubleshooting

### Common Issues
1. **API Key Invalid:** Verify key restrictions and enabled APIs
2. **Quota Exceeded:** Monitor usage, implement caching
3. **No Channels Found:** Company may not have YouTube presence
4. **Rate Limit Errors:** Implement proper backoff strategy

### Error Handling
```python
try:
    analysis = quick_prospect_youtube_analysis(company_name)
except YouTubeAPIError as e:
    if e.status_code == 403:
        # Quota exceeded or key restricted
        logger.warning(f"API access restricted: {e}")
    elif e.status_code == 404:
        # Channel not found
        analysis = {'has_youtube_presence': False}
except Exception as e:
    logger.error(f"Unexpected error: {e}")
```

## ROI Metrics

### Sales Intelligence Value
- **Research Time Savings:** 15-30 minutes per prospect → 2-3 minutes
- **Personalization Quality:** 40% increase in response rates
- **Competitive Awareness:** Real-time competitor content monitoring
- **Market Timing:** Identify optimal engagement windows

### Key Performance Indicators
- **API Efficiency:** API calls per successful intelligence gather
- **Data Coverage:** Percentage of prospects with YouTube presence
- **Engagement Lift:** Response rate improvement from YouTube insights
- **Competitive Wins:** Deals influenced by competitive intelligence

## Advanced Features

### 1. Content Trend Analysis
Track content themes across time periods to identify strategy shifts.

### 2. Influencer Identification
Identify key personnel appearing in videos for stakeholder mapping.

### 3. Product Launch Detection
Monitor for new product announcements and feature releases.

### 4. Partnership Intelligence
Detect collaboration opportunities from guest appearances and partnerships.

## Integration Checklist

- [ ] YouTube Data API v3 enabled in Google Cloud Console
- [ ] API key configured with proper restrictions
- [ ] Rate limiting implemented
- [ ] Caching strategy deployed
- [ ] Error handling configured
- [ ] CRM integration tested
- [ ] Sales team training completed
- [ ] Monitoring and alerts configured

---

**Next Steps:**
1. Configure API keys and test basic functionality
2. Train sales team on YouTube intelligence insights
3. Integrate with existing CRM workflows
4. Monitor performance and optimize queries
5. Scale to full prospect database