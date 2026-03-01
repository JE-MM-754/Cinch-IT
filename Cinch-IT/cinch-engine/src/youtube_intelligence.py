"""
CinchIT AI Sales Engine - YouTube Intelligence Module
Leverages YouTube Data API v3 for prospect research and competitive analysis
"""

import os
import json
import time
from typing import Dict, List, Optional, Any
from dataclasses import dataclass
from datetime import datetime, timedelta
import requests
from urllib.parse import quote
import logging

# Configure logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

@dataclass
class YouTubeChannelData:
    """Data structure for YouTube channel analysis"""
    channel_id: str
    channel_title: str
    subscriber_count: int
    video_count: int
    view_count: int
    created_date: str
    description: str
    keywords: List[str]
    recent_videos: List[Dict]
    engagement_metrics: Dict
    content_themes: List[str]
    upload_frequency: str
    
@dataclass
class CompetitorAnalysis:
    """Data structure for competitor YouTube analysis"""
    company_name: str
    channels: List[YouTubeChannelData]
    content_strategy: str
    target_audience: str
    key_messages: List[str]
    performance_score: float
    recommendations: List[str]

class YouTubeIntelligence:
    """YouTube Data API v3 integration for sales intelligence"""
    
    def __init__(self):
        self.api_key = os.getenv('YOUTUBE_API_KEY')
        self.base_url = "https://www.googleapis.com/youtube/v3"
        self.rate_limit = int(os.getenv('YOUTUBE_RATE_LIMIT', 100))  # requests per minute
        self.request_count = 0
        self.last_reset = time.time()
        
        if not self.api_key:
            raise ValueError("YouTube API key not found in environment variables")
    
    def _check_rate_limit(self):
        """Implement rate limiting to avoid API quota exceeded"""
        current_time = time.time()
        
        # Reset counter every minute
        if current_time - self.last_reset > 60:
            self.request_count = 0
            self.last_reset = current_time
        
        # Check if we've hit the limit
        if self.request_count >= self.rate_limit:
            sleep_time = 60 - (current_time - self.last_reset)
            logger.warning(f"Rate limit reached. Sleeping for {sleep_time:.2f} seconds")
            time.sleep(sleep_time)
            self.request_count = 0
            self.last_reset = time.time()
    
    def _make_request(self, endpoint: str, params: Dict) -> Dict:
        """Make authenticated request to YouTube API"""
        self._check_rate_limit()
        
        params['key'] = self.api_key
        url = f"{self.base_url}/{endpoint}"
        
        try:
            response = requests.get(url, params=params)
            response.raise_for_status()
            self.request_count += 1
            return response.json()
        except requests.exceptions.RequestException as e:
            logger.error(f"YouTube API request failed: {e}")
            return {}
    
    def search_company_channels(self, company_name: str, max_results: int = 10) -> List[Dict]:
        """Search for YouTube channels associated with a company"""
        params = {
            'part': 'id,snippet',
            'type': 'channel',
            'q': f"{company_name} official",
            'maxResults': max_results,
            'order': 'relevance'
        }
        
        data = self._make_request('search', params)
        channels = []
        
        for item in data.get('items', []):
            channel_info = {
                'channel_id': item['id']['channelId'],
                'title': item['snippet']['title'],
                'description': item['snippet']['description'],
                'thumbnail': item['snippet']['thumbnails'].get('high', {}).get('url', ''),
                'published_at': item['snippet']['publishedAt']
            }
            channels.append(channel_info)
        
        return channels
    
    def get_channel_details(self, channel_id: str) -> Optional[YouTubeChannelData]:
        """Get detailed information about a specific YouTube channel"""
        params = {
            'part': 'snippet,statistics,contentDetails',
            'id': channel_id
        }
        
        data = self._make_request('channels', params)
        
        if not data.get('items'):
            logger.warning(f"No data found for channel ID: {channel_id}")
            return None
        
        channel = data['items'][0]
        snippet = channel['snippet']
        stats = channel['statistics']
        
        # Get recent videos for engagement analysis
        recent_videos = self.get_recent_videos(channel_id, max_results=20)
        
        # Analyze content themes
        content_themes = self._analyze_content_themes(recent_videos)
        
        # Calculate engagement metrics
        engagement_metrics = self._calculate_engagement_metrics(recent_videos, stats)
        
        return YouTubeChannelData(
            channel_id=channel_id,
            channel_title=snippet['title'],
            subscriber_count=int(stats.get('subscriberCount', 0)),
            video_count=int(stats.get('videoCount', 0)),
            view_count=int(stats.get('viewCount', 0)),
            created_date=snippet['publishedAt'],
            description=snippet['description'],
            keywords=snippet.get('tags', []),
            recent_videos=recent_videos,
            engagement_metrics=engagement_metrics,
            content_themes=content_themes,
            upload_frequency=self._calculate_upload_frequency(recent_videos)
        )
    
    def get_recent_videos(self, channel_id: str, max_results: int = 20) -> List[Dict]:
        """Get recent videos from a channel for analysis"""
        # First, get the uploads playlist ID
        params = {
            'part': 'contentDetails',
            'id': channel_id
        }
        
        channel_data = self._make_request('channels', params)
        
        if not channel_data.get('items'):
            return []
        
        uploads_playlist = channel_data['items'][0]['contentDetails']['relatedPlaylists']['uploads']
        
        # Get videos from uploads playlist
        params = {
            'part': 'snippet',
            'playlistId': uploads_playlist,
            'maxResults': max_results
        }
        
        playlist_data = self._make_request('playlistItems', params)
        videos = []
        
        # Get detailed stats for each video
        video_ids = [item['snippet']['resourceId']['videoId'] for item in playlist_data.get('items', [])]
        
        if video_ids:
            params = {
                'part': 'statistics,snippet',
                'id': ','.join(video_ids)
            }
            
            video_details = self._make_request('videos', params)
            
            for video in video_details.get('items', []):
                video_info = {
                    'video_id': video['id'],
                    'title': video['snippet']['title'],
                    'description': video['snippet']['description'],
                    'published_at': video['snippet']['publishedAt'],
                    'view_count': int(video['statistics'].get('viewCount', 0)),
                    'like_count': int(video['statistics'].get('likeCount', 0)),
                    'comment_count': int(video['statistics'].get('commentCount', 0)),
                    'thumbnail': video['snippet']['thumbnails'].get('high', {}).get('url', ''),
                    'duration': video.get('contentDetails', {}).get('duration', '')
                }
                videos.append(video_info)
        
        return videos
    
    def _analyze_content_themes(self, videos: List[Dict]) -> List[str]:
        """Analyze content themes from video titles and descriptions"""
        # Simple keyword extraction - could be enhanced with NLP
        all_text = " ".join([
            video['title'] + " " + video.get('description', '')[:200]
            for video in videos
        ]).lower()
        
        # Common business/tech themes to look for
        themes = {
            'product_demos': ['demo', 'demonstration', 'product', 'feature', 'walkthrough'],
            'thought_leadership': ['insight', 'trend', 'future', 'industry', 'vision'],
            'customer_success': ['customer', 'success', 'case study', 'testimonial', 'review'],
            'company_culture': ['team', 'culture', 'behind the scenes', 'office', 'employee'],
            'educational': ['tutorial', 'how to', 'guide', 'learn', 'education', 'training'],
            'events_webinars': ['webinar', 'event', 'conference', 'summit', 'workshop'],
            'announcements': ['announce', 'launch', 'release', 'new', 'introducing'],
            'partnerships': ['partner', 'collaboration', 'integration', 'alliance']
        }
        
        detected_themes = []
        for theme, keywords in themes.items():
            if any(keyword in all_text for keyword in keywords):
                detected_themes.append(theme)
        
        return detected_themes
    
    def _calculate_engagement_metrics(self, videos: List[Dict], channel_stats: Dict) -> Dict:
        """Calculate engagement metrics for the channel"""
        if not videos:
            return {}
        
        total_views = sum(video['view_count'] for video in videos)
        total_likes = sum(video['like_count'] for video in videos)
        total_comments = sum(video['comment_count'] for video in videos)
        
        avg_views = total_views / len(videos) if videos else 0
        subscribers = int(channel_stats.get('subscriberCount', 1))
        
        engagement_rate = (total_likes + total_comments) / total_views * 100 if total_views > 0 else 0
        
        return {
            'average_views_per_video': avg_views,
            'total_recent_views': total_views,
            'engagement_rate': round(engagement_rate, 2),
            'subscriber_to_view_ratio': round(avg_views / subscribers * 100, 2) if subscribers > 0 else 0,
            'recent_video_count': len(videos)
        }
    
    def _calculate_upload_frequency(self, videos: List[Dict]) -> str:
        """Calculate how frequently the channel uploads content"""
        if len(videos) < 2:
            return "insufficient_data"
        
        # Calculate days between videos
        dates = [datetime.fromisoformat(video['published_at'].replace('Z', '+00:00')) for video in videos]
        dates.sort(reverse=True)  # Most recent first
        
        # Calculate average days between uploads
        intervals = []
        for i in range(len(dates) - 1):
            interval = (dates[i] - dates[i + 1]).days
            intervals.append(interval)
        
        avg_interval = sum(intervals) / len(intervals) if intervals else 0
        
        if avg_interval <= 1:
            return "daily"
        elif avg_interval <= 7:
            return "weekly"
        elif avg_interval <= 30:
            return "monthly"
        elif avg_interval <= 90:
            return "quarterly"
        else:
            return "rarely"
    
    def analyze_competitor(self, company_name: str) -> CompetitorAnalysis:
        """Comprehensive competitor analysis via YouTube presence"""
        logger.info(f"Starting competitor analysis for: {company_name}")
        
        # Search for company channels
        channel_results = self.search_company_channels(company_name)
        
        channels = []
        for channel_result in channel_results[:3]:  # Analyze top 3 channels
            channel_data = self.get_channel_details(channel_result['channel_id'])
            if channel_data:
                channels.append(channel_data)
        
        if not channels:
            logger.warning(f"No YouTube channels found for {company_name}")
            return CompetitorAnalysis(
                company_name=company_name,
                channels=[],
                content_strategy="no_youtube_presence",
                target_audience="unknown",
                key_messages=[],
                performance_score=0.0,
                recommendations=["Consider establishing YouTube presence for thought leadership"]
            )
        
        # Analyze overall content strategy
        all_themes = []
        total_engagement = 0
        total_subscribers = 0
        
        for channel in channels:
            all_themes.extend(channel.content_themes)
            total_engagement += channel.engagement_metrics.get('engagement_rate', 0)
            total_subscribers += channel.subscriber_count
        
        # Determine content strategy
        theme_counts = {theme: all_themes.count(theme) for theme in set(all_themes)}
        primary_strategy = max(theme_counts.keys(), default="mixed") if theme_counts else "undefined"
        
        # Calculate performance score (0-100)
        avg_engagement = total_engagement / len(channels) if channels else 0
        performance_score = min(100, avg_engagement * 10 + (total_subscribers / 1000))
        
        # Generate recommendations
        recommendations = self._generate_recommendations(channels, performance_score, primary_strategy)
        
        return CompetitorAnalysis(
            company_name=company_name,
            channels=channels,
            content_strategy=primary_strategy,
            target_audience=self._determine_target_audience(channels),
            key_messages=self._extract_key_messages(channels),
            performance_score=round(performance_score, 1),
            recommendations=recommendations
        )
    
    def _determine_target_audience(self, channels: List[YouTubeChannelData]) -> str:
        """Determine target audience based on content analysis"""
        # Analyze content themes and descriptions to infer audience
        all_content = " ".join([
            channel.description + " " + " ".join([video['title'] for video in channel.recent_videos])
            for channel in channels
        ]).lower()
        
        audience_indicators = {
            'developers': ['developer', 'api', 'code', 'programming', 'technical'],
            'business_leaders': ['executive', 'ceo', 'business', 'enterprise', 'roi'],
            'marketers': ['marketing', 'campaign', 'brand', 'customer', 'growth'],
            'general_public': ['anyone', 'everyone', 'simple', 'easy', 'beginner'],
            'industry_professionals': ['professional', 'expert', 'advanced', 'industry']
        }
        
        scores = {}
        for audience, keywords in audience_indicators.items():
            scores[audience] = sum(1 for keyword in keywords if keyword in all_content)
        
        return max(scores.keys(), key=scores.get) if scores else "general_business"
    
    def _extract_key_messages(self, channels: List[YouTubeChannelData]) -> List[str]:
        """Extract key marketing messages from video content"""
        # Simple extraction from recent video titles and descriptions
        messages = []
        
        for channel in channels:
            # Look for common value proposition keywords in video titles
            for video in channel.recent_videos[:10]:  # Recent 10 videos
                title = video['title'].lower()
                if any(keyword in title for keyword in ['solution', 'better', 'faster', 'save', 'improve', 'boost']):
                    messages.append(video['title'])
        
        return messages[:5]  # Return top 5 key messages
    
    def _generate_recommendations(self, channels: List[YouTubeChannelData], score: float, strategy: str) -> List[str]:
        """Generate strategic recommendations based on analysis"""
        recommendations = []
        
        if score < 20:
            recommendations.append("Low engagement - consider more interactive content and audience engagement")
        
        if strategy == "product_demos":
            recommendations.append("Heavy focus on product demos - opportunity to diversify with thought leadership")
        elif strategy == "mixed":
            recommendations.append("Good content variety - maintain diverse content strategy")
        
        # Check upload frequency
        freq_analysis = {}
        for channel in channels:
            freq = channel.upload_frequency
            freq_analysis[freq] = freq_analysis.get(freq, 0) + 1
        
        most_common_freq = max(freq_analysis.keys(), key=freq_analysis.get) if freq_analysis else "unknown"
        
        if most_common_freq == "rarely":
            recommendations.append("Infrequent posting - consistent content calendar could improve engagement")
        elif most_common_freq == "daily":
            recommendations.append("High-frequency posting - ensure quality over quantity")
        
        return recommendations

# Utility function for sales teams
def quick_prospect_youtube_analysis(company_name: str) -> Dict:
    """Quick analysis for sales reps to understand prospect's YouTube presence"""
    try:
        youtube_intel = YouTubeIntelligence()
        analysis = youtube_intel.analyze_competitor(company_name)
        
        return {
            'company': company_name,
            'has_youtube_presence': len(analysis.channels) > 0,
            'total_subscribers': sum(ch.subscriber_count for ch in analysis.channels),
            'content_focus': analysis.content_strategy,
            'target_audience': analysis.target_audience,
            'performance_score': analysis.performance_score,
            'key_insights': analysis.recommendations[:3],
            'recent_activity': [
                {
                    'channel': ch.channel_title,
                    'recent_videos': len(ch.recent_videos),
                    'upload_frequency': ch.upload_frequency
                }
                for ch in analysis.channels
            ]
        }
    except Exception as e:
        logger.error(f"Error in quick analysis for {company_name}: {e}")
        return {
            'company': company_name,
            'error': str(e),
            'has_youtube_presence': False
        }

if __name__ == "__main__":
    # Example usage
    company = "Salesforce"
    result = quick_prospect_youtube_analysis(company)
    print(json.dumps(result, indent=2))