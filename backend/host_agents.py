from uagents import Model, Agent, Context, Bureau
from typing import Dict, Any
import google.generativeai as genai
import os

# Class for the emotion
class Emotion(Model):
    emotion: str


audience_feedback_agent = Agent(
    name = "Audience Feedback Agent",
    seed = "Audience Feedback Agent recovery phrase"
)

sentiment_analysis_agent = Agent(
    name = "Sentiment Analysis Agent",
    seed = "Sentiment Analysis Agent recovery phrase"
)

@audience_feedback_agent.on_event("startup")
async def startup(ctx: Context):
    ctx.logger.info(f"Starting up {audience_feedback_agent.name}")
    ctx.logger.info(f"With address: {audience_feedback_agent.address}")

@sentiment_analysis_agent.on_event("startup")
async def startup(ctx: Context):
    ctx.logger.info(f"Starting up {sentiment_analysis_agent.name}")
    ctx.logger.info(f"With address: {sentiment_analysis_agent.address}")

# Input: json of all the audience's emotions
# Output: A feedback message for the host 
@audience_feedback_agent.on_query(model=Emotion)
async def audience_feedback_query(ctx: Context, emotion: Emotion):
    genai.configure(api_key=os.getenv("GEMINI_API_KEY"))
    model = genai.GenerativeModel(
            'models/gemini-1.5-pro-latest'
        )
    
    input_prompt = f"""
    You are a sentiment analysis agent for online meetings. 
    I have found a overall emotion for the people in the meeting, which is {emotion}.
    Based on this overall emotion, generate a feedback message for what the host should do to make the meeting better.
    """

    output = model.generate_content(input_prompt)

    return output
    

@sentiment_analysis_agent.on_query(model=Emotion)
async def sentiment_analysis_query(ctx: Context, data: Dict[str, Any]):
    ctx.logger.info(f"Received data: {data}")
    # Extract predictions
    predictions = data.get("language", {}).get("predictions", [])
    
    # Initialize emotion scores
    emotion_totals = {}
    emotion_counts = {}

    # Aggregate emotion scores
    for prediction in predictions:
        for emotion in prediction.get("emotions", []):
            name = emotion["name"]
            score = emotion["score"]
            if name in emotion_totals:
                emotion_totals[name] += score
                emotion_counts[name] += 1
            else:
                emotion_totals[name] = score
                emotion_counts[name] = 1

    # Calculate average scores
    overall_emotions = {name: emotion_totals[name] / emotion_counts[name] for name in emotion_totals}

    ctx.logger.info(f"Overall emotions: {overall_emotions}")
    ctx.logger.info(f"Hello, I'm agent {sentiment_analysis_agent.name} and my address is {sentiment_analysis_agent.address}.")

    await ctx.send(audience_feedback_agent.address, Emotion(emotion={overall_emotions}))
    return overall_emotions

bureau = Bureau(port=8000)
bureau.add(audience_feedback_agent)
bureau.add(sentiment_analysis_agent)

# Run all the agents in the Bureau
if __name__ == "__main__":
    bureau.run()