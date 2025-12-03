data = [
    ("A", "Клапан открыт"),
    ("B", "Клапан закрыт"),
    ("V1, V2", "Входные клапаны регенерации"),
    ("V5", "Обходной клапан регенерации"),
    ("V6, V7", "Входные клапаны охладителя"),
    ("V8, V9", "Выходные клапаны охладителя"),
    ("V10, V11", "Клапаны воздуха регенерации"),
    ("V12", "Клапан регенерации 1"),
    ("V13", "Клапан регенерации 2"),
    ("V14", "Предохранительные клапаны регенерации (опция)"),
    ("V21", "Воздушный впускной клапан охладителя 1"),
    ("V22", "Ручной клапан"),
    ("TT02", "Датчик температуры на входе регенерационного охладителя"),
    ("TT05", "Датчик температуры на входе охладителя"),
    ("TT07", "Датчик температуры в нижней части сосуда B"),
    ("TT08", "Датчик температуры в нижней части сосуда A"),
    ("TT09", "Фильтр управляющего воздуха"),
    ("PT02", "Регулятор давления"),
    ("AI", "Электромагнитный клапан 5/2 с ограничителем расхода"),
    ("AT22", "Ресивер управляющего воздуха (только для 4150/5000)"),
    ("PT01", "Давление на входе охладителя"),
    ("PT06", "Давление на выходе охладителя"),
    ("PDS1", "Защитный фильтр"),
    ("PD02", "Выходной фильтр"),
    ("PT03", "Давление в сосуде A"),
    ("PT04", "Давление в сосуде B"),
    ("CV", "Охладитель"),
    ("HE", "Теплообменник"),
    ("SSS", "Водоотделитель"),
    ("CL", "Гаситель пульсаций"),
    ("VSD", "Компрессор с частотным приводом"),
    ("HC", "Контроль влажности"),
    ("PD", "Точка росы под давлением"),
    ("IP", "Щит приборов"),
    ("TT", "Датчик температуры"),
    ("PIC", "Индикатор давления"),
    ("PDSI", "Индикатор точки росы"),
    ("W1, W2", "Водоотделители (только для 4150/5000)"),
]

TITLE = "Перевод обозначений"
HEADER = "Обозначение | Перевод"

# PDF page settings
PAGE_WIDTH = 595
PAGE_HEIGHT = 842
MARGIN_LEFT = 50
MARGIN_TOP = 60
LEADING = 18
FONT_SIZE = 12
FONT = "/F1"


def escape_text(text: str) -> str:
    return text.replace("\\", "\\\\").replace("(", "\\(").replace(")", "\\)")


def build_text_lines():
    lines = [TITLE, "", HEADER, ""]
    for key, value in data:
        lines.append(f"{key} | {value}")
    return lines


def generate_pdf(filename: str):
    lines = build_text_lines()
    # Prepare content stream
    y_start = PAGE_HEIGHT - MARGIN_TOP
    # We'll use T* with leading to step lines
    content_lines = ["BT", f"{FONT} {FONT_SIZE} Tf", f"{LEADING} TL", f"{MARGIN_LEFT} {y_start} Td"]
    for idx, line in enumerate(lines):
        if idx == 0:
            content_lines.append(f"({escape_text(line)}) Tj")
        else:
            content_lines.append("T*")
            content_lines.append(f"({escape_text(line)}) Tj")
    content_lines.append("ET")
    content = "\n".join(content_lines) + "\n"
    content_bytes = content.encode("utf-8")

    objects = []
    # 1 Catalog
    objects.append("<< /Type /Catalog /Pages 2 0 R >>")
    # 2 Pages
    objects.append("<< /Type /Pages /Kids [3 0 R] /Count 1 >>")
    # 3 Page
    objects.append(
        "<< /Type /Page /Parent 2 0 R /MediaBox [0 0 {0} {1}] "
        "/Contents 4 0 R /Resources << /Font << /F1 5 0 R >> >> >>".format(
            PAGE_WIDTH, PAGE_HEIGHT
        )
    )
    # 4 Contents
    objects.append(
        "<< /Length {length} >>\nstream\n{content}endstream".format(
            length=len(content_bytes), content=content
        )
    )
    # 5 Font
    objects.append("<< /Type /Font /Subtype /Type1 /BaseFont /Helvetica >>")

    xref_entries = ["0000000000 65535 f "]
    output = ["%PDF-1.4\n"]
    for i, obj in enumerate(objects, start=1):
        offset = sum(len(part.encode("utf-8")) for part in output)
        xref_entries.append(f"{offset:010d} 00000 n ")
        output.append(f"{i} 0 obj\n{obj}\nendobj\n")

    xref_offset = sum(len(part.encode("utf-8")) for part in output)
    xref_table = ["xref\n", f"0 {len(objects)+1}\n"]
    xref_table.extend(entry + "\n" for entry in xref_entries)
    xref_table.append("trailer\n")
    xref_table.append(f"<< /Size {len(objects)+1} /Root 1 0 R >>\n")
    xref_table.append("startxref\n")
    xref_table.append(f"{xref_offset}\n")
    xref_table.append("%%EOF\n")

    with open(filename, "wb") as f:
        for part in output:
            f.write(part.encode("utf-8"))
        for part in xref_table:
            f.write(part.encode("utf-8"))


if __name__ == "__main__":
    generate_pdf("translation_table.pdf")
