## Backend API

The application relies on a REST API running on `http://localhost:8000`.

| Method   | Endpoint                    | Description                                                                   |
| :------- | :-------------------------- | :---------------------------------------------------------------------------- |
| `GET`    | `/meals`                    | List all available meals                                                      |
| `POST`   | `/meals`                    | Create a new meal (FormData: `name`, `description`, `tags`, `rating`, `file`) |
| `PUT`    | `/meals/:id`                | Update an existing meal                                                       |
| `DELETE` | `/meals/:id`                | Delete a meal                                                                 |
| `GET`    | `/plans`                    | Get all planned meals (mapped by date)                                        |
| `GET`    | `/plans/:date`              | Get meals for a specific date (`YYYY-MM-DD`)                                  |
| `POST`   | `/plans/:date`              | Add a meal to a specific date                                                 |
| `DELETE` | `/plans/:date/:id`          | Remove a meal from a plan                                                     |
| `GET`    | `/analytics/frequent-meals` | Get top meals (Query param: `?days=30`)                                       |
