"""
Enrichment service — fills in missing contact data via Apollo.io.
"""

import json
import httpx
from datetime import datetime, timezone
from typing import Optional, Dict
from sqlalchemy.orm import Session

from config import get_settings
from models import Contact, AuditLog

settings = get_settings()

APOLLO_ENRICH_URL = "https://api.apollo.io/v1/people/match"
APOLLO_ORG_URL = "https://api.apollo.io/v1/organizations/enrich"


async def enrich_contact_apollo(db: Session, contact: Contact) -> Dict:
    """
    Enrich a single contact via Apollo.io People Match API.
    Returns the enrichment data dict.
    """
    if not settings.apollo_api_key:
        return {"error": "Apollo API key not configured"}

    if contact.apollo_enriched:
        return json.loads(contact.enrichment_data) if contact.enrichment_data else {}

    # Build search params — use what we have
    params = {}
    if contact.first_name:
        params["first_name"] = contact.first_name
    if contact.last_name:
        params["last_name"] = contact.last_name
    if contact.company:
        params["organization_name"] = contact.company
    if contact.email:
        params["email"] = contact.email

    if not params:
        return {"error": "No data to search with"}

    try:
        async with httpx.AsyncClient(timeout=30) as client:
            response = await client.post(
                APOLLO_ENRICH_URL,
                headers={
                    "Content-Type": "application/json",
                    "Cache-Control": "no-cache",
                },
                json={
                    "api_key": settings.apollo_api_key,
                    **params,
                }
            )

            if response.status_code == 200:
                data = response.json()
                person = data.get("person", {})

                # Update contact with enriched data
                if person:
                    if not contact.email and person.get("email"):
                        contact.email = person["email"].lower()
                    if not contact.mobile and person.get("phone_numbers"):
                        for phone in person["phone_numbers"]:
                            if phone.get("type") == "mobile":
                                contact.mobile = phone.get("sanitized_number", "")
                                break
                    if not contact.phone and person.get("phone_numbers"):
                        for phone in person["phone_numbers"]:
                            if phone.get("type") in ("work", "work_direct"):
                                contact.phone = phone.get("sanitized_number", "")
                                break

                    # Store full enrichment data
                    enrichment = {
                        "title": person.get("title", ""),
                        "headline": person.get("headline", ""),
                        "linkedin_url": person.get("linkedin_url", ""),
                        "city": person.get("city", ""),
                        "state": person.get("state", ""),
                        "country": person.get("country", ""),
                        "employment_history": person.get("employment_history", []),
                        "org": {
                            "name": person.get("organization", {}).get("name", ""),
                            "website": person.get("organization", {}).get("website_url", ""),
                            "industry": person.get("organization", {}).get("industry", ""),
                            "employee_count": person.get("organization", {}).get("estimated_num_employees"),
                            "founded_year": person.get("organization", {}).get("founded_year"),
                        },
                        "enriched_at": datetime.now(timezone.utc).isoformat(),
                    }

                    contact.enrichment_data = json.dumps(enrichment)
                    contact.apollo_enriched = True
                    contact.enriched_at = datetime.now(timezone.utc)

                    # Update status if we now have email
                    if contact.email and contact.status == "needs_enrichment":
                        contact.status = "ready"

                    # Audit
                    audit = AuditLog(
                        action="contact_enriched",
                        entity_type="contact",
                        entity_id=contact.id,
                        details=json.dumps({
                            "source": "apollo",
                            "fields_updated": [
                                k for k, v in {
                                    "email": person.get("email"),
                                    "mobile": person.get("phone_numbers"),
                                    "title": person.get("title"),
                                }.items() if v
                            ]
                        }),
                    )
                    db.add(audit)

                    return enrichment

                return {"error": "No match found in Apollo"}

            elif response.status_code == 429:
                return {"error": "Apollo rate limit reached. Try again later."}
            else:
                return {"error": f"Apollo API error: {response.status_code} - {response.text}"}

    except Exception as e:
        return {"error": f"Apollo enrichment failed: {str(e)}"}


async def verify_business_google(db: Session, contact: Contact) -> Dict:
    """
    Verify business is still operating via Google Places API.
    """
    if not settings.google_places_api_key:
        return {"error": "Google Places API key not configured"}

    if not contact.company:
        return {"error": "No company name to search"}

    try:
        async with httpx.AsyncClient(timeout=15) as client:
            response = await client.get(
                "https://maps.googleapis.com/maps/api/place/findplacefromtext/json",
                params={
                    "input": f"{contact.company} Massachusetts",
                    "inputtype": "textquery",
                    "fields": "name,formatted_address,business_status,place_id,types",
                    "key": settings.google_places_api_key,
                }
            )

            if response.status_code == 200:
                data = response.json()
                candidates = data.get("candidates", [])

                if candidates:
                    place = candidates[0]
                    is_active = place.get("business_status") == "OPERATIONAL"
                    contact.business_verified = True
                    contact.business_active = is_active

                    if not is_active:
                        contact.do_not_contact = True
                        contact.do_not_contact_reason = f"Business not operational (Google: {place.get('business_status', 'unknown')})"
                        contact.status = "do_not_contact"

                    audit = AuditLog(
                        action="business_verified",
                        entity_type="contact",
                        entity_id=contact.id,
                        details=json.dumps({
                            "source": "google_places",
                            "business_status": place.get("business_status"),
                            "address": place.get("formatted_address"),
                            "is_active": is_active,
                        }),
                    )
                    db.add(audit)

                    return {
                        "found": True,
                        "active": is_active,
                        "status": place.get("business_status"),
                        "address": place.get("formatted_address"),
                    }

                return {"found": False, "active": None}

            return {"error": f"Google Places error: {response.status_code}"}

    except Exception as e:
        return {"error": f"Business verification failed: {str(e)}"}
