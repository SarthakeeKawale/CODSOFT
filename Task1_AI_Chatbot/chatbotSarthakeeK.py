import re
import random
from datetime import datetime

class ImprovedChatbot:
    def __init__(self):
        self.name = "ChatBot"
        
        # Defining the intents with keywords and synonyms
        self.intents = {
            'greeting': {
                'keywords': ['hi', 'hello', 'hey', 'greetings', 'good morning', 
                           'good afternoon', 'good evening', 'sup', 'yo'],
                'responses': [
                    "Hello! How can I help you today?",
                    "Hi there! What can I do for you?",
                    "Hey! Nice to meet you!"
                ]
            },
            
            'farewell': {
                'keywords': ['bye', 'goodbye', 'see you', 'exit', 'quit', 
                           'later', 'farewell', 'close'],
                'responses': [
                    "Goodbye! Have a great day!",
                    "See you later! Take care!",
                    "Bye! Come back anytime!"
                ]
            },
            
            'how_are_you': {
                'keywords': ['how are you', 'how are u', 'hows it going', 
                           'whats up', 'how do you do', 'how r u'],
                'responses': [
                    "I'm doing great, thanks for asking! How about you?",
                    "I'm just a bot, but I'm functioning perfectly! How are you?",
                    "All systems running smoothly! What about you?"
                ]
            },
            
            'user_wellbeing': {
                'keywords': ['im good', 'im fine', 'im okay', 'im great', 
                           'doing well', 'not bad', 'pretty good'],
                'responses': [
                    "That's wonderful to hear!",
                    "Glad you're doing well!",
                    "Great! How can I help you today?"
                ]
            },
            
            'name_query': {
                'keywords': ['your name', 'who are you', 'what are you called',
                           'introduce yourself', 'whats your name'],
                'responses': [
                    f"I'm {self.name}, your friendly chatbot assistant!",
                    f"My name is {self.name}. Nice to meet you!",
                    f"I go by {self.name}. How can I help you?"
                ]
            },
            
            'user_name': {
                'keywords': ['my name is', 'im', 'i am', 'call me', 'this is'],
                'responses': [
                    "Nice to meet you, {name}!",
                    "Hello {name}! Great to chat with you!",
                    "Welcome {name}!"
                ]
            },
            
            'time_query': {
                'keywords': ['time', 'current time', 'what time', 'time now'],
                'responses': [
                    f"The current time is {datetime.now().strftime('%I:%M %p')}"
                ]
            },
            
            'date_query': {
                'keywords': ['date', 'today', 'current date', 'what day', 
                           'todays date', 'day is it'],
                'responses': [
                    f"Today is {datetime.now().strftime('%B %d, %Y')}"
                ]
            },
            
            'help': {
                'keywords': ['help', 'what can you do', 'capabilities', 
                           'assist', 'support', 'commands'],
                'responses': [
                    """I can help you with:
• Greetings and conversation
• Tell you the current time and date
• Answer questions about myself
• Provide jokes and fun facts
• Basic math calculations (just type: 5 + 3)
• Weather info (simulated)
• Motivational quotes
Just talk naturally!"""
                ]
            },
            
            'joke': {
                'keywords': ['joke', 'make me laugh', 'funny', 'humor', 
                           'something funny', 'laugh'],
                'responses': [
                    "Why don't scientists trust atoms? Because they make up everything!",
                    "Why did the programmer quit his job? He didn't get arrays!",
                    "What do you call a bear with no teeth? A gummy bear!",
                    "Why do programmers prefer dark mode? Because light attracts bugs!",
                    "How do you comfort a JavaScript bug? You console it!"
                ]
            },
            
            'fact': {
                'keywords': ['fun fact', 'fact', 'interesting', 'tell me something',
                           'did you know', 'trivia'],
                'responses': [
                    "Fun fact: Honey never spoils! Archaeologists found 3000-year-old honey in Egyptian tombs that was still edible.",
                    "Fun fact: Octopuses have three hearts and blue blood!",
                    "Fun fact: A group of flamingos is called a 'flamboyance'!",
                    "Fun fact: Python was named after Monty Python, not the snake!",
                    "Fun fact: Bananas are berries, but strawberries aren't!"
                ]
            },
            
            'thanks': {
                'keywords': ['thank', 'thanks', 'appreciate', 'grateful', 'thx'],
                'responses': [
                    "You're welcome! Happy to help!",
                    "No problem at all!",
                    "Glad I could help!",
                    "Anytime! That's what I'm here for!"
                ]
            },
            
            'weather': {
                'keywords': ['weather', 'temperature', 'forecast', 'raining',
                           'sunny', 'cloudy', 'hot', 'cold'],
                'responses': [
                    "I can't check real weather, but I hope it's beautiful where you are!",
                    "I don't have access to weather data, but I hope you have great weather!",
                    "As a chatbot, I can't check the weather, but I hope it's nice outside!"
                ]
            },
            
            'motivation': {
                'keywords': ['motivate', 'inspiration', 'inspire me', 'motivational',
                           'need motivation', 'encourage'],
                'responses': [
                    "Believe you can and you're halfway there!",
                    "Every expert was once a beginner. Keep going!",
                    "Success is not final, failure is not fatal. Keep moving forward!",
                    "You've got this! Take it one step at a time!"
                ]
            },
            
            'age': {
                'keywords': ['how old', 'your age', 'age'],
                'responses': [
                    "I'm a timeless AI, but I was created recently!",
                    "Age is just a number, especially for bots like me!",
                    "I don't age like humans, but I'm constantly learning!"
                ]
            },
            
            'creator': {
                'keywords': ['who made you', 'creator', 'who built you', 
                           'who created you', 'your developer'],
                'responses': [
                    "I was created by a Python developer as a learning project!",
                    "A talented programmer built me to demonstrate chatbot concepts!",
                    "I'm the creation of someone learning about AI and chatbots!"
                ]
            },
            
            'love': {
                'keywords': ['love you', 'i love you', 'love u'],
                'responses': [
                    "Aww, that's sweet! I appreciate you too!",
                    "That's kind of you! I'm here whenever you need me!",
                    "Thank you! I enjoy our conversations!"
                ]
            },
            
            'compliment': {
                'keywords': ['smart', 'intelligent', 'helpful', 'awesome',
                           'amazing', 'great', 'wonderful', 'cool bot'],
                'responses': [
                    "Thank you! That means a lot!",
                    "You're too kind! I try my best!",
                    "Thanks! You're pretty awesome yourself!"
                ]
            },
        }
    
    def extract_name(self, user_input):
        """Extract user's name from input"""
        patterns = [
            r'my name is (\w+)',
            r'i\'?m (\w+)',
            r'i am (\w+)',
            r'call me (\w+)',
            r'this is (\w+)',
        ]
        
        for pattern in patterns:
            match = re.search(pattern, user_input.lower())
            if match:
                return match.group(1).capitalize()
        return None
    
    def calculate_expression(self, user_input):
        """Extract and calculate mathematical expressions"""
        # Find numbers and operators (handles spaces)
        match = re.search(r'([\d.]+)\s*([\+\-\*\/×÷])\s*([\d.]+)', user_input)
        if match:
            num1, operator, num2 = match.groups()
            num1, num2 = float(num1), float(num2)
            
            # Normalize operators
            operator = operator.replace('×', '*').replace('÷', '/')
            
            try:
                if operator == '+':
                    result = num1 + num2
                elif operator == '-':
                    result = num1 - num2
                elif operator == '*':
                    result = num1 * num2
                elif operator == '/':
                    if num2 == 0:
                        return "I can't divide by zero! Try a different number."
                    result = num1 / num2
                
                return f"The answer is: {result}"
            except Exception:
                return None
        return None
    
    def detect_intent(self, user_input):
        """Detect user intent based on keywords"""
        user_input_lower = user_input.lower()
        
        # Score each intent based on keyword matches
        scores = {}
        for intent, data in self.intents.items():
            score = 0
            for keyword in data['keywords']:
                if keyword in user_input_lower:
                    # Longer keyword matches get higher scores
                    score += len(keyword.split())
            if score > 0:
                scores[intent] = score
        
        # Return intent with highest score
        if scores:
            return max(scores, key=scores.get)
        return None
    
    def get_response(self, user_input):
        """Process user input and generate response"""
        user_input = user_input.strip()
        
        # Check for empty input
        if not user_input:
            return "I didn't catch that. Could you say something?"
        
        # Check for math calculations first
        if any(op in user_input for op in ['+', '-', '*', '/', '×', '÷']):
            calc_result = self.calculate_expression(user_input)
            if calc_result:
                return calc_result
        
        # To Check for name introduction
        name = self.extract_name(user_input)
        if name:
            return random.choice(self.intents['user_name']['responses']).format(name=name)
        
        # Detect intent
        intent = self.detect_intent(user_input)
        
        if intent:
            return random.choice(self.intents[intent]['responses'])
        
        # Default response if no intent detected
        default_responses = [
            "I'm not sure I understand. Could you rephrase that?",
            "Hmm, I don't quite get that. Try asking something else!",
            "That's interesting! I'm still learning. Try 'help' to see what I can do!",
            "I'm not sure about that. Ask me something else!"
        ]
        return random.choice(default_responses)
    
    def chat(self):
        """Main chat loop"""
        print("="*60)
        print(f"     Welcome! I'm {self.name}, your chatbot assistant")
        print("="*60)
        print("💬 Just talk naturally! Type 'bye' or 'quit' to exit\n")
        
        while True:
            user_input = input("You: ").strip()
            
            if not user_input:
                continue
            
            # Check for exit
            if self.detect_intent(user_input) == 'farewell':
                print(f"{self.name}: {self.get_response(user_input)}")
                break
            
            # Get and display response
            response = self.get_response(user_input)
            print(f"{self.name}: {response}\n")

# Run the chatbot
if __name__ == "__main__":
    bot = ImprovedChatbot()
    bot.chat()

    # I made this chatbot using Python. It can handle various intents, including greetings, farewells, time/date queries, jokes, facts, and basic math calculations. Enjoy chatting!