# Book Management API

This project implements a fully functional **CRUD (Create, Retrieve, Update, Delete)** API for the `Book` resource using Django REST Framework (DRF) Generic Views. The API is designed for efficiency and secured using DRF's built-in permission system.

---

## 📚 API Endpoints Overview

The following table summarizes the endpoints, their operations, and the required permission levels.

| Endpoint | HTTP Method | Operation | View Class | Permissions |
| :--- | :--- | :--- | :--- | :--- |
| `/api/books/` | **GET** | Retrieve List of Books | `BookListCreateAPIView` | **PUBLIC** (Read-Only) |
| `/api/books/` | **POST** | Create New Book | `BookListCreateAPIView` | **AUTHENTICATED** |
| `/api/books/<pk>/` | **GET** | Retrieve Single Book Detail | `BookRetrieveUpdateDestroyAPIView` | **PUBLIC** (Read-Only) |
| `/api/books/<pk>/` | **PUT/PATCH** | Update Existing Book | `BookRetrieveUpdateDestroyAPIView` | **AUTHENTICATED** |
| `/api/books/<pk>/` | **DELETE** | Delete Book | `BookRetrieveUpdateDestroyAPIView` | **AUTHENTICATED** |

---

## 🛠️ View Configuration and Customizations

The API uses two generic view classes to manage all CRUD operations efficiently.

### 1. `BookListCreateAPIView` (List and Create)

This view handles collection-level operations (`GET` and `POST`).

| Setting/Hook | Implementation | Purpose |
| :--- | :--- | :--- |
| **`serializer_class`** | `BookSerializer` | Utilizes the serializer for automatic data validation (e.g., preventing future publication years) and data structure mapping. |
| **`permission_classes`** | `[IsAuthenticatedOrReadOnly]` | **Security Enforcement:** Allows anonymous users to perform **read** (`GET`) operations but restricts the **creation** (`POST`) of new books to logged-in users only. |
| **`perform_create()`** | Overridden Hook | Used to execute custom logic (e.g., logging or setting non-exposed fields) immediately prior to saving a new Book instance. |

### 2. `BookRetrieveUpdateDestroyAPIView` (Detail, Update, and Delete)

This view handles instance-level operations (`GET`, `PUT/PATCH`, and `DELETE`) using the primary key (`pk`).

| Setting/Hook | Implementation | Purpose |
| :--- | :--- | :--- |
| **`serializer_class`** | `BookSerializer` | Ensures data is correctly validated before modification or retrieval. |
| **`permission_classes`** | `[IsAuthenticatedOrReadOnly]` | **Security Enforcement:** Allows anonymous users to **read** (`GET`) book details but restricts all **write** operations (`PUT`, `PATCH`, `DELETE`) to authenticated users. |
| **`perform_update()`** | Overridden Hook | Used to execute custom logic (e.g., auditing changes) immediately prior to saving the updated Book instance. |

---

## 🔑 Serializer Details

The `BookSerializer` and `AuthorSerializer` are configured to handle the many-to-one relationship between Book and Author efficiently, avoiding circular dependencies and ensuring RESTful communication:

* **`Author` Field:** In the `BookSerializer`, the relationship is exposed via two fields:
    * `author`: A **read-only** nested field that returns the full Author details on `GET` requests.
    * `author_id`: A **write-only** field that accepts the Author's primary key (`ID`) for `POST`, `PUT`, and `PATCH` requests, simplifying data submission.

* **Custom Validation:** The `BookSerializer` includes a `validate_publication_year` method to ensure the entered year is not set in the future.

---

## 🛡️ Testing and Verification

Permissions are confirmed by the following behavior:

* **Anonymous Users:** Can successfully perform **GET** requests to list or view details. Any attempt to use $\text{POST}$, $\text{PUT}$, $\text{PATCH}$, or $\text{DELETE}$ will result in a **403 Forbidden** response.
* **Authenticated Users:** Have full $\text{CRUD}$ access across all endpoints.