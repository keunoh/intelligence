def to_camel_case(snake_str):
    parts = snake_str.lower().split('_')
    return parts[0] + ''.join(word.capitalize() for word in parts[1:])

def generate_sql(dml_type, table_name, columns_input):
    columns = [col.strip() for col in columns_input.split(',')] if columns_input else []
    tab = "    "           # 4칸 스페이스
    first_tab = tab * 2    # 8칸
    deep_tab = tab * 3     # 12칸
    deeper_tab = tab * 3 + "  "  # 14칸

    comment_insert = "/* com.myApp.homepage.business.mapper.FileMapper.createFile */"
    comment_update = "/* com.myApp.homepage.business.mapper.FileMapper.updateFile */"
    comment_select = "/* com.myApp.homepage.business.mapper.FileMapper.selectFile */"
    comment_delete = "/* com.myApp.homepage.business.mapper.FileMapper.deleteFile */"
    
    if dml_type == "C":
        column_lines = ("\n".join(
            (f"{deeper_tab}{col}" if i == 0 else f"{deep_tab}, {col}") for i, col in enumerate(columns)
        ))
        values_lines = ("\n".join(
            (f"{deeper_tab}#{{{to_camel_case(col)}}}" if i == 0 else f"{deep_tab}, #{{{to_camel_case(col)}}}") for i, col in enumerate(columns)
        ))

        return f"""INSERT INTO {comment_insert}
{tab}{table_name} 
{first_tab}(
{column_lines}
{first_tab}) VALUES (
{values_lines}
{first_tab});
"""

    elif dml_type == "U":
        max_len = max(len(col) for col in columns)
        set_clause = ("\n".join(
            (f"{deeper_tab}{col.ljust(max_len)} = #{{{to_camel_case(col)}}}" if i == 0 else f"{deep_tab}, {col.ljust(max_len)} = #{{{to_camel_case(col)}}}") for i, col in enumerate(columns)
        ))

        return f"""UPDATE {comment_update}
{tab}{table_name} 
{first_tab}  SET
{set_clause}
{first_tab}WHERE /* condition */;
"""

    elif dml_type == "R":
        first_indent = "       "  # 7칸 (첫 번째 컬럼)
        normal_indent = "     "   # 5칸 (두 번째 이후 컬럼)
        column_lines = ("\n".join(
            (f"{first_indent}{col}" if i == 0 else f"{normal_indent}, {col}") for i, col in enumerate(columns)
        ))

        return f"""SELECT {comment_select}
{column_lines}
  FROM {table_name} 
 WHERE /* condition */;
"""

    elif dml_type == "D":
        return f"""DELETE {comment_delete}
  FROM {table_name} 
 WHERE /* condition */;
"""

    else:
        return "Unsupported DML type. Only C, R, U, D are supported."

if __name__ == "__main__":
    while True:
        print("=" * 50)
        table_name = input("Enter table name: ")

        while True:
            dml_type = input("Enter DML type (C=Create, R=Read, U=Update, D=Delete): ").strip().upper()
            if dml_type in ["C", "R", "U", "D"]:
                break
            else:
                print("Invalid DML type. Please enter only C, R, U, or D.")

        columns_input = ""
        if dml_type in ["C", "R", "U"]:
            columns_input = input("Enter column names (comma-separated): ")

        result = generate_sql(dml_type, table_name, columns_input)
        print("\n" + "=" * 80)
        print("Generated SQL")
        print("=" * 80)
        print(result)
        print("=" * 80 + "\n")

        cont = input("Do you want to generate another SQL? (y/n): ")
        if cont.lower() != 'y':
            print("\nExiting...")
            break
