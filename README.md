##### Alexandra Florentina Georgiana Lache, 332CD

## __HealthStats Server__

---

### __Project description__

A *multithreaded Python **Flask** web server* for processing health statistics. Tasks
 are handled *asynchronously* through a **custom threadpool** and served via **REST
  API routes**. Data is processed with **pandas** and returned in *JSON format*.

---

### Implementation

- Every request to the server is turned into a job, assigned a unique job_id, and added
 to a job queue processed by a custom ThreadPool.

- ***DataIngestor***: Handles all logic related to reading and processing CSVs using
_pandas_. It encapsulates data access and helps convert results into dictionaries 
for easy JSON serialization.

- *Factory Design Pattern*: A TaskFactory provides a unified interface to handle
 different tasks in a uniform and maintainable way.

- *ThreadPool*: Uses an internal `Queue` to manage pending jobs, and also tracks
 job statuses in a dictionary. Uses an Event flag for managin graceful shutdown.

---

### __Endpoints__

| Endpoint                      | Description                                                                             |
| ----------------------------- | --------------------------------------------------------------------------------------- |
| `/api/states_mean`            | Returns mean `Data_Value` for each state, sorted ascending.                             |
| `/api/state_mean`             | Returns mean `Data_Value` for a given state.                                            |
| `/api/best5`                  | Returns the top 5 states with the lowest mean `Data_Value`.                             |
| `/api/worst5`                 | Returns the bottom 5 states with the highest mean `Data_Value`.                         |
| `/api/global_mean`            | Returns the overall mean `Data_Value`.                                                  |
| `/api/diff_from_mean`         | Returns the difference between each state’s mean and the global mean.                   |
| `/api/state_diff_from_mean`   | Returns the difference between a given state’s mean and the global mean.                |
| `/api/mean_by_category`       | Returns the average `Data_Value` per category segment (Stratification1) for each state. |
| `/api/state_mean_by_category` | Same as above but limited to a specific state.                                          |
| `/api/graceful_shutdown`    | Initiates a clean shutdown: no new requests accepted, ongoing jobs finish. Returns `"running"` or `"done"`.|
| `/api/jobs`                 | Returns status of all jobs: `"running"` or `"done"`.                                                        |
| `/api/num_jobs`             | Returns the number of remaining jobs in the queue.                                                          |
| `/api/get_results/<job_id>` | Fetches result of a completed job. Handles invalid or incomplete jobs with appropriate error messages.      |


---

### __Unit Testing__

The project includes a comprehensive suite of unit tests using Python’s 
built-in `unittest` framework.

All major data processing tasks are tested independently. For floating-point comparisons,
 we use assertAlmostEqual with a small delta to ensure tolerance to rounding errors.

To run the tests:

```bash
python3 -m unittest -v unittests/test_webserver.py
```
---

### __Logging__

The application uses the standard Python `logging` module to track server activity, errors, and request flow.

---