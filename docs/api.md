# Varustevahti API

local url: [http://127.0.0.1:8000](http://127.0.0.1:8000)

Rahti url: [https://backend-git-varustevahti.2.rahtiapp.fi](https://backend-git-varustevahti.2.rahtiapp.fi)

Swagger UI´s interactive docs: [https://backend-git-varustevahti.2.rahtiapp.fi/docs](https://backend-git-varustevahti.2.rahtiapp.fi/docs)

Information taken from: [https://backend-git-varustevahti.2.rahtiapp.fi/openapi.json](https://backend-git-varustevahti.2.rahtiapp.fi/openapi.json)

---

## Items

### POST /items/auto

Create a new item automatically from an uploaded image, used with camera or taken from gallery.

- **Request body**: multipart/form-data

Fields:

| Field    | Type    | Required | Description                      |
|----------|---------|----------|----------------------------------|
| `file`   | binary  | yes      | Image file of the item          |
| `name`   | string  | yes      | Item name                       |
| `location` | string | no       | Where the item is        |
| `owner`  | string  | no       | Owner of the item               |

- **Response 200**: Succesful Response
- **Response 422**: Validation Error

---

### GET /items

Get all items.

- **Response 200**: Successful Response
- **Response 422**: Validation Error

### POST /items/

Create a new item through endpoint.

- **Request body**: application/json from ItemBase

Required fields in ItemBase:

- name (string)  
- location (string)  
- desc (string)  
- owner (string)  
- category_id (integer)  
- group_id (integer)

Optional:

- image (string)  
- size (string)  
- on_market_place (integer, default 0)  
- price (number)

- **Response 200**: Successful Response
- **Response 422**: Validation Error

---

### GET /items/{item_id}

Get an item with it´s item_id.

- **Path parameter**: item_id
- **Response 200**: Successful Response
- **Response 422**: Validation Error

### PUT /items/{item_id}

Update an item.

- **Path parameter**: item_id
- **Request body**: application/json, all fields are optional
- **Response 200**: Successful Response
- **Response 422**: Validation Error

### DELETE /items/{item_id}

Delete an item.

- **Path parameter**: item_id
- **Response 200**: Successful Response
- **Response 422**: Validation Error

---

### GET /items/category/{category_id}

Get all items in one category.

- **Path parameter**: category_id
- **Response 200**: Successful Response
- **Response 422**: Validation Error

---

### GET /items/group/{group_id}

Get all items of one group.

- **Path parameter**: group_id
- **Response 200**: Successful Response
- **Response 422**: Validation Error

---

### GET /items/market

Get all items that are posted to marketplace.

- **Response 200**: Successful Response
- **Response 422**: Validation Error

---

### GET /items/recent?limit={limit}

Get most recent items.

- **Query parameters**:
  - limit (integer, optional, default 10)
- **Response 200**: Successful Response
- **Response 422**: Validation Error

---

### POST /items/{item_id}/post_to_market

Post an item to the marketplace.

- **Path parameter**:`item_id
- **Request body**: application/x-www-form-urlencoded

Fields:

| Field   | Type   | Required |
|---------|--------|----------|
| price | number | yes      |

- **Response 200**: Successful Response
- **Response 422**: Validation Error

---

## Categories

### GET /categories

List all categories.

- **Response 200**: Successful Response
- **Response 422**: Validation Error

### POST /categories

Create a new category.

- **Request body**: application/json from CategoryBase
  - Required: name (string)

- **Response 200**: Successful Response
- **Response 422**: Validation Error

---

## Groups

### GET /groups

List all groups.

- **Response 200**: Successful Response
- **Response 422**: Validation Error

### POST /groups

Create a new group.

- **Request body**:`application/json from GroupBase  
  - Required: name (string)

- **Response 200**: Successful Response
- **Response 422**: Validation Error
