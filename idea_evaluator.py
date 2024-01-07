"""
This file aims to act as an Idea Evaluator for ideas that would boost the Circular Economy 
"""

import pandas as pd
import numpy as np
import csv
import os
import csv 
from openai import OpenAI
import re
import random
import plotly.graph_objects as go 

class IdeaEvaluator:
    def __init__(self, dataset_path):
        self.dataset_path = dataset_path
        self.OpenAI_key = self.load_openai_key()
        self.client = OpenAI(api_key=self.OpenAI_key)
        #populating dataset 
        self.rows = []
        self.populate_rows(self.rows)
        self.baseline_metrics  = {'Market Potential':20, 'Scalability':20,'Feasibility':20,'Maturity Stage':20,'Technological Innovation':20}

        #baseline model data 
        self.baseline_model_data = []
        self.categories = {}
        self.fieldnames=['Index', 'Problem', 'Solution', 'Market Potential', 'Scalability', 'Feasibility','Maturity Stage','Technological Innovation', 'Combined Score', 'Category']


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
    
    def generate_results(self, idx, problem, solution, metrics):
        score = int(100 / len(metrics))

        metricList = ''
        for metric in metrics:
            metricList = metricList + metric + ", "
        metricList = metricList[:-2]

        example = ''
        for metric in metrics:
            metricList = metricList + metric + " : " + str(random.randint(1, score)) + " "
        metricList = metricList[:-1]

        messages = [
        {
            "role": "system",
            "content": '''You are an AI-powered decision-support tool used to evaluate innovative circular economy business opportunities.
              You are given a problem statement and a solution. Here are a few important metrics you need to evaluate these solutions on, 
              Metrics : ''' + metricList + '''. Follow these steps for the output :
              Step 1 : For each metric, you provide a score for the solution between 0 and ''' + str(score) + '''. The higher the score, the better the solution.
              Step 2 : You must create a combined score, by aggregating (sum of) all the individual scores from the metrics above. This score should be between 0 and 100.
              Step 3 : You are going to categorize the given problem into a category relevant to strengthening the circular economy. Only mention the category name, and not the description.
              Ensure each criteria is given equal weightage, and is scored out of 20. Ensure that the output is in one line always. Ensure that the output is exactly the same format 
              as the example, with the same number of spaces and punctuation. You do not have to show your reasoning for the scores.''',
        },
        {
            "role": "user",
            "content": '''Problem Statement : The construction industry is indubitably one of the significant contributors to global waste, contributing approximately 1.3 billion tons of waste annually, exerting significant pressure on our landfills and natural resources. Traditional construction methods entail single-use designs that require frequent demolitions, leading to resource depletion and wastage.
                          Solution : Herein, we propose an innovative approach to mitigate this problem: Modular Construction. This method embraces recycling and reuse, taking a significant stride towards a circular economy. Modular construction involves utilizing engineered components in a manufacturing facility that are later assembled on-site. These components are designed for easy disassembling, enabling them to be reused in diverse projects, thus significantly reducing waste and conserving resources. Not only does this method decrease construction waste by up to 90%, but it also decreases construction time by 30-50%, optimizing both environmental and financial efficiency. This reduction in time corresponds to substantial financial savings for businesses. Moreover, the modular approach allows greater flexibility, adapting to changing needs over time. We believe, by adopting modular construction, the industry can transit from a 'take, make and dispose' model to a more sustainable 'reduce, reuse, and recycle' model, driving the industry towards a more circular and sustainable future. The feasibility of this concept is already being proven in markets around the globe, indicating its potential for scalability and real-world application.''',
        },
        {
            "role": "assistant",
            "content": "Market Potential: 15 Scalability: 12 Feasibility: 19 Maturity Stage: 14 Technological Innovation: 11 Combined Score: 71 Category: Construction",
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
        tokens = msg.split(': ')
        print(tokens)

        result = [idx, problem, solution]
      
        for x in range(1, len(metrics) + 2): # offset by 2 because it starts at 1 and need extra token for combined score
            result.append(tokens[x].split()[0])

        result.append(tokens[-1])
        return result

    def baseline_model(self):
        for row in self.rows:
            baseline_row = self.generate_results(row[0], row[1], row[2], ['Market Potential', 'Scalability', 'Feasibility','Maturity Stage','Technological Innovation'])
            self.baseline_model_data.append(baseline_row)
        self.baseline_model_data.sort(key=lambda x: x[::-1], reverse=True)

        with open('./data/baseline_results.csv','w', newline = '', encoding = 'latin-1') as file:
            writer = csv.writer(file, self.fieldnames)
            writer.writerow(self.fieldnames)
            writer.writerows(self.baseline_model_data)

    def populate_categories(self):
        for row in self.baseline_model_data:
            category = row[-1]
            if category in self.categories:
                self.categories[category] += 1 
            else:
                self.categories[category] = 1
        print(self.categories)

    def filter_categories(self, model, category):
        filter = []
        for row in model:
            if category == row[-1]:
                filter.append(row)

        with open(f"./data/filtered_{category}_results.csv","w" ,newline = '', encoding = 'latin-1') as file:
            writer = csv.writer(file, self.fieldnames)
            writer.writerow(self.fieldnames)
            writer.writerows(filter)

    def bar_visualization(self):
        keys = list(self.categories.keys())
        values = list(self.categories.values())

        fig = go.Figure(data=[go.Bar(x=keys, y=values)])
        fig.update_layout(title_text='Category Distribution', xaxis_title='Categories', yaxis_title='Frequency')
        fig.show()

    
    
    def run_evaluator(self):
        cyclic_geese = '''    
  /$$$$$$                      /$$ /$$                  /$$$$$$                                         
 /$$__  $$                    | $$|__/                 /$$__  $$                                        
| $$  \__/ /$$   /$$  /$$$$$$$| $$ /$$  /$$$$$$$      | $$  \__/  /$$$$$$   /$$$$$$   /$$$$$$$  /$$$$$$ 
| $$      | $$  | $$ /$$_____/| $$| $$ /$$_____/      | $$ /$$$$ /$$__  $$ /$$__  $$ /$$_____/ /$$__  $$
| $$      | $$  | $$| $$      | $$| $$| $$            | $$|_  $$| $$$$$$$$| $$$$$$$$|  $$$$$$ | $$$$$$$$
| $$    $$| $$  | $$| $$      | $$| $$| $$            | $$  \ $$| $$_____/| $$_____/ \____  $$| $$_____/
|  $$$$$$/|  $$$$$$$|  $$$$$$$| $$| $$|  $$$$$$$      |  $$$$$$/|  $$$$$$$|  $$$$$$$ /$$$$$$$/|  $$$$$$$
 \______/  \____  $$ \_______/|__/|__/ \_______/       \______/  \_______/ \_______/|_______/  \_______/
           /$$  | $$                                                                                    
          |  $$$$$$/                                                                                    
           \______/ '''
        print(cyclic_geese)
        print("Welcome to the Cyclic Geese Idea Evaluator!!")
        print("Our evaluator provides a baseline analysis of all of the ideas but also provides user-based analysis :)")
        print("Running Baseline Model...")
        self.baseline_model()
        print("The results of the baseline can be found in \'data/baseline_model.csv\'")
        print("Baseline results are sorted based on which idea we think are better and also have a 'Category' field that will help you better understand the data.")
        print("Now that we have a baseline model, let's do some visualization eh ;)")
        self.populate_categories()
        self.bar_visualization()

        
if __name__ == "__main__":
    evaluator = IdeaEvaluator("./data/AI_EarthHack_Dataset_Small.csv")
    evaluator.run_evaluator()
    # evaluator.baseline_model()

        