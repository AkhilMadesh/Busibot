# Busibot API Specification

## Base URL
```
Production: https://api.busibot.io/api/v1
Development: http://localhost:8000/api/v1
```

## Authentication

All endpoints require JWT authentication in the `Authorization` header:
```
Authorization: Bearer <access_token>
```

---

## Authentication Endpoints

### Sign Up
```http
POST /auth/signup
Content-Type: application/json

{
  "email": "user@example.com",
  "password": "securepassword123",
  "firstName": "John",
  "lastName": "Doe"
}

Response (201):
{
  "accessToken": "eyJhbGc...",
  "refreshToken": "eyJhbGc...",
  "tokenType": "bearer"
}
```

### Login
```http
POST /auth/login
Content-Type: application/json

{
  "email": "user@example.com",
  "password": "securepassword123"
}

Response (200):
{
  "accessToken": "eyJhbGc...",
  "refreshToken": "eyJhbGc...",
  "tokenType": "bearer"
}
```

### Refresh Token
```http
POST /auth/refresh
Content-Type: application/json

{
  "refreshToken": "eyJhbGc..."
}

Response (200):
{
  "accessToken": "eyJhbGc...",
  "refreshToken": "eyJhbGc...",
  "tokenType": "bearer"
}
```

### Logout
```http
POST /auth/logout

Response (200):
{
  "message": "Successfully logged out"
}
```

---

## Users Endpoints

### Get Current User
```http
GET /users/me
Authorization: Bearer <token>

Response (200):
{
  "id": "uuid",
  "email": "user@example.com",
  "firstName": "John",
  "lastName": "Doe",
  "company": "Acme Corp",
  "createdAt": "2024-01-15T10:30:00Z",
  "updatedAt": "2024-01-15T10:30:00Z"
}
```

### Update User Profile
```http
PUT /users/me
Authorization: Bearer <token>
Content-Type: application/json

{
  "firstName": "Jane",
  "lastName": "Smith",
  "company": "Tech Startup"
}

Response (200):
{
  "id": "uuid",
  "email": "user@example.com",
  "firstName": "Jane",
  "lastName": "Smith",
  "company": "Tech Startup",
  "createdAt": "2024-01-15T10:30:00Z",
  "updatedAt": "2024-01-15T11:00:00Z"
}
```

---

## Ideas Endpoints

### Generate Business Idea
```http
POST /ideas/generate
Authorization: Bearer <token>
Content-Type: application/json

{
  "industry": "SaaS",
  "interests": ["AI", "productivity", "automation"],
  "budget": 50000,
  "targetMarket": "SMBs"
}

Response (200):
{
  "id": "uuid",
  "title": "AI Meeting Assistant",
  "description": "...",
  "industry": "SaaS",
  "problem": "...",
  "solution": "...",
  "marketSize": "$50B",
  "validation": null,
  "createdAt": "2024-01-15T10:30:00Z",
  "updatedAt": "2024-01-15T10:30:00Z"
}
```

### Validate Idea
```http
POST /ideas/{ideaId}/validate
Authorization: Bearer <token>
Content-Type: application/json

{
  "marketFocus": "Enterprise"
}

Response (200):
{
  "id": "uuid",
  "title": "AI Meeting Assistant",
  "description": "...",
  "industry": "SaaS",
  "problem": "...",
  "solution": "...",
  "marketSize": "$50B",
  "validation": {
    "marketSize": "$50B",
    "competitionLevel": "High",
    "feasibilityScore": 8.5,
    "recommendation": "Go - Strong market opportunity"
  },
  "createdAt": "2024-01-15T10:30:00Z",
  "updatedAt": "2024-01-15T10:45:00Z"
}
```

### List Ideas
```http
GET /ideas?skip=0&limit=20
Authorization: Bearer <token>

Response (200):
[
  {
    "id": "uuid",
    "title": "AI Meeting Assistant",
    "description": "...",
    "industry": "SaaS",
    "createdAt": "2024-01-15T10:30:00Z",
    "updatedAt": "2024-01-15T10:30:00Z"
  }
]
```

### Get Idea
```http
GET /ideas/{ideaId}
Authorization: Bearer <token>

Response (200):
{
  "id": "uuid",
  "title": "AI Meeting Assistant",
  "description": "...",
  "industry": "SaaS",
  "problem": "...",
  "solution": "...",
  "marketSize": "$50B",
  "validation": {...},
  "createdAt": "2024-01-15T10:30:00Z",
  "updatedAt": "2024-01-15T10:30:00Z"
}
```

---

## Business Plans Endpoints

### Generate Business Plan
```http
POST /plans/generate
Authorization: Bearer <token>
Content-Type: application/json

{
  "ideaId": "uuid",
  "companyName": "MeetAI Inc",
  "targetMarket": "Enterprise"
}

Response (200):
{
  "id": "uuid",
  "ideaId": "uuid",
  "title": "MeetAI Business Plan",
  "executiveSummary": "...",
  "marketAnalysis": "...",
  "businessModel": "...",
  "goToMarketStrategy": "...",
  "financialProjections": {...},
  "createdAt": "2024-01-15T10:30:00Z",
  "updatedAt": "2024-01-15T10:30:00Z"
}
```

### List Business Plans
```http
GET /plans
Authorization: Bearer <token>

Response (200):
[
  {
    "id": "uuid",
    "ideaId": "uuid",
    "title": "MeetAI Business Plan",
    "createdAt": "2024-01-15T10:30:00Z",
    "updatedAt": "2024-01-15T10:30:00Z"
  }
]
```

---

## Market Research Endpoints

### Get Market Research
```http
GET /market-research/{ideaId}
Authorization: Bearer <token>

Response (200):
{
  "id": "uuid",
  "ideaId": "uuid",
  "marketSize": "$50B",
  "growthRate": 0.25,
  "marketTrends": ["AI adoption", "Remote work", "Automation"],
  "competitors": [
    {
      "name": "Competitor A",
      "marketShare": 0.15,
      "strengths": ["Brand", "Network"],
      "weaknesses": ["Price", "UX"]
    }
  ],
  "customerSegments": ["Enterprises", "Mid-market"],
  "createdAt": "2024-01-15T10:30:00Z",
  "updatedAt": "2024-01-15T10:30:00Z"
}
```

---

## Financial Forecasts Endpoints

### Generate Forecast
```http
POST /forecasts/generate
Authorization: Bearer <token>
Content-Type: application/json

{
  "ideaId": "uuid",
  "initialInvestment": 250000,
  "monthlyBurnRate": 50000
}

Response (200):
{
  "id": "uuid",
  "ideaId": "uuid",
  "breakEvenMonth": 18,
  "runwayMonths": 5,
  "projections": [
    {
      "period": "Month 1",
      "revenue": 0,
      "expenses": 50000,
      "profit": -50000,
      "cashFlow": -50000
    }
  ],
  "assumptions": {
    "annualGrowth": "15%",
    "customerAcquisitionCost": "$500"
  },
  "createdAt": "2024-01-15T10:30:00Z",
  "updatedAt": "2024-01-15T10:30:00Z"
}
```

---

## Investor Matching Endpoints

### Get Investor Matches
```http
GET /investors/match/{ideaId}
Authorization: Bearer <token>

Response (200):
[
  {
    "id": "uuid",
    "name": "Sequoia Capital",
    "type": "VC",
    "industryFocus": ["SaaS", "AI", "Enterprise"],
    "investmentRange": "$2M - $50M",
    "matchScore": 0.95,
    "reasoning": "Perfect fit for AI SaaS startups in enterprise space",
    "contactEmail": "investments@sequoia.com",
    "website": "https://sequoia.com",
    "createdAt": "2024-01-15T10:30:00Z"
  }
]
```

---

## Chat Endpoints

### Send Message
```http
POST /chat/message
Authorization: Bearer <token>
Content-Type: application/json

{
  "conversationId": "uuid" (optional),
  "message": "How should I price my SaaS product?"
}

Response (200):
{
  "id": "uuid",
  "conversationId": "uuid",
  "userMessage": "How should I price my SaaS product?",
  "assistantResponse": "Based on your market analysis, here are pricing strategies...",
  "createdAt": "2024-01-15T10:30:00Z"
}
```

### List Conversations
```http
GET /chat/conversations
Authorization: Bearer <token>

Response (200):
[
  {
    "id": "uuid",
    "title": "Pricing Strategy Discussion",
    "createdAt": "2024-01-15T10:30:00Z",
    "updatedAt": "2024-01-15T11:00:00Z"
  }
]
```

### Get Conversation
```http
GET /chat/conversations/{conversationId}
Authorization: Bearer <token>

Response (200):
{
  "id": "uuid",
  "title": "Pricing Strategy Discussion",
  "messages": [
    {
      "id": "uuid",
      "conversationId": "uuid",
      "userMessage": "How should I price my SaaS product?",
      "assistantResponse": "...",
      "createdAt": "2024-01-15T10:30:00Z"
    }
  ],
  "createdAt": "2024-01-15T10:30:00Z",
  "updatedAt": "2024-01-15T11:00:00Z"
}
```

---

## Error Responses

All endpoints return error responses in the following format:

```json
{
  "detail": "Error message",
  "status": 400
}
```

### Common Status Codes
- `200` - Success
- `201` - Created
- `400` - Bad Request
- `401` - Unauthorized
- `403` - Forbidden
- `404` - Not Found
- `429` - Too Many Requests (Rate Limited)
- `500` - Internal Server Error

---

## Rate Limiting

API endpoints are rate limited to **100 requests per 60 seconds** per user.

Rate limit headers:
```
X-RateLimit-Limit: 100
X-RateLimit-Remaining: 95
X-RateLimit-Reset: 1705328460
```

---

**API Version**: 1.0.0
**Last Updated**: June 2024
