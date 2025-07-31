import os
import requests
from typing import Dict, List, Optional
from dotenv import load_dotenv

load_dotenv()

class QlooService:
    def __init__(self):
        self.api_key = os.getenv("QLOO_API_KEY")
        self.base_url = os.getenv("QLOO_BASE_URL", "https://hackathon.api.qloo.com")
        self.headers = {
            "Authorization": f"Bearer {self.api_key}",
            "Content-Type": "application/json"
        }
    
    def get_affinities(self, entities: List[str], domains: List[str] = None) -> Dict:
        """Get cultural affinities for given entities across specified domains."""
        try:
            if domains is None:
                domains = ["music", "film", "television", "books", "travel", "brands"]
            
            payload = {
                "entities": entities,
                "domains": domains,
                "limit": 10
            }
            
            response = requests.post(
                f"{self.base_url}/affinities",
                headers=self.headers,
                json=payload,
                timeout=30
            )
            
            if response.status_code == 200:
                data = response.json()
                return {
                    "success": True,
                    "affinities": self._process_affinities(data),
                    "raw_data": data
                }
            else:
                return {
                    "success": False,
                    "error": f"API Error: {response.status_code} - {response.text}"
                }
                
        except Exception as e:
            return {
                "success": False,
                "error": f"Request failed: {str(e)}"
            }
    
    def get_recommendations(self, seed_entities: List[str], target_domain: str, limit: int = 5) -> Dict:
        """Get recommendations in a specific domain based on seed entities."""
        try:
            payload = {
                "seed": seed_entities,
                "domain": target_domain,
                "limit": limit
            }
            
            response = requests.post(
                f"{self.base_url}/recommendations",
                headers=self.headers,
                json=payload,
                timeout=30
            )
            
            if response.status_code == 200:
                data = response.json()
                return {
                    "success": True,
                    "recommendations": self._process_recommendations(data, target_domain),
                    "raw_data": data
                }
            else:
                return {
                    "success": False,
                    "error": f"API Error: {response.status_code} - {response.text}"
                }
                
        except Exception as e:
            return {
                "success": False,
                "error": f"Request failed: {str(e)}"
            }
    
    def extract_entities_from_text(self, text: str) -> List[str]:
        """Extract potential entities from user text for Qloo processing."""
        # Simple entity extraction - can be enhanced with NLP
        import re
        
        # Look for quoted items, capitalized words, and common cultural references
        entities = []
        
        # Find quoted items
        quoted = re.findall(r'"([^"]*)"', text)
        entities.extend(quoted)
        
        # Find capitalized phrases (potential proper nouns)
        capitalized = re.findall(r'\b[A-Z][a-z]+(?:\s+[A-Z][a-z]+)*\b', text)
        entities.extend(capitalized)
        
        # Common cultural keywords
        cultural_keywords = [
            'jazz', 'rock', 'classical', 'hip-hop', 'electronic', 'folk',
            'sci-fi', 'fantasy', 'thriller', 'romance', 'comedy', 'drama',
            'travel', 'adventure', 'mystery', 'historical', 'contemporary',
            'urban', 'rural', 'futuristic', 'vintage', 'modern'
        ]
        
        text_lower = text.lower()
        for keyword in cultural_keywords:
            if keyword in text_lower:
                entities.append(keyword)
        
        # Remove duplicates and filter short/common words
        entities = list(set([e for e in entities if len(e) > 2 and e.lower() not in ['the', 'and', 'with', 'for']]))
        
        return entities[:10]  # Limit to top 10 entities
    
    def create_cultural_context(self, user_input: str) -> str:
        """Create cultural context string from user input using Qloo affinities."""
        entities = self.extract_entities_from_text(user_input)
        
        if not entities:
            return ""
        
        affinities_result = self.get_affinities(entities)
        
        if not affinities_result["success"]:
            return ""
        
        cultural_elements = []
        affinities = affinities_result["affinities"]
        
        for domain, items in affinities.items():
            if items:
                top_items = items[:3]  # Top 3 items per domain
                cultural_elements.append(f"{domain}: {', '.join(top_items)}")
        
        return "; ".join(cultural_elements)
    
    def _process_affinities(self, raw_data: Dict) -> Dict:
        """Process raw affinity data into organized format."""
        processed = {}
        
        if "affinities" in raw_data:
            for affinity in raw_data["affinities"]:
                domain = affinity.get("domain", "unknown")
                name = affinity.get("name", "")
                
                if domain not in processed:
                    processed[domain] = []
                
                if name:
                    processed[domain].append(name)
        
        return processed
    
    def _process_recommendations(self, raw_data: Dict, domain: str) -> List[str]:
        """Process raw recommendation data into list of names."""
        recommendations = []
        
        if "recommendations" in raw_data:
            for rec in raw_data["recommendations"]:
                name = rec.get("name", "")
                if name:
                    recommendations.append(name)
        
        return recommendations
    
    def get_taste_profile_suggestions(self, preferences: Dict) -> Dict:
        """Generate taste profile suggestions based on user preferences."""
        try:
            all_entities = []
            
            # Collect entities from all preference categories
            for category, items in preferences.items():
                if isinstance(items, list):
                    all_entities.extend(items)
                elif isinstance(items, str):
                    all_entities.append(items)
            
            if not all_entities:
                return {"success": False, "error": "No preferences provided"}
            
            # Get cross-domain affinities
            affinities_result = self.get_affinities(all_entities)
            
            if affinities_result["success"]:
                return {
                    "success": True,
                    "profile": affinities_result["affinities"],
                    "suggestions": self._create_story_suggestions(affinities_result["affinities"])
                }
            else:
                return affinities_result
                
        except Exception as e:
            return {
                "success": False,
                "error": f"Profile generation failed: {str(e)}"
            }
    
    def _create_story_suggestions(self, affinities: Dict) -> List[str]:
        """Create story theme suggestions based on affinities."""
        suggestions = []
        
        domains = list(affinities.keys())
        
        # Create cross-domain suggestions
        if len(domains) >= 2:
            for i in range(min(3, len(domains) - 1)):
                domain1 = domains[i]
                domain2 = domains[i + 1]
                
                items1 = affinities.get(domain1, [])
                items2 = affinities.get(domain2, [])
                
                if items1 and items2:
                    suggestion = f"A story combining {items1[0]} from {domain1} with {items2[0]} from {domain2}"
                    suggestions.append(suggestion)
        
        return suggestions[:5]  # Limit to 5 suggestions 