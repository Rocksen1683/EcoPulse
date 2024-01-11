from src.idea_evaluator import *

"""
Run this file for the EcoPulse Idea Validator. Honk Honk :)
"""

if __name__ == "__main__":
    evaluator = IdeaEvaluator("./data/AI_EarthHack_Dataset_Small.csv")
    evaluator.run_evaluator()
