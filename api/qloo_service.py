import os
import requests
from typing import Dict, List, Optional
from dotenv import load_dotenv

load_dotenv()

class QlooService:
    def __init__(self):
        self.api_key = os.getenv("QLOO_API_KEY")
        self.base_url = os.getenv("QLOO_BASE_URL", "https://hackathon.api.qloo.com")
        
        # Debug: Check if API key is loaded
        if not self.api_key:
            print("WARNING: QLOO_API_KEY not found in environment variables")
        
        # Try different authentication methods
        self.headers = {
            "X-API-Key": self.api_key,  # Try X-API-Key header
            "Content-Type": "application/json"
        }
        
        # Alternative headers if X-API-Key doesn't work
        self.headers_alt = {
            "Authorization": f"Bearer {self.api_key}",
            "Content-Type": "application/json"
        }
        
        # Debug: Print headers for troubleshooting
        print(f"Qloo API Headers: {self.headers}")
    
    def get_affinities(self, entities: List[str], domains: List[str] = None) -> Dict:
        """Get cultural affinities using Qloo Insights API with Taste Analysis."""
        try:
            if not entities:
                return {"success": False, "error": "No entities provided"}
            
            # Use the correct Insights API endpoint
            endpoint = f"{self.base_url}/v2/insights"
            
            # Build query parameters according to Insights API with Taste Analysis
            params = {
                "filter.type": "urn:tag"
            }
            
            # Add entity types based on domains
            entity_types = []
            if domains:
                for domain in domains:
                    if domain == "music":
                        entity_types.append("urn:entity:music")
                    elif domain == "film":
                        entity_types.append("urn:entity:movie")
                    elif domain == "television":
                        entity_types.append("urn:entity:tv_show")
                    elif domain == "books":
                        entity_types.append("urn:entity:book")
                    elif domain == "travel":
                        entity_types.append("urn:entity:place")
                    elif domain == "brands":
                        entity_types.append("urn:entity:brand")
            
            if entity_types:
                params["filter.parents.types"] = ",".join(entity_types)
            
            # Try to use entities directly as signal.interests.tags instead of entities
            if entities:
                # Use tags instead of entities for better compatibility
                params["signal.interests.tags"] = ",".join(entities[:5])  # Limit to 5 entities
            
            # Try with X-API-Key header (primary method)
            response = requests.get(
                endpoint,
                headers=self.headers,
                params=params,
                timeout=30
            )
            
            # If 401, try with Authorization header
            if response.status_code == 401:
                response = requests.get(
                    endpoint,
                    headers=self.headers_alt,
                    params=params,
                    timeout=30
                )
            
            if response.status_code == 200:
                data = response.json()
                return {
                    "success": True,
                    "affinities": self._process_taste_analysis(data),
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
        """Get recommendations using Qloo Insights API with Taste Analysis."""
        try:
            if not seed_entities:
                return {"success": False, "error": "No seed entities provided"}
            
            # Use the correct Insights API endpoint
            endpoint = f"{self.base_url}/v2/insights"
            
            # Build query parameters for recommendations
            params = {
                "filter.type": "urn:tag"
            }
            
            # Map target domain to entity type
            domain_mapping = {
                "music": "urn:entity:music",
                "film": "urn:entity:movie",
                "television": "urn:entity:tv_show",
                "books": "urn:entity:book",
                "travel": "urn:entity:place",
                "brands": "urn:entity:brand"
            }
            
            if target_domain in domain_mapping:
                params["filter.parents.types"] = domain_mapping[target_domain]
            
            # Add signal entities from seed
            if seed_entities:
                params["signal.interests.entities"] = ",".join(seed_entities[:3])  # Limit to 3 entities
            
            # Try with X-API-Key header (primary method)
            response = requests.get(
                endpoint,
                headers=self.headers,
                params=params,
                timeout=30
            )
            
            # If 401, try with Authorization header
            if response.status_code == 401:
                response = requests.get(
                    endpoint,
                    headers=self.headers_alt,
                    params=params,
                    timeout=30
                )
            
            if response.status_code == 200:
                data = response.json()
                return {
                    "success": True,
                    "recommendations": self._process_taste_analysis_recommendations(data, target_domain),
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
    
    def _get_affinities_fallback(self, entities: List[str], domains: List[str] = None) -> Dict:
        """Fallback method when entity search fails."""
        try:
            # Create basic affinities from entities without API call
            affinities = {}
            
            if domains:
                for domain in domains:
                    affinities[domain] = entities[:3]  # Use original entities as fallback
            
            return {
                "success": True,
                "affinities": affinities,
                "source": "fallback"
            }
            
        except Exception as e:
            return {
                "success": False,
                "error": f"Fallback failed: {str(e)}"
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
    
    def search_entities(self, query: str, entity_type: str = None) -> List[str]:
        """Search for entities using Qloo Entity Search API."""
        try:
            endpoint = f"{self.base_url}/entity_search"
            
            params = {
                "q": query,
                "limit": 5
            }
            
            if entity_type:
                params["type"] = entity_type
            
            # Try with X-API-Key header
            response = requests.get(
                endpoint,
                headers=self.headers,
                params=params,
                timeout=30
            )
            
            # If 401, try with Authorization header
            if response.status_code == 401:
                response = requests.get(
                    endpoint,
                    headers=self.headers_alt,
                    params=params,
                    timeout=30
                )
            
            if response.status_code == 200:
                data = response.json()
                entities = []
                
                if "results" in data and "entities" in data["results"]:
                    for entity in data["results"]["entities"]:
                        entity_id = entity.get("entity_id", "")
                        if entity_id:
                            entities.append(entity_id)
                
                return entities
            else:
                print(f"Entity search failed: {response.status_code} - {response.text}")
                return []
                
        except Exception as e:
            print(f"Entity search exception: {e}")
            return []
    
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
    
    def _process_taste_analysis(self, raw_data: Dict) -> Dict:
        """Process Insights API response with Taste Analysis into organized format."""
        try:
            affinities = {}
            
            # Handle Insights API response format with Taste Analysis
            if "results" in raw_data and "tags" in raw_data["results"]:
                tags = raw_data["results"]["tags"]
                
                # Group tags by their types and relevance
                for tag in tags[:15]:  # Look at more tags for better filtering
                    tag_name = tag.get("name", "")
                    tag_types = tag.get("types", [])
                    
                    # Skip tags that are too generic or irrelevant
                    generic_tags = [
                        "coin toss", "hair pulling", "experiment", "timeline", 
                        "truth or dare", "twerking", "announcement", "thrown out",
                        "self absorption", "coral reef", "unwed pregnancy"
                    ]
                    
                    if tag_name.lower() in generic_tags:
                        continue
                    
                    # Map tag types to domains with better filtering
                    for tag_type in tag_types:
                        if "movie" in tag_type or "tv_show" in tag_type:
                            if "film" not in affinities:
                                affinities["film"] = []
                            if tag_name not in affinities["film"]:
                                affinities["film"].append(tag_name)
                        elif "music" in tag_type:
                            if "music" not in affinities:
                                affinities["music"] = []
                            if tag_name not in affinities["music"]:
                                affinities["music"].append(tag_name)
                        elif "book" in tag_type:
                            if "books" not in affinities:
                                affinities["books"] = []
                            if tag_name not in affinities["books"]:
                                affinities["books"].append(tag_name)
                        elif "place" in tag_type:
                            if "travel" not in affinities:
                                affinities["travel"] = []
                            if tag_name not in affinities["travel"]:
                                affinities["travel"].append(tag_name)
                        elif "brand" in tag_type:
                            if "brands" not in affinities:
                                affinities["brands"] = []
                            if tag_name not in affinities["brands"]:
                                affinities["brands"].append(tag_name)
                
                # If no relevant results, add some cultural themes based on common patterns
                if not affinities:
                    affinities = {
                        "film": ["Cinematic storytelling", "Visual narrative", "Dramatic tension"],
                        "music": ["Rhythmic elements", "Melodic themes", "Cultural soundscape"],
                        "books": ["Literary depth", "Character development", "Narrative structure"],
                        "travel": ["Cultural exploration", "Geographic diversity", "Urban landscapes"],
                        "brands": ["Lifestyle integration", "Cultural identity", "Modern aesthetics"]
                    }
                
                # Limit each domain to 3 items
                for domain in affinities:
                    affinities[domain] = affinities[domain][:3]
            
            return affinities
            
        except Exception as e:
            print(f"Error processing taste analysis: {e}")
            return {}
    
    def _process_recommendations(self, raw_data: Dict, domain: str) -> List[str]:
        """Process raw recommendation data into list of names."""
        recommendations = []
        
        if "recommendations" in raw_data:
            for rec in raw_data["recommendations"]:
                name = rec.get("name", "")
                if name:
                    recommendations.append(name)
        
        return recommendations
    
    def _process_taste_analysis_recommendations(self, raw_data: Dict, domain: str) -> List[str]:
        """Process Insights API recommendations with Taste Analysis into list of names."""
        try:
            recommendations = []
            
            # Handle Insights API response format with Taste Analysis
            if "results" in raw_data and "tags" in raw_data["results"]:
                tags = raw_data["results"]["tags"]
                
                # Map domain to tag types
                domain_mapping = {
                    "music": ["urn:entity:music"],
                    "film": ["urn:entity:movie", "urn:entity:tv_show"],
                    "television": ["urn:entity:tv_show"],
                    "books": ["urn:entity:book"],
                    "travel": ["urn:entity:place"],
                    "brands": ["urn:entity:brand"]
                }
                
                target_types = domain_mapping.get(domain, [])
                
                # Filter tags by domain type
                for tag in tags[:10]:  # Limit to 10 tags
                    tag_name = tag.get("name", "")
                    tag_types = tag.get("types", [])
                    
                    # Check if tag belongs to target domain
                    for tag_type in tag_types:
                        if any(target_type in tag_type for target_type in target_types):
                            if tag_name and tag_name not in recommendations:
                                recommendations.append(tag_name)
                                break
                
                # Limit to requested number
                recommendations = recommendations[:5]
            
            return recommendations
            
        except Exception as e:
            print(f"Error processing taste analysis recommendations: {e}")
            return []
    
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
            
            # Filter out empty entities
            all_entities = [entity.strip() for entity in all_entities if entity.strip()]
            
            if not all_entities:
                return {"success": False, "error": "No valid preferences provided"}
            
            # Try Qloo API first - this is the primary method for hackathon
            try:
                # Limit entities to avoid API overload
                if len(all_entities) > 10:
                    all_entities = all_entities[:10]
                
                # Get cross-domain affinities from Qloo API
                affinities_result = self.get_affinities(all_entities)
                
                if affinities_result["success"]:
                    return {
                        "success": True,
                        "profile": affinities_result["affinities"],
                        "suggestions": self._create_story_suggestions(affinities_result["affinities"]),
                        "source": "qloo_api"
                    }
                else:
                    # Log the error for debugging
                    print(f"Qloo API failed: {affinities_result.get('error', 'Unknown error')}")
                    
            except Exception as e:
                print(f"Qloo API exception: {e}")
            
            # Only use fallback if Qloo API completely fails
            print("Using fallback profile generation")
            return self._create_basic_profile(preferences, all_entities)
                
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
    
    def _create_basic_profile(self, preferences: Dict, entities: List[str]) -> Dict:
        """Create a basic cultural profile from user preferences when Qloo API is unavailable."""
        try:
            suggestions = []
            
            # Create suggestions based on user preferences
            for category, items in preferences.items():
                if items and len(items) > 0:
                    # Create story themes based on preferences
                    if category == "music":
                        for item in items[:2]:
                            suggestions.append(f"Stories with {item} music themes")
                    elif category == "film":
                        for item in items[:2]:
                            suggestions.append(f"Stories inspired by {item} cinematic style")
                    elif category == "books":
                        for item in items[:2]:
                            suggestions.append(f"Stories with {item} literary elements")
                    elif category == "travel":
                        for item in items[:2]:
                            suggestions.append(f"Stories set in {item} locations")
                    elif category == "brands":
                        for item in items[:2]:
                            suggestions.append(f"Stories featuring {item} lifestyle elements")
                    elif category == "other":
                        for item in items[:2]:
                            suggestions.append(f"Stories incorporating {item} interests")
            
            # Create cross-category suggestions
            categories = list(preferences.keys())
            if len(categories) >= 2:
                for i in range(min(3, len(categories) - 1)):
                    cat1 = categories[i]
                    cat2 = categories[i + 1]
                    items1 = preferences.get(cat1, [])
                    items2 = preferences.get(cat2, [])
                    
                    if items1 and items2:
                        suggestions.append(f"Stories combining {items1[0]} from {cat1} with {items2[0]} from {cat2}")
            
            return {
                "success": True,
                "profile": {"basic_preferences": preferences},
                "suggestions": suggestions[:5],
                "fallback": True
            }
            
        except Exception as e:
            return {
                "success": False,
                "error": f"Basic profile creation failed: {str(e)}"
            } 