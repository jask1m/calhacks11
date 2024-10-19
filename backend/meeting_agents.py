from uagents import Model, Agent, Context, Bureau
from typing import Dict, Any
import google.generativeai as genai
import os

class Engagement(Model):
    engagement: str

engagement_boost_agent = Agent(
    name = "Engagement Boost Agent",
    seed = "Engagement Boost Agent recovery phrase"
)

@engagement_boost_agent.on_event("startup")
async def startup(ctx: Context):
    ctx.logger.info(f"Starting up {engagement_boost_agent.name}")
    ctx.logger.info(f"With address: {engagement_boost_agent.address}")

@engagement_boost_agent.on_query(model=Engagement)
async def engagement_boost_query(ctx: Context, engagement: Engagement):
    if engagement.engagement == "low":
        genai.configure(api_key=os.getenv("GEMINI_API_KEY"))
        model = genai.GenerativeModel('models/gemini-1.5-pro-latest')

        input_prompt = """
        The engagement levels in the meeting are low. Generate a reminder or prompt to encourage participants to ask questions, vote in polls, or participate in discussions.
        """

        generated_content = model.generate(input_prompt)
        ctx.logger.info(f"Generated reminder: {generated_content}")

        # Send the generated content to participants
        await ctx.send(engagement_boost_agent.address, {"message": generated_content})

        return generated_content