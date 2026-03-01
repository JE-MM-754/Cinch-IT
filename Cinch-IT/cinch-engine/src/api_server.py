"""
CinchIT AI Sales Engine - FastAPI Server
REST API for sales intelligence platform
"""

import os
import json
import asyncio
from typing import Dict, List, Optional, Any
from datetime import datetime
from fastapi import FastAPI, HTTPException, BackgroundTasks, Depends, Request
from fastapi.middleware.cors import CORSMiddleware
from fastapi.responses import HTMLResponse, JSONResponse
from pydantic import BaseModel, Field
import logging

# Import our main engine
from main import CinchITSalesEngine

# Configure logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

# Initialize FastAPI app
app = FastAPI(
    title="CinchIT AI Sales Engine API",
    description="Enterprise-grade AI sales intelligence platform",
    version="1.0.0",
    docs_url="/docs",
    redoc_url="/redoc"
)

# CORS middleware
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],  # Configure appropriately for production
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Initialize the sales engine
sales_engine = CinchITSalesEngine()

# Request/Response Models
class ProspectRequest(BaseModel):
    company_name: str = Field(..., description="Target company name")
    contact_name: Optional[str] = Field(None, description="Contact person name")
    contact_email: Optional[str] = Field(None, description="Contact email address")

class ProspectResponse(BaseModel):
    prospect_id: str
    company_name: str
    contact_name: str
    contact_email: str
    intelligence_summary: str
    key_insights: List[str]
    competitive_threats: List[str]
    engagement_recommendations: List[str]
    best_contact_time: str
    personalization_data: Dict[str, Any]

class DeadLeadRequest(BaseModel):
    leads: List[Dict[str, Any]] = Field(..., description="List of dead leads data")

class CompetitorRequest(BaseModel):
    competitors: List[str] = Field(..., description="List of competitor company names")

class EngineStatus(BaseModel):
    status: str
    modules: Dict[str, bool]
    statistics: Dict[str, Any]
    configuration: Dict[str, Any]
    last_updated: str

# API Routes
@app.get("/", response_class=HTMLResponse)
async def root():
    """Landing page with API overview"""
    html_content = """
    <!DOCTYPE html>
    <html>
    <head>
        <title>CinchIT AI Sales Engine</title>
        <style>
            body { font-family: Arial, sans-serif; max-width: 800px; margin: 50px auto; padding: 20px; }
            .header { text-align: center; color: #2c3e50; }
            .module { background: #f8f9fa; padding: 20px; margin: 20px 0; border-radius: 8px; }
            .endpoint { background: #e3f2fd; padding: 15px; margin: 10px 0; border-radius: 5px; }
            code { background: #f1f1f1; padding: 2px 6px; border-radius: 3px; }
        </style>
    </head>
    <body>
        <div class="header">
            <h1>🎯 CinchIT AI Sales Engine</h1>
            <p>Enterprise-grade AI sales intelligence platform</p>
            <p><strong>Status:</strong> <span style="color: green;">Running</span></p>
        </div>
        
        <div class="module">
            <h2>📊 Core Capabilities</h2>
            <ul>
                <li><strong>Prospect Intelligence:</strong> YouTube analysis & market research</li>
                <li><strong>Dead Lead Reactivation:</strong> AI-powered lead scoring & campaign generation</li>
                <li><strong>Competitor Analysis:</strong> Real-time competitive intelligence</li>
                <li><strong>Market Signals:</strong> Industry trend monitoring & alerts</li>
            </ul>
        </div>
        
        <div class="module">
            <h2>🚀 Quick Start Endpoints</h2>
            
            <div class="endpoint">
                <strong>POST /api/v1/prospect/analyze</strong>
                <p>Analyze prospect for sales intelligence</p>
                <code>{"company_name": "TechCorp", "contact_name": "John Smith"}</code>
            </div>
            
            <div class="endpoint">
                <strong>POST /api/v1/leads/dead-analysis</strong>
                <p>Analyze dead leads for reactivation opportunities</p>
                <code>{"leads": [{"lead_id": "L001", "company_name": "Corp"}]}</code>
            </div>
            
            <div class="endpoint">
                <strong>POST /api/v1/competitors/track</strong>
                <p>Track competitor movements and alerts</p>
                <code>{"competitors": ["Salesforce", "HubSpot"]}</code>
            </div>
            
            <div class="endpoint">
                <strong>GET /api/v1/engine/status</strong>
                <p>Get engine status and performance metrics</p>
            </div>
        </div>
        
        <div class="module">
            <h2>📚 Documentation</h2>
            <p>
                <a href="/docs">Interactive API Docs (Swagger)</a> |
                <a href="/redoc">API Documentation (ReDoc)</a> |
                <a href="/api/v1/engine/status">System Status</a>
            </p>
        </div>
        
        <div class="header">
            <p><small>Built with FastAPI • Powered by AI • Enterprise Ready</small></p>
        </div>
    </body>
    </html>
    """
    return HTMLResponse(content=html_content)

@app.get("/health")
async def health_check():
    """Health check endpoint for monitoring"""
    return {"status": "healthy", "timestamp": datetime.now().isoformat()}

@app.get("/api/v1/engine/status", response_model=EngineStatus)
async def get_engine_status():
    """Get comprehensive engine status"""
    try:
        status = sales_engine.get_engine_status()
        return EngineStatus(**status)
    except Exception as e:
        logger.error(f"Status check failed: {e}")
        raise HTTPException(status_code=500, detail=str(e))

@app.post("/api/v1/prospect/analyze", response_model=ProspectResponse)
async def analyze_prospect(request: ProspectRequest):
    """Generate comprehensive prospect intelligence"""
    try:
        logger.info(f"Analyzing prospect: {request.company_name}")
        
        # Generate prospect intelligence
        prospect_intel = await sales_engine.generate_prospect_intelligence(
            company_name=request.company_name,
            contact_name=request.contact_name or "",
            contact_email=request.contact_email or ""
        )
        
        return ProspectResponse(
            prospect_id=prospect_intel.prospect_id,
            company_name=prospect_intel.company_name,
            contact_name=prospect_intel.contact_name,
            contact_email=prospect_intel.contact_email,
            intelligence_summary=prospect_intel.intelligence_summary,
            key_insights=prospect_intel.key_insights,
            competitive_threats=prospect_intel.competitive_threats,
            engagement_recommendations=prospect_intel.engagement_recommendations,
            best_contact_time=prospect_intel.best_contact_time,
            personalization_data=prospect_intel.personalization_data
        )
        
    except Exception as e:
        logger.error(f"Prospect analysis failed for {request.company_name}: {e}")
        raise HTTPException(status_code=500, detail=f"Analysis failed: {str(e)}")

@app.post("/api/v1/leads/dead-analysis")
async def analyze_dead_leads(request: DeadLeadRequest):
    """Analyze dead leads for reactivation opportunities"""
    try:
        logger.info(f"Analyzing {len(request.leads)} dead leads")
        
        result = sales_engine.analyze_dead_leads(request.leads)
        
        if 'error' in result:
            raise HTTPException(status_code=500, detail=result['error'])
        
        return result
        
    except Exception as e:
        logger.error(f"Dead lead analysis failed: {e}")
        raise HTTPException(status_code=500, detail=f"Analysis failed: {str(e)}")

@app.post("/api/v1/competitors/track")
async def track_competitors(request: CompetitorRequest):
    """Track competitor movements and intelligence"""
    try:
        logger.info(f"Tracking {len(request.competitors)} competitors")
        
        result = sales_engine.track_competitors(request.competitors)
        
        if 'error' in result:
            raise HTTPException(status_code=500, detail=result['error'])
        
        return result
        
    except Exception as e:
        logger.error(f"Competitor tracking failed: {e}")
        raise HTTPException(status_code=500, detail=f"Tracking failed: {str(e)}")

@app.post("/api/v1/engine/update")
async def run_intelligence_update(background_tasks: BackgroundTasks):
    """Run intelligence update in background"""
    try:
        logger.info("Starting background intelligence update")
        
        # Run update in background
        background_tasks.add_task(sales_engine.run_daily_intelligence_update)
        
        return {
            "message": "Intelligence update started",
            "status": "running",
            "timestamp": datetime.now().isoformat()
        }
        
    except Exception as e:
        logger.error(f"Intelligence update failed: {e}")
        raise HTTPException(status_code=500, detail=str(e))

@app.get("/api/v1/youtube/analyze/{company_name}")
async def youtube_analysis(company_name: str):
    """Quick YouTube presence analysis"""
    try:
        from youtube_intelligence import quick_prospect_youtube_analysis
        
        result = quick_prospect_youtube_analysis(company_name)
        return result
        
    except Exception as e:
        logger.error(f"YouTube analysis failed for {company_name}: {e}")
        raise HTTPException(status_code=500, detail=str(e))

@app.get("/api/v1/dashboard/metrics")
async def get_dashboard_metrics():
    """Get dashboard metrics for UI"""
    try:
        status = sales_engine.get_engine_status()
        
        metrics = {
            "total_prospects_analyzed": status['statistics']['prospects_analyzed'],
            "leads_reactivated": status['statistics']['leads_reactivated'],
            "competitors_tracked": status['statistics']['competitors_tracked'],
            "engine_uptime": "24h",  # Would calculate actual uptime
            "last_update": status['statistics']['last_run'],
            "modules_active": sum(status['modules'].values()),
            "success_rate": 0.95,  # Would calculate from actual data
            "avg_response_time": "1.2s"  # Would measure actual response times
        }
        
        return metrics
        
    except Exception as e:
        logger.error(f"Metrics retrieval failed: {e}")
        raise HTTPException(status_code=500, detail=str(e))

@app.get("/api/v1/prospects/{prospect_id}")
async def get_prospect_details(prospect_id: str):
    """Get detailed prospect information by ID"""
    # In real implementation, this would query the database
    return {
        "message": "Prospect details endpoint",
        "prospect_id": prospect_id,
        "note": "Would retrieve stored prospect data from database"
    }

@app.post("/api/v1/alerts/configure")
async def configure_alerts(alert_config: Dict[str, Any]):
    """Configure intelligence alerts and thresholds"""
    try:
        # In real implementation, this would update alert configurations
        return {
            "message": "Alert configuration updated",
            "config": alert_config,
            "timestamp": datetime.now().isoformat()
        }
        
    except Exception as e:
        logger.error(f"Alert configuration failed: {e}")
        raise HTTPException(status_code=500, detail=str(e))

@app.get("/api/v1/export/data")
async def export_intelligence_data(format: str = "json"):
    """Export intelligence data for analysis"""
    try:
        # In real implementation, this would export comprehensive data
        export_data = {
            "export_timestamp": datetime.now().isoformat(),
            "format": format,
            "data": {
                "prospects": [],
                "competitors": [],
                "alerts": [],
                "metrics": {}
            }
        }
        
        return export_data
        
    except Exception as e:
        logger.error(f"Data export failed: {e}")
        raise HTTPException(status_code=500, detail=str(e))

# Error handlers
@app.exception_handler(404)
async def not_found_handler(request: Request, exc):
    return JSONResponse(
        status_code=404,
        content={"error": "Endpoint not found", "path": str(request.url)}
    )

@app.exception_handler(500)
async def internal_error_handler(request: Request, exc):
    logger.error(f"Internal server error: {exc}")
    return JSONResponse(
        status_code=500,
        content={"error": "Internal server error", "detail": "Check server logs for details"}
    )

# Startup event
@app.on_event("startup")
async def startup_event():
    logger.info("CinchIT AI Sales Engine API starting up...")
    logger.info("Engine modules initialized and ready")

# Shutdown event
@app.on_event("shutdown")
async def shutdown_event():
    logger.info("CinchIT AI Sales Engine API shutting down...")

if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=8000, log_level="info")