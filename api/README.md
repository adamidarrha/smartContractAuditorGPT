# Solodit API Wrapper Documentation

This documentation provides an overview of the API endpoints available in the Solodit API Wrapper. This wrapper simplifies interactions with the Solodit.xyz API, making it more accessible for GPT usage.

## Base URL

`http://your-api-base-url.com/api/v1`

## Endpoints

### 1. Tags

- **Endpoint**: `/tags`
- **Method**: GET
- **Description**: Retrieve available tags for filtering issues.
- **Response**: An array of strings representing tags.
- **example**: "1/64 Rule","51% Attack","Aave"

### 2. Protocol Categories

- **Endpoint**: `/protocols/categories`
- **Method**: GET
- **Description**: Get available protocol categories.
- **Response**: An array of strings representing protocol categories.
- **example**: "Algo-Stables","Bridge","CDP"

### 3. Audit Firms

- **Endpoint**: `/auditfirms`
- **Method**: GET
- **Description**: Retrieve a list of audit firms.
- **Response**: An array of strings representing audit firms.
- **example**: "name":"AuditOne"

### 4. Issues

- **Endpoint**: `/issues`
- **Method**: GET
- **Description**: Get issues based on various filters.
- **Query Parameters**:
  - `source`: Source of the issue (string).
  - `impact`: Impact level, e.g., HIGH, MEDIUM, GAS, LOW (string).
  - `finder`: Identifier of the finder (string).
  - `protocol`: Protocol name (string).
  - `pcategories`: Protocol categories (string).
  - `protocol_forked_from`: The original protocol from which the current protocol was forked (string).
  - `min_finders`: Minimum number of finders (integer).
  - `report_date`: Date of the report (string).
  - `quality_scores`: Quality scores (string).
  - `general_scores`: General scores (string).
  - `tags`: Tags for filtering (string).
  - `bookmarked`: Filter for bookmarked issues (boolean).
  - `markasread`: Mark issues as read (string).
  - `keyword`: Keyword for search (string).
  - `page`: Page number for pagination (integer).
- **Response**: An array of objects, each representing an issue.

## Notes

- this is made to be used with openai gpts actions, better to just use solodit original api.
- need to include your authorization token in a .env file as SOLODIT_AUTH_TOKEN.
- can also use Basic auth to authenticate "Basic Base64(username:password)"