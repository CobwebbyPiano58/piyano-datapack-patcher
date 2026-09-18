# Piyano Datapack Patcher

[日本語](./README.md) | [English](./README.en.md)

A tool for converting major JSON files in Minecraft Java Edition data packs to match specification changes between game versions.

Currently, it supports **Minecraft Java Edition 26.2 → 26.3** and can automatically migrate some data pack elements to the newer format.

> [!WARNING]
> This tool is still under development and does not guarantee a perfect conversion for every data pack.  
> Always test the converted data pack in an actual Minecraft environment before using it.

## Supported Versions

| Source | Target | Status |
| --- | --- | --- |
| 26.2 | 26.3 | Supported |

This tool supports **stable release to stable release conversions only**.  
Conversions between Snapshots, Pre-Releases, and Release Candidates are not supported.

## Supported Data Pack Elements

The 26.2 → 26.3 conversion currently supports the following elements.

| registry |
| --- |
| `advancement` |
| `item_modifier` |
| `loot_table` |
| `predicate` |
| `number_provider` |
| `villager_trade` |
| `trade_set` |

> Inline definitions inside mcfunction commands are not converted.

- Examples of unsupported elements
  - `minecraft:pot_decorations` component
  - `minecraft:exploration_map` loot function
  - `worldgen/` registry
    - `block_state_provider`, etc.

## Download

A Windows `.exe` build is provided.

Download it from GitHub Releases.

https://github.com/CobwebbyPiano58/piyano-datapack-patcher/releases/latest

## Usage

1. Prepare the data pack you want to convert.
2. Drag and drop either the data pack **folder** or **`.zip` file** onto the `piyano-datapack-patcher` `.exe`.
3. After the conversion finishes, a converted `.zip` will be created in the same directory as the input data pack.

The default output name uses the following format:

```text
<original_name>_patched_<target_version>.zip
```

Example: `my_datapack_patched_26.3.zip`

## Output and Logs

By default, the converted `.zip` is created in the same directory as the input data pack.

A log of successfully converted resources is stored **inside the converted data pack**.

If an unexpected error occurs, an error log is saved **in the same directory as the `.exe` that was executed**.  
When reporting an issue, attaching this log can help with investigating the cause.

## Important Notes

- This tool does not guarantee complete conversion of every specification change from 26.2 to 26.3.
- A converted data pack is not guaranteed to load successfully in Minecraft JE 26.3. Test it thoroughly before replacing the version used in your actual world or server.
- A feature for modifying the original data pack in place is available only through the CLI. Use it at your own risk.

## Bug Reports and Pull Requests

Bug reports are accepted through GitHub Issues.

If you find a missing conversion or other problem, please include as much of the following information as possible:

- Minecraft version of the source data pack
- The affected file or `registry`
- What happened
- Error log
- A minimal reproducible data pack or JSON example, if it can be shared

Pull Requests are also welcome.

However, support for highly specific use cases or individual custom requirements is not guaranteed.  
Depending on the scope or purpose of an Issue or Pull Request, it may not be implemented or accepted.

## Development

This project is developed in Python.

Development currently focuses on Minecraft Java Edition 26.2 → 26.3 conversion support.  
Support for future Minecraft updates may be added as needed.

## References

The official Minecraft 26.3 release article is used as a reference when implementing conversion rules.

- [Minecraft Java Edition 26.3](https://www.minecraft.net/en-us/article/minecraft-java-edition-26-3)

## License

Copyright (c) 2026 CobwebbyPiano58

This project is licensed under the [MIT License](./LICENSE).

## Author

**CobwebbyPiano58**
