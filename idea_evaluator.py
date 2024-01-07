"""
This file aims to act as an Idea Evaluator for ideas that would boost the Circular Economy 
"""

import pandas as pd
import numpy as np
import csv
import os
from openai import OpenAI

class IdeaEvaluator:
    def __init__(self, dataset_path):
        self.dataset_path = dataset_path
        self.OpenAI_key = self.load_openai_key()
        
    def load_openai_key(self):
        try:
            with open(".env", "r") as env_file:
                lines = env_file.readlines()
                for line in lines:
                    key, value = line.strip().split("=")
                    if key.strip() == "OPENAI_KEY":
                        return value.strip()
        except FileNotFoundError:
            print(".env file not found.")
        except Exception as e:
            print(f"Error loading OPENAI_KEY: {e}")
        return None

if __name__ == "__main__":
    evaluator = IdeaEvaluator("./data/AI_EarthHack_Dataset_Small.csv")
    print(evaluator.OpenAI_key)

        