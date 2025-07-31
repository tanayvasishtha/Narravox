import os
import requests
from typing import Dict, List, Optional
from dotenv import load_dotenv

load_dotenv()

class PerplexityService:
    def __init__(self):
        self.api_key = os.getenv("PERPLEXITY_API_KEY")
        self.base_url = "https://api.perplexity.ai"
        self.headers = {
            "Authorization": f"Bearer {self.api_key}",
            "Content-Type": "application/json"
        }
    
    def generate_story_opener(self, prompt: str, cultural_context: str = "") -> Dict:
        """Generate initial story content based on user prompt and cultural context."""
        try:
            enhanced_prompt = self._create_story_prompt(prompt, cultural_context)
            
            payload = {
                "model": "sonar-pro",
                "messages": [
                    {
                        "role": "system",
                        "content": "You are a creative storyteller who crafts engaging narratives. Create vivid, immersive story openings that incorporate cultural elements naturally. Keep responses to 2-3 paragraphs."
                    },
                    {
                        "role": "user",
                        "content": enhanced_prompt
                    }
                ],
                "max_tokens": 300,
                "temperature": 0.7
            }
            
            response = requests.post(
                f"{self.base_url}/chat/completions",
                headers=self.headers,
                json=payload,
                timeout=30
            )
            
            if response.status_code == 200:
                data = response.json()
                return {
                    "success": True,
                    "content": data["choices"][0]["message"]["content"],
                    "usage": data.get("usage", {})
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
    
    def continue_story(self, story_history: List[Dict], user_input: str, cultural_context: str = "") -> Dict:
        """Continue the story based on history and new user input."""
        try:
            messages = [
                {
                    "role": "system",
                    "content": "You are continuing a collaborative story. Maintain narrative consistency and incorporate cultural elements naturally. Respond with 2-3 paragraphs that advance the plot."
                }
            ]
            
            # Add conversation history
            for entry in story_history[-6:]:  # Last 6 turns for context
                messages.append({
                    "role": "user" if entry["type"] == "user" else "assistant",
                    "content": entry["content"]
                })
            
            # Add current user input with cultural context
            enhanced_input = self._enhance_with_culture(user_input, cultural_context)
            messages.append({
                "role": "user",
                "content": enhanced_input
            })
            
            payload = {
                "model": "sonar-pro",
                "messages": messages,
                "max_tokens": 300,
                "temperature": 0.7
            }
            
            response = requests.post(
                f"{self.base_url}/chat/completions",
                headers=self.headers,
                json=payload,
                timeout=30
            )
            
            if response.status_code == 200:
                data = response.json()
                return {
                    "success": True,
                    "content": data["choices"][0]["message"]["content"],
                    "usage": data.get("usage", {})
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
    
    def generate_branching_options(self, current_story: str, cultural_context: str = "") -> Dict:
        """Generate multiple story continuation options."""
        try:
            prompt = f"""Based on this story:

{current_story}

Generate 3 distinct continuation options that:
1. Advance the plot in different directions
2. Incorporate these cultural elements: {cultural_context}
3. Each option should be 1-2 sentences

Format as:
Option 1: [continuation]
Option 2: [continuation]  
Option 3: [continuation]"""

            payload = {
                "model": "sonar-pro",
                "messages": [
                    {
                        "role": "system",
                        "content": "You are a creative storyteller generating branching narrative options. Provide exactly 3 distinct, engaging choices."
                    },
                    {
                        "role": "user",
                        "content": prompt
                    }
                ],
                "max_tokens": 200,
                "temperature": 0.8
            }
            
            response = requests.post(
                f"{self.base_url}/chat/completions",
                headers=self.headers,
                json=payload,
                timeout=30
            )
            
            if response.status_code == 200:
                data = response.json()
                content = data["choices"][0]["message"]["content"]
                options = self._parse_options(content)
                return {
                    "success": True,
                    "options": options,
                    "usage": data.get("usage", {})
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
    
    def _create_story_prompt(self, user_prompt: str, cultural_context: str) -> str:
        """Create enhanced prompt with cultural context."""
        base_prompt = f"Create an engaging story opening based on: {user_prompt}"
        
        if cultural_context:
            base_prompt += f"\n\nIncorporate these cultural elements naturally: {cultural_context}"
        
        return base_prompt
    
    def _enhance_with_culture(self, user_input: str, cultural_context: str) -> str:
        """Enhance user input with cultural context."""
        enhanced = user_input
        
        if cultural_context:
            enhanced += f"\n\nConsider incorporating: {cultural_context}"
        
        return enhanced
    
    def _parse_options(self, content: str) -> List[str]:
        """Parse branching options from API response."""
        options = []
        lines = content.split('\n')
        
        for line in lines:
            line = line.strip()
            if line.startswith(('Option 1:', 'Option 2:', 'Option 3:')):
                option_text = line.split(':', 1)[1].strip()
                options.append(option_text)
        
        # Fallback if parsing fails
        if len(options) != 3:
            options = [
                "Continue with the current storyline",
                "Introduce a plot twist",
                "Shift perspective to another character"
            ]
        
        return options 