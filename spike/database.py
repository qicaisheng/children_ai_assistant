chat_history = []
summary = ""
saved_roles_templates = {}

def get_saved_roles():
    saved_roles = list(saved_roles_templates.keys())
    print(saved_roles)
    return saved_roles


get_saved_roles()