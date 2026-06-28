import sys
import warnings
from market_resrch_crew.crew import MarketResrchCrew

warnings.filterwarnings("ignore", category=SyntaxWarning, module="pysbd")

# This main file is intended to be a way for you to run your
# crew locally, so refrain from adding unnecessary logic into this file.
# Replace with inputs you want to test with, it will automatically
# interpolate any tasks and agents information

def run():
    """
    Run the crew.
    """
    inputs = {
        'product_idea': 'An AI-powered tool that automatically generates UI mockups and frontend code from hand-drawn sketches or text descriptions.'
    }
    
    try:
        MarketResrchCrew().crew().kickoff(inputs=inputs)
    except Exception as e:
        raise Exception(f"An error occurred while running the crew: {e}")

def train():
    """
    Train the crew for a given number of iterations.
    """
    inputs = {
        "product_idea": "An AI-powered tool that automatically generates UI mockups and frontend code from hand-drawn sketches or text descriptions."
    }
    try:
        MarketResrchCrew().crew().train(n_iterations=int(sys.argv[1]), filename=sys.argv[2], inputs=inputs)
    except Exception as e:
        raise Exception(f"An error occurred while training the crew: {e}")

def replay():
    """
    Replay the crew execution from a specific task.
    """
    try:
        MarketResrchCrew().crew().replay(task_id=sys.argv[1])
    except Exception as e:
        raise Exception(f"An error occurred while replaying the crew: {e}")

def test():
    """
    Test the crew execution and returns the results.
    """
    inputs = {
        "product_idea": "An AI-powered tool that automatically generates UI mockups and frontend code from hand-drawn sketches or text descriptions."
    }
    try:
        MarketResrchCrew().crew().test(n_iterations=int(sys.argv[1]), inputs=inputs)
    except Exception as e:
        raise Exception(f"An error occurred while testing the crew: {e}")
