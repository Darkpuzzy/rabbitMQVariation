import asyncio
import json

import aio_pika


RABBIT_REPLY = "amq.rabbitmq.reply-to"


async def main():
    connection = await aio_pika.connect_robust(
        "amqp://guest:guest@127.0.0.1/"
    )

    async with connection:
        channel = await connection.channel()

        callback_queue = await channel.get_queue(RABBIT_REPLY)

        # Creating asyncio.Queue for response
        rq = asyncio.Queue(maxsize=1)

        # сначала подписываемся
        consumer_tag = await callback_queue.consume(
            callback=rq.put,  # помещаем сообщение в asyncio.Queue
            no_ack=True,  # еще один важный нюанс
        )

        # Publish messages on default_exchange stack
        await channel.default_exchange.publish(
            message=aio_pika.Message(
                body=b"hello",
                reply_to=RABBIT_REPLY  # This need to show stack for callback
            ),
            routing_key="test"
        )

        # Answer from rq asyncio.Queue
        response = await rq.get()
        print("---" * 30)
        print(response.body)
        print("---" * 30)

        # Clear RABBIT_REPLY
        await callback_queue.cancel(consumer_tag)


if __name__ == "__main__":
    asyncio.run(main())
