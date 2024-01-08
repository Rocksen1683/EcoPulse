# AIEarthHack - EcoPulse
This is a submission for the Harvard AI EarthHack Challenge 2024 by team `Cyclic Geese` :)

`EcoPulse` is a gen-AI powered Idea Validator tool that will help you find ideas that can boost the circular economy. It provides the user with a baseline model that evaluates ideas based on fixed metrics and refines the model based on the user's profile and needs.

## Requirements 
You would need a valid `OpenAI` API key to run EcoPulse.\
You would also need the following Python libraries:
- `openai` 
- `plotly`
- `time`
- `csv`

## Running Instructions
Here are the step-by-step instructions to run EcoPulse:
1. Add your `OpenAI` API Key in the `.env` file.
2. Upload your dataset in the `data` directory.
3. Open the `eco_pulse.py` file. 
4. Pass the relative path of your dataset to the `IdeaEvaluator` instance.
5. Run `eco_pulse.py` and have a good time!
