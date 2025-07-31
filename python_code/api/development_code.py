from agents import GuardAgent, ClassificationAgent, DetailsAgent, AgentProtocol, RecommendationAgent, OrderTakingAgent
import os
from typing import Dict

import pathlib
import sys
folder_path = pathlib.Path(__file__).parent.resolve()

def main():
    guard_agent = GuardAgent()
    classification_agent = ClassificationAgent()
    recommendationAgent = RecommendationAgent(
            os.path.join(folder_path, "recommendation_objects/apriori_recommendations.json"),
            os.path.join(folder_path, "recommendation_objects/popularity_recommendation.csv"),    
        )

    agent_dict: Dict[str, AgentProtocol] = {
        "details_agent": DetailsAgent(),
        "recommendation_agent": recommendationAgent,
        "order_taking_agent": OrderTakingAgent(recommendationAgent)
    }

    messages = []
    while True:
        # Display the chat history
        os.system('cls' if os.name == 'nt' else 'clear')

        print("\n\nPrint Messages ...............")
        for message in messages:
            print(f"{message['role'].capitalize()}: {message['content']}")

        # Get user input
        prompt = input("User: ")
        messages.append({"role": "user", "content": prompt})
        
        # Get GuardAgent's response
        guard_agent_response = guard_agent.get_response(messages)
      
        print("Guard agent output: ", guard_agent_response) 
        if guard_agent_response["memory"]["guard_decision"] == "not allowed":
            messages.append(guard_agent_response)
            continue

        # Get Classification Agent's response
        classification_agent_response = classification_agent.get_response(messages)
        chosen_agent = classification_agent_response["memory"][
            "classification_decision"
        ]
        print("Chosen Agent: ", chosen_agent)

        # one of the agent type
        agent = agent_dict[chosen_agent]
        # given the message, get the agent response
        response = agent.get_response(messages)
        messages.append(response)



if __name__ == "__main__":
    main()
   