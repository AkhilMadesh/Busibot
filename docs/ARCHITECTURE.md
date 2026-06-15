# Busibot - System Architecture

## 🏗️ Architecture Overview

```
┌─────────────────────────────────────────────────────────────────────┐
│                         CLIENT LAYER                                │
│  ┌────────────────────────────────────────────────────────────┐    │
│  │  Next.js 15 SPA (React 19, TypeScript, Tailwind CSS)      │    │
│  │  - Dashboard                                               │    │
│  │  - Idea Generation Interface                               │    │
│  │  - Business Plan Builder                                   │    │
│  │  - Chat Interface                                          │    │
│  │  - Analytics & Tracking                                    │    │
│  └────────────────────────────────────────────────────────────┘    │
└──────────────────────────────┬──────────────────────────────────────┘
                               │ HTTP/REST
                               │
┌──────────────────────────────┴──────────────────────────────────────┐
│                    API GATEWAY & REVERSE PROXY                      │
│                      (Nginx / CloudFlare)                          │
└──────────────────────────────┬──────────────────────────────────────┘
                               │
┌──────────────────────────────┴──────────────────────────────────────┐
│                       APPLICATION LAYER                             │
│  ┌────────────────────────────────────────────────────────────┐    │
│  │         FastAPI Server (Python 3.11)                      │    │
│  │                                                             │    │
│  │  ┌──────────────────────────────────────────────────┐     │    │
│  │  │ REST API Endpoints                               │     │    │
│  │  │ - /api/v1/auth/*                                 │     │    │
│  │  │ - /api/v1/ideas/*                                │     │    │
│  │  │ - /api/v1/plans/*                                │     │    │
│  │  │ - /api/v1/market-research/*                      │     │    │
│  │  │ - /api/v1/forecasts/*                            │     │    │
│  │  │ - /api/v1/investors/*                            │     │    │
│  │  │ - /api/v1/chat/*                                 │     │    │
│  │  └──────────────────────────────────────────────────┘     │    │
│  │                                                             │    │
│  │  ┌──────────────────────────────────────────────────┐     │    │
│  │  │ LangGraph AI Agent Orchestration                 │     │    │
│  │  │                                                  │     │    │
│  │  │  ├─ Business Analyst Agent                      │     │    │
│  │  │  ├─ Startup Mentor Agent                        │     │    │
│  │  │  ├─ Financial Advisor Agent                     │     │    │
│  │  │  ├─ Investor Matching Agent                     │     │    │
│  │  │  └─ Market Research Agent                       │     │    │
│  │  └──────────────────────────────────────────────────┘     │    │
│  │                                                             │    │
│  │  ┌──────────────────────────────────────────────────┐     │    │
│  │  │ Service Layer                                    │     │    │
│  │  │ - AuthService                                    │     │    │
│  │  │ - IdeaService                                    │     │    │
│  │  │ - BusinessPlanService                            │     │    │
│  │  │ - ChatService                                    │     │    │
│  │  │ - InvestorService                                │     │    │
│  │  └──────────────────────────────────────────────────┘     │    │
│  │                                                             │    │
│  │  ┌──────────────────────────────────────────────────┐     │    │
│  │  │ Middleware                                       │     │    │
│  │  │ - Authentication (JWT)                           │     │    │
│  │  │ - Rate Limiting                                  │     │    │
│  │  │ - Request Logging                                │     │    │
│  │  │ - Error Handling                                 │     │    │
│  │  │ - CORS Protection                                │     │    │
│  │  └──────────────────────────────────────────────────┘     │    │
│  └────────────────────────────────────────────────────────────┘    │
└──────────────┬──────────────────────┬──────────────────┬────────────┘
               │                      │                  │
               │ SQL               │ Cache           │ API Calls
               │                      │                  │
┌──────────────┴──────────┐  ┌────────┴───────┐  ┌──────┴──────────────┐
│  PostgreSQL 15          │  │   Redis 7      │  │  External APIs      │
│  - Users                │  │   - Sessions   │  │  - OpenAI           │
│  - Projects             │  │   - Cache      │  │  - Anthropic        │
│  - Ideas                │  │   - Rate Limit │  │  - Pinecone         │
│  - Business Plans       │  │   - Queues     │  │  - Crunchbase       │
│  - Conversations        │  │                │  │  - News APIs        │
│  - Financial Forecasts  │  └────────────────┘  └─────────────────────┘
│  - Investor Matches     │
│  - Audit Logs           │
└─────────────────────────┘

        └─ Vector DB (Pinecone) for RAG ─┘
```

## 🔄 Request Flow

```
1. Client Request
   User Action (Click, Form Submit)
        ↓
2. API Call (Next.js API Client)
   Axios with JWT authentication
        ↓
3. Rate Limiting & Auth Check
   Middleware validation
        ↓
4. Route Handler
   Find appropriate endpoint
        ↓
5. Service Layer
   Business logic execution
        ↓
6. AI Agent Orchestration (if needed)
   LangGraph multi-agent system
        ↓
7. Database & Cache Operations
   PostgreSQL + Redis
        ↓
8. External API Calls
   LLM, Vector DB, Market Data
        ↓
9. Response Processing
   Format and serialize data
        ↓
10. Client Update
    UI re-render with new data
```

## 🤖 AI Agent Architecture (LangGraph)

### Multi-Agent System

```
┌─────────────────────────────────────────────────────────────┐
│                   User Query / Request                       │
└────────────────────────────┬────────────────────────────────┘
                             │
                             ↓
                    ┌────────────────┐
                    │  Agent Router  │
                    └────────┬───────┘
                             │
        ┌────────────────────┼────────────────────┐
        │                    │                    │
        ↓                    ↓                    ↓
┌──────────────┐     ┌──────────────┐     ┌──────────────┐
│   Business   │     │   Startup    │     │  Financial   │
│   Analyst    │     │    Mentor    │     │   Advisor    │
│   Agent      │     │   Agent      │     │   Agent      │
├──────────────┤     ├──────────────┤     ├──────────────┤
│ Capabilities │     │ Capabilities │     │ Capabilities │
│ - Market     │     │ - Strategy   │     │ - P&L        │
│   sizing     │     │   guidance   │     │   modeling   │
│ - Industry   │     │ - Risk ID    │     │ - Cash flow  │
│   analysis   │     │ - Growth     │     │   analysis   │
│ - Competitor │     │   roadmap    │     │ - Unit econ  │
│   research   │     │              │     │   analysis   │
└──────────────┘     └──────────────┘     └──────────────┘
        │                    │                    │
        └────────────────────┼────────────────────┘
                             │
                             ↓
                    ┌────────────────┐
                    │  Agent Memory  │
                    │   (Vector DB)  │
                    └────────┬───────┘
                             │
        ┌────────────────────┼────────────────────┐
        │                    │                    │
        ↓                    ↓                    ↓
┌──────────────┐     ┌──────────────┐     ┌──────────────┐
│   Investor   │     │   Market     │     │  Conversation│
│   Matching   │     │  Research    │     │   Memory     │
│   Agent      │     │   Agent      │     │   (Redis)    │
├──────────────┤     ├──────────────┤     ├──────────────┤
│ Capabilities │     │ Capabilities │     │ Capabilities │
│ - VC/Angel   │     │ - Trend ID   │     │ - Context    │
│   matching   │     │ - Customer   │     │   preservation
│ - Portfolio  │     │   insights   │     │ - Multi-turn │
│   fit        │     │ - Opp.       │     │   support    │
│ - Investment │     │   spotting   │     │              │
│   thesis     │     │              │     │              │
└──────────────┘     └──────────────┘     └──────────────┘
        │                    │
        └────────────────────┼────────────────────┘
                             │
                             ↓
                    ┌────────────────┐
                    │   Response     │
                    │  Aggregation   │
                    └────────┬───────┘
                             │
                             ↓
                    ┌────────────────┐
                    │  Client Update │
                    └────────────────┘
```

## 💾 Database Schema Overview

### Core Tables

```
users
├── id (UUID)
├── email (VARCHAR UNIQUE)
├── password_hash (VARCHAR)
├── first_name (VARCHAR)
├── last_name (VARCHAR)
├── company (VARCHAR)
├── created_at (TIMESTAMP)
└── updated_at (TIMESTAMP)

projects
├── id (UUID)
├── user_id (FK → users)
├── title (VARCHAR)
├── description (TEXT)
├── status (ENUM)
├── created_at (TIMESTAMP)
└── updated_at (TIMESTAMP)

ideas
├── id (UUID)
├── user_id (FK → users)
├── title (VARCHAR)
├── description (TEXT)
├── industry (VARCHAR)
├── problem (TEXT)
├── solution (TEXT)
├── market_size (VARCHAR)
├── validation_score (FLOAT)
├── created_at (TIMESTAMP)
└── updated_at (TIMESTAMP)

business_plans
├── id (UUID)
├── idea_id (FK → ideas)
├── user_id (FK → users)
├── executive_summary (TEXT)
├── market_analysis (TEXT)
├── business_model (TEXT)
├── go_to_market_strategy (TEXT)
├── financial_projections (JSONB)
├── created_at (TIMESTAMP)
└── updated_at (TIMESTAMP)

conversations
├── id (UUID)
├── user_id (FK → users)
├── title (VARCHAR)
├── context (JSONB)
├── created_at (TIMESTAMP)
└── updated_at (TIMESTAMP)

messages
├── id (UUID)
├── conversation_id (FK → conversations)
├── user_message (TEXT)
├── assistant_response (TEXT)
├── agent_metadata (JSONB)
├── created_at (TIMESTAMP)
└── updated_at (TIMESTAMP)

financial_forecasts
├── id (UUID)
├── idea_id (FK → ideas)
├── user_id (FK → users)
├── break_even_month (INT)
├── runway_months (FLOAT)
├── projections (JSONB)
├── assumptions (JSONB)
├── created_at (TIMESTAMP)
└── updated_at (TIMESTAMP)

investor_matches
├── id (UUID)
├── idea_id (FK → ideas)
├── investor_id (UUID)
├── investor_name (VARCHAR)
├── match_score (FLOAT)
├── reasoning (TEXT)
├── created_at (TIMESTAMP)
└── updated_at (TIMESTAMP)

audit_logs
├── id (UUID)
├── user_id (FK → users)
├── action (VARCHAR)
├── resource_type (VARCHAR)
├── resource_id (UUID)
├── changes (JSONB)
├── created_at (TIMESTAMP)
└── ip_address (VARCHAR)
```

## 🔐 Security Architecture

```
┌─────────────────────────────────────────┐
│     HTTPS/TLS Encryption (in transit)   │
└─────────────┬───────────────────────────┘
              │
┌─────────────┴───────────────────────────┐
│  JWT Token Authentication                │
│  - Issued on login/signup                │
│  - Verified on each request              │
│  - 24-hour expiration                    │
└─────────────┬───────────────────────────┘
              │
┌─────────────┴───────────────────────────┐
│  Authorization & Access Control          │
│  - Role-based access (User/Admin)        │
│  - Resource ownership validation         │
│  - Rate limiting (100 req/min)           │
└─────────────┬───────────────────────────┘
              │
┌─────────────┴───────────────────────────┐
│  Data Protection                         │
│  - Password hashing (bcrypt)             │
│  - Sensitive data encryption             │
│  - SQL injection prevention              │
│  - XSS protection                        │
│  - CSRF tokens                           │
└─────────────┬───────────────────────────┘
              │
┌─────────────┴───────────────────────────┐
│  Audit & Monitoring                      │
│  - All actions logged                    │
│  - Sentry error tracking                 │
│  - Health checks & uptime monitoring     │
└─────────────────────────────────────────┘
```

## 📊 Deployment Architecture

### Development
- Docker Compose for local setup
- PostgreSQL, Redis, FastAPI, Next.js in containers
- Hot reload enabled

### Production
- **Frontend**: Vercel or AWS CloudFront + S3
- **Backend**: AWS ECS Fargate + ALB
- **Database**: AWS RDS PostgreSQL (Multi-AZ)
- **Cache**: AWS ElastiCache Redis
- **Storage**: AWS S3 for files
- **CDN**: CloudFront for static assets
- **Monitoring**: CloudWatch, Sentry, DataDog

## 🚀 Scaling Strategy

### Phase 1: MVP (1,000 users)
- Single server deployment
- Monolithic architecture
- Manual scaling

### Phase 2: Growth (100,000 users)
- Horizontal scaling with load balancing
- Database replication (read replicas)
- Redis clustering for caching
- CDN for static assets
- Async jobs for heavy processing

### Phase 3: Scale (1M+ users)
- Microservices architecture
- Kubernetes orchestration
- Event-driven architecture (message queues)
- Database sharding
- Advanced caching strategies (distributed cache)
- Real-time features (WebSockets)
- Global distribution (multi-region)

## 🔄 CI/CD Pipeline

```
Git Push
   ↓
GitHub Actions
   ├─ Lint & Format Check
   ├─ Unit Tests
   ├─ Integration Tests
   ├─ Build Docker Images
   ├─ Push to Registry
   └─ Deploy to Production
        ↓
  ECS/Kubernetes
        ↓
  Health Checks
        ↓
  Smoke Tests
        ↓
  Production Live
```

## 📈 Performance Targets

| Metric | Target | Current |
|--------|--------|----------|
| API Response Time | < 200ms (p95) | - |
| Chat Response | < 5s (avg) | - |
| Page Load Time | < 3s | - |
| Database Query | < 50ms (p95) | - |
| Uptime SLA | 99.9% | - |
| Concurrent Users | 10,000+ | - |

---

**Last Updated**: June 2024
**Version**: 1.0.0
