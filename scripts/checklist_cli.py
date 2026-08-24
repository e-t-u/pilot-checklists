#!/usr/bin/env python3
"""
Aviation-Grade Checklist Engine & Card Generator
Implements NASA / FAA / QRH human factors checklist principles:
- Challenge - Response format with dot-leaders
- Do-Verify vs Read-and-Do execution modes
- Killer Items & Immediate Action (Boldface) isolation
- Phase-of-Operation chunking (5-9 items max)
- Terminal interactive runner & Card rendering (Markdown, A5/A6 Landscape PDF, HTML, Plaintext)
"""

import sys
import os
import json
import argparse
import subprocess
import tempfile
from pathlib import Path
from typing import Dict, List, Any, Optional

TEMPLATES_DIR = Path(__file__).resolve().parent.parent / "templates"

class Colors:
    HEADER = "\033[95m"
    BLUE = "\033[94m"
    CYAN = "\033[96m"
    GREEN = "\033[92m"
    YELLOW = "\033[93m"
    RED = "\033[91m"
    BOLD = "\033[1m"
    UNDERLINE = "\033[4m"
    DIM = "\033[2m"
    RESET = "\033[0m"


def load_checklist(filepath_or_name: str) -> Dict[str, Any]:
    p = Path(filepath_or_name)
    if not p.is_file():
        p = TEMPLATES_DIR / f"{filepath_or_name}.json"
        if not p.is_file():
            p = TEMPLATES_DIR / filepath_or_name
            if not p.is_file():
                raise FileNotFoundError(f"Checklist not found: {filepath_or_name}")
    with open(p, "r", encoding="utf-8") as f:
        return json.load(f)


def format_dot_leader(challenge: str, response: str, target_width: int = 58) -> str:
    max_resp_len = 28
    if len(response) > max_resp_len:
        resp_display = response[:max_resp_len - 1] + "."
    else:
        resp_display = response

    avail_for_ch = target_width - len(resp_display) - 4
    if len(challenge) > avail_for_ch:
        ch_display = challenge[:avail_for_ch - 1] + "."
    else:
        ch_display = challenge

    lead_len = target_width - len(ch_display) - len(resp_display) - 2
    if lead_len < 2:
        lead_len = 2
    dots = "." * lead_len
    return f"{ch_display} {dots} {resp_display}"


def render_markdown_card(data: Dict[str, Any]) -> str:
    title = data.get("title", "CHECKLIST CARD").upper()
    code = data.get("code", "CHK-01")
    mode = data.get("mode", "DO-VERIFY").upper()
    trigger = data.get("trigger", "BEFORE PROCEEDING")
    flow = data.get("flow_pattern", None)
    phases = data.get("phases", [])
    memory_actions = data.get("immediate_memory_actions", [])

    BOX_WIDTH = 70
    INNER_WIDTH = 66

    def pad_line(content: str) -> str:
        if len(content) > INNER_WIDTH:
            content = content[:INNER_WIDTH]
        pad = INNER_WIDTH - len(content)
        return f"│ {content}{' ' * pad} │"

    lines = []
    lines.append("```text")
    lines.append("┌" + "─" * (BOX_WIDTH - 2) + "┐")

    code_tag = f"[{code}]"
    t_space = INNER_WIDTH - len(code_tag) - 3
    t_str = title[:t_space]
    lines.append(pad_line(f"{t_str}{' ' * (INNER_WIDTH - len(t_str) - len(code_tag))}{code_tag}"))
    lines.append(pad_line(f"MODE: {mode}  |  PAUSE TRIGGER: {trigger}"))
    lines.append("├" + "─" * (BOX_WIDTH - 2) + "┤")

    if flow:
        lines.append(pad_line(f"TACTILE FLOW: {flow}"))
        lines.append("├" + "─" * (BOX_WIDTH - 2) + "┤")

    if memory_actions:
        lines.append(pad_line("BOLDFACE (IMMEDIATE MEMORY ACTIONS - EXECUTE BEFORE CARD):"))
        for item in memory_actions:
            ch = item.get("challenge", "").upper()
            resp = item.get("response", "").upper()
            row = format_dot_leader(ch, resp, INNER_WIDTH - 4)
            lines.append(pad_line(f" * {row}"))
        lines.append("├" + "─" * (BOX_WIDTH - 2) + "┤")

    for p_idx, phase in enumerate(phases):
        p_name = phase.get("name", f"PHASE {p_idx+1}").upper()
        lines.append(pad_line(f">> {p_name}"))
        items = phase.get("items", [])
        for it in items:
            ch = it.get("challenge", "").upper()
            resp = it.get("response", "").upper()
            killer = it.get("killer", False)
            prefix = "[!] " if killer else "[ ] "
            row = format_dot_leader(ch, resp, INNER_WIDTH - 4)
            lines.append(pad_line(f"{prefix}{row}"))
        if p_idx < len(phases) - 1:
            lines.append("├" + "─" * (BOX_WIDTH - 2) + "┤")

    lines.append("├" + "─" * (BOX_WIDTH - 2) + "┤")
    lines.append(pad_line("AVIATION SAFETY STANDARD  |  POINT & VERIFY  |  DO NOT GUESS"))
    lines.append("└" + "─" * (BOX_WIDTH - 2) + "┘")
    lines.append("```")
    return "\n".join(lines)


def render_html_card(
    data: Dict[str, Any],
    theme: str = "print",
    size: str = "a5",
    orientation: str = "landscape"
) -> str:
    title = data.get("title", "CHECKLIST CARD").upper()
    code = data.get("code", "CHK-01")
    mode = data.get("mode", "DO-VERIFY").upper()
    trigger = data.get("trigger", "BEFORE PROCEEDING")
    flow = data.get("flow_pattern", "")
    phases = data.get("phases", [])
    memory_actions = data.get("immediate_memory_actions", [])

    is_emergency = "EMERGENCY" in mode or "ABNORMAL" in mode or "QRH" in code
    is_landscape = orientation.lower() == "landscape"
    is_a6 = size.lower() == "a6"

    # Dimensions & Page Setup
    if is_a6 and is_landscape:
        page_size_css = "A6 landscape"
        margin_css = "3mm"
        card_max_w = "142mm"
        card_min_h = "99mm"
        title_font_pt = "9.5pt"
        base_font_pt = "6.8pt"
        resp_font_pt = "6.5pt"
        header_pad = "3px 6px"
        section_pad = "2px 2px 3px 2px"
        row_pad = "1px 2px"
        row_margin = "0.5px 0"
        chk_box_size = "10px"
    elif is_a6 and not is_landscape:
        page_size_css = "A6 portrait"
        margin_css = "3.5mm"
        card_max_w = "98mm"
        card_min_h = "141mm"
        title_font_pt = "10pt"
        base_font_pt = "7.2pt"
        resp_font_pt = "7pt"
        header_pad = "4px 8px"
        section_pad = "3px 2px 4px 2px"
        row_pad = "1.5px 3px"
        row_margin = "1px 0"
        chk_box_size = "11px"
    elif is_landscape:  # A5 Landscape (Default Kneeboard)
        page_size_css = "A5 landscape"
        margin_css = "6mm"
        card_max_w = "198mm"
        card_min_h = "136mm"
        title_font_pt = "13.5pt"
        base_font_pt = "10.5pt"
        resp_font_pt = "10.5pt"
        header_pad = "7px 12px"
        section_pad = "3px 2px 5px 2px"
        row_pad = "2px 4px"
        row_margin = "1px 0"
        chk_box_size = "13px"
    else:  # A5 Portrait
        page_size_css = "A5 portrait"
        margin_css = "8mm"
        card_max_w = "132mm"
        card_min_h = "194mm"
        title_font_pt = "13pt"
        base_font_pt = "10pt"
        resp_font_pt = "10pt"
        header_pad = "7px 12px"
        section_pad = "3px 2px 5px 2px"
        row_pad = "2px 4px"
        row_margin = "1px 0"
        chk_box_size = "12px"

    # Color Palette
    if theme == "print":
        bg_body = "#F8FAFC"
        bg_card = "#FFFFFF"
        border_card = "#0F172A"
        header_bg = "#DC2626" if is_emergency else "#0B192C"
        header_text = "#FFFFFF"
        badge_bg = "rgba(255, 255, 255, 0.2)"
        meta_bg = "#F1F5F9"
        meta_text = "#475569"
        meta_accent = "#DC2626" if is_emergency else "#0284C7"
        flow_bg = "#FEF3C7"
        flow_border = "#F59E0B"
        flow_text = "#92400E"
        mem_bg = "#FEF2F2"
        mem_border = "#DC2626"
        mem_title = "#991B1B"
        phase_title = "#DC2626" if is_emergency else "#0369A1"
        phase_border = "#E2E8F0"
        ch_text = "#0F172A"
        resp_text = "#DC2626" if is_emergency else "#0284C7"
        killer_bg = "#FFF1F2"
        killer_border = "#E11D48"
        killer_resp = "#BE123C"
        dot_color = "#94A3B8"
        footer_bg = "#0B192C"
        footer_text = "#94A3B8"
    else:  # Dark Cockpit OLED
        bg_body = "#090D16"
        bg_card = "#0F172A"
        border_card = "#334155"
        header_bg = "#DC2626" if is_emergency else "#0284C7"
        header_text = "#FFFFFF"
        badge_bg = "rgba(0, 0, 0, 0.35)"
        meta_bg = "#090D16"
        meta_text = "#94A3B8"
        meta_accent = "#EF4444" if is_emergency else "#38BDF8"
        flow_bg = "#1E1E2F"
        flow_border = "#F59E0B"
        flow_text = "#FBBF24"
        mem_bg = "rgba(220, 38, 38, 0.15)"
        mem_border = "#DC2626"
        mem_title = "#FCA5A5"
        phase_title = "#EF4444" if is_emergency else "#38BDF8"
        phase_border = "#334155"
        ch_text = "#F8FAFC"
        resp_text = "#EF4444" if is_emergency else "#38BDF8"
        killer_bg = "rgba(239, 68, 68, 0.12)"
        killer_border = "#EF4444"
        killer_resp = "#F87171"
        dot_color = "#475569"
        footer_bg = "#090D16"
        footer_text = "#64748B"

    html = f"""<!DOCTYPE html>
<html lang="en">
<head>
<meta charset="UTF-8">
<title>{title} - Aviation Checklist Card</title>
<style>
  @import url('https://fonts.googleapis.com/css2?family=B612:ital,wght@0,400;0,700;1,400;1,700&family=B612+Mono:ital,wght@0,400;0,700;1,400;1,700&display=swap');

  @page {{
    size: {page_size_css};
    margin: {margin_css};
  }}
  * {{ box-sizing: border-box; margin: 0; padding: 0; }}
  body {{
    font-family: "B612", -apple-system, BlinkMacSystemFont, "Segoe UI", Roboto, Helvetica, Arial, sans-serif;
    background: {bg_body};
    color: {ch_text};
    display: flex;
    justify-content: center;
    align-items: center;
    min-height: 100vh;
    padding: 0;
  }}
  .card {{
    background: {bg_card};
    border: 2.5px solid {border_card};
    border-radius: 8px;
    width: 100%;
    max-width: {card_max_w};
    min-height: {card_min_h};
    display: flex;
    flex-direction: column;
    justify-content: space-between;
    overflow: hidden;
    box-shadow: 0 4px 15px rgba(0, 0, 0, 0.12);
  }}
  .card-header {{
    background: {header_bg};
    color: {header_text};
    padding: {header_pad};
    display: flex;
    justify-content: space-between;
    align-items: center;
    border-bottom: 2px solid rgba(0, 0, 0, 0.25);
  }}
  .card-title {{
    font-size: {title_font_pt};
    font-weight: 700;
    letter-spacing: 0.3px;
  }}
  .card-code {{
    font-family: "B612 Mono", monospace;
    font-size: 9.5pt;
    font-weight: 700;
    background: {badge_bg};
    padding: 3px 8px;
    border-radius: 4px;
    letter-spacing: 0.5px;
    white-space: nowrap;
    margin-left: 10px;
  }}
  .meta-bar {{
    background: {meta_bg};
    padding: 5px 12px;
    font-size: 8pt;
    display: flex;
    justify-content: space-between;
    border-bottom: 1.5px solid {phase_border};
    color: {meta_text};
    font-weight: 600;
  }}
  .meta-bar strong {{ color: {meta_accent}; font-weight: 800; }}
  .flow-box {{
    background: {flow_bg};
    border-left: 4px solid {flow_border};
    padding: 5px 12px;
    font-size: 8pt;
    color: {flow_text};
    font-weight: 700;
    border-bottom: 1px solid {phase_border};
  }}
  .content-area {{
    flex-grow: 1;
    padding: 6px 10px;
  }}
  .memory-box {{
    background: {mem_bg};
    border: 1.5px solid {mem_border};
    margin: 4px 0 6px 0;
    border-radius: 5px;
    padding: 5px 8px;
  }}
  .memory-title {{
    color: {mem_title};
    font-size: 7.5pt;
    font-weight: 900;
    text-transform: uppercase;
    letter-spacing: 0.5px;
    margin-bottom: 4px;
  }}
  .section {{
    padding: {section_pad};
    border-bottom: 1px solid {phase_border};
  }}
  .section:last-child {{ border-bottom: none; }}
  .phase-header {{
    font-size: 8.5pt;
    font-weight: 900;
    color: {phase_title};
    text-transform: uppercase;
    letter-spacing: 0.5px;
    margin-bottom: 2px;
    display: flex;
    align-items: center;
    gap: 4px;
  }}
  .checklist-row {{
    display: flex;
    align-items: center;
    padding: {row_pad};
    margin: {row_margin};
    border-radius: 3px;
    font-size: {base_font_pt};
    border-left: 3px solid transparent;
  }}
  .checklist-row.killer {{
    background: {killer_bg};
    border-left: 3px solid {killer_border};
  }}
  .chk-box {{
    display: inline-flex;
    justify-content: center;
    align-items: center;
    width: {chk_box_size};
    height: {chk_box_size};
    min-width: {chk_box_size};
    max-width: {chk_box_size};
    border: 1.5px solid {dot_color};
    border-radius: 2px;
    margin-right: 6px;
    background: {bg_card};
    font-family: "B612 Mono", monospace;
    font-size: 7.5pt;
    font-weight: 700;
    color: transparent;
  }}
  .killer .chk-box {{
    border: 1.5px solid {killer_border};
    color: {killer_border};
    background: {killer_bg};
  }}
  .challenge {{
    font-weight: 400;
    color: {ch_text};
    white-space: nowrap;
  }}
  .killer .challenge {{
    font-weight: 700;
    color: {ch_text};
  }}
  .leader {{
    flex-grow: 1;
    min-width: 12px;
    border-bottom: 1.5px dotted {dot_color};
    margin: 0 6px;
    height: 7px;
  }}
  .response {{
    font-weight: 700;
    color: {resp_text};
    white-space: nowrap;
    text-align: right;
    font-family: "B612 Mono", monospace;
    font-size: {resp_font_pt};
    letter-spacing: 0.2px;
  }}
  .killer .response {{
    color: {killer_resp};
  }}
  .card-footer {{
    background: {footer_bg};
    color: {footer_text};
    padding: 6px 10px;
    font-size: 7pt;
    font-weight: 700;
    letter-spacing: 0.8px;
    text-align: center;
    border-top: 2px solid {border_card};
  }}
</style>
</head>
<body>
<div class="card">
  <div>
    <div class="card-header">
      <div class="card-title">✈ {title}</div>
      <div class="card-code">{code}</div>
    </div>
    <div class="meta-bar">
      <div>MODE: <strong>{mode}</strong></div>
      <div>TRIGGER: <strong>{trigger}</strong></div>
    </div>
"""
    if flow:
        html += f"""    <div class="flow-box">TACTILE FLOW: {flow}</div>\n"""

    html += """    <div class="content-area">\n"""

    def format_challenge_title(text: str) -> str:
        acronyms = {"ID", "QR", "TSA", "EVOA", "PBS", "VM", "PVE", "SSH", "PDF", "API", "WIP", "ANC", "GIT", "DB", "EE", "FI", "TS", "EE/FI/TS", "LI-ION"}
        words = text.split(" ")
        formatted = []
        for w in words:
            # Check inside parens e.g. (li-ion) or (ee/fi/ts)
            if w.startswith("(") and w.endswith(")"):
                inner = w[1:-1]
                if inner.upper() in acronyms or "/" in inner:
                    parts = [p.upper() if p.upper() in acronyms else p.capitalize() for p in inner.split("/")]
                    formatted.append(f"({'/'.join(parts)})")
                    continue
            w_clean = w.strip("(),/")
            if w_clean.upper() in acronyms:
                formatted.append(w.upper())
            elif w.startswith("~/"):
                formatted.append(w)
            elif w.lower() in {"&", "/", "+", "->", "to", "or", "in", "of", "and", "the", "for"}:
                formatted.append(w.lower() if w != "&" else "&")
            else:
                formatted.append(w.capitalize())
        return " ".join(formatted)

    def render_section(phase_obj):
        p_name = phase_obj.get("name", "").upper()
        s_html = f"""      <div class="section">\n        <div class="phase-header">&gt;&gt; {p_name}</div>\n"""
        for item in phase_obj.get("items", []):
            ch = format_challenge_title(item.get("challenge", ""))
            resp = item.get("response", "").upper()
            killer = item.get("killer", False)
            k_cls = " killer" if killer else ""
            k_char = "!" if killer else "&nbsp;"
            s_html += f"""        <div class="checklist-row{k_cls}">
          <span class="chk-box">{k_char}</span>
          <span class="challenge">{ch}</span>
          <span class="leader"></span>
          <span class="response">{resp}</span>
        </div>\n"""
        s_html += "      </div>\n"
        return s_html

    if memory_actions:
        html += """      <div class="memory-box">\n        <div class="memory-title">BOLDFACE (IMMEDIATE MEMORY ACTIONS - EXECUTE FIRST)</div>\n"""
        for item in memory_actions:
            ch = item.get("challenge", "").upper()
            resp = item.get("response", "").upper()
            html += f"""        <div class="checklist-row killer">
          <span class="chk-box">!</span>
          <span class="challenge">{ch}</span>
          <span class="leader"></span>
          <span class="response">{resp}</span>
        </div>\n"""
        html += "      </div>\n"

    for p in phases:
        html += render_section(p)

    html += """    </div>
  </div>
  <div class="card-footer">AVIATION SAFETY STANDARD &bull; POINT &amp; VERIFY &bull; DO NOT GUESS</div>
</div>
</body>
</html>
"""
    return html


def generate_pdf(
    data: Dict[str, Any],
    output_pdf_path: str,
    theme: str = "print",
    size: str = "a5",
    orientation: str = "landscape"
) -> bool:
    html_content = render_html_card(data, theme=theme, size=size, orientation=orientation)
    out_path = Path(output_pdf_path).resolve()
    out_path.parent.mkdir(parents=True, exist_ok=True)

    with tempfile.NamedTemporaryFile("w", suffix=".html", delete=False, encoding="utf-8") as f:
        f.write(html_content)
        temp_html = f.name

    try:
        cmd = [
            "uv", "run", "--with", "weasyprint", "weasyprint",
            temp_html,
            str(out_path)
        ]
        res = subprocess.run(cmd, capture_output=True, text=True)
        if res.returncode == 0:
            print(f"Generated {size.upper()} {orientation.capitalize()} PDF: {out_path}")
            return True
        else:
            print(f"WeasyPrint error: {res.stderr}")
            return False
    except Exception as e:
        print(f"Failed to run WeasyPrint: {e}")
        return False
    finally:
        if os.path.exists(temp_html):
            os.remove(temp_html)


def run_interactive(data: Dict[str, Any]):
    title = data.get("title", "CHECKLIST CARD").upper()
    code = data.get("code", "CHK-01")
    mode = data.get("mode", "DO-VERIFY").upper()
    trigger = data.get("trigger", "BEFORE PROCEEDING")
    flow = data.get("flow_pattern", None)
    phases = data.get("phases", [])
    memory_actions = data.get("immediate_memory_actions", [])

    print("\n" + "=" * 60)
    print(f"{Colors.BOLD}{Colors.CYAN}AVIATION CHECKLIST RUNNER: {title} [{code}]{Colors.RESET}")
    print(f"{Colors.DIM}OPERATIONAL MODE:{Colors.RESET} {Colors.BOLD}{mode}{Colors.RESET}")
    print(f"{Colors.DIM}PAUSE TRIGGER:   {Colors.RESET} {Colors.YELLOW}{trigger}{Colors.RESET}")
    if flow:
        print(f"{Colors.DIM}FLOW SWEEP:      {Colors.RESET} {Colors.GREEN}{flow}{Colors.RESET}")
    print("=" * 60 + "\n")

    if memory_actions:
        print(f"{Colors.RED}{Colors.BOLD}[!] IMMEDIATE MEMORY ACTIONS (CONFIRM FIRST):{Colors.RESET}")
        for it in memory_actions:
            ch = it.get("challenge", "").upper()
            resp = it.get("response", "").upper()
            prompt_str = f"  {Colors.BOLD}{ch}{Colors.RESET} {Colors.DIM}...{Colors.RESET} {Colors.YELLOW}{resp}{Colors.RESET}"
            input(f"{prompt_str}  [Press Enter to confirm]")
        print()

    total_items = 0
    checked_items = 0

    for p_idx, phase in enumerate(phases):
        p_name = phase.get("name", f"PHASE {p_idx+1}").upper()
        print(f"\n{Colors.BOLD}{Colors.BLUE}─── PHASE: {p_name} ───{Colors.RESET}")
        items = phase.get("items", [])
        for it in items:
            total_items += 1
            ch = it.get("challenge", "").upper()
            resp = it.get("response", "").upper()
            killer = it.get("killer", False)

            if killer:
                badge = f"{Colors.RED}{Colors.BOLD}[KILLER ITEM]{Colors.RESET}"
                ch_formatted = f"{Colors.RED}{Colors.BOLD}{ch}{Colors.RESET}"
                resp_formatted = f"{Colors.RED}{Colors.BOLD}{resp}{Colors.RESET}"
            else:
                badge = f"{Colors.GREEN}[CHECK]{Colors.RESET}"
                ch_formatted = f"{Colors.BOLD}{ch}{Colors.RESET}"
                resp_formatted = f"{Colors.CYAN}{Colors.BOLD}{resp}{Colors.RESET}"

            dot_line = format_dot_leader(ch, resp, 50)
            print(f"\n{badge} {ch_formatted}")
            prompt = f"      Expected: {resp_formatted} -> Confirm? [Y/n]: "

            ans = input(prompt).strip().lower()
            if ans == "n" or ans == "no":
                print(f"\n{Colors.RED}{Colors.BOLD}CHECKLIST HALTED! Item '{ch}' not verified.{Colors.RESET}")
                print(f"{Colors.YELLOW}Correct the discrepancy and re-run checklist before proceeding.{Colors.RESET}")
                sys.exit(1)
            checked_items += 1

    print("\n" + "=" * 60)
    print(f"{Colors.GREEN}{Colors.BOLD}ALL {checked_items}/{total_items} CHECKLIST ITEMS CONFIRMED COMPLETE.{Colors.RESET}")
    print(f"{Colors.CYAN}Ready for departure/execution. Safe operations!{Colors.RESET}")
    print("=" * 60 + "\n")


def list_templates():
    print(f"\n{Colors.BOLD}{Colors.CYAN}Available Aviation Checklist Cards in Library:{Colors.RESET}")
    print("=" * 60)
    if not TEMPLATES_DIR.is_dir():
        print("Templates directory not found.")
        return
    for item in sorted(TEMPLATES_DIR.glob("*.json")):
        try:
            with open(item, "r", encoding="utf-8") as f:
                d = json.load(f)
                name = item.stem
                title = d.get("title", name)
                code = d.get("code", "CHK")
                mode = d.get("mode", "DO-VERIFY")
                print(f" * {Colors.BOLD}{name:<22}{Colors.RESET} [{code:<6}] {title:<30} ({mode})")
        except Exception:
            print(f" * {item.name}")
    print("=" * 60)
    print("Run terminal verification: python3 scripts/checklist_cli.py run <name>")
    print("Generate A5 Landscape PDF:  python3 scripts/checklist_cli.py pdf <name> -o <file.pdf>\n")


def main():
    parser = argparse.ArgumentParser(description="Aviation Checklist Runner & Landscape Card Generator")
    subparsers = parser.add_subparsers(dest="command")

    # List command
    subparsers.add_parser("list", help="List all installed checklist templates")

    # Run command
    run_parser = subparsers.add_parser("run", help="Run interactive challenge-response in terminal")
    run_parser.add_argument("name", help="Name or path of checklist template")

    # Card / Print command
    card_parser = subparsers.add_parser("card", help="Render markdown card to stdout")
    card_parser.add_argument("name", help="Name or path of checklist template")

    # HTML command
    html_parser = subparsers.add_parser("html", help="Render standalone HTML card")
    html_parser.add_argument("name", help="Name or path of checklist template")
    html_parser.add_argument("-o", "--output", help="Output HTML file path", default=None)
    html_parser.add_argument("--theme", choices=["print", "dark"], default="print", help="Theme style")
    html_parser.add_argument("--size", choices=["a5", "a6"], default="a5", help="Card size")
    html_parser.add_argument("--orientation", choices=["landscape", "portrait"], default="landscape", help="Orientation")

    # PDF command
    pdf_parser = subparsers.add_parser("pdf", help="Render print-ready Landscape vector PDF card")
    pdf_parser.add_argument("name", help="Name or path of checklist template")
    pdf_parser.add_argument("-o", "--output", help="Output PDF file path", default=None)
    pdf_parser.add_argument("--theme", choices=["print", "dark"], default="print", help="Theme style")
    pdf_parser.add_argument("--size", choices=["a5", "a6"], default="a5", help="Card size (a5 or a6)")
    pdf_parser.add_argument("--orientation", choices=["landscape", "portrait"], default="landscape", help="Orientation")

    # PDF-ALL command
    pdf_all_parser = subparsers.add_parser("pdf-all", help="Render all checklist cards to Landscape PDFs in a directory")
    pdf_all_parser.add_argument("-d", "--dir", default="./pdf", help="Output directory for generated PDFs")
    pdf_all_parser.add_argument("--theme", choices=["print", "dark"], default="print", help="Theme style")
    pdf_all_parser.add_argument("--size", choices=["a5", "a6"], default="a5", help="Card size (a5 or a6)")
    pdf_all_parser.add_argument("--orientation", choices=["landscape", "portrait"], default="landscape", help="Orientation")

    args = parser.parse_args()

    if args.command == "list" or not args.command:
        list_templates()
        return

    if args.command == "run":
        data = load_checklist(args.name)
        run_interactive(data)
    elif args.command == "card":
        data = load_checklist(args.name)
        print(render_markdown_card(data))
    elif args.command == "html":
        data = load_checklist(args.name)
        html_content = render_html_card(data, theme=args.theme, size=args.size, orientation=args.orientation)
        if args.output:
            with open(args.output, "w", encoding="utf-8") as f:
                f.write(html_content)
            print(f"Wrote HTML card to {args.output}")
        else:
            print(html_content)
    elif args.command == "pdf":
        data = load_checklist(args.name)
        out_file = args.output or f"{data.get('code', 'card').lower()}_{args.size}_{args.orientation}.pdf"
        generate_pdf(data, out_file, theme=args.theme, size=args.size, orientation=args.orientation)
    elif args.command == "pdf-all":
        out_dir = Path(args.dir)
        out_dir.mkdir(parents=True, exist_ok=True)
        templates = sorted(TEMPLATES_DIR.glob("*.json"))
        print(f"Generating {len(templates)} {args.size.upper()} {args.orientation.capitalize()} PDF cards into {out_dir}...")
        for p in templates:
            data = load_checklist(str(p))
            out_pdf = out_dir / f"{p.stem}.pdf"
            generate_pdf(data, str(out_pdf), theme=args.theme, size=args.size, orientation=args.orientation)


if __name__ == "__main__":
    main()
