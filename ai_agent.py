from typing import Dict, Any
from actor import Actor

class AIAgent(Actor):
    def __init__(self, name: str) -> None:
        super().__init__(name)
        self.knowledge: Dict[str, str] = {}

    async def handle_message(self, message: Dict[str, Any]) -> None:
        """Handle incoming messages and make decisions."""
        if message['type'] == 'greet':
            response = await self.greet(message['name'])
        elif message['type'] == 'learn':
            response = await self.learn(message['name'], message['info'])
        elif message['type'] == 'ask':
            response = await self.answer_question(message['question'])
        else:
            response = "I don't understand."

        print(f"Agent {self.name} response: {response}")

    async def greet(self, name: str) -> str:
        """Simple greeting logic."""
        return f"Hello, {name}!"

    async def learn(self, name: str, info: str) -> str:
        """Learning behavior: agent stores new knowledge."""
        self.knowledge[name] = info
        return f"Learned about {name}: {info}"

    async def answer_question(self, question: str) -> str:
        """Answer questions based on learned knowledge."""
        if question in self.knowledge:
            return f"I know about {question}: {self.knowledge[question]}"
        else:
            return "I don't know the answer to that." 