import asyncio
from typing import Any, Dict

class Actor:
    def __init__(self, name: str) -> None:
        self.name = name
        self.queue: asyncio.Queue = asyncio.Queue()
        self.running: bool = True

    async def start(self) -> None:
        """Start the actor's message processing loop."""
        while self.running:
            message = await self.queue.get()
            await self.handle_message(message)

    async def handle_message(self, message: Dict[str, Any]) -> None:
        """Override this to define the actor's behavior."""
        raise NotImplementedError

    async def send(self, message: Dict[str, Any]) -> None:
        """Send a message to the actor."""
        await self.queue.put(message)

    def stop(self) -> None:
        """Stop the actor."""
        self.running = False 