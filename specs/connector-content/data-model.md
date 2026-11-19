# CONN-ARR-MCP-CONNECTOR-CONTENT — Data model

The packaged ontology declares classes only in the `https://knuckles-team.github.io/ontology/connector/arr#` namespace. No class IRI collides with core.

| Entity | Fields | Relations |
|---|---|---|
| `owl:Class` in `arr:` | `rdfs:label`, `rdfs:comment` | `rdfs:subClassOf` one core class |
| Television episode | the core `:TelevisionEpisode` class | `arr:route-TelevisionEpisode-sonarr` routes it to Sonarr |

The full class list and core parents are in [../arr-suite/data-model.md](../arr-suite/data-model.md).
