# -*- coding: utf-8 -*-
import re
from pathlib import Path

ROOT = Path(__file__).resolve().parent
WPP = "https://wa.me/5519981433666"
SKIP = {"google9a829d4374024afb.html"}


def fix_servicos_dropdown(t: str) -> str:
    btn = '<button class="nav-dropbtn">'
    idx = 0
    while True:
        i = t.find(btn, idx)
        if i == -1:
            break
        if t.find("Serviços", i, i + 250) == -1:
            idx = i + 1
            continue
        menu_start = t.find('<div class="dropdown-menu">', i)
        if menu_start == -1:
            idx = i + 1
            continue
        hr = t.find("<hr class=\"dropdown-divider\">", menu_start)
        if hr == -1:
            idx = i + 1
            continue
        m2 = re.search(
            r"</div>\s*</div>\s*<div class=\"(nav-sep|nav-dropdown)",
            t[menu_start:],
        )
        if not m2:
            idx = i + 1
            continue
        chunk_end = menu_start + m2.start()
        inner = t[menu_start:chunk_end]
        parts = inner.split("<hr class=\"dropdown-divider\">", 1)
        if len(parts) != 2:
            idx = i + 1
            continue
        before, after = parts
        before = re.sub(r"<a href=\"#\">", '<a href="gestao-de-frotas.html">', before, count=1)
        before = re.sub(r"<a href=\"#\">", '<a href="telemetria.html">', before, count=1)
        before = re.sub(r"<a href=\"#\">", '<a href="videotelemetria.html">', before, count=1)
        after = re.sub(r"<a href=\"#\">", '<a href="gestao-de-risco.html">', after, count=1)
        new_inner = before + "<hr class=\"dropdown-divider\">" + after
        t = t[:menu_start] + new_inner + t[chunk_end:]
        break
    return t


def fix_file(path: Path) -> None:
    t = path.read_text(encoding="utf-8")
    orig = t

    t = fix_servicos_dropdown(t)

    t = t.replace('<a href="#">Sobre Nós</a>', '<a href="sobre.html">Sobre Nós</a>')
    t = t.replace('<a href="#" class="btn-nav-cta">', '<a href="contato.html" class="btn-nav-cta">')
    t = t.replace(
        '<a href="#" style="font-size:13px;color:#111;text-decoration:none;font-weight:500;font-family:\'Ubuntu\',sans-serif;padding:8px 14px;border-radius:4px;transition:all .2s;" onmouseover="this.style.color=\'#DE3934\';this.style.background=\'#FDF0EF\'" onmouseout="this.style.color=\'#111\';this.style.background=\'transparent\'">Contato</a>',
        '<a href="contato.html" style="font-size:13px;color:#111;text-decoration:none;font-weight:500;font-family:\'Ubuntu\',sans-serif;padding:8px 14px;border-radius:4px;transition:all .2s;" onmouseover="this.style.color=\'#DE3934\';this.style.background=\'#FDF0EF\'" onmouseout="this.style.color=\'#111\';this.style.background=\'transparent\'">Contato</a>',
    )

    t = t.replace(
        '<a href="#" style="font-size:13px;color:#111;text-decoration:none;font-weight:500;font-family:\'Ubuntu\',sans-serif;padding:8px 14px;border-radius:4px;transition:all .2s;" style="font-size:13px;color:#DE3934;text-decoration:none;font-weight:700;font-family:\'Ubuntu\',sans-serif;">Contato</a>',
        '<a href="contato.html" style="font-size:13px;color:#111;text-decoration:none;font-weight:500;font-family:\'Ubuntu\',sans-serif;padding:8px 14px;border-radius:4px;transition:all .2s;" onmouseover="this.style.color=\'#DE3934\';this.style.background=\'#FDF0EF\'" onmouseout="this.style.color=\'#111\';this.style.background=\'transparent\'">Contato</a>',
    )

    t = t.replace('<a href="#" class="btn-wpp">', f'<a href="{WPP}" target="_blank" rel="noopener" class="btn-wpp">')

    t = t.replace('<a href="#contato"', '<a href="contato.html"')
    t = t.replace('<a href="#contato">', '<a href="contato.html">')

    t = t.replace(
        '<a href="#" style="color:var(--wpp);margin-top:6px;">WhatsApp →</a>',
        f'<a href="{WPP}" target="_blank" rel="noopener" style="color:var(--wpp);margin-top:6px;">WhatsApp →</a>',
    )
    t = t.replace(
        '<a href="#" style="color:var(--wpp);margin-top:8px;">WhatsApp →</a>',
        f'<a href="{WPP}" target="_blank" rel="noopener" style="color:var(--wpp);margin-top:8px;">WhatsApp →</a>',
    )

    t = t.replace(
        '<a href="#">Gestão de Frotas</a>',
        '<a href="gestao-de-frotas.html">Gestão de Frotas</a>',
    )
    t = t.replace('<a href="#">Telemetria</a>', '<a href="telemetria.html">Telemetria</a>')
    t = t.replace(
        '<a href="#">Videotelemetria</a>',
        '<a href="videotelemetria.html">Videotelemetria</a>',
    )
    t = t.replace(
        '<a href="#">Gestão de Risco</a>',
        '<a href="gestao-de-risco.html">Gestão de Risco</a>',
    )

    t = t.replace('<a href="#">Contato</a>', '<a href="contato.html">Contato</a>')

    if path.name == "index.html":
        t = t.replace(
            '<a href="#" class="btn-red">Solicitar Orçamento Gratuito</a>',
            '<a href="contato.html" class="btn-red">Solicitar Orçamento Gratuito</a>',
        )
        t = t.replace(
            '<a href="#" class="btn-ghost">Ver Serviços</a>',
            '<a href="#servicos" class="btn-ghost">Ver Serviços</a>',
        )
        t = t.replace(
            '<a href="#" class="btn-red">Preencher Formulário</a>',
            '<a href="contato.html" class="btn-red">Preencher Formulário</a>',
        )
        t = t.replace(
            '<a href="#" class="btn-red">Quero começar agora</a>',
            '<a href="contato.html" class="btn-red">Quero começar agora</a>',
        )
        t = t.replace(
            "<button class=\"form-submit\">Solicitar Orçamento Gratuito</button>",
            "<a href=\"contato.html\" class=\"form-submit\" role=\"button\">Solicitar Orçamento Gratuito</a>",
        )
        if "id=\"servicos\"" not in t and "services-section" in t:
            t = t.replace(
                '<section class="services-section">',
                '<section class="services-section" id="servicos">',
                1,
            )
        t = t.replace(
            "  .form-submit { width: 100%; background: var(--red); color: white; font-size: 14px; font-weight: 700; padding: 11px; border-radius: 4px; border: none; cursor: pointer; margin-top: 4px; font-family: 'Barlow', sans-serif; }",
            "  a.form-submit { text-decoration: none; display: block; text-align: center; box-sizing: border-box; }\n  .form-submit { width: 100%; background: var(--red); color: white; font-size: 14px; font-weight: 700; padding: 11px; border-radius: 4px; border: none; cursor: pointer; margin-top: 4px; font-family: 'Barlow', sans-serif; }",
            1,
        )

    if t != orig:
        path.write_text(t, encoding="utf-8")
        print("updated", path.name)
    else:
        print("unchanged", path.name)


def main() -> None:
    for p in sorted(ROOT.glob("*.html")):
        if p.name in SKIP:
            continue
        fix_file(p)


if __name__ == "__main__":
    main()
