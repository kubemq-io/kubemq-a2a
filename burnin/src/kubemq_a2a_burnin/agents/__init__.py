"""Mock agent infrastructure for burn-in testing."""

from kubemq_a2a_burnin.agents.base import BaseMockAgent
from kubemq_a2a_burnin.agents.echo_agent import EchoAgent
from kubemq_a2a_burnin.agents.error_agent import ErrorAgent
from kubemq_a2a_burnin.agents.manager import AgentManager
from kubemq_a2a_burnin.agents.oversize_agent import OversizeAgent
from kubemq_a2a_burnin.agents.slow_agent import SlowAgent
from kubemq_a2a_burnin.agents.stream_agent import StreamAgent

__all__ = [
    "AgentManager",
    "BaseMockAgent",
    "EchoAgent",
    "ErrorAgent",
    "OversizeAgent",
    "SlowAgent",
    "StreamAgent",
]
