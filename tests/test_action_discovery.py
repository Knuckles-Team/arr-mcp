"""Action discovery, plural aliases, and did-you-mean hints for arr dispatch."""

from __future__ import annotations

from unittest.mock import MagicMock

import pytest

from arr_mcp.mcp_server import execute_arr_action


def _radarr(action: str):
    return execute_arr_action(
        service_name="radarr",
        base_url="http://radarr.local",
        api_key="x",
        verify=False,
        action=action,
        params_json="{}",
        auth_kw="token",
    )


def test_list_actions_returns_real_method_names():
    res = _radarr("list_actions")
    assert res["service"] == "radarr"
    # The real "list all movies" method is singular get_movie...
    assert "get_movie" in res["actions"]
    # ...and the intuitive plural is NOT a real method (the original bug).
    assert "get_movies" not in res["actions"]


def test_plural_alias_routes_to_singular(monkeypatch):
    import arr_mcp.api.api_client_radarr as radarr_mod

    monkeypatch.setattr(
        radarr_mod.Api, "get_movie", MagicMock(return_value={"aliased": True})
    )
    # The reported failing call: get_movies should now resolve to get_movie.
    assert _radarr("get_movies") == {"aliased": True}


def test_unknown_action_suggests_and_points_to_discovery():
    with pytest.raises(ValueError) as excinfo:
        _radarr("get_movei")  # typo for get_movie
    msg = str(excinfo.value)
    assert "list_actions" in msg
    assert "get_movie" in msg  # did-you-mean suggestion
