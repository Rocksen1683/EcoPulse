"""
This file aims to act as an Idea Evaluator for ideas that would boost the Circular Economy 
"""

import pandas as pd
import numpy as np
import csv
import os
import csv 
from openai import OpenAI

class IdeaEvaluator:
    def __init__(self, dataset_path):
        self.dataset_path = dataset_path
        self.OpenAI_key = self.load_openai_key()
        self.client = OpenAI(api_key=self.OpenAI_key)
        #populating dataset 
        self.rows = []
        self.populate_rows(self.rows)
        self.baseline_metrics  = {'Market Potential':20, 'Scalability':20,'Feasibility':20,'Maturity Stage':20,'Technological Innovation':20}


    def populate_rows(self, rows):
        with open(self.dataset_path, encoding = 'latin-1') as file:
            csv_reader = csv.reader(file)
            header = next(csv_reader)
            for row in csv_reader:
                rows.append(row)
        
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
    
    def get_number_tokens(self, res, tokens):
        for token in tokens: 
            if token.isdigit():
                res.append(token)

    def generate_baseline_results(self, idx, problem, solution):
        messages = [
            {
                "role": "system",
                "content": '''You are an AI-powered decision-support tool to evaluate innovative circular economy business opportunities. You are given a problem statement and a solution. You have to evaluate the solution based on the problem statement and provide a score for the solution. 
                You are to evaluate the solution based on the following metrics : Market Potential, Scalability, Feasibility, Maturity Stage,Technological Innovation. For each metric, you provide a score between 0 and 20. Ensure that the output is exactly the same format as the example. The higher the score, the better the solution.
                You must also finally create a combined score, by aggregating all the scores from the metrics above. The score should be between 0 and 100. The higher the score, the better the solution. Ensure each criteria is given equal weightage, and is scored out of 20.''',
            },
            {
                "role": "user",
                "content": '''Problem Statement : The construction industry is indubitably one of the significant contributors to global waste, contributing approximately 1.3 billion tons of waste annually, exerting significant pressure on our landfills and natural resources. Traditional construction methods entail single-use designs that require frequent demolitions, leading to resource depletion and wastage.
                            Solution : Herein, we propose an innovative approach to mitigate this problem: Modular Construction. This method embraces recycling and reuse, taking a significant stride towards a circular economy. Modular construction involves utilizing engineered components in a manufacturing facility that are later assembled on-site. These components are designed for easy disassembling, enabling them to be reused in diverse projects, thus significantly reducing waste and conserving resources. Not only does this method decrease construction waste by up to 90%, but it also decreases construction time by 30-50%, optimizing both environmental and financial efficiency. This reduction in time corresponds to substantial financial savings for businesses. Moreover, the modular approach allows greater flexibility, adapting to changing needs over time. We believe, by adopting modular construction, the industry can transit from a 'take, make and dispose' model to a more sustainable 'reduce, reuse, and recycle' model, driving the industry towards a more circular and sustainable future. The feasibility of this concept is already being proven in markets around the globe, indicating its potential for scalability and real-world application.''',
            },
            {
                "role": "assistant",
                "content": "Market Potential: 15 Scalability: 12 Feasibility: 19 Maturity Stage: 14 Technological Innovation: 11 Combined Score: 71",
            },
            {
                "role": "user",
                "content": "Problem Statement : " + problem + " Solution : " + solution,
            }
        ]
        
        res = self.client.chat.completions.create(
            model = "gpt-3.5-turbo",
            messages = messages
        )
        msg = res.choices[0].message.content
        print(idx, msg)
        tokens = msg.split(' ')
        #   print(tokens)
        result = [idx, problem, solution]
        self.get_number_tokens(result, tokens)
        return result

    def baseline_model(self):
        baseline_model = []
        fieldnames=['Index', 'Problem', 'Solution', 'Market Potential', 'Scalability', 'Feasibility','Maturity Stage','Technological Innovation', 'Combined Score']
        baseline_model.append(fieldnames)
        
        for row in self.rows:
            baseline_row = self.generate_baseline_results(row[0], row[1], row[2])
            baseline_model.append(baseline_row)
            baseline_model.append(self.generate_baseline_results(self.rows[0][0], self.rows[0][1], self.rows[0][2]))
            baseline_model.pop(1)
            baseline_model.sort(key=lambda x: x[::-1], reverse=True)

        with open('./data/baseline_results.csv','w', newline = '', encoding = 'latin-1') as file:
            writer = csv.writer(file, fieldnames)
            writer.writerows(baseline_model)


if __name__ == "__main__":
    evaluator = IdeaEvaluator("./data/AI_EarthHack_Dataset_Small.csv")
    evaluator.baseline_model()

        