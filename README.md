# Varustevahti
Repository for back end

## What the project does
The application is a smart inventory tool for tracking personal or shared equipment. Users can add items by taking a photo or selecting from the gallery, fill in details like name, category, location, and attach receipts. Groups make it possible for families or teams to manage shared items together, while the My Items page lets users browse, search, and filter their own gear.

## Why the project is usefull
The project is usefull for people with lots of ice hockey gear. For example hockey families, who have many size of hockey gear and as children grow up, it is easy to keep track what you allready have. 

## Application architecture

```mermaid
flowchart TB
    subgraph RN[React Native App (Expo)]
      UI[UI & Navigation\n(React Navigation)]
      SQ[Local History\nExpo SQLite]
      RQ[React Query\n(Axios/Fetch)]
      CAM[Camera / Image Picker]
      UI --> CAM
      UI --> RQ
      UI --> SQ
    end

    subgraph API[Backend (FastAPI, Python)]
      INFER[ML Inference\n(PyTorch)]
      DB[(DB: SQLite/Postgres)]
      FS[(Image Storage\n/uploads or cloud)]
    end

    CAM -->|image (multipart/form-data)| RQ
    RQ -->|HTTPS POST /images| API
    API -->|store| FS
    API -->|run| INFER
    API -->|save results| DB
    API -->|JSON results| RQ
    RQ -->|update UI + cache| SQ
...


## Used Technologies

### Frontend
- **React + TypeScript** – for building the user interface.
- **Vite** – simple and fast development setup for React + Typescript projects. 
- **TailwindCSS or MUI** – to style the application.
- **Axios** – For making HTTP requests to the backend API.  

### Backend
- **FastAPI (Python)** – web framework for building our API. 
- **SQLite** – local development database  

### Machine Learning
- **PyTorch** – to load and run the image recognition model.

### Tools
- **Docker / Docker Compose** – to setup backend, machine learning and frontend all in one. 
- **GitHub** – for version control and collaboration.
- **pytest / Jest** – for testing backend and frontend.




