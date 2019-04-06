from active_members.adhesion_api import AdhesionAPI


def update_adhesion_membership(member):
    api = AdhesionAPI()
    adhesion_member = api.get_member_id(member.adhesion_id)
    if adhesion_member is not None:
        member.has_valid_membership = adhesion_member["has_valid_membership"]
        member.save()
        return True
    else:
        return False
