# Varustevahti

* Nico Pekkanen: Machine learning
* Timo Lampinen: User interface
* Daniel Thagapsov: Backend
* Jeremias Pajari: Development operations

---
<details>
  <summary><strong>About the Varustevahti</strong></summary> 
  
<details>
  
  <summary><strong>What the project does</strong></summary>

  The application is a smart inventory tool designed for tracking personal or shared equipment.
  Users can add items by taking a photo or selecting from the gallery, and fill in details like
  name, category and location. Groups make it possible for families or teams to manage shared items
  together, while the My Items page lets users browse, search, and filter their own gear.

  The system includes a React Native (Expo) mobile frontend and a FastAPI backend deployed on CSC Rahti.
  The frontend is not deployed to App/Play stores due to cost, but can be fully used via Expo Go during development.
  User authentication is implemented with Clerk.
</details>

<details>
  <summary><strong>What is it?</strong></summary>
  
  Varustevahti is a mobile inventory tool for storing and organizing sports equipment.
  Users can add items by taking photos, track what they own, and manage group-based inventories
  such as family items or ice-hockey team gear.
</details>

<details>
  <summary><strong>How to use</strong></summary>
  
  You have few screen for different purposes:
  My Items: 
  You can search from your items, just by typing few letters.
  in this screen you see your few of your items. 
  Your categories, in where your gear belongs. 
  Recent items show the latest items you have put in or changed the info.
  You can also check your stuff by locations.
  All the headers also open different screens.

  If you tap any single item. It is opened in new screen where you can change the details of the item. 
  Here you can also set price and put the item on market. Or even delete an item.

  Add Item:
  In this screen you add items to your inventory. 
  Adding photo without typing the name first sends the image to backend for AI identification. 
  You get suggested name and gategory back. After this you can add other info if you want, including
  location, description, size etc. The only mandatory info is name.

  Market:
  You can see all the items people have put on market. You see the name and price at this time.
  You can search from market and if you want to check details just tap on the item name.
  This open item in new window. Unfotunately you can't see picture of the item. 
  In the future you should be able to send message to the owner by pushing a button, but this feature is still
  unavailable. It requires backend support for authenticaiting users and securely giving away user data.

  Locations:
  In here you can add location for your gear.

  Profile:
  This includes trash can - just in case you want to see what you have not allready deleted locally.
  You can also sync with backend just by pushing a button if you want.

  Groups: <Feature not yet develop>
  Groups is not yet developed. Groups needs a good backend support which does not exist. 
  Groups would able many people to track same stuff. For example football teams to see how many balls,
  cones, jerseys etc they have. Or a scout group to follow who has the big tent now etc
  
</details>
</details>


<details>
  <summary><strong>Frontend (React Native + Expo)</strong></summary>

  Frontend repository: 
  https://github.com/Varustevahti/Frontend

  <details>
    <summary><strong>Used Technologies</strong></summary>

    - React Native, Expo – Framework for the mobile app  
      https://docs.expo.dev/

    - React Navigation – Page navigation  
      https://reactnavigation.org/

    - React Native Paper – UI components  
      https://callstack.github.io/react-native-paper/

    - Axios – HTTP requests  
      https://axios-http.com/docs/intro

    - Expo SQLite – Local history storage  
      https://docs.expo.dev/versions/latest/sdk/sqlite/
  </details>

  <details>
    <summary><strong>Mockup pages (Google Stitch) & color palette</strong></summary>

    | First page | Add item page | Groups page | Inside group |
    |------------|--------------:|-------------:|-------------:|
    | <img src="Näyttökuva 2025-08-24 kello 19.49.11.png" width="300"/> | <img src="Näyttökuva 2025-08-24 kello 19.48.30.png" width="300"/> | <img src="Näyttökuva 2025-08-24 kello 19.48.50.png" width="300"/> | <img src="Näyttökuva 2025-08-24 kello 19.48.57.png" width="300"/> |

    Color palette

    - Background: `#F8FBFA`  
    - Text: `#52946B`  
    - Selected Text: `#0D1A12`  
    - Fill: `#EAF2EC`  
    - Button: `#71DE86`  
  </details>

  <details>
    <summary><strong>Dependencies</strong></summary>

    react-native-paper  
    expo-image-picker  
    react-navigation  
    @react-navigation/native  
    @react-navigation/bottom-tabs  
    @react-navigation/native-stack  
    react-native-screens  
    react-native-safe-area-context  
    react-native-gesture-handler  
    react-native-reanimated  
    expo/vector-icons  
    expo-sqlite  
  </details>

</details>



<details>
 <summary><strong>Backend (FastAPI, Python)</strong></summary>



<details>
    <summary><strong>Architecture diagrams</strong></summary>
  
Application architecture:
  
```mermaid
flowchart TB
    subgraph RN ["React Native App (Expo)"]
      UI["User interface"]
      SQ["Local History (Expo SQLite)"]
      RQ["React Query (Axios)"]
      CAM["Camera / Image Picker"]
      UI --> CAM
      UI --> RQ
      UI --> SQ
    end

    subgraph API ["Backend (FastAPI, Python)"]
      INFER["Machine learning Inference (PyTorch)"]
      DB[("Database: SQLite")]
    end

    CAM -->|image upload| RQ
    RQ -->|HTTPS POST| API
    API --> INFER
    API --> DB
    API -->|JSON results| RQ
    RQ --> SQ
``````````

Sequence diagram:

  ```mermaid
sequenceDiagram
    autonumber
    participant U as User
    participant FE as Expo Frontend (Mobile)
    participant BE as FastAPI Backend (Rahti)
    participant AI as AI_Model (torch)
    participant DB as SQLite /workspace/varustevahti.db

    %% --- Normal CRUD ---
    U ->> FE: User opens the application
    FE ->> BE: GET /items/
    BE ->> DB: Get all items
    DB -->> BE: Item list
    BE -->> FE: 200 OK + JSON
    FE -->> U: Show list

    %% --- Add new item ---
    U ->> FE: Fill item information
    FE ->> BE: POST /items/
    BE ->> DB: Add new item
    DB -->> BE: OK
    BE -->> FE: 200 OK

    %% --- recognition (items/auto) ---
    U ->> FE: Pick photo (camera / gallery)
    FE ->> BE: POST /items/auto

    BE ->> AI: Activate Ai-model
    AI ->> AI: Performs model inference
    AI -->> BE: Prediction (category, gear-type)

    BE ->> DB: Saves automaticly created info
    DB -->> BE: OK
    BE -->> FE: 200 OK + predicted data

    FE -->> U: Shows automaticly recognized item
``````````````````````
</details>


<details>
<summary><strong>API documentation</strong></summary>


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


</details>
 <details>
 <summary><strong>Used technologies</strong></summary>

- FastAPI (Python) – backend API that receives images and returns recognition results.
  
  (Documentation: https://fastapi.tiangolo.com/)
  
- SQLite – database for storing items and recognition history.
  
  (Documentation: https://sqlite.org/docs.html)

</details>
<details>
<summary><strong>Machine Learning</strong></summary>

- PyTorch – to load and run the image recognition model.
  
  (Documentation: https://docs.pytorch.org/tutorials/index.html)

</details>
<details>
<summary><strong>Tools</strong></summary>

- Docker – to setup backend, machine learning and frontend all in one.
  
  (Documentation: https://docs.docker.com/)
  
- GitHub – for version control and collaboration.
  
  (Documentation: https://docs.github.com/en)
  
- CSC Rahti - Deployment
  
  (Documentation: https://docs.csc.fi/cloud/rahti/)

</details>
</details>

<details>
 <summary><strong>If you want authentication</strong></summary>
  
You have to create .env file, and add your Clerk credentials to it.
Example:

  
CLERK_SECRET_KEY=YourOwnSecretKey
CLERK_ISSUER=YourOWnClerkIssuer
CLERK_JWKS_URL=YourOwnJWKSURL

</details>

<details>
<summary><strong>Cybersecurity</strong></summary>
Our user interface is secured with Clerk´s interface. But it doesnt operate on our backend, which makes it a huge security risk. We have taken this under our consideration and we have implemented several backend security mechanisms using FastAPI and SQLAlchemy´s ORM:
  - Every request to API is validated using Pydantic models, ensuring correct data types and preventing unexpected input        from reaching the database
  - Internal errors are not returned to client. FastAPI returns generic error messages while detailed exceptions are logged     else where, preventing possible leakage of sensitive information.
  - All database operations use SQLAlchemy ORM query builder instead of raw SQL strings. This ORM layer ensures that user-      controlled data is allways parametrized, eliminating SQL-injection vulnerabilities.
Clerks user_id can be connected to our owner_id, then each user can access, only their own data, which could have increased our cybersecurity alot.
  
Because we didnt deploy our app for customers to use, we left Clerk´s security policies such as two-step verification, email, username & password correct inputs and other validations unconfigurated, for developers to do their work without unnecessary obstacles. 

Otherwise we have securely kept our .env credentials away from public and we have no hardcoded passwords or other critical information on our codebase
</details>

---

### ⚠️ Security concerns

**Do not store any sensitive or valuable information in Rahti at this time!**

- The database currently **lacks established cybersecurity protections**.
- There is **no authentication, authorization, or data validation** in place.
- The database is **fully open and accessible to anyone**.

A more detailed security description will be provided on **24.11.2025**.

---

### Cloning project:
git clone https://github.com/Varustevahti/Frontend.git

cd Frontend

### Install Expo environment
```bash
npx expo install
```
### Install dependencies
#### Expo
```bash
npx expo install react-native-paper expo-image-picker @react-navigation/native @react-navigation/bottom-tabs @react-navigation/native-stack @react-native-picker/picker react-native-safe-area-context react-native-screens @expo/vector-icons react-native-gesture-handler react-native-reanimated react-native-get-random-values expo-sqlite
```
#### NPM
```bash
npm install @react-navigation/native-stack @react-navigation/bottom-tabs
```
---

### To stars the project 
```bash
npx expo start

with

iOS-emulator
npx expo run:ios

Or

Android-emulator
npx expo run:android

Or

scan the QR code using Expo Go
```

---

## Running backend locally
1. Clone the repository
   git clone https://github.com/Varustevahti/Backend.git
   
   cd Backend

3. Create a virtual environment
**Windows**
```bash
python -m venv venv
```

**MacOS/Linux**
```bash
python3 -m venv venv
```

3. Activate the virtual environment

**Windows**
```bash
venv\Scripts\Activate
```

**MacOS/Linux**
```bash
source venv/bin/activate
```

4. Install the requirements into the virtual environment

```bash
pip install -r requirements.txt
```

5. Run the application
```bash
uvicorn app.main:app --reload
```

6. Testing can be performed using the generated URL
```bash
http://127.0.0.1:8000/docs
```
---

## Docker instructions
### Build: 
docker build -t varustevahti-backend .
### Run:
docker run -p 8080:8000 varustevahti-backend


