# 📚 LibraryProject – Permissions & Groups Setup

## ✅ Permissions

The app uses Django's built-in permissions system.

| Permission    | Description              | Used In View        |
|---------------|--------------------------|----------------------|
| can_create    | Allows adding new books  | add_book            |
| can_edit      | Allows editing books     | edit_book           |
| can_delete    | Allows deleting books    | delete_book         |

These are defined in the `Book` model under `class Meta: permissions`.

---

## ✅ Roles & Groups

You can manage permissions via **Django Admin → Groups**:

### 1. Admin
- Has all permissions (`is_superuser=True` automatically grants all).

### 2. Librarian
- Permissions: `can_create`, `can_edit`

### 3. Member
- No special permissions, can only view books.

---

## ✅ How to Assign Permissions
1. Log in to the Django Admin (`/admin`).
2. Go to **Groups** or **Users**.
3. Add the required permissions:
   - **Example for Librarian:** Assign `can_create` and `can_edit` only.
   - **Example for Member:** No permissions needed.

---

## ✅ Enforcing Permissions in Views

Views are protected using Django decorators:

```python
@permission_required('bookshelf.can_create', raise_exception=True)
def add_book(request): ...

@permission_required('bookshelf.can_edit', raise_exception=True)
def edit_book(request, pk): ...

@permission_required('bookshelf.can_delete', raise_exception=True)
def delete_book(request, pk): ...
