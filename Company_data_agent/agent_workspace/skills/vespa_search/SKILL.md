---
name: vespa-company-search
description: Search and retrieve company profiles, funding rounds, and financial data from the Vespa AI 'pefund' index. Use this when you need specific details about a company's revenue, investors, or history for a given tenant.
---

# Vespa Company Search Skill

This skill allows the agent to execute structured queries against the Vespa AI database to extract high-fidelity company information from the `pefund.summary` source.

## Database Schema
The data is stored in the `pefund.summary` source with the following relevant fields:
- `content_summary_chunk`: Markdown text containing company details or funding history.
- `url`: The source document URL (S3/PDF).
- `tenant_id`: Mandatory UUID for data isolation.
- `file_id`: Unique identifier for the source file.
- `doc_type`: Category of document (e.g., 'apollo').

## Querying Guidelines (YQL)

### 1. Mandatory Filters
Every query **must** include a `tenant_id` filter to ensure data privacy.
- **Pattern:** `where tenant_id contains "[UUID]"`

### 2. Document Types
Use the `doc_type` filter to narrow results. Records from the Apollo dataset should be targeted using:
- **Pattern:** `AND doc_type IN ('apollo')`

### 3. Search Logic
- For broad retrieval: Use `select *` or specify the fields `content_summary_chunk, url, tenant_id`.
- For specific lookups: Add `AND content_summary_chunk contains "keyword"` to the `where` clause.

## Examples

### Example 1: Retrieve all data for a specific tenant
**Query:**
```sql
select content_summary_chunk, url, tenant_id, file_id 
from sources pefund.summary 
where tenant_id contains "90da21d0-8e83-4e84-961b-e6fec8b9dafe" 
AND doc_type IN ('apollo')
``` 