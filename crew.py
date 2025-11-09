from crewai import Crew, Process
import streamlit as st  # Fixed: was 'Streamlit'
from tools import get_yt_tool
from agent import create_agents
from tasks import create_tasks

# Get user inputs
input_channel_name = "@"+st.text_input("Enter Channel Name (e.g., krishnaik06):", placeholder="@krishnaik06")

# Don't add @ here - let the tool function handle it
input_topic = st.text_input("Enter the topic for which you want to blog about:", placeholder="Machine Learning")

# Only proceed if both inputs are provided
if st.button("Generate Blog") and input_channel_name and input_topic:
    with st.spinner("Generating your blog post..."):
        # Initialize the YouTube tool with the channel name
        yt_tool = get_yt_tool(input_channel_name)
        
        # Create agents with the tool
        blog_researcher, blog_writer = create_agents(yt_tool)
        
        # Create tasks with the tool and agents
        research_task, write_task = create_tasks(yt_tool, blog_researcher, blog_writer)
        
        # Forming the tech-focused crew with some enhanced configurations
        crew = Crew(
            agents=[blog_researcher, blog_writer],
            tasks=[research_task, write_task],
            process=Process.sequential,  # Optional: Sequential task execution is default
            memory=True,
            cache=True,
            max_rpm=100,
            share_crew=True
        )

        # Start the task execution process with enhanced feedback
        result = crew.kickoff(inputs={'topic': input_topic})
        
        st.success("Blog post generated!")
        st.markdown("### Generated Blog Post")
        st.write(result)