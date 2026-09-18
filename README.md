# Piyano Datapack Patcher

[日本語](./README.md) | [English](./README.en.md)

Minecraft Java Edition のデータパックの主要なJSONファイルを、バージョン間の仕様変更に合わせて変換するためのツールです。

現在は **Minecraft Java Edition 26.2 → 26.3** の変換に対応しており、一部のデータパック要素を自動でアップコンバートできます。

> [!WARNING]
> 本ツールは開発中です。すべてのデータパックで完全な変換を保証するものではありません。  
> 変換後のデータパックは、実際の環境で動作確認してから使用してください。

## 対応バージョン

| 変換元 | 変換先 | 対応状況 |
| --- | --- | --- |
| 26.2 | 26.3 | 対応 |

本ツールは **正式リリースから正式リリースへの変換のみ** を対象としています。  
Snapshot、Pre-Release、Release Candidate 間の変換はサポート対象外です。

## 対応しているデータパック要素

現在、主に以下の要素の 26.2 → 26.3 変換に対応しています。

| registry | 
| --- | 
| `advancement` |
| `item_modifier` |
| `loot_table` |
| `predicate` |
| `number_provider` |
| `villager_trade` |
| `trade_set` |

> mcfunction内のインライン表記は変換対象外です。

 - 非対応要素の例
   - `minecraft:pot_decorations` component
   - `minecraft:exploration_map` loot function
   - `worldgen/` registry
     - `block_state_provider` など

## ダウンロード

Windows 向けの `.exe` を配布します。

GitHub Releases からダウンロードしてください。

> Release ページへのリンクは、公開後にここへ追加してください。

## 使い方

1. 変換したいデータパックを用意します。
2. データパックの **フォルダ** または **`.zip` ファイル** を `PiyanoDatapackPatcher` の `.exe` にドラッグ＆ドロップします。
3. 変換が完了すると、入力したデータパックと同じ階層に変換済みの `.zip` が生成されます。

デフォルトの出力名は次の形式です。

```text
<元の名前>_patched_<変換先バージョン>.zip
```

例: `my_datapack_patched_26.3.zip`

## 出力とログ

通常は、入力されたデータパックと同じ階層に変換済み `.zip` を生成します。

変換処理の成功ログは、**変換後のデータパック内** に保存されます。

予期しないエラーが発生した場合は、**実行した `.exe` と同じ場所** にエラーログを保存します。  
不具合報告の際は、このログを添付していただけると原因調査に役立ちます。

## 注意事項

- 本ツールは 26.2 → 26.3 の仕様変更すべてを完全に変換できることを保証するものではありません。
- 変換後のデータパックは Minecraft JE 26.3 環境での読み込みを保証するものではありません。本番環境へ上書きは、検証を十分に重ねてから行ってください。
- CLIからのみ元データパックを直接変更する機能が利用できますが、使用は自己責任でお願いします。

## 不具合報告・Pull Request

不具合報告は GitHub Issues で受け付けています。

変換漏れや不具合を見つけた場合は、可能であれば以下の情報を添えてください。

- 変換元データパックの Minecraft バージョン
- 変換対象となったファイルや `registry`
- 発生した症状
- エラーログ
- 再現可能な最小構成のデータパックや JSON (共有可能な場合)

Pull Request も歓迎します。

ただし、用途が限定的な機能追加や個別仕様への対応を保証するものではありません。  
Issue や Pull Request の内容によっては、対応を見送る場合があります。

## 開発について

このプロジェクトは Python で開発されています。

現時点では Minecraft Java Edition 26.2 → 26.3 の変換を中心に実装しています。  
今後の Minecraft アップデートについても、必要に応じて対応範囲を拡張する予定です。

## 参考資料

変換仕様の確認には、Minecraft 公式の 26.3 リリース記事を参考にしています。

- [Minecraft Java Edition 26.3](https://www.minecraft.net/en-us/article/minecraft-java-edition-26-3)

## License

Copyright (c) 2026 CobwebbyPiano58

This project is licensed under the [MIT License](./LICENSE).

## Author

**CobwebbyPiano58**
