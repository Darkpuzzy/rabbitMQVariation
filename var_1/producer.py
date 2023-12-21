import asyncio
import json

import aio_pika


async def main() -> None:
    connection = await aio_pika.connect_robust(
        "amqp://guest:guest@127.0.0.1/",
    )

    async with connection:
        routing_key = "test_queue"
        test_dict = '{"id": 5, "price": 1500}'

        channel = await connection.channel()
        print(channel)
        payload = json.dumps(test_dict)
        await channel.default_exchange.publish(
            aio_pika.Message(body=payload.encode()),
            routing_key=routing_key,
        )


if __name__ == "__main__":
    asyncio.run(main())
