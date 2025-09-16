# Varustevahti

## What the project does
The application is a smart inventory tool for tracking personal or shared equipment. Users can add items by taking a photo or selecting from the gallery, fill in details like name, category, location, and attach receipts. Groups make it possible for families or teams to manage shared items together, while the My Items page lets users browse, search, and filter their own gear.

## Why the project is usefull
The project is usefull for people with lots of ice hockey gear. For example hockey families, who have many size of hockey gear and as children grow up, it is easy to keep track what you allready have. 

## Application architecture

```mermaid
flowchart TB
    subgraph RN ["React Native App (Expo)"]
      UI["User interface"]
      SQ["Local History (Expo SQLite)"]
      RQ["React Query (Axios/Fetch)"]
      CAM["Camera / Image Picker"]
      UI --> CAM
      UI --> RQ
      UI --> SQ
    end

    subgraph API ["Backend (FastAPI, Python)"]
      INFER["ML Inference (PyTorch)"]
      DB[("DB: SQLite")]
      FS[("Image Storage")]
    end

    CAM -->|image upload| RQ
    RQ -->|HTTPS POST| API
    API --> FS
    API --> INFER
    API --> DB
    API -->|JSON results| RQ
    RQ --> SQ
```


## Used Technologies

### Frontend
- **React Native, Expo** – Framework building the mobile app.
- **React Navigation** – Navigation between screens.
- **React Native Paper or NativeWind** – to style the mobile app.
- **Axios** – For making HTTP requests to the backend API.
- **Expo SQLite** - For local history storage inside the app.

### Backend
- **FastAPI (Python)** – backend API that receives images and returns recognition results. 
- **SQLite** – database for storing items and recognition history.

### Machine Learning
- **PyTorch** – to load and run the image recognition model.

### Tools
- **Docker / Docker Compose** – to setup backend, machine learning and frontend all in one. 
- **GitHub** – for version control and collaboration.
- **pytest / Jest** – for testing backend and frontend.

## Flow of actions

```mermaid
sequenceDiagram
  participant U as User
  participant App as Expo App
  participant API as FastAPI
  participant ML as PyTorch
  participant DB as Database
  participant FS as File Storage

  U->>App: Take/choose photo
  App->>API: POST /images
  API->>FS: Save image
  API->>ML: Run inference
  ML-->>API: Labels + confidence
  API->>DB: Save metadata + results
  API-->>App: JSON results
  App->>App: Update UI & cache locally

```
## Mockup pages (made in Google Stitch)
| First page | Add item page | Groups page |Inside of a group |
|:-----------|:------------:|------------:|------------:|
| <img src="my_items.png" alt="first page" width="300"/>      | <img src="add_item.png" alt="add item page" width="300"/>       | <img src="groups.png" alt="my groups page" width="300"/>|<img src="Soccer_team_group.png" alt="group: soccer teams items page" width="300"/>       |

Colors used

Background color #F8FBFA<br>
Text color #52946B <br>
Text color Selected #0D1A12 <br>
Fill color #EAF2EC <br>
Button color bright green #71DE86 <br>




