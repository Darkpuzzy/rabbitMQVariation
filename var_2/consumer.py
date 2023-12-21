import asyncio
from functools import partial

import aio_pika


async def consumer(
    msg: aio_pika.IncomingMessage,
    channel: aio_pika.RobustChannel
):
    async with msg.process():

        print("---"*30)
        print(msg.body)
        print("---" * 30)

        # Check on reply_to
        if msg.reply_to:
            # Callback in default exchange
            await channel.default_exchange.publish(
                message=aio_pika.Message(
                    body="Callback Hi".encode(),
                    correlation_id=msg.correlation_id,
                ),
                routing_key=msg.reply_to,  # This is necessary method for callback to producer
            )


async def main():
    connection = await aio_pika.connect_robust(
        "amqp://guest:guest@127.0.0.1/"
    )

    queue_name = "test"

    async with connection:
        channel = await connection.channel()
        queue = await channel.declare_queue(queue_name)
        # через partial прокидываем в наш обработчик сам канал
        await queue.consume(partial(consumer, channel=channel))

        try:
            await asyncio.Future()
        except Exception:
            pass


if __name__ == "__main__":
    asyncio.run(main())
