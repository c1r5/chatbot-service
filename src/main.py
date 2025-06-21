import asyncio
import logging
import signal
from typing import Literal, cast
from uvicorn import Config, Server

from dotenv import load_dotenv


from modules.bot import run_telegram_bot
from modules.helpers import getenv
from modules.server import app_instance


load_dotenv()

EnvironmentMode = Literal["dev", "prod"]

env_value = getenv("ENVIRONMENT_MODE", "dev")  # default to 'dev' if not set

if env_value not in ("dev", "prod"):
    raise ValueError(f"Invalid ENVIRONMENT_MODE: {env_value}")

ENVIRONMENT_MODE: EnvironmentMode = cast(EnvironmentMode, env_value)

logging.basicConfig(
    level=logging.INFO,
    format="(%(asctime)s) %(levelname)s %(message)s",
    datefmt="%m/%d/%y - %H:%M:%S %Z",
    filename=f"logs/{ENVIRONMENT_MODE}.log",
)
logger = logging.getLogger(__name__)


# Function to run FastAPI server
async def run_fastapi():
    config = Config(app=app_instance, host="0.0.0.0",
                    port=8000, loop="asyncio")
    server = Server(config)
    await server.serve()


async def main():
    loop = asyncio.get_running_loop()
    stop_event = asyncio.Event()

    def shutdown():
        print("Shutdown signal received.")
        stop_event.set()

    for sig in (signal.SIGINT, signal.SIGTERM):
        loop.add_signal_handler(sig, shutdown)

    fastapi_task = asyncio.create_task(run_fastapi())
    bot_task = asyncio.create_task(run_telegram_bot())

    await stop_event.wait()

    print("Cancelando tarefas...")
    fastapi_task.cancel()
    bot_task.cancel()

    try:
        await asyncio.gather(fastapi_task, bot_task)
    except asyncio.CancelledError:
        print("Tarefas canceladas com sucesso.")


if __name__ == "__main__":
    try:
        asyncio.run(main())
    except KeyboardInterrupt:
        print("Encerrado pelo usuário.")

