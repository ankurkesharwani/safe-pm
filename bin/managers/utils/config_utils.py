def update_config(file_path, db, password_hash, salt):
    updated_lines = []
    with open(file_path, 'r') as file:
        lines = file.readlines()
        for line in lines:
            if not line.startswith(db):
                updated_lines.append(line.strip())

        file.close()
    updated_lines.append(f"{db}:{password_hash},{salt}")
    with open(file_path, 'w') as file:
        for line in updated_lines:
            file.write(line + "\n")
        file.close()


def get_password_hash_and_salt(file_path: str, db: str) -> (str, str):
    selected_line = None
    with open(file_path, 'r') as file:
        lines = file.readlines()
        for line in lines:
            if line.startswith(db):
                selected_line = line
                break
        file.close()

    components = selected_line.strip().split(":")[1].split(",")
    return components[0], components[1]
