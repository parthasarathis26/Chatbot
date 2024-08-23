import pandas as pd
from rasa_sdk import Action, Tracker
from rasa_sdk.executor import CollectingDispatcher
from rasa_sdk.events import SlotSet

# Paths to CSV files
water_level_csv = 'data/water_level.csv'
water_quality_csv = 'data/water_quality.csv'

# Load the CSV files into DataFrames
df_water_level = pd.read_csv(water_level_csv)
df_water_quality = pd.read_csv(water_quality_csv)

# Step 2: Generate nlu.yml
def generate_nlu_file():
    with open('data/nlu.yml', 'a') as nlu_file:
        nlu_file.write("\n")  # Add a newline for separation
        # Water level intents
        for index, row in df_water_level.iterrows():
            nlu_file.write(f"- intent: inquire_water_level\n")
            nlu_file.write(f"  examples: |\n")
            nlu_file.write(f"    - What is the water level in {row['Elaiyur']}?\n")
            nlu_file.write(f"    - How high is the water level at {row['Elaiyur']}?\n")
        
        # Water quality intents
        for index, row in df_water_quality.iterrows():
            nlu_file.write(f"- intent: inquire_water_quality\n")
            nlu_file.write(f"  examples: |\n")
            nlu_file.write(f"    - What is the water quality in {row['Adyar']}?\n")
            nlu_file.write(f"    - How good is the water quality at {row['Adyar']}?\n")


# Step 3: Generate rules.yml
def generate_rules_file():
    with open('data/rules.yml', 'a') as rules_file:
        rules_file.write("\n")  # Add a newline for separation
        rules_file.write("- rule: Respond to water level inquiry\n")
        rules_file.write("  steps:\n")
        rules_file.write("  - intent: inquire_water_level\n")
        rules_file.write("  - action: action_inquire_water_level\n")
        
        rules_file.write("- rule: Respond to water quality inquiry\n")
        rules_file.write("  steps:\n")
        rules_file.write("  - intent: inquire_water_quality\n")
        rules_file.write("  - action: action_inquire_water_quality\n")

# Step 4: Generate domain.yml
def generate_domain_file():
    with open('domain.yml', 'a') as domain_file:
        domain_file.write("\n")  # Add a newline for separation
        domain_file.write("intents:\n")
        domain_file.write("  - inquire_water_level\n")
        domain_file.write("  - inquire_water_quality\n")
        
        domain_file.write("entities:\n")
        domain_file.write("  - location\n")
        
        domain_file.write("slots:\n")
        domain_file.write("  location:\n")
        domain_file.write("    type: text\n")
        domain_file.write("    mappings:\n")
        domain_file.write("    - type: from_entity\n")
        domain_file.write("      entity: location\n")
        
        domain_file.write("responses:\n")
        domain_file.write("  utter_water_level:\n")
        domain_file.write("    - text: 'The water level at {location} is {water_level} meters.'\n")
        
        domain_file.write("  utter_water_quality:\n")
        domain_file.write("    - text: 'The water quality at {location} is {water_quality}.'\n")
        
        domain_file.write("actions:\n")
        domain_file.write("  - action_inquire_water_level\n")
        domain_file.write("  - action_inquire_water_quality\n")

# Step 5: Generate stories.yml
def generate_stories_file():
    with open('data/stories.yml', 'a') as stories_file:
        stories_file.write("\n")  # Add a newline for separation
        # Water level stories
        for index, row in df_water_level.iterrows():
            stories_file.write(f"- story: inquire water level in {row['Elaiyur']}\n")
            stories_file.write("  steps:\n")
            stories_file.write(f"  - intent: inquire_water_level\n")
            stories_file.write(f"    entities:\n")
            stories_file.write(f"    - location: {row['Elaiyur']}\n")
            stories_file.write("  - action: action_inquire_water_level\n")
        
        # Water quality stories
        for index, row in df_water_quality.iterrows():
            stories_file.write(f"- story: inquire water quality in {row['Adyar']}\n")
            stories_file.write("  steps:\n")
            stories_file.write(f"  - intent: inquire_water_quality\n")
            stories_file.write(f"    entities:\n")
            stories_file.write(f"    - location: {row['Adyar']}\n")
            stories_file.write("  - action: action_inquire_water_quality\n")


# Step 6: Implement custom actions
class ActionInquireWaterLevel(Action):
    def name(self) -> str:
        return "action_inquire_water_level"

    def run(self, dispatcher: CollectingDispatcher, tracker: Tracker, domain: dict) -> list:
        location = tracker.get_slot('location')
        if pd.isna(location):
            dispatcher.utter_message(text="Sorry, I didn't get the location. Could you please specify it again?")
            return []
        
        # Extract water level data from the CSV based on location
        row = df_water_level[df_water_level['Elaiyur'] == location]
        if not row.empty:
            water_level = row.iloc[0, -1]  # Assuming the last column is the water level
            dispatcher.utter_message(text=f"The water level at {location} is {water_level} meters.")
        else:
            dispatcher.utter_message(text=f"Sorry, I don't have information for {location}.")
        
        return [SlotSet("location", location)]


class ActionInquireWaterQuality(Action):
    def name(self) -> str:
        return "action_inquire_water_quality"

    def run(self, dispatcher: CollectingDispatcher, tracker: Tracker, domain: dict) -> list:
        location = tracker.get_slot('location')
        if pd.isna(location):
            dispatcher.utter_message(text="Sorry, I didn't get the location. Could you please specify it again?")
            return []
        
        # Extract water quality data from the CSV based on location
        row = df_water_quality[df_water_quality['Adyar'] == location]
        if not row.empty:
            water_quality = row.iloc[0, -2]  # Assuming the last meaningful column before NaNs is water quality
            dispatcher.utter_message(text=f"The water quality at {location} is {water_quality}.")
        else:
            dispatcher.utter_message(text=f"Sorry, I don't have information for {location}.")
        
        return [SlotSet("location", location)]


# Step 7: Execute the functions to generate the files
generate_nlu_file()
generate_rules_file()
generate_domain_file()
generate_stories_file()
