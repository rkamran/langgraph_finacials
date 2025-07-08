import asyncio

from langchain_core.messages import AIMessageChunk
from agents import graph
from PIL import Image
import io

async def main():
    # # Uncomment the following lines to display graph
    # image = graph.get_graph().draw_mermaid_png()
    # pil_image = Image.open(io.BytesIO(image))
    # pil_image.show()

    async for messages in graph.astream({"ticker": "IBM"}, stream_mode="messages"):
        if messages and isinstance(messages[0], AIMessageChunk):
            print(messages[0].content, end='')


# Press the green button in the gutter to run the script.
if __name__ == '__main__':
    asyncio.run(main())


