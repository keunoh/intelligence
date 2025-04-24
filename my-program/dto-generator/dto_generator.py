#!/usr/bin/env python3
"""
CLI script: Generate Java VO class from DB column definitions without separators.
Interactive: paste lines where each line is COLUMN_NAME+SQL_TYPE+DESCRIPTION; blank line to finish.
Built EXE with PyInstaller:
  pyinstaller --onefile generate_vo_from_columns.py --name generate_vo
Usage:
  > generate_vo.exe
  Paste lines (no separators), one per line:
    AFFI_SEQint계열사순번
    AFFI_NMvarchar(200)계열사명
    ...
    <blank line>
  ========================================
  Generated VO at: ./vo/ExamplePVO.java
  ========================================
  Generate another? (y/n):
"""
import os
import sys
import random
import re
from datetime import date

# Default settings; modify as needed
DEFAULT_PACKAGE = "vo"
DEFAULT_CLASS_NAME = "ExamplePVO"
DEFAULT_AUTHOR = "김근오"
DEFAULT_DESCRIPTION = "MB예시테이블PVO"

# Map SQL types to Java types
def map_sql_type(sql_type: str) -> str:
    t = sql_type.lower()
    if t.startswith(('varchar', 'char', 'text')):
        return 'String'
    if t in ('int', 'integer', 'tinyint', 'smallint', 'mediumint'):
        return 'Integer'
    if t == 'bigint':
        return 'Long'
    if t in ('decimal', 'numeric', 'float', 'double'):
        return 'BigDecimal'
    if t in ('datetime', 'timestamp'):
        return 'LocalDateTime'
    if t == 'date':
        return 'LocalDate'
    if t in ('bit', 'boolean'):
        return 'Boolean'
    return 'String'

# Convert snake_case to camelCase
def snake_to_camel(name: str) -> str:
    parts = name.lower().split('_')
    return parts[0] + ''.join(p.capitalize() for p in parts[1:])

# Templates
JAVA_TEMPLATE = '''package {package};

import com.bcom.common.vo.AbstractVO;
import lombok.Getter;
import lombok.Setter;
import lombok.ToString;
import io.swagger.v3.oas.annotations.media.Schema;
{extra_imports}
/**
 * @packageName : {package}
 * @fileName : {class_name}.java
 * @author : {author}
 * @date : {date}
 * @description : {description}
 * ==========================================================
 * DATE          AUTHOR          NOTE
 * ==========================================================
 * {date}    {author}            최초 생성
 */
@Getter
@Setter
@ToString
public class {class_name} extends AbstractVO {{
    private static final long serialVersionUID = {serial}L;

{fields}    
}}'''

FIELD_TEMPLATE = '''    /** {comment} */
    @Schema(name = "{field_name}", description = "{comment}", defaultValue = "")
    private {java_type} {field_name};

'''

# Parse lines without separators
def parse_lines(lines):
    entries = []
    # Pattern: COLUMN_NAME (uppercase+digits+_) + TYPE (letters+(digits) optional) + COMMENT
    pattern = re.compile(r'^([A-Z][A-Z0-9_]*)([A-Za-z]+(?:\(\d+(?:,\d+)?\))?)(.+)$')
    for idx, line in enumerate(lines, start=1):
        text = line.strip()
        if not text:
            continue
        m = pattern.match(text)
        if not m:
            print(f"Warning: line {idx} not valid, skipping: '{line}'")
            continue
        col, sql_type, comment = m.groups()
        entries.append((col, sql_type, comment.strip()))
    return entries

# Generate VO class file
def generate_vo():
    print("Paste lines (COLUMN_NAME+TYPE+DESCRIPTION), blank line to finish:")
    raw_lines = []
    while True:
        try:
            line = input()
        except EOFError:
            break
        if not line.strip():
            break
        raw_lines.append(line)
    entries = parse_lines(raw_lines)
    if not entries:
        print("No valid entries. Aborting.")
        return

    # Base imports
    imports = {
        'import com.bcom.common.vo.AbstractVO;',
        'import lombok.Getter;',
        'import lombok.Setter;',
        'import lombok.ToString;',
        'import io.swagger.v3.oas.annotations.media.Schema;'
    }
    fields_str = ''
    for col, sql_type, comment in entries:
        java_type = map_sql_type(sql_type)
        if java_type == 'LocalDateTime':
            imports.add('import java.time.LocalDateTime;')
        if java_type == 'LocalDate':
            imports.add('import java.time.LocalDate;')
        if java_type == 'BigDecimal':
            imports.add('import java.math.BigDecimal;')
        field_name = snake_to_camel(col)
        fields_str += FIELD_TEMPLATE.format(
            comment=comment,
            field_name=field_name,
            java_type=java_type
        )

    extra_imports = '\n'.join(sorted(imports - {
        'import com.bcom.common.vo.AbstractVO;',
        'import lombok.Getter;',
        'import lombok.Setter;',
        'import lombok.ToString;',
        'import io.swagger.v3.oas.annotations.media.Schema;'
    }))

    today = date.today().strftime("%Y-%m-%d")
    serial = random.getrandbits(64)
    content = JAVA_TEMPLATE.format(
        package=DEFAULT_PACKAGE,
        class_name=DEFAULT_CLASS_NAME,
        author=DEFAULT_AUTHOR,
        date=today,
        description=DEFAULT_DESCRIPTION,
        serial=serial,
        fields=fields_str,
        extra_imports=extra_imports
    )

    # Write to file under ./vo/
    out_root = os.getcwd()
    pkg_path = os.path.join(out_root, *DEFAULT_PACKAGE.split('.'))
    os.makedirs(pkg_path, exist_ok=True)
    file_path = os.path.join(pkg_path, DEFAULT_CLASS_NAME + '.java')
    with open(file_path, 'w', encoding='utf-8') as f:
        f.write(content)

    print("=" * 40)
    print(f"Generated VO at: {file_path}")
    print("=" * 40)

# Main loop
def main():
    try:
        while True:
            generate_vo()
            cont = input("Generate another? (y/n): ").strip().lower()
            if cont != 'y':
                print("Exiting.")
                break
    except KeyboardInterrupt:
        print("\nInterrupted. Exiting.")
    except Exception as e:
        print(f"Error: {e}", file=sys.stderr)

if __name__ == '__main__':
    main()
