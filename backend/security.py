USERS = {
    "alice": {
        "groups": [
            "Employees"
        ]
    },

    "bob": {
        "groups": [
            "Employees",
            "HR"
        ]
    },

    "carol": {
        "groups": [
            "Employees",
            "ProjectAlpha"
        ]
    },

    "david": {
        "groups": [
            "Employees",
            "Finance"
        ]
    }
}

def get_user_groups(user_id: str) -> list[str]:
    user = USERS.get(user_id)
    if not user:
        return []
    return user["groups"]


def build_security_filter(user_groups: list[str]) -> str:
    if not user_groups:
        # No groups = no access
        return "false"

    groups = ",".join(user_groups)

    return (
        "group_ids/any("
        f"g:search.in(g, '{groups}', ',')"
        ")"
    )