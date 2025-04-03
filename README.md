backend/
│── api/
│   ├── migrations/
│   ├── models/
│   │   ├── __init__.py
│   │   ├── allocation_detail.py
│   │   ├── customers.py
│   │   ├── plant.py
│   │   ├── tally_session.py
│   │   ├── weight_classification.py
│   ├── serializers/
│   │   ├── __init__.py
│   │   ├── allocation_detail_serializer.py
│   │   ├── customers_serializer.py
│   │   ├── plant_serializer.py
│   │   ├── tally_session_serializer.py
│   │   ├── weight_classification_serializer.py
│   ├── views/
│   │   ├── __init__.py
│   │   ├── allocation_detail_views.py
│   │   ├── customers_views.py
│   │   ├── plant_views.py
│   │   ├── tally_session_views.py
│   │   ├── weight_classification_views.py
│   ├── urls/
│   │   ├── __init__.py
│   │   ├── allocation_detail_urls.py
│   │   ├── customers_urls.py
│   │   ├── plant_urls.py
│   │   ├── tally_session_urls.py
│   │   ├── weight_classification_urls.py
│   ├── permissions.py
│   ├── utils.py
│   ├── tests/
│   │   ├── __init__.py
│   │   ├── test_allocation_detail.py
│   │   ├── test_customers.py
│   │   ├── test_plant.py
│   │   ├── test_tally_session.py
│   │   ├── test_weight_classification.py
│   ├── admin.py
│   ├── apps.py
│   ├── __init__.py



<aside>
💡

Note: the tables have links within their names to help with understanding references

</aside>

- Customers Table
    
    
    | Column Name | Type | Description |
    | --- | --- | --- |
    | `id` | INT (Primary Key) | Unique customer ID |
    | `name` | TEXT | Name of the customer |
- WeightClassification Table
    
    
    | Column Name | Type | Description |
    | --- | --- | --- |
    | `id` | INT (Primary Key) | Unique weight class ID |
    | [`plantId`](https://www.notion.so/Database-Structure-1b4d4d3f7db780c9bbd7c98e8dab1259?pvs=21) | INT (Foreign Key) | References `Plant.id` (which plant this classification belongs to) |
    | `classification` | TEXT | Weight category (e.g., SQ, US, P1, etc.) |
    | `min_weight` | FLOAT | Minimum weight for this classification |
    | `max_weight` | FLOAT | Maximum weight for this classification |
- PlantTable
    
    
    | Column Name | Type | Description |
    | --- | --- | --- |
    | `id` | INT (Primary Key) | Unique plant ID |
    | `name` | TEXT | Name of the butchering plant |
- TallySession (or Operation) Table
    
    
    | Column Name | Type | Description |
    | --- | --- | --- |
    | `id` | INT (Primary Key) | Unique tally session ID |
    | [`customerId`](https://www.notion.so/Database-Structure-1b4d4d3f7db780c9bbd7c98e8dab1259?pvs=21) | INT (Foreign Key) | References `Customers.id` |
    | [`plantId`](https://www.notion.so/Database-Structure-1b4d4d3f7db780c9bbd7c98e8dab1259?pvs=21) | INT (Foreign Key) | References `Plant.id` |
    | `date` | DATETIME | Date and time of the operation |
    | `status` | TEXT | Status of the session (e.g., ongoing, completed) |
- AllocationDetail Table
    
    
    | Column Name | Type | Description |
    | --- | --- | --- |
    | `id` | INT (Primary Key) | Unique allocation detail ID |
    | [`tallySessionId`](https://www.notion.so/Database-Structure-1b4d4d3f7db780c9bbd7c98e8dab1259?pvs=21) | INT (Foreign Key) | References `TallySession.id` |
    | [`weightClassId`](https://www.notion.so/Database-Structure-1b4d4d3f7db780c9bbd7c98e8dab1259?pvs=21) | INT (Foreign Key) | References `WeightClassification.id` (ensures valid classification) |
    | `required_bags` | FLOAT | Required bags for that classification |
    | `allocated_bags` | FLOAT | Actual allocated bags during that tally session |

# Workflow Example

1. **Session Setup:**
    
    When Customer A is chosen for an operation, a new TallySession record is created, linking to Customer A.
    
2. **Input Customer Allocation:**
    
    The required allocations are input—for example, SQ = 40, US = 50, OS = 20. For each allocation, insert a record into AllocationDetail that includes the requestedHeads for that weight classification.
    
3. **Tallying Process:**
    - Tally-er: Inputs weights which are automatically classified (using the logic defined from the WeightClassification table) and increments the tallyErCount for the corresponding AllocationDetail record.
    - Dispatcher: Re-tallies and updates dispatcherCount for the corresponding records.
4. **Validation:**
    
    After the session, you can compare tallyErCount and dispatcherCount for each classification to flag any mismatches.
    
    Advantages of This Structure
    
    - Normalization: The weight ranges and labels are stored once in WeightClassification.
    - Flexibility: Each session (in TallySession) can have a dynamic set of allocations (in AllocationDetail), tailored to each customer’s needs.
    - Simplicity in Queries: You can easily join TallySession, AllocationDetail, and WeightClassification to generate reports, compare tallies, and validate discrepancies.
    - Extensibility: If a customer’s allocation changes over time, or if you need to add new classifications, you can do so without modifying multiple tables.
