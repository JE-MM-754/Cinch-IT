# AI Sales Engine Demo - Software Architecture

**Objective:** Create a unified, professional SaaS demo platform showcasing 3 distinct AI sales tools in one cohesive application.

## 🏗️ High-Level Architecture

### Multi-Module Demo Platform
```
AI Sales Engine Demo Platform
├── Module 1: Dead Lead Reactivation
├── Module 2: AI Prospecting Engine  
├── Module 3: Sales Intelligence Dashboard
└── Shared: Common UI, Navigation, Auth (demo), Data Layer
```

**Philosophy:** One unified demo app that can showcase different "products" rather than separate demo sites.

## 🗂️ Application Structure

### Recommended File Structure
```
src/
├── app/                          # Next.js App Router
│   ├── layout.tsx               # Root layout with navigation
│   ├── page.tsx                 # Demo selector/overview dashboard
│   ├── reactivation/            # Dead Lead Reactivation Module
│   │   ├── page.tsx             # Module dashboard
│   │   ├── contacts/            # Dormant contacts management
│   │   ├── sequences/           # Reactivation email sequences
│   │   └── analytics/           # Reactivation performance
│   ├── prospecting/             # AI Prospecting Module  
│   │   ├── page.tsx             # Module dashboard
│   │   ├── discovery/           # Lead discovery tools
│   │   ├── outreach/            # Multi-channel campaigns
│   │   └── scoring/             # Lead scoring & qualification
│   └── intelligence/            # Sales Intelligence Module
│       ├── page.tsx             # Module dashboard  
│       ├── insights/            # AI-powered insights
│       ├── pipeline/            # Pipeline management
│       └── forecasting/         # Revenue forecasting
├── components/                   # Shared UI Components
│   ├── ui/                      # Base components (buttons, cards, etc.)
│   ├── charts/                  # Data visualization components
│   ├── tables/                  # Data table components
│   └── navigation/              # Navigation components
├── lib/                         # Utilities & Configuration
│   ├── demo-data/              # Mock data for all modules
│   ├── utils.ts                # Utility functions
│   └── types.ts                # TypeScript definitions
└── styles/                      # Styling
    └── globals.css             # Global styles & Tailwind
```

## 🎯 Module Architecture

### Module Design Pattern
Each demo module follows a consistent pattern:

```typescript
interface DemoModule {
  id: string;                    // 'reactivation' | 'prospecting' | 'intelligence'
  name: string;                  // Display name
  description: string;           // Module description
  dashboard: ReactComponent;     // Module dashboard page
  routes: Route[];              // Module-specific routes
  demoData: DemoDataSet;        // Mock data for this module
  metrics: MetricDefinition[];  // Key metrics to display
}
```

### Navigation Architecture
```typescript
// Multi-level navigation system
interface NavigationStructure {
  global: {
    moduleSwitcher: ModuleSelector;  // Switch between modules
    userProfile: DemoUserProfile;   // Demo user context
    notifications: DemoNotifications; // Fake notifications
  };
  module: {
    sidebar: ModuleSidebar;         // Module-specific navigation
    breadcrumbs: Breadcrumb[];      // Current page location
    actions: ActionButton[];       // Context actions
  };
}
```

## 📊 Demo Data Architecture

### Centralized Mock Data System
```typescript
// lib/demo-data/index.ts
export interface DemoDataManager {
  reactivation: {
    dormantContacts: Contact[];
    reactivationCampaigns: Campaign[];
    emailSequences: EmailSequence[];
    performanceMetrics: Metrics;
  };
  prospecting: {
    discoveredLeads: Lead[];
    outreachCampaigns: Campaign[];
    leadScoring: ScoringResults[];
    pipelineMetrics: Metrics;
  };
  intelligence: {
    pipelineData: PipelineEntry[];
    revenueForecasts: Forecast[];
    aiInsights: Insight[];
    performanceAnalytics: Analytics;
  };
  shared: {
    demoUser: User;
    companySettings: Settings;
    integrationStatus: Integration[];
  };
}
```

### Realistic Demo Data Requirements
- **Contact Data:** 500+ realistic B2B contacts with company info, titles, engagement history
- **Email Content:** Actual email templates, sequences, A/B test variations
- **Performance Data:** Realistic metrics (open rates, response rates, conversion rates)
- **Time Series Data:** Historical data for charts/trends (6+ months of data)
- **AI Insights:** Realistic AI-generated recommendations and insights

## 🎨 UI/UX Architecture

### Design System
```typescript
// Consistent design tokens
interface DesignSystem {
  colors: {
    primary: '#0ea5e9';      // Sky blue - professional SaaS
    secondary: '#6366f1';     // Indigo - AI/tech
    success: '#10b981';       // Emerald
    warning: '#f59e0b';       // Amber  
    danger: '#ef4444';        // Red
    neutral: '#64748b';       // Slate
  };
  typography: {
    heading: 'font-bold text-gray-900';
    body: 'text-gray-700';
    caption: 'text-gray-500 text-sm';
  };
  spacing: {
    section: 'py-6';
    container: 'px-4 sm:px-6 lg:px-8';
  };
}
```

### Component Library Standards
- **Buttons:** Primary, secondary, outline, ghost variants
- **Cards:** Stats cards, content cards, dashboard widgets
- **Tables:** Sortable, filterable, paginated data tables
- **Charts:** Line, bar, pie, funnel charts using Recharts
- **Forms:** Input fields, select dropdowns, toggles, date pickers
- **Navigation:** Sidebar, breadcrumbs, tabs, pagination

## 🔧 Technical Architecture

### State Management Strategy
```typescript
// Use React Context for demo state
interface DemoContext {
  currentModule: DemoModule;
  userData: DemoUser;
  settings: DemoSettings;
  switchModule: (moduleId: string) => void;
  updateSettings: (settings: Partial<DemoSettings>) => void;
}
```

### Routing Strategy
```
/                           # Demo selector/overview
/reactivation               # Dead Lead Reactivation dashboard
/reactivation/contacts      # Dormant contacts list
/reactivation/sequences     # Email sequence builder
/reactivation/analytics     # Performance analytics

/prospecting                # AI Prospecting dashboard  
/prospecting/discovery      # Lead discovery interface
/prospecting/outreach       # Campaign management
/prospecting/scoring        # Lead scoring results

/intelligence               # Sales Intelligence dashboard
/intelligence/insights      # AI insights feed
/intelligence/pipeline      # Pipeline visualization
/intelligence/forecasting   # Revenue forecasting
```

### Performance Considerations
- **Code Splitting:** Lazy load modules for faster initial load
- **Data Virtualization:** For large contact/lead tables
- **Caching Strategy:** Cache demo data in localStorage
- **Image Optimization:** Optimized avatars and company logos
- **Bundle Size:** Keep each module under 200KB

## 🔌 Integration Points

### External Services (Demo Mode)
```typescript
interface DemoIntegrations {
  crm: 'salesforce' | 'hubspot' | 'pipedrive';  // Demo CRM connection
  email: 'gmail' | 'outlook' | 'mailgun';       // Demo email provider
  linkedin: boolean;                             // Demo LinkedIn integration
  calendly: boolean;                            // Demo calendar integration
}
```

### API Simulation Layer
```typescript
// Simulate real API responses with delays and error states
interface APISimulator {
  contacts: {
    list: () => Promise<Contact[]>;
    search: (query: string) => Promise<Contact[]>;
    update: (id: string, data: Partial<Contact>) => Promise<Contact>;
  };
  campaigns: {
    create: (campaign: Campaign) => Promise<Campaign>;
    launch: (id: string) => Promise<LaunchResult>;
    analytics: (id: string) => Promise<CampaignAnalytics>;
  };
}
```

## 🚀 Deployment Architecture

### Environment Configuration
```typescript
interface DeploymentConfig {
  production: {
    domain: 'ai-sales-engine-demo.vercel.app';
    analytics: 'disabled';           // No tracking in demo
    apiMode: 'simulation';          // Always use mock data
  };
  development: {
    domain: 'localhost:3000';
    hotReload: true;
    debugMode: true;
  };
}
```

### Build Strategy
- **Static Generation:** Pre-render all demo pages for fast loading
- **Client Hydration:** Interactive elements load after initial render
- **Progressive Enhancement:** Works without JavaScript for basic navigation

## 🔒 Security & Privacy

### Demo Data Security
- **No Real Data:** All contacts, companies, emails are fictional
- **No External Calls:** No real API calls, no data collection
- **Privacy Compliant:** No cookies, tracking, or user data storage
- **Secure Deployment:** HTTPS, security headers, no exposed secrets

## 🎛️ Customization System

### Multi-Tenant Demo Capability
```typescript
interface DemoCustomization {
  branding: {
    companyName: string;
    logo: string;
    primaryColor: string;
    accentColor: string;
  };
  modules: {
    enabled: ('reactivation' | 'prospecting' | 'intelligence')[];
    featured: string;          // Which module to highlight
  };
  demoData: {
    industry: 'tech' | 'finance' | 'healthcare' | 'real-estate';
    companySize: 'startup' | 'midmarket' | 'enterprise';
    geography: 'us' | 'eu' | 'apac';
  };
}
```

## 📋 Implementation Priorities

### Phase 1: Foundation (High Priority)
1. **Unified Navigation:** Module switcher, professional sidebar
2. **Design System:** Consistent components and styling
3. **Demo Data:** Realistic mock data for all modules
4. **Routing Infrastructure:** Clean URLs and navigation

### Phase 2: Core Modules (High Priority)  
1. **Dead Lead Reactivation:** Dashboard, contacts, sequences, analytics
2. **AI Prospecting:** Dashboard, discovery, outreach, scoring
3. **Sales Intelligence:** Dashboard, insights, pipeline, forecasting

### Phase 3: Polish (Medium Priority)
1. **Interactive Elements:** Charts, filters, search, sorting
2. **Animations:** Smooth transitions and micro-interactions  
3. **Responsive Design:** Mobile-optimized layouts
4. **Performance:** Code splitting and optimization

### Phase 4: Advanced (Low Priority)
1. **Customization:** Easy theming and branding
2. **Export Features:** Demo PDF reports, data exports
3. **Advanced Charts:** Interactive dashboards with drill-down
4. **Demo Scenarios:** Guided demo flows with narratives

## 🎯 Success Metrics

### Technical Goals
- **Load Time:** < 2 seconds initial load
- **Bundle Size:** < 1MB total JavaScript
- **Lighthouse Score:** 95+ performance, accessibility, SEO
- **Cross-Browser:** Works in Chrome, Firefox, Safari, Edge

### Business Goals  
- **Demo Readiness:** 100% functional for live prospect demos
- **Customizable:** Easy to rebrand for different prospects
- **Impressive:** Enterprise-grade appearance and functionality
- **Memorable:** Prospects remember and reference the demo

---

**Next Step:** Hand this architecture to Codex with specific implementation instructions for each component.