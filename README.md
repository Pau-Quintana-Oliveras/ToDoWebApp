# ✅ To-Do List API amb JSON

Un petit servei REST per gestionar tasques pendents amb **FastAPI** i persistència en **fitxer JSON**.

Pots provar-lo a https://todo.santaannaserver.uk/

---
✨ Funcionalitats

Afegir tasques amb títol i data límit opcional.

Marcar una tasca com a completada.

Desmarcar una tasca (tornar-la a pendent).

Filtrar tasques:
- Totes
- Només pendents
- Només completades

Persistència en fitxer JSON.
---
## 🚀 Requeriments

- Python 3.9+
- pip
---

## 📦 Instal·lació i execució en local
1. Clona aquest repositori
```bash
git clone <repo>
cd todo-app
```
2. Instal·la dependències
```bash
pip install -r requirements.txt
```
3. Arranca el servidor 
```bash
uvicorn main:app --reload
```     
4.Obre al navegador:
👉 http://127.0.0.1:8000
---
📂 Estructura del projecte
```bash
.
├── main.py             # API FastAPI
├── requirements.txt    # Dependències
├── tasks.json          # Fitxer de dades (es genera automàticament)
└── templates/
    └── index.html      # Interfície web

```
🔗 API Endpoints
| Mètode | Endpoint                    | Descripció                    |
| ------ | --------------------------- | ----------------------------- |
| `POST` | `/tasks`                    | Afegir una tasca nova         |
| `GET`  | `/tasks`                    | Llistar totes les tasques     |
| `GET`  | `/tasks?completed=true`     | Llistar només les completades |
| `GET`  | `/tasks?completed=false`    | Llistar només les pendents    |
| `GET`  | `/tasks/completed`          | Llistar completades           |
| `GET`  | `/tasks/pending`            | Llistar pendents              |
| `PUT`  | `/tasks/{title}/complete`   | Marcar com a completada       |
| `PUT`  | `/tasks/{title}/uncomplete` | Tornar-la a pendent           |