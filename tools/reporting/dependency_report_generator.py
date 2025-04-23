from pathlib import Path
import json

def generate_html_report(json_report_path: str, html_path: str) -> Path:
    """
    指定したJSONレポートを読み込み、HTML形式のレポートを生成して保存する。
    :param json_report_path: JSONレポートファイルのパス
    :param html_path: 出力するHTMLファイルのパス
    :return: 出力したHTMLファイルのPathオブジェクト
    """
    json_path = Path(json_report_path)
    html_path_obj = Path(html_path)

    # JSONを読み込む
    with json_path.open(encoding="utf-8") as f:
        data = json.load(f)

    # 必要なデータを取得
    missing = data.get("missing_dependencies", {})
    cycle_count = data.get("cycle_count", 0)
    integrity_score = data.get("integrity_score", data.get("health_score", 0))

    # HTMLコンテンツを構築
    lines = []
    lines.append("<!DOCTYPE html>")
    lines.append("<html>")
    lines.append("<head>")
    lines.append("  <meta charset=\"UTF-8\">")
    lines.append("  <title>Dependency Integrity Report</title>")
    lines.append("</head>")
    lines.append("<body>")
    lines.append("  <h1>Dependency Integrity Report</h1>")
    lines.append(f"  <p>Cycles detected: {cycle_count}</p>")
    lines.append(f"  <p>Integrity Score: {integrity_score}</p>")

    if missing:
        lines.append("  <h2>Missing Dependencies</h2>")
        lines.append("  <ul>")
        for file, deps in missing.items():
            deps_list = ", ".join(deps)
            lines.append(f"    <li>{file}: {deps_list}</li>")
        lines.append("  </ul>")

    lines.append("</body>")
    lines.append("</html>")

    content = "\n".join(lines)

    # HTMLファイルを書き出し
    html_path_obj.write_text(content, encoding="utf-8")
    return html_path_obj
