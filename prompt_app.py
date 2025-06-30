#!/usr/bin/env python3
"""
Five Principles Prompt Engineering App - Streamlit Version
=========================================================

A beautiful web application using Streamlit and LangChain that implements 
the Five Principles of Prompting to generate well-structured prompts.

The Five Principles:
1. Give Direction
2. Specify Format  
3. Provide Examples
4. Evaluate Quality
5. Divide Labor

Author: AI Assistant
Date: 2025
"""

import os
import json
import time
from typing import Dict, List, Optional, Tuple
from dataclasses import dataclass, asdict
from enum import Enum

# Streamlit imports
import streamlit as st
from streamlit_option_menu import option_menu

# LangChain imports
from langchain.llms import OpenAI
from langchain.chat_models import ChatOpenAI
from langchain.prompts import PromptTemplate, ChatPromptTemplate
from langchain.schema import HumanMessage, SystemMessage
from langchain.output_parsers import PydanticOutputParser, OutputFixingParser
from langchain.chains import LLMChain, SimpleSequentialChain
from pydantic import BaseModel, Field

# Additional imports
import plotly.express as px
import plotly.graph_objects as go
import pandas as pd


class TaskComplexity(Enum):
    """Define task complexity levels for labor division"""
    SIMPLE = "Simple"
    MODERATE = "Moderate"
    COMPLEX = "Complex"
    VERY_COMPLEX = "Very Complex"


class OutputFormat(Enum):
    """Define common output formats"""
    TEXT = "Plain Text"
    JSON = "JSON"
    LIST = "Bulleted List"
    EMAIL = "Email"
    CODE = "Code"
    ESSAY = "Essay"
    REPORT = "Report"
    CREATIVE = "Creative Writing"


@dataclass
class PromptRequest:
    """Structure for user's prompt request"""
    task_description: str
    target_audience: str = ""
    desired_tone: str = ""
    output_format: OutputFormat = OutputFormat.TEXT
    complexity: TaskComplexity = TaskComplexity.SIMPLE
    context: str = ""
    constraints: List[str] = None
    examples_needed: bool = True
    
    def __post_init__(self):
        if self.constraints is None:
            self.constraints = []


class GeneratedPrompt(BaseModel):
    """Pydantic model for the generated prompt structure"""
    direction: str = Field(description="Clear direction and context for the AI")
    format_specification: str = Field(description="Specific format requirements")
    examples: List[str] = Field(description="Relevant examples to guide the AI")
    quality_criteria: str = Field(description="Criteria for evaluating output quality")
    subtasks: List[str] = Field(description="Broken down subtasks if needed")
    final_prompt: str = Field(description="The complete, optimized prompt")
    confidence_score: float = Field(description="Confidence score (0-1) for prompt quality")


class StreamlitPromptApp:
    """Streamlit application class implementing the Five Principles of Prompting"""
    
    def __init__(self):
        """Initialize the Streamlit app"""
        self.setup_page_config()
        self.initialize_session_state()
        self.setup_llm()
        self.setup_chains()
    
    def setup_page_config(self):
        """Configure Streamlit page settings"""
        st.set_page_config(
            page_title="Five Principles Prompt Engineering",
            page_icon="🚀",
            layout="wide",
            initial_sidebar_state="expanded"
        )
        
        # Custom CSS for better styling
        st.markdown("""
        <style>
        .main-header {
            font-size: 3rem;
            color: #1f77b4;
            text-align: center;
            margin-bottom: 2rem;
        }
        .principle-card {
            background-color: #f0f2f6;
            padding: 1rem;
            border-radius: 10px;
            margin: 1rem 0;
            border-left: 5px solid #1f77b4;
        }
        .success-box {
            background-color: #d4edda;
            color: #155724;
            padding: 1rem;
            border-radius: 5px;
            margin: 1rem 0;
        }
        .warning-box {
            background-color: #fff3cd;
            color: #856404;
            padding: 1rem;
            border-radius: 5px;
            margin: 1rem 0;
        }
        .prompt-output {
            background-color: #f8f9fa;
            padding: 1.5rem;
            border-radius: 10px;
            border: 2px solid #28a745;
            margin: 1rem 0;
        }
        </style>
        """, unsafe_allow_html=True)
    
    def initialize_session_state(self):
        """Initialize Streamlit session state variables"""
        if 'generated_prompt' not in st.session_state:
            st.session_state.generated_prompt = None
        if 'prompt_components' not in st.session_state:
            st.session_state.prompt_components = None
        if 'api_key_valid' not in st.session_state:
            st.session_state.api_key_valid = False
        if 'demo_mode' not in st.session_state:
            st.session_state.demo_mode = False
    
    def setup_llm(self):
        """Setup LangChain LLM with API key handling"""
        # API Key input in sidebar
        with st.sidebar:
            st.markdown("### 🔑 API Configuration")
            
            demo_mode = st.checkbox("Demo Mode (No API Required)", value=st.session_state.demo_mode)
            st.session_state.demo_mode = demo_mode
            
            if not demo_mode:
                api_key = st.text_input(
                    "OpenAI API Key", 
                    type="password",
                    help="Enter your OpenAI API key to use live AI generation"
                )
                
                if api_key:
                    try:
                        os.environ["OPENAI_API_KEY"] = api_key
                        self.llm = ChatOpenAI(
                            model="gpt-3.5-turbo",
                            temperature=0.3,
                            max_tokens=2000
                        )
                        st.session_state.api_key_valid = True
                        st.success("✅ API key validated!")
                    except Exception as e:
                        st.error(f"❌ API key error: {e}")
                        self.llm = None
                        st.session_state.api_key_valid = False
                else:
                    self.llm = None
                    st.session_state.api_key_valid = False
            else:
                self.llm = None
                st.info("🎭 Running in demo mode")
    
    def setup_chains(self):
        """Setup LangChain chains for each principle"""
        
        # Principle 1: Give Direction Chain
        self.direction_template = PromptTemplate(
            input_variables=["task", "audience", "tone", "context"],
            template="""
            Analyze this task and create clear, specific direction:
            
            Task: {task}
            Target Audience: {audience}
            Desired Tone: {tone}
            Context: {context}
            
            Create a clear direction statement that tells the AI exactly what to do,
            who the audience is, and what tone to use. Be specific and actionable.
            
            Direction:
            """
        )
        
        # Principle 2: Specify Format Chain
        self.format_template = PromptTemplate(
            input_variables=["output_format", "constraints"],
            template="""
            Create specific format instructions for this output:
            
            Desired Format: {output_format}
            Constraints: {constraints}
            
            Provide detailed formatting requirements including structure, 
            length, style, and any specific elements that must be included.
            
            Format Specification:
            """
        )
        
        # Principle 3: Provide Examples Chain
        self.examples_template = PromptTemplate(
            input_variables=["task", "output_format", "tone"],
            template="""
            Generate 2-3 relevant examples for this task:
            
            Task: {task}
            Output Format: {output_format}
            Tone: {tone}
            
            Create examples that demonstrate exactly what good output looks like.
            Make them diverse but all high-quality.
            
            Examples:
            """
        )
        
        # Principle 4: Quality Evaluation Chain
        self.quality_template = PromptTemplate(
            input_variables=["task", "audience", "output_format"],
            template="""
            Define quality criteria for evaluating the output:
            
            Task: {task}
            Audience: {audience}
            Output Format: {output_format}
            
            Create specific, measurable criteria for what makes a high-quality response.
            Include both content quality and format adherence.
            
            Quality Criteria:
            """
        )
        
        # Principle 5: Divide Labor Chain
        self.labor_template = PromptTemplate(
            input_variables=["task", "complexity"],
            template="""
            Break down this task into manageable subtasks:
            
            Task: {task}
            Complexity: {complexity}
            
            If the task is complex, divide it into 3-5 logical subtasks.
            If it's simple, explain why it doesn't need division.
            Order the subtasks logically.
            
            Subtasks:
            """
        )
        
        # Initialize output parser
        self.output_parser = PydanticOutputParser(pydantic_object=GeneratedPrompt)
    
    def render_header(self):
        """Render the main header and introduction"""
        st.markdown('<h1 class="main-header">🚀 Five Principles Prompt Engineering</h1>', unsafe_allow_html=True)
        
        st.markdown("""
        <div style="text-align: center; margin-bottom: 2rem;">
        Transform your vague AI requests into powerful, structured prompts using the Five Principles of Prompting!
        </div>
        """, unsafe_allow_html=True)
        
        # Five Principles Overview
        with st.expander("📖 Learn About the Five Principles", expanded=False):
            col1, col2 = st.columns(2)
            
            with col1:
                st.markdown("""
                **1. 🎯 Give Direction**
                - Provide clear, specific instructions
                - Define the task and context
                - Specify the target audience
                
                **2. 📋 Specify Format**
                - Define the output structure
                - Set length and style requirements
                - Include formatting constraints
                
                **3. 💡 Provide Examples**
                - Show what good output looks like
                - Demonstrate the desired style
                - Include diverse, high-quality samples
                """)
            
            with col2:
                st.markdown("""
                **4. ✅ Evaluate Quality**
                - Define success criteria
                - Set measurable standards
                - Include both content and format requirements
                
                **5. 🔧 Divide Labor**
                - Break complex tasks into steps
                - Create logical workflows
                - Make tasks manageable and clear
                """)
    
    def collect_user_input(self) -> PromptRequest:
        """Collect user input through Streamlit interface"""
        
        st.markdown("## 📝 Tell Us About Your Task")
        
        # Main task description
        task_description = st.text_area(
            "What task do you want the AI to perform?",
            placeholder="e.g., Write a blog post about sustainable gardening for beginners",
            height=100,
            help="Be as specific as possible about what you want the AI to accomplish"
        )
        
        if not task_description:
            st.warning("⚠️ Please describe your task to continue.")
            return None
        
        # Two-column layout for additional inputs
        col1, col2 = st.columns(2)
        
        with col1:
            target_audience = st.text_input(
                "Target Audience",
                placeholder="e.g., beginner gardeners, marketing professionals",
                help="Who will be reading or using this output?"
            )
            
            desired_tone = st.text_input(
                "Desired Tone",
                placeholder="e.g., professional, friendly, academic",
                help="What tone should the AI use?"
            )
            
            context = st.text_area(
                "Additional Context",
                placeholder="Any background information or special considerations",
                height=80,
                help="Provide any relevant background information"
            )
        
        with col2:
            output_format = st.selectbox(
                "Output Format",
                options=[fmt.value for fmt in OutputFormat],
                help="How should the output be structured?"
            )
            
            complexity = st.selectbox(
                "Task Complexity",
                options=[comp.value for comp in TaskComplexity],
                index=1,  # Default to Moderate
                help="How complex is this task?"
            )
            
            examples_needed = st.checkbox(
                "Include Examples in Prompt",
                value=True,
                help="Should the generated prompt include examples?"
            )
        
        # Constraints section
        st.markdown("### 🔒 Constraints & Requirements")
        constraints_text = st.text_area(
            "Additional Constraints",
            placeholder="e.g., Under 500 words, Include 3 main points, Use formal language",
            help="Enter any specific requirements, one per line"
        )
        
        constraints = [c.strip() for c in constraints_text.split('\n') if c.strip()] if constraints_text else []
        
        # Convert string selections back to enums
        output_format_enum = next(fmt for fmt in OutputFormat if fmt.value == output_format)
        complexity_enum = next(comp for comp in TaskComplexity if comp.value == complexity)
        
        return PromptRequest(
            task_description=task_description,
            target_audience=target_audience or "general audience",
            desired_tone=desired_tone or "professional and helpful",
            output_format=output_format_enum,
            complexity=complexity_enum,
            context=context,
            constraints=constraints,
            examples_needed=examples_needed
        )
    
    def apply_five_principles(self, request: PromptRequest) -> Dict[str, str]:
        """Apply each of the five principles to generate prompt components"""
        
        components = {}
        
        if st.session_state.demo_mode or not st.session_state.api_key_valid:
            # Demo mode - return structured examples
            return self._generate_demo_components(request)
        
        # Progress bar for LLM processing
        progress_bar = st.progress(0)
        status_text = st.empty()
        
        try:
            # Principle 1: Give Direction
            status_text.text("🎯 Applying Principle 1: Give Direction...")
            progress_bar.progress(20)
            direction_chain = LLMChain(llm=self.llm, prompt=self.direction_template)
            components["direction"] = direction_chain.run(
                task=request.task_description,
                audience=request.target_audience,
                tone=request.desired_tone,
                context=request.context
            ).strip()
            
            # Principle 2: Specify Format
            status_text.text("📋 Applying Principle 2: Specify Format...")
            progress_bar.progress(40)
            format_chain = LLMChain(llm=self.llm, prompt=self.format_template)
            components["format_specification"] = format_chain.run(
                output_format=request.output_format.value,
                constraints=", ".join(request.constraints) if request.constraints else "None"
            ).strip()
            
            # Principle 3: Provide Examples
            status_text.text("💡 Applying Principle 3: Provide Examples...")
            progress_bar.progress(60)
            if request.examples_needed:
                examples_chain = LLMChain(llm=self.llm, prompt=self.examples_template)
                examples_text = examples_chain.run(
                    task=request.task_description,
                    output_format=request.output_format.value,
                    tone=request.desired_tone
                ).strip()
                components["examples"] = [ex.strip() for ex in examples_text.split('\n') if ex.strip()]
            else:
                components["examples"] = ["Examples omitted per user request"]
            
            # Principle 4: Evaluate Quality
            status_text.text("✅ Applying Principle 4: Evaluate Quality...")
            progress_bar.progress(80)
            quality_chain = LLMChain(llm=self.llm, prompt=self.quality_template)
            components["quality_criteria"] = quality_chain.run(
                task=request.task_description,
                audience=request.target_audience,
                output_format=request.output_format.value
            ).strip()
            
            # Principle 5: Divide Labor
            status_text.text("🔧 Applying Principle 5: Divide Labor...")
            progress_bar.progress(100)
            labor_chain = LLMChain(llm=self.llm, prompt=self.labor_template)
            subtasks_text = labor_chain.run(
                task=request.task_description,
                complexity=request.complexity.value
            ).strip()
            components["subtasks"] = [task.strip() for task in subtasks_text.split('\n') if task.strip()]
            
            status_text.text("✅ All principles applied successfully!")
            time.sleep(1)  # Brief pause to show completion
            
        except Exception as e:
            st.error(f"Error applying principles: {e}")
            components = self._generate_demo_components(request)
        
        finally:
            progress_bar.empty()
            status_text.empty()
        
        return components
    
    def _generate_demo_components(self, request: PromptRequest) -> Dict[str, str]:
        """Generate demo components when LLM is not available"""
        return {
            "direction": f"You are an expert assistant helping {request.target_audience}. "
                        f"Your task is to {request.task_description}. "
                        f"Use a {request.desired_tone} tone throughout your response. "
                        f"Context: {request.context}",
            
            "format_specification": f"Format your response as {request.output_format.value}. "
                                  f"Additional constraints: {', '.join(request.constraints) if request.constraints else 'None'}",
            
            "examples": [
                f"Example 1: [Sample output for {request.task_description}]",
                f"Example 2: [Another sample showing good {request.output_format.value} format]",
                f"Example 3: [Third example demonstrating {request.desired_tone} tone]"
            ] if request.examples_needed else ["Examples omitted per user request"],
            
            "quality_criteria": f"Ensure your response: 1) Directly addresses {request.task_description}, "
                              f"2) Is appropriate for {request.target_audience}, "
                              f"3) Follows the {request.output_format.value} format exactly, "
                              f"4) Maintains {request.desired_tone} tone",
            
            "subtasks": [
                f"Step 1: Analyze the {request.task_description} requirements",
                f"Step 2: Research relevant information for {request.target_audience}",
                f"Step 3: Structure content in {request.output_format.value} format",
                f"Step 4: Review and refine for {request.desired_tone} tone"
            ] if request.complexity != TaskComplexity.SIMPLE else ["Task is simple enough to complete in one step"]
        }
    
    def assemble_final_prompt(self, components: Dict[str, str]) -> GeneratedPrompt:
        """Assemble all components into the final optimized prompt"""
        
        # Create final prompt structure
        final_prompt = f"""
{components['direction']}

{components['format_specification']}

Examples of good output:
{chr(10).join(f'- {ex}' for ex in components['examples'])}

Quality criteria:
{components['quality_criteria']}

Approach this task step by step:
{chr(10).join(f'{i+1}. {task}' for i, task in enumerate(components['subtasks']))}

Now, please complete the task following all the above guidelines.
"""
        
        # Calculate confidence score based on completeness
        confidence_factors = [
            len(components.get("direction", "")) > 50,
            len(components.get("format_specification", "")) > 20,
            len(components.get("examples", [])) > 0,
            len(components.get("quality_criteria", "")) > 30,
            len(components.get("subtasks", [])) > 0
        ]
        confidence_score = sum(confidence_factors) / len(confidence_factors)
        
        return GeneratedPrompt(
            direction=components["direction"],
            format_specification=components["format_specification"],
            examples=components["examples"],
            quality_criteria=components["quality_criteria"],
            subtasks=components["subtasks"],
            final_prompt=final_prompt.strip(),
            confidence_score=confidence_score
        )
    
    def display_results(self, result: GeneratedPrompt, components: Dict[str, str]):
        """Display the generated prompt results in Streamlit"""
        
        st.markdown("## 🎉 Your Optimized Prompt is Ready!")
        
        # Confidence score with visual indicator
        col1, col2, col3 = st.columns([1, 2, 1])
        with col2:
            confidence_percentage = result.confidence_score * 100
            st.metric(
                label="Confidence Score", 
                value=f"{confidence_percentage:.0f}%",
                help="How confident we are in the prompt quality"
            )
            
            # Visual confidence indicator
            if confidence_percentage >= 80:
                st.success("🎯 Excellent prompt quality!")
            elif confidence_percentage >= 60:
                st.info("👍 Good prompt quality")
            else:
                st.warning("⚠️ Consider refining your inputs")
        
        # Tabs for different views
        tab1, tab2, tab3 = st.tabs(["📋 Final Prompt", "🔍 Principle Breakdown", "📊 Analysis"])
        
        with tab1:
            st.markdown("### 🎯 Your Optimized Prompt")
            st.markdown(f'<div class="prompt-output">{result.final_prompt}</div>', unsafe_allow_html=True)
            
            # Copy button and download
            col1, col2 = st.columns(2)
            with col1:
                if st.button("📋 Copy to Clipboard", use_container_width=True):
                    st.code(result.final_prompt, language="text")
                    st.success("Prompt ready to copy!")
            
            with col2:
                st.download_button(
                    label="💾 Download Prompt",
                    data=result.final_prompt,
                    file_name="optimized_prompt.txt",
                    mime="text/plain",
                    use_container_width=True
                )
        
        with tab2:
            st.markdown("### 🔍 How Each Principle Was Applied")
            
            principles = [
                ("🎯 Give Direction", result.direction),
                ("📋 Specify Format", result.format_specification),
                ("💡 Provide Examples", "\n".join(f"• {ex}" for ex in result.examples)),
                ("✅ Evaluate Quality", result.quality_criteria),
                ("🔧 Divide Labor", "\n".join(f"{i+1}. {task}" for i, task in enumerate(result.subtasks)))
            ]
            
            for title, content in principles:
                with st.expander(title, expanded=False):
                    st.write(content)
        
        with tab3:
            st.markdown("### 📊 Prompt Analysis")
            
            # Create analysis metrics
            analysis_data = {
                "Principle": ["Direction", "Format", "Examples", "Quality", "Labor"],
                "Completeness": [
                    min(len(result.direction) / 100, 1.0),
                    min(len(result.format_specification) / 50, 1.0),
                    min(len(result.examples) / 2, 1.0),
                    min(len(result.quality_criteria) / 75, 1.0),
                    min(len(result.subtasks) / 3, 1.0)
                ]
            }
            
            # Create radar chart
            fig = go.Figure()
            fig.add_trace(go.Scatterpolar(
                r=analysis_data["Completeness"],
                theta=analysis_data["Principle"],
                fill='toself',
                name='Completeness Score'
            ))
            
            fig.update_layout(
                polar=dict(
                    radialaxis=dict(
                        visible=True,
                        range=[0, 1]
                    )),
                showlegend=False,
                title="Principle Implementation Completeness"
            )
            
            st.plotly_chart(fig, use_container_width=True)
            
            # Word count analysis
            word_counts = {
                "Direction": len(result.direction.split()),
                "Format Spec": len(result.format_specification.split()),
                "Quality Criteria": len(result.quality_criteria.split()),
                "Final Prompt": len(result.final_prompt.split())
            }
            
            df_words = pd.DataFrame(list(word_counts.items()), columns=["Component", "Word Count"])
            fig_bar = px.bar(df_words, x="Component", y="Word Count", title="Word Count by Component")
            st.plotly_chart(fig_bar, use_container_width=True)
    
    def run(self):
        """Main Streamlit application"""
        
        # Render header
        self.render_header()
        
        # Main application flow
        request = self.collect_user_input()
        
        if request:
            if st.button("🚀 Generate Optimized Prompt", type="primary", use_container_width=True):
                with st.spinner("Applying the Five Principles..."):
                    # Apply the five principles
                    components = self.apply_five_principles(request)
                    st.session_state.prompt_components = components
                    
                    # Assemble final prompt
                    result = self.assemble_final_prompt(components)
                    st.session_state.generated_prompt = result
                
                # Display results
                if st.session_state.generated_prompt:
                    self.display_results(st.session_state.generated_prompt, st.session_state.prompt_components)
        
        # Footer
        st.markdown("---")
        st.markdown("""
        <div style="text-align: center; color: #666;">
        Built with ❤️ using Streamlit and LangChain | 
        <a href="https://github.com" target="_blank">GitHub</a> | 
        <a href="mailto:contact@example.com">Contact</a>
        </div>
        """, unsafe_allow_html=True)


def main():
    """Entry point for the Streamlit application"""
    app = StreamlitPromptApp()
    app.run()


if __name__ == "__main__":
    main()
