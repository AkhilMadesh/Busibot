// User Types
export interface User {
  id: string
  email: string
  firstName: string
  lastName: string
  company?: string
  createdAt: Date
  updatedAt: Date
}

// Auth Types
export interface SignupRequest {
  email: string
  password: string
  firstName: string
  lastName: string
}

export interface LoginRequest {
  email: string
  password: string
}

export interface TokenResponse {
  accessToken: string
  refreshToken: string
  tokenType: string
}

// Business Idea Types
export interface BusinessIdea {
  id: string
  title: string
  description: string
  industry: string
  problem: string
  solution: string
  marketSize?: string
  validation?: IdeaValidation
  createdAt: Date
  updatedAt: Date
}

export interface IdeaValidation {
  marketSize: string
  competitionLevel: string
  feasibilityScore: number
  recommendation: string
}

export interface IdeaGenerateRequest {
  industry: string
  interests: string[]
  budget: number
  targetMarket?: string
}

// Business Plan Types
export interface BusinessPlan {
  id: string
  ideaId: string
  title: string
  executiveSummary: string
  marketAnalysis: string
  businessModel: string
  goToMarketStrategy: string
  financialProjections: Record<string, any>
  createdAt: Date
  updatedAt: Date
}

// Market Research Types
export interface MarketResearch {
  id: string
  ideaId: string
  marketSize: string
  growthRate: number
  marketTrends: string[]
  competitors: CompetitorInfo[]
  customerSegments: string[]
  createdAt: Date
  updatedAt: Date
}

export interface CompetitorInfo {
  name: string
  marketShare?: number
  strengths: string[]
  weaknesses: string[]
}

// Financial Forecast Types
export interface FinancialForecast {
  id: string
  ideaId: string
  breakEvenMonth: number
  runwayMonths: number
  projections: FinancialProjection[]
  assumptions: Record<string, string>
  createdAt: Date
  updatedAt: Date
}

export interface FinancialProjection {
  period: string
  revenue: number
  expenses: number
  profit: number
  cashFlow: number
}

// Investor Types
export interface InvestorMatch {
  id: string
  name: string
  type: 'VC' | 'Angel' | 'Accelerator'
  industryFocus: string[]
  investmentRange: string
  matchScore: number
  reasoning: string
  contactEmail?: string
  website?: string
  createdAt: Date
}

// Chat Types
export interface ChatMessage {
  id: string
  conversationId: string
  userMessage: string
  assistantResponse: string
  createdAt: Date
}

export interface Conversation {
  id: string
  title: string
  messages: ChatMessage[]
  createdAt: Date
  updatedAt: Date
}

export interface ChatMessageRequest {
  conversationId?: string
  message: string
}

// API Response Types
export interface ApiResponse<T> {
  data?: T
  error?: string
  message?: string
  status: number
}

export interface PaginatedResponse<T> {
  data: T[]
  total: number
  page: number
  pageSize: number
}
