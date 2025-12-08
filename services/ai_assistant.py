# AIAssistant service class
import streamlit as st
import google.generativeai as genai
from typing import List, Dict, Optional
import re

class AIAssistant:
    """Wrapper around Google Gemini AI for chat functionality."""

    def __init__(self, system_prompt: str = "You are a helpful assistant.", 
                 history_key: str = "chat_history"):
        self._system_prompt = system_prompt
        self._history_key = history_key
        self._model = None
        self._model_name = None
        self._supports_system_instruction = False
        self._configure_api()

    def _configure_api(self) -> None:
        """Configure the Gemini API with the key from secrets."""
        api_key = st.secrets.get("GOOGLE_API_KEY")
        if not api_key:
            self._model = None
            return
            
        try:
            genai.configure(api_key=api_key)
            
            # First, try to get list of available models
            available_model_names = []
            try:
                models = genai.list_models()
                for model in models:
                    if hasattr(model, 'supported_generation_methods'):
                        if 'generateContent' in model.supported_generation_methods:
                            # Remove 'models/' prefix if present
                            model_name = model.name.replace('models/', '')
                            available_model_names.append(model_name)
            except:
                pass  # If listing fails, continue with default list
            
            # Build list of models to try: available ones first, then defaults
            model_names = []
            if available_model_names:
                # Use available models first
                model_names.extend(available_model_names[:3])  # Try first 3 available
            # Add fallback models
            model_names.extend([
                "gemini-pro",           # Most widely available
                "models/gemini-pro",    # With models/ prefix
            ])
            
            self._model = None
            self._model_name = None
            last_error = None
            
            for model_name in model_names:
                try:
                    # Try to use system_instruction first (preferred)
                    try:
                        self._model = genai.GenerativeModel(
                            model_name=model_name,
                            system_instruction=self._system_prompt
                        )
                        self._model_name = model_name
                        self._supports_system_instruction = True
                        break  # Successfully created model
                    except Exception as e1:
                        # system_instruction not supported, try without it
                        try:
                            self._model = genai.GenerativeModel(model_name=model_name)
                            self._model_name = model_name
                            self._supports_system_instruction = False
                            break  # Successfully created model without system instruction
                        except Exception as e2:
                            # Both failed, try next model
                            last_error = e2 if "404" not in str(e1) else e1
                            continue
                            
                except Exception as e:
                    last_error = e
                    continue
            
            if self._model is None:
                # All models failed, store the last error
                self._model = None
                if "api_error" not in st.session_state:
                    error_msg = str(last_error) if last_error else "No available models found"
                    st.session_state["api_error"] = error_msg
                    # Also try to list available models for better error message
                    try:
                        available = self.list_available_models(api_key)
                        if available and len(available) > 0:
                            st.session_state["api_error"] += f"\n\nAvailable models: {', '.join(available[:5])}"
                    except:
                        pass
                    
        except Exception as e:
            # Configuration error
            self._model = None
            if "api_error" not in st.session_state:
                st.session_state["api_error"] = str(e)

    def is_configured(self) -> bool:
        """Check if API is properly configured."""
        return self._model is not None
    
    @staticmethod
    def list_available_models(api_key: str) -> List[str]:
        """List all available models for debugging."""
        try:
            genai.configure(api_key=api_key)
            models = genai.list_models()
            available = []
            for model in models:
                # Check if model supports generateContent
                if hasattr(model, 'supported_generation_methods'):
                    if 'generateContent' in model.supported_generation_methods:
                        # Extract just the model name (remove 'models/' prefix if present)
                        model_name = model.name.replace('models/', '')
                        available.append(model_name)
            return available if available else ["No models found"]
        except Exception as e:
            return [f"Error listing models: {str(e)}"]
    
    def _is_quota_error(self, error: Exception) -> bool:
        """Check if error is a quota/rate limit error."""
        error_str = str(error).lower()
        quota_indicators = [
            "quota",
            "rate limit",
            "429",
            "exceeded",
            "free_tier"
        ]
        return any(indicator in error_str for indicator in quota_indicators)
    
    def _extract_retry_delay(self, error: Exception) -> Optional[int]:
        """Extract retry delay from error message if available."""
        error_str = str(error)
        if "retry in" in error_str.lower():
            try:
                # Try to extract seconds from error message
                match = re.search(r'retry in ([\d.]+)s', error_str.lower())
                if match:
                    return int(float(match.group(1))) + 1  # Add 1 second buffer
            except:
                pass
        return None

    def set_system_prompt(self, prompt: str) -> None:
        """Update the system prompt and reinitialize model."""
        self._system_prompt = prompt
        self._configure_api()

    def get_history(self) -> List[Dict[str, str]]:
        """Get chat history from session state."""
        if self._history_key not in st.session_state:
            st.session_state[self._history_key] = []
        return st.session_state[self._history_key]

    def add_to_history(self, role: str, content: str) -> None:
        """Add a message to chat history."""
        history = self.get_history()
        history.append({"role": role, "content": content})

    def clear_history(self) -> None:
        """Clear the chat history."""
        st.session_state[self._history_key] = []

    def send_message(self, user_message: str) -> str:
        """Send a message and get AI response with streaming."""
        if not self.is_configured():
            return "Error: API not configured"

        # Add user message to history
        self.add_to_history("user", user_message)

        # Build conversation history for API
        history = self.get_history()
        
        # If model doesn't support system_instruction, prepend it to first message
        if not self._supports_system_instruction and len(history) == 1:
            # First message, include system prompt
            enhanced_message = f"{self._system_prompt}\n\nUser: {user_message}"
        else:
            enhanced_message = user_message
        
        chat = self._model.start_chat(history=[
            {"role": m["role"], "parts": [m["content"]]}
            for m in history[:-1]
        ])

        # Get response
        try:
            response = chat.send_message(enhanced_message)
            reply = response.text
            self.add_to_history("model", reply)
            return reply
        except Exception as e:
            if self._is_quota_error(e):
                retry_delay = self._extract_retry_delay(e)
                if retry_delay:
                    return f"⚠️ **API Quota Exceeded**\n\nYou've reached the free tier limit for the Gemini API. Please wait {retry_delay} seconds before trying again, or check your [API usage](https://ai.dev/usage?tab=rate-limit).\n\n**Alternative:** You can continue using the dashboard features without the AI assistant."
                else:
                    return "⚠️ **API Quota Exceeded**\n\nYou've reached the free tier limit for the Gemini API. Please check your [API usage](https://ai.dev/usage?tab=rate-limit) or wait a few minutes before trying again.\n\n**Alternative:** You can continue using the dashboard features without the AI assistant."
            return f"❌ **API Error:** {str(e)}\n\nPlease check your API configuration or try again later."

    def send_message_stream(self, user_message: str, container):
        """Send a message and stream the response to a container."""
        if not self.is_configured():
            container.markdown("❌ **Error:** API not configured. Please check your API key in `.streamlit/secrets.toml`")
            return "Error: API not configured"

        # Add user message to history
        self.add_to_history("user", user_message)

        # Build conversation history for API
        history = self.get_history()
        
        # If model doesn't support system_instruction, prepend it to first message
        if not self._supports_system_instruction and len(history) == 1:
            # First message, include system prompt
            enhanced_message = f"{self._system_prompt}\n\nUser: {user_message}"
        else:
            enhanced_message = user_message
        
        chat = self._model.start_chat(history=[
            {"role": m["role"], "parts": [m["content"]]}
            for m in history[:-1]
        ])

        # Get streaming response
        try:
            full_reply = ""
            response = chat.send_message(enhanced_message, stream=True)
            for chunk in response:
                if chunk.text:
                    full_reply += chunk.text
                    container.markdown(full_reply + "▌")
            container.markdown(full_reply)
            self.add_to_history("model", full_reply)
            return full_reply
        except Exception as e:
            if self._is_quota_error(e):
                retry_delay = self._extract_retry_delay(e)
                if retry_delay:
                    error_msg = f"""⚠️ **API Quota Exceeded**

You've reached the free tier limit for the Gemini API. Please wait **{retry_delay} seconds** before trying again.

**What you can do:**
- Check your [API usage dashboard](https://ai.dev/usage?tab=rate-limit)
- Wait for the quota to reset (usually daily)
- Continue using other dashboard features without the AI assistant

**Note:** The free tier has limited requests per day. Consider upgrading your API plan for higher limits."""
                else:
                    error_msg = """⚠️ **API Quota Exceeded**

You've reached the free tier limit for the Gemini API. 

**What you can do:**
- Check your [API usage dashboard](https://ai.dev/usage?tab=rate-limit)
- Wait a few minutes and try again
- Continue using other dashboard features without the AI assistant

**Note:** The free tier has limited requests per day. Consider upgrading your API plan for higher limits."""
            else:
                error_msg = f"""❌ **API Error**

{str(e)}

**Troubleshooting:**
- Check your API key configuration in `.streamlit/secrets.toml`
- Verify your API key is valid at [Google AI Studio](https://aistudio.google.com/)
- Try again in a few moments"""
            
            container.markdown(error_msg)
            # Don't add error messages to history
            return error_msg

