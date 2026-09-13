"""Import smoke for ultra package."""
import ultra
import ultra.agents
import ultra.client
import ultra.config
import ultra.doctor
import ultra.gateway
import ultra.llm
import ultra.plugins
import ultra.skills
import ultra.tui


def test_version():
    assert ultra.__version__.startswith("0.2.")
