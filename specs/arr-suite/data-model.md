# CONN-ARR-MCP-SUITE — Data model

The ontology namespace is `http://knuckles.team/kg/arr#` (`arr:`). The core namespace is `http://knuckles.team/kg#` (`:`). Every class subclasses one core class and reaches `bfo:Entity` through core.

| Class | Core parent | Meaning |
|---|---|---|
| `arr:SuiteApp` | `:Application` | One application of the arr media suite (Radarr, Sonarr, Lidarr, Chaptarr, Prowlarr, Bazarr, Seerr). |
| `arr:AppInstance` | `:AssetInstance` | One deployed instance of a suite app, reached at its base URL setting with its API key setting. |
| `arr:Library` | `:MediaLibrary` | The managed store of media one app instance holds (the movie, TV, music or book library). |
| `arr:LibraryRootFolder` | `:Folder` | A root folder where an app stores library files; the data location of a library. |
| `arr:IndexerPool` | `:ConfigurationItemCollection` | The search indexers Prowlarr manages and syncs to the apps. |
| `arr:SubtitleStore` | `:MediaCollection` | The subtitle files Bazarr manages beside the media of Sonarr and Radarr. |
| `arr:RequestQueue` | `:Collection` | The user media requests Seerr holds before routing them to Radarr or Sonarr. |
| `arr:DownloadClient` | `:ConfigurationItem` | A download client an app sends grabbed releases to (for example qBittorrent). |
| `arr:QueueItem` | `:DownloadTransfer` | One download in an app's queue. |
| `arr:SubtitleFile` | `:MediaFile` | A subtitle file stored beside a media file. |
| `arr:LabelTag` | `:Concept` | A label an app attaches to media, indexers or clients to group them. |
| `arr:FederationLink` | `:ConfigurationItemCollection` | Two suite apps working together: indexer sync, request forwarding or subtitles. |
| `arr:RoutingRule` | `:Policy` | Which app instance a kind of media request routes to, and the root folder it lands in. |
| `arr:ConnectorTool` | `:Tool` | One typed MCP tool of the arr-mcp connector: one upstream API operation. |
| `arr:ToolUseContract` | `:Procedure` | A workflow: which tools run, in what order, with which parameters. |
| `arr:ContractStep` | `:TaskStep` | One ordered step of a tool-use contract: one tool call. |
| `arr:ParameterBinding` | `:ActionParameter` | Where one parameter of a step comes from: operator input, a constant, or an earlier step's result. |
| `arr:ConnectorSkill` | `:Procedure` | A skill shipped in the connector package: a set of task workflows over the connector's tools. |
| `arr:ConnectorPrompt` | `:Prompt` | A prompt shipped in the connector package; an agent definition arbora builds an agent from. |
| `arr:ArrAgentRole` | `:Role` | A business role an agent plays over the arr suite; a connector prompt is its system prompt. |
| `arr:ArrOperator` | `arr:ArrAgentRole` | The Arr Suite Operator role over the arr suite. |
| `arr:MediaLibrarian` | `arr:ArrAgentRole` | The Media Librarian role over the arr suite. |
| `arr:RequestManager` | `arr:ArrAgentRole` | The Media Request Manager role over the arr suite. |
| `arr:IndexerMaintainer` | `arr:ArrAgentRole` | The Indexer Maintainer role over the arr suite. |
| `arr:SubtitleCurator` | `arr:ArrAgentRole` | The Subtitle Curator role over the arr suite. |
| `arr:DownloadMonitor` | `arr:ArrAgentRole` | The Download Monitor role over the arr suite. |

## Relations

| Property | From | To |
|---|---|---|
| `arr:instanceOf` | `arr:AppInstance` | `arr:SuiteApp` |
| `arr:holdsLibrary` | `arr:AppInstance` | `arr:Library` |
| `arr:storedIn` | `arr:Library` | `arr:LibraryRootFolder` |
| `arr:holdsMediaClass` | `arr:Library` | core class |
| `arr:downloadsWith` | `arr:AppInstance` | `arr:DownloadClient` |
| `arr:federationSource` | `arr:FederationLink` | `arr:AppInstance` |
| `arr:federationTarget` | `arr:FederationLink` | `arr:AppInstance` |
| `arr:federationKind` | `arr:FederationLink` | literal |
| `arr:routesMediaClass` | `arr:RoutingRule` | core class |
| `arr:routesTo` | `arr:RoutingRule` | `arr:AppInstance` |
| `arr:landsIn` | `arr:RoutingRule` | `arr:LibraryRootFolder` |
| `arr:toolOf` | `arr:ConnectorTool` | `arr:SuiteApp` |
| `arr:toolName` | `arr:ConnectorTool` | literal |
| `arr:toolPrefix` | `arr:SuiteApp` | literal |
| `arr:apiBasePath` | `arr:SuiteApp` | literal |
| `arr:baseUrlSetting` | `arr:AppInstance` | literal |
| `arr:apiKeySetting` | `arr:AppInstance` | literal |
| `arr:rootFolderPath` | `arr:LibraryRootFolder` | literal |
| `arr:hasStep` | `arr:ToolUseContract` | `arr:ContractStep` |
| `arr:stepIndex` | `arr:ContractStep` | literal |
| `arr:callsTool` | `arr:ContractStep` | `arr:ConnectorTool` |
| `arr:precedesStep` | `arr:ContractStep` | `arr:ContractStep` |
| `arr:bindsParameter` | `arr:ContractStep` | `arr:ParameterBinding` |
| `arr:parameterName` | `arr:ParameterBinding` | literal |
| `arr:parameterSource` | `arr:ParameterBinding` | literal |
| `arr:needsApproval` | `arr:ContractStep` | literal |
| `arr:contractOf` | `arr:ToolUseContract` | `arr:ConnectorSkill` |
| `arr:skillName` | `arr:ConnectorSkill` | literal |
| `arr:usesSkill` | `arr:ConnectorPrompt` | `arr:ConnectorSkill` |
| `arr:runsContract` | `arr:ConnectorPrompt` | `arr:ToolUseContract` |
| `arr:usesTool` | `arr:ConnectorPrompt` | `arr:ConnectorTool` |
| `arr:systemPromptForRole` | `arr:ConnectorPrompt` | `arr:ArrAgentRole` |
| `arr:promptName` | `arr:ConnectorPrompt` | literal |
| `arr:resourceUri` | any | literal |

## Ingested records

`arr_ingest_library` writes core-class nodes: `:Film` (Radarr movie, keyed `tmdbId`), `:Series` (Sonarr series, keyed `tvdbId`), `:MediaIndexer` (Prowlarr indexer) and `:QualityProfile`, linked by `hasQualityProfile`.
