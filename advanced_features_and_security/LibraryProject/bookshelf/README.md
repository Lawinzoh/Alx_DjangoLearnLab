# Bookshelf App - Permissions and Groups Setup

## Overview
This app uses Django groups and permissions to control access to CRUD operations on the `Book` model. Users are assigned to groups, and each group has specific permissions. Permissions are enforced in views using Django’s `@permission_required` decorator.

---

## Groups

- **Editors**: Can create and edit books.
- **Viewers**: Can only view books.
- **Admins**: Full access (view, create, edit, delete).

---

## Permissions Variables

The following permission variables are used in the setup script:

- `can_view`  → Permission to view books
- `can_create` → Permission to create books
- `can_edit` → Permission to edit books
- `can_delete` → Permission to delete books

---

## Setting Up Groups and Permissions

```python
from django.contrib.auth.models import Group, Permission

# Create groups
editors = Group.objects.create(name="Editors")
viewers = Group.objects.create(name="Viewers")
admins = Group.objects.create(name="Admins")

# Fetch permissions
can_view = Permission.objects.get(codename="can_view")
can_create = Permission.objects.get(codename="can_create")
can_edit = Permission.objects.get(codename="can_edit")
can_delete = Permission.objects.get(codename="can_delete")

# Assign permissions to groups
editors.permissions.add(can_create, can_edit)
viewers.permissions.add(can_view)
admins.permissions.add(can_view, can_create, can_edit, can_delete)