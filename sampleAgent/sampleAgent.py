from typing import Any, List, Union
from uuid import UUID

from pydantic import Field
from uagents import Agent, Context, Model
from uagents.setup import fund_agent_if_low


class TestRequest(Model):
    message: str


class DrcpQueryFromPeerApi(Model):
    jsonrpc: str
    method: str = Field(default="query", const=True)
    params: List[Any]
    id: Union[str, UUID]


class Response(Model):
    text: str


# test info:
# agent address: agent1qt8q20p0vsp7y5dkuehwkpmsppvynxv8esg255fwz6el68rftvt5klpyeuj
# agent wallet address: fetch1dc5s9wmerlsvdq9gxp76xxldk8jzp8l9zlyakr
agent = Agent(
    name="sample_agent_name",
    seed="sample_agent_seed",
    port=8001,
    endpoint="http://localhost:8001/submit",
)
fund_agent_if_low(agent.wallet.address())


@agent.on_event("startup")
async def startup(ctx: Context):
    ctx.logger.info(f"Starting up {agent.name}")
    ctx.logger.info(f"With address: {agent.address}")
    ctx.logger.info(f"And wallet address: {agent.wallet.address()}")


# query from PeerAPI
@agent.on_query(model=DrcpQueryFromPeerApi, replies={Response})
async def query_handler(ctx: Context, sender: str, _query: TestRequest):
    ctx.logger.info("Query received by the Sample Agent")
    try:
        # do something here with the _query
        ctx.logger.info(_query)
        await ctx.send(
            sender, Response(text="Successful query response from the Sample Agent")
        )
    except Exception:
        await ctx.send(sender, Response(text="fail"))


agent.run()
