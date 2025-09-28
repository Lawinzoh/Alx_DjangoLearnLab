
This documentation details the strategy used for unit testing the Django REST Framework (DRF) Book API, outlines the implemented test cases, and provides instructions for execution and result interpretation.

1. Testing Strategy and Approach
The testing strategy is built around Django's standard unit test framework, utilizing DRF's APITestCase and APIClient classes to accurately simulate HTTP requests to the endpoints.

Key Focus Areas:
Area	Goal	Test Class
CRUD Operations	Verify that standard RESTful operations (Create, Read, Update, Delete) function correctly. Check for proper saving, retrieval, and deletion of data, and confirm correct status codes (e.g., 200, 201, 204).	PrivateBookApiTests
Permissions	Ensure the IsAuthenticatedOrReadOnly permission class is correctly enforced. Anonymous users must be able to read (GET) but must be denied write access (POST, PUT, DELETE) with a 403 Forbidden.	PublicBookApiTests
Advanced Queries	Validate that the implemented filters.SearchFilter, django_filters.DjangoFilterBackend, and filters.OrderingFilter process query parameters correctly and return the expected filtered, searched, or sorted data.	PrivateBookApiTests
Data Integrity	Test cases include scenarios for invalid data (e.g., future publication year) to ensure the serializer returns a 400 Bad Request with meaningful error messages.	PrivateBookApiTests

Export to Sheets
2. Individual Test Cases Summary
The tests are organized into two classes based on authentication status:

A. PublicBookApiTests (Anonymous/Read-Only)
Test Case	Method/Endpoint	Expectation	Status Code
test_retrieve_books_list_success	GET /books/	Successfully retrieve all books.	200 OK
test_retrieve_book_detail_success	GET /books/<id>/	Successfully retrieve a single book detail.	200 OK
test_create_book_denied_anonymous	POST /books/create/	Creation must be denied.	403 Forbidden
test_update_book_denied_anonymous	PUT/PATCH /books/<id>/update/	Update must be denied.	403 Forbidden
test_delete_book_denied_anonymous	DELETE /books/<id>/delete/	Deletion must be denied.	403 Forbidden

Export to Sheets
B. PrivateBookApiTests (Authenticated/Full Access)
Test Case	Method/Endpoint	Expectation	Status Code
test_create_book_success	POST /books/create/	Successfully create a book and verify database count.	201 Created
test_full_update_book_success	PUT /books/<id>/update/	Fully update a book's fields.	200 OK
test_partial_update_book_success	PATCH /books/<id>/update/	Partially update a book's fields.	200 OK
test_delete_book_success	DELETE /books/<id>/delete/	Successfully remove the book from the database.	204 No Content
test_filter_by_publication_year_gte	GET /books/?publication_year_gte=2010	Returns only books published in 2010 or later.	200 OK
test_search_by_author_name	GET /books/?search=SciFi	Returns only books matching the author's name.	200 OK
test_ordering_by_publication_year_desc	GET /books/?ordering=-publication_year	Returns books sorted from newest to oldest.	200 OK
test_combination_query	GET /books/?year_gte=2000&ordering=title	Returns filtered data, then ensures correct ordering.	200 OK

Export to Sheets
3. Guidelines for Running Tests
The tests are executed using Django's test runner, which ensures the project environment and settings are properly loaded.

A. Execution Command
Ensure you are in the directory containing manage.py and run the following command to execute all tests within the api application:

Bash

python manage.py test api
B. Interpreting Test Results
The output provides a clear summary of the test run:

Status	Meaning	Action Required
OK	All tests passed successfully. The code behaves as expected.	None. Proceed to the next development step.
FAIL	An assertion within a test case failed (e.g., asserting a status code of 200, but receiving 400).	Review the specific test logic and the corresponding view/serializer code.
ERROR	A Python exception occurred during test execution (e.g., TemplateDoesNotExist, AttributeError, NoReverseMatch).	This indicates a structural problem, often in the api/urls.py or api/views.py, that needs immediate fixing before the tests can reliably check functionality.