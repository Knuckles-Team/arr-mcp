"""The suite surface: every upstream operation is one typed tool (CONN-ARR-MCP-SUITE).

Bound tests of ``specs/arr-suite/requirements.md``: the census against the
upstream API descriptions, the typed-only tool surface, the response
boundary, and the content tier (skills, agent-definition prompts and the
ontology with its tool-use contracts and its roll-up to medulla core).
"""

from __future__ import annotations

import ast
import asyncio
import importlib
import importlib.util
import json
import re
from pathlib import Path

import httpx
import pytest

rdflib = pytest.importorskip("rdflib")
from rdflib.namespace import OWL, RDF, RDFS  # noqa: E402

ID = "CONN-ARR-MCP-SUITE"
ROOT = Path(__file__).resolve().parents[1]
PKG = ROOT / "arr_mcp"
APPS = ("radarr", "sonarr", "lidarr", "prowlarr", "chaptarr", "bazarr", "seerr")
CENSUS = json.loads((ROOT / "tests/fixtures/upstream_operations.json").read_text())
KG = "http://knuckles.team/kg#"
ARR = "http://knuckles.team/kg/arr#"
BFO_ENTITY = rdflib.URIRef("http://purl.obolibrary.org/obo/BFO_0000001")


def _norm(path: str) -> str:
    return re.sub(r"\{[^}]*\}", "{}", path.rstrip("/")) or "/"


def _client_operations(app: str) -> dict[tuple[str, str], str]:
    """``(VERB, path)`` -> method name, read from the client source."""
    tree = ast.parse((PKG / f"api/api_client_{app}.py").read_text())
    found: dict[tuple[str, str], str] = {}
    for cls in (n for n in tree.body if isinstance(n, ast.ClassDef)):
        for fn in cls.body:
            if not isinstance(fn, ast.FunctionDef) or fn.name.startswith("_"):
                continue
            for call in ast.walk(fn):
                if not (
                    isinstance(call, ast.Call)
                    and getattr(call.func, "attr", "") == "_request"
                    and len(call.args) >= 2
                ):
                    continue
                verb, path = call.args[0], call.args[1]
                if isinstance(path, ast.JoinedStr):
                    text = "".join(
                        v.value if isinstance(v, ast.Constant) else "{x}"
                        for v in path.values
                    )
                else:
                    text = path.value
                found[(verb.value, _norm(text))] = fn.name
                break
    return found


@pytest.fixture(scope="module")
def served():
    from fastmcp import Client
    from scion_sdk.connector import build_server

    _, mcp = build_server("arr_mcp", command_args=[])

    async def collect():
        async with Client(mcp) as client:
            return (
                await client.list_tools(),
                await client.list_prompts(),
                await client.list_resources(),
            )

    tools, prompts, resources = asyncio.run(collect())
    return (
        {tool.name: tool for tool in tools},
        {prompt.name: prompt for prompt in prompts},
        {str(resource.uri) for resource in resources},
    )


# --- R001: one typed tool per upstream operation ---------------------------


@pytest.mark.spec(f"{ID}-R001")
@pytest.mark.parametrize("app", APPS)
def test_every_upstream_operation_has_a_client_method(app):
    ours = _client_operations(app)
    upstream = {
        (op.split(" ", 1)[0], _norm(op.split(" ", 1)[1]))
        for op in CENSUS[app]["operations"]
    }
    missing = sorted(upstream - set(ours))
    assert not missing, f"{app}: upstream operations without a tool: {missing}"
    stray = sorted(set(ours) - upstream)
    assert not stray, f"{app}: client calls routes the upstream does not serve: {stray}"


@pytest.mark.spec(f"{ID}-R001")
@pytest.mark.parametrize("app", APPS)
def test_every_client_method_is_served_as_a_tool(app, served):
    tools, _, _ = served
    for method in set(_client_operations(app).values()):
        assert f"{app}_{method}" in tools


# --- R002: typed only; no action routing and no raw request ---------------


@pytest.mark.spec(f"{ID}-R002")
def test_no_action_routed_or_raw_request_tool(served):
    tools, _, _ = served
    for name, tool in tools.items():
        properties = set((tool.inputSchema or {}).get("properties", {}))
        assert "params_json" not in properties, name
        assert not name.endswith("_action"), name
        assert not name.endswith("_request") or name.startswith("seerr_"), name
        assert not ({"method", "endpoint"} <= properties), name


@pytest.mark.spec(f"{ID}-R002")
def test_deletes_ask_for_confirmation(served):
    tools, _, _ = served
    deletes = [t for n, t in tools.items() if "_delete_" in n]
    assert deletes
    for tool in deletes:
        assert tool.annotations.destructiveHint is True, tool.name


# --- R003: the response boundary --------------------------------------------


def _api(module_name, handler):
    module = importlib.import_module(f"arr_mcp.api.api_client_{module_name}")
    api = module.Api(base_url="http://arr.test:8080", api_key="k")
    api._session = httpx.Client(
        base_url="http://arr.test:8080", transport=httpx.MockTransport(handler)
    )
    return api


@pytest.mark.spec(f"{ID}-R003")
def test_an_html_page_is_refused_not_reported_as_success():
    def handler(request):
        return httpx.Response(
            200, text="<html>app</html>", headers={"content-type": "text/html"}
        )

    api = _api("bazarr", handler)
    with pytest.raises(RuntimeError, match="NOT_AN_API_RESPONSE"):
        api.get_episodes_blacklist()


@pytest.mark.spec(f"{ID}-R003")
def test_bazarr_routes_and_query_parameters_match_the_live_api():
    seen = []

    def handler(request):
        seen.append(request)
        return httpx.Response(200, json={"data": [], "total": 0})

    api = _api("bazarr", handler)
    api.get_episodes_wanted(start=0, length=5)
    api.patch_episodes_subtitles(
        seriesid=1, episodeid=2, language="en", forced=False, hi=False
    )
    assert seen[0].url.path == "/api/episodes/wanted"
    assert dict(seen[0].url.params) == {"start": "0", "length": "5"}
    assert seen[1].method == "PATCH"
    assert seen[1].url.params["episodeid"] == "2"


@pytest.mark.spec(f"{ID}-R003")
def test_seerr_body_fields_travel_as_json():
    seen = []

    def handler(request):
        seen.append(request)
        return httpx.Response(201, json={"id": 1})

    api = _api("seerr", handler)
    api.post_request(media_type="movie", media_id=603, is4k=False)
    assert seen[0].url.path == "/api/v1/request"
    assert json.loads(seen[0].content) == {
        "mediaType": "movie",
        "mediaId": 603,
        "is4k": False,
    }


# --- R004: skills, prompts and contracts name only served tools -----------


@pytest.fixture(scope="module")
def graph():
    g = rdflib.Graph()
    for path in sorted((PKG / "ontology").glob("*.ttl")):
        g.parse(path, format="turtle")
    return g


def _contract_tools(g):
    return {str(name) for name in g.objects(None, rdflib.URIRef(ARR + "toolName"))}


@pytest.mark.spec(f"{ID}-R004")
def test_contract_tools_are_served(graph, served):
    tools, _, _ = served
    missing = sorted(_contract_tools(graph) - set(tools))
    assert not missing, missing


@pytest.mark.spec(f"{ID}-R004")
def test_every_app_has_a_skill_and_contracts(graph):
    skills = {
        str(o)
        for s in graph.subjects(RDF.type, rdflib.URIRef(ARR + "ConnectorSkill"))
        for o in graph.objects(s, rdflib.URIRef(ARR + "skillName"))
    }
    for skill in skills:
        assert (PKG / "skills" / skill / "SKILL.md").is_file(), skill
    contract_apps = {name.split("_", 1)[0] for name in _contract_tools(graph)}
    assert set(APPS) <= contract_apps


@pytest.mark.spec(f"{ID}-R004")
def test_contract_steps_are_ordered_and_bound(graph):
    has_step = rdflib.URIRef(ARR + "hasStep")
    index = rdflib.URIRef(ARR + "stepIndex")
    calls = rdflib.URIRef(ARR + "callsTool")
    contracts = list(graph.subjects(RDF.type, rdflib.URIRef(ARR + "ToolUseContract")))
    assert len(contracts) >= 20
    for contract in contracts:
        steps = list(graph.objects(contract, has_step))
        assert steps, contract
        positions = sorted(int(graph.value(step, index)) for step in steps)
        assert positions == list(range(1, len(steps) + 1)), contract
        for step in steps:
            assert graph.value(step, calls) is not None, step


@pytest.mark.spec(f"{ID}-R004")
def test_skill_files_name_only_served_tools(served):
    tools, _, _ = served
    named = re.compile(
        r"`((?:radarr|sonarr|lidarr|prowlarr|chaptarr|bazarr|seerr|arr)_"
        r"(?:get|post|put|patch|delete|add|ingest)_[a-z0-9_]+)`"
    )
    for skill in (PKG / "skills").glob("*/SKILL.md"):
        if skill.parent.name == "arr-mcp-development":
            continue
        for name in named.findall(skill.read_text()):
            assert name in tools, f"{skill.parent.name}: {name}"


# --- R005: prompts are agent definitions linked in the ontology -----------


PROMPTS = sorted(p.stem for p in (PKG / "prompts").glob("*.json"))


@pytest.mark.spec(f"{ID}-R005")
def test_operator_and_role_prompts_exist():
    assert "arr_operator" in PROMPTS
    assert {"media_librarian", "request_manager", "indexer_maintainer"} <= set(PROMPTS)


@pytest.mark.spec(f"{ID}-R005")
@pytest.mark.parametrize("name", PROMPTS)
def test_prompt_is_a_complete_agent_definition(name, served, graph):
    tools, prompts, _ = served
    assert name in prompts
    doc = json.loads((PKG / "prompts" / f"{name}.json").read_text())
    assert doc["role"] == "system"
    text = doc["instructions"]["core_directive"]
    for section in (
        "Goal:",
        "Skills",
        "Workflows",
        "Data locations:",
        "Guardrails:",
        "Outputs:",
    ):
        assert section in text, f"{name}: {section}"
    for tool in doc["tools"]:
        assert tool in tools, f"{name}: {tool}"
    for skill in doc["skills"]:
        assert (PKG / "skills" / skill / "SKILL.md").is_file()
    node = rdflib.URIRef(ARR + f"prompt-{name}")
    assert (node, RDF.type, rdflib.URIRef(ARR + "ConnectorPrompt")) in graph
    linked = {
        str(graph.value(t, rdflib.URIRef(ARR + "toolName")))
        for t in graph.objects(node, rdflib.URIRef(ARR + "usesTool"))
    }
    assert linked == set(doc["tools"])
    role = graph.value(node, rdflib.URIRef(ARR + "systemPromptForRole"))
    assert str(role) == doc["systemPromptFor"]


# --- R006: data location, routing and federation --------------------------


@pytest.mark.spec(f"{ID}-R006")
def test_every_app_has_an_instance_library_and_settings(graph):
    instance_of = rdflib.URIRef(ARR + "instanceOf")
    for app in APPS:
        node = rdflib.URIRef(ARR + f"instance-{app}")
        assert graph.value(node, instance_of) == rdflib.URIRef(ARR + f"app-{app}")
        assert graph.value(node, rdflib.URIRef(ARR + "holdsLibrary")) is not None
        setting = str(graph.value(node, rdflib.URIRef(ARR + "baseUrlSetting")))
        assert setting == f"{app.upper()}_BASE_URL"


@pytest.mark.spec(f"{ID}-R006")
def test_routing_and_federation_are_recorded(graph):
    routes = list(graph.subjects(RDF.type, rdflib.URIRef(ARR + "RoutingRule")))
    links = list(graph.subjects(RDF.type, rdflib.URIRef(ARR + "FederationLink")))
    kinds = {
        str(graph.value(link, rdflib.URIRef(ARR + "federationKind"))) for link in links
    }
    assert len(routes) >= 5
    assert {"syncsIndexersTo", "forwardsRequestsTo", "subtitlesFor"} <= kinds


# --- R007: every class rolls up to medulla core, never by import ----------


def _core_graph():
    spec = importlib.util.find_spec("medulla")
    if spec is None or not spec.submodule_search_locations:
        pytest.fail(
            "the test extra installs medulla, whose wheel ships the core ontology"
        )
    core = rdflib.Graph()
    for location in spec.submodule_search_locations:
        for path in sorted(Path(location, "ontology").glob("*.ttl")):
            if not path.name.endswith(".shapes.ttl"):
                core.parse(path, format="turtle")
    return core


@pytest.mark.spec(f"{ID}-R007")
def test_no_ontology_imports(graph):
    assert list(graph.objects(None, OWL.imports)) == []


@pytest.mark.spec(f"{ID}-R007")
def test_every_class_reaches_medulla_core_and_bfo_entity(graph):
    core = _core_graph()
    merged = core + graph
    core_classes = set(core.subjects(RDF.type, OWL.Class))
    classes = [c for c in graph.subjects(RDF.type, OWL.Class) if str(c).startswith(ARR)]
    assert len(classes) >= 20
    for cls in classes:
        ancestors = set(merged.transitive_objects(cls, RDFS.subClassOf)) - {cls}
        assert ancestors & core_classes, f"{cls} extends no medulla core class"
        assert BFO_ENTITY in ancestors, f"{cls} does not reach bfo:Entity"
    for cls in graph.subjects(RDF.type, OWL.Class):
        assert str(cls).startswith(ARR), f"{cls}: core classes are never redeclared"


@pytest.mark.spec(f"{ID}-R007")
def test_media_classes_the_library_holds_are_core(graph):
    core = _core_graph()
    core_classes = set(core.subjects(RDF.type, OWL.Class))
    for held in graph.objects(None, rdflib.URIRef(ARR + "holdsMediaClass")):
        assert held in core_classes, held
    assert str(KG + "Film") in {str(c) for c in core_classes}


# --- R008: knowledge-graph ingest uses core classes and served tools ------


@pytest.mark.spec(f"{ID}-R008")
def test_ingest_presets_name_served_tools_with_current_pins(served):
    import yaml
    from fastmcp import Client
    from scion_sdk.connector import build_server
    from scion_sdk.manifest.live_contract import validate_live_tool_contract

    tools, _, _ = served
    presets = yaml.safe_load((PKG / "ontology/mappings/source.yaml").read_text())
    _, mcp = build_server("arr_mcp", command_args=[])

    async def listing():
        async with Client(mcp) as client:
            return await client.session.list_tools()

    listed = asyncio.run(listing())
    for preset in presets["sync"]:
        assert preset["tool"] in tools, preset["preset"]
        assert "action" not in preset, preset["preset"]
        live = validate_live_tool_contract(listed, tool_name=preset["tool"])
        assert live.compatibility_sha256 == preset["tool_schema_sha256"], preset[
            "preset"
        ]


@pytest.mark.spec(f"{ID}-R008")
def test_ingest_node_types_are_medulla_core_classes():
    core = _core_graph()
    source = (PKG / "kg_ingest.py").read_text()
    for node_type in set(re.findall(r'"node_type": "([A-Za-z]+)"', source)):
        assert (rdflib.URIRef(KG + node_type), RDF.type, OWL.Class) in core, node_type


# --- R009: Bazarr operations hidden from its swagger -------------------------


@pytest.mark.spec(f"{ID}-R009")
def test_bazarr_settings_save_posts_the_settings_page_form():
    seen = []

    def handler(request):
        seen.append(request)
        return httpx.Response(204)

    api = _api("bazarr", handler)
    assert api.post_system_settings(
        settings={
            "settings-general-use_sonarr": True,
            "settings-general-enabled_providers": ["gestdown", "yifysubtitles"],
            "languages-enabled": ["en"],
        }
    ) == {"status": "success"}
    request = seen[0]
    assert (request.method, request.url.path) == ("POST", "/api/system/settings")
    body = request.content.decode()
    assert "settings-general-use_sonarr=true" in body
    assert body.count("settings-general-enabled_providers=") == 2
    assert "languages-enabled=en" in body


@pytest.mark.spec(f"{ID}-R009")
def test_bazarr_hidden_operations_are_served(served):
    tools, _, _ = served
    for name in (
        "bazarr_get_system_settings",
        "bazarr_post_system_settings",
        "bazarr_patch_system_notifications",
        "bazarr_post_system_restart",
    ):
        assert name in tools, name


# --- R010: a failed call carries the app's own reason ------------------------


@pytest.mark.spec(f"{ID}-R010")
@pytest.mark.parametrize(
    ("body", "reason"),
    [
        (
            [
                {
                    "propertyName": "Host",
                    "errorMessage": "Unable to connect to qBittorrent",
                    "severity": "error",
                }
            ],
            "Host: Unable to connect to qBittorrent",
        ),
        (
            {
                "title": "One or more validation errors occurred.",
                "errors": {"$": ["missing required properties including: 'folderType'."]},
            },
            "$: missing required properties including: 'folderType'.",
        ),
        ({"message": "Request not found"}, "Request not found"),
    ],
)
def test_a_failed_call_raises_with_the_upstream_reason(body, reason):
    from arr_mcp.api._security import raise_for_api_error

    response = httpx.Response(
        400, json=body, request=httpx.Request("POST", "http://arr.test/api")
    )
    with pytest.raises(RuntimeError) as raised:
        raise_for_api_error(response)
    assert str(raised.value).startswith("API error: HTTP 400: ")
    assert reason in str(raised.value)


@pytest.mark.spec(f"{ID}-R010")
def test_a_proxy_error_page_is_named_not_dumped():
    def handler(request):
        return httpx.Response(
            504, text="<html>504 Gateway Time-out</html>", headers={"content-type": "text/html"}
        )

    api = _api("bazarr", handler)
    with pytest.raises(RuntimeError, match=r"HTTP 504: the app answered with a web page"):
        api.get_badges()


@pytest.mark.spec(f"{ID}-R010")
@pytest.mark.parametrize("app", APPS)
def test_every_client_raises_through_the_shared_boundary(app):
    source = (PKG / f"api/api_client_{app}.py").read_text()
    assert "raise_for_api_error(response)" in source
    assert 'RuntimeError(f"API error: HTTP {response.status_code}")' not in source


@pytest.mark.spec(f"{ID}-R010")
def test_long_upstream_operations_have_minutes_not_seconds():
    from arr_mcp.api import _security

    assert _security.REQUEST_TIMEOUT.read >= 300
    assert _security._MAX_RESPONSE_SECONDS >= 300


# --- R011: provisioning workflows proven live are contracts -----------------


PROVISIONING = {
    "bazarr-connect-sonarr-radarr": ("arr-subtitle-management", "subtitle_curator"),
    "bazarr-enable-free-providers": ("arr-subtitle-management", "subtitle_curator"),
    "arr-repair-download-client": ("arr-download-queue", "download_monitor"),
    "chaptarr-provision-book-library": ("arr-book-library", "media_librarian"),
    "prowlarr-replace-dead-indexer": ("arr-indexer-management", "indexer_maintainer"),
    "seerr-route-requests-by-quality": ("arr-media-requests", "request_manager"),
}


@pytest.mark.spec(f"{ID}-R011")
@pytest.mark.parametrize("contract", sorted(PROVISIONING))
def test_provisioning_contracts_are_recorded_with_approval_steps(contract, graph):
    skill, prompt = PROVISIONING[contract]
    node = rdflib.URIRef(ARR + f"contract-{contract}")
    assert (node, RDF.type, rdflib.URIRef(ARR + "ToolUseContract")) in graph
    assert graph.value(node, rdflib.URIRef(ARR + "contractOf")) == rdflib.URIRef(
        ARR + f"skill-{skill}"
    )
    approvals = [
        bool(graph.value(step, rdflib.URIRef(ARR + "needsApproval")).toPython())
        for step in graph.objects(node, rdflib.URIRef(ARR + "hasStep"))
    ]
    assert any(approvals), contract
    for runner in (prompt, "arr_operator"):
        doc = json.loads((PKG / "prompts" / f"{runner}.json").read_text())
        assert contract in doc["contracts"], runner
        assert (
            rdflib.URIRef(ARR + f"prompt-{runner}"),
            rdflib.URIRef(ARR + "runsContract"),
            node,
        ) in graph
    assert f"(`{contract}`)" in (PKG / "skills" / skill / "SKILL.md").read_text()


# --- R012: settings reads never return secret values -------------------------


@pytest.mark.spec(f"{ID}-R012")
def test_bazarr_settings_read_masks_secrets():
    def handler(request):
        return httpx.Response(
            200,
            json={
                "auth": {"apikey": "k1", "username": ""},
                "sonarr": {"apikey": "k2", "ip": "127.0.0.1"},
                "plex": {"encryption_key": "k3", "token": ""},
                "translator": {"gemini_keys": ["k4"]},
                "general": {"use_sonarr": True, "enabled_providers": ["gestdown"]},
            },
        )

    api = _api("bazarr", handler)
    out = api.get_system_settings()
    assert out["auth"]["apikey"] == "<set>"
    assert out["sonarr"] == {"apikey": "<set>", "ip": "127.0.0.1"}
    assert out["plex"] == {"encryption_key": "<set>", "token": ""}
    assert out["translator"]["gemini_keys"] == "<set>"
    assert out["general"]["enabled_providers"] == ["gestdown"]
    assert "k1" not in json.dumps(out) and "k4" not in json.dumps(out)


# --- R013: the whole surface is declared -------------------------------------


@pytest.mark.spec(f"{ID}-R013")
def test_every_tool_is_called_by_a_contract_step(served):
    from arr_mcp.connector_contracts import CONTRACTS

    tools, _, _ = served
    called = {step.tool for contract in CONTRACTS for step in contract.steps}
    assert not sorted(set(tools) - called - {"connector_status"}), "tools no contract calls"
