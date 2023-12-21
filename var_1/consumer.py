import asyncio
import json
import logging

import aio_pika

"""
The daemon server
"""


async def main() -> None:
    logging.basicConfig(level=logging.INFO)
    connection = await aio_pika.connect_robust(
        "amqp://guest:guest@127.0.0.1/",
    )

    queue_name = "test_queue"

    async with connection:  # This cycle for accept messages
        # Creating channel
        channel = await connection.channel()

        # Will take no more than 10 messages in advance
        await channel.set_qos(prefetch_count=10)

        # Declaring queue
        queue = await channel.declare_queue(queue_name, auto_delete=True)

        async with queue.iterator() as queue_iter:  # This cycle for read messages
            async for message in queue_iter:
                async with message.process():
                    print(message.body)
                    print("---" * 30)
                    print(json.loads(message.body.decode()))
                    print("---" * 30)

                    if queue.name in message.body.decode():
                        print("---"*30)
                        print(message.body.decode())
                        print("---" * 30)



if __name__ == "__main__":
    asyncio.run(main())
