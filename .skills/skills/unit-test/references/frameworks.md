# Testing Frameworks Guide

Comprehensive guide to modern testing frameworks with focus on Vitest and Jest.

## Table of Contents

- [Framework Comparison](#framework-comparison)
- [Vitest (Recommended)](#vitest-recommended)
- [Jest (Legacy)](#jest-legacy)
- [Migration Guide](#migration-guide)
- [Playwright (E2E)](#playwright-e2e)
- [Testing Library (DOM)](#testing-library-dom)

---

## Framework Comparison

### Vitest vs Jest: The 2025 Comparison

| Feature | Vitest | Jest |
|---------|--------|------|
| **Speed** | ⚡⚡⚡ Extremely Fast | ⚡ Moderate |
| **ESM Support** | ✅ Native | ⚠️ Requires config |
| **TypeScript** | ✅ Out of box | ⚠️ Requires ts-jest |
| **Watch Mode** | ✅ Instant HMR | ⚠️ Slower restart |
| **Vite Integration** | ✅ Native | ❌ Not supported |
| **Ecosystem** | 📈 Growing (3.8M/week) | 🏆 Mature (35M/week) |
| **Community** | 📈 Rapidly growing | 🏆 Established |
| **Debugging** | ✅ Good | ✅ Excellent |
| **Snapshot** | ✅ Supported | ✅ Supported |
| **Coverage** | ✅ v8 built-in | ✅ Istanbul |

### Performance Benchmarks

```
Test Suite Size: 1000 tests

┌─────────────────┬──────────────┬──────────────┐
│     Metric      │    Vitest    │     Jest     │
├─────────────────┼──────────────┼──────────────┤
│ Cold Start      │    2.3s      │    8.7s      │
│ Warm Start      │    0.8s      │    3.2s      │
│ Watch Mode HMR  │    0.1s      │    1.5s      │
│ Full Suite Run  │    4.2s      │    12.8s     │
│ Memory Usage    │    180MB     │    450MB     │
└─────────────────┴──────────────┴──────────────┘
```

### When to Choose

**Choose Vitest When:**
- Starting a new project
- Using Vite for bundling
- ESM-first codebase
- Speed is critical
- Modern TypeScript setup

**Choose Jest When:**
- Large existing Jest codebase
- Complex project configuration
- Need mature ecosystem plugins
- React Native development
- Enterprise with established tooling

---

## Vitest (Recommended)

### Installation

```bash
npm install -D vitest @vitest/ui
```

### Configuration

```typescript
// vitest.config.ts
import { defineConfig } from 'vitest/config';

export default defineConfig({
  test: {
    globals: true,
    environment: 'jsdom',
    include: ['src/**/*.{test,spec}.{js,mjs,cjs,ts,mts,cts,jsx,tsx}'],
    exclude: ['node_modules', 'dist', '.idea', '.git', '.cache'],
    coverage: {
      provider: 'v8',
      reporter: ['text', 'json', 'html'],
      exclude: [
        'node_modules/',
        'src/**/*.d.ts',
        'src/**/*.test.ts',
      ],
    },
    setupFiles: ['./src/test/setup.ts'],
  },
});
```

### Basic Usage

```typescript
import { describe, it, expect, vi, beforeEach, afterEach } from 'vitest';

describe('UserService', () => {
  let service: UserService;
  let mockRepo: any;

  beforeEach(() => {
    mockRepo = {
      save: vi.fn(),
      findById: vi.fn(),
    };
    service = new UserService(mockRepo);
  });

  afterEach(() => {
    vi.clearAllMocks();
  });

  it('should create user', () => {
    mockRepo.save.mockReturnValue({ id: '1', name: 'John' });

    const result = service.createUser({ name: 'John' });

    expect(result.id).toBe('1');
    expect(mockRepo.save).toHaveBeenCalledWith({ name: 'John' });
  });
});
```

### Mocking

```typescript
// Function mock
const mockFn = vi.fn();
mockFn.mockReturnValue('value');
mockFn.mockReturnValueOnce('first call');
mockFn.mockImplementation((arg) => arg * 2);

// Spy
const spy = vi.spyOn(object, 'method');
spy.mockReturnValue('mocked');

// Module mock
vi.mock('./module', () => ({
  default: vi.fn(),
  namedExport: vi.fn(),
}));

// Mock with implementation
vi.mock('./api', () => ({
  fetchUser: vi.fn((id) => Promise.resolve({ id, name: 'Test' })),
}));

// Mock restoration
spy.mockRestore();
vi.restoreAllMocks();
```

### Timers

```typescript
it('handles timers', () => {
  vi.useFakeTimers();

  const callback = vi.fn();
  setTimeout(callback, 1000);

  vi.advanceTimersByTime(1000);
  expect(callback).toHaveBeenCalled();

  vi.useRealTimers();
});
```

### Async Handling

```typescript
// Promises
it('handles async', async () => {
  const result = await asyncFunction();
  expect(result).toBe('value');
});

// waitFor
import { waitFor } from '@testing-library/react';

it('waits for condition', async () => {
  doSomething();
  await waitFor(() => {
    expect(screen.getByText('Loaded')).toBeInTheDocument();
  });
});

// vi.waitFor (Vitest native)
it('waits with vi.waitFor', async () => {
  await vi.waitFor(() => {
    expect(someCondition).toBe(true);
  });
});
```

### Snapshot Testing

```typescript
import { render } from '@testing-library/react';

it('matches snapshot', () => {
  const { container } = render(<Component />);
  expect(container).toMatchSnapshot();
});

// Inline snapshot
it('matches inline snapshot', () => {
  expect(result).toMatchInlineSnapshot(`
    {
      "id": 1,
      "name": "John"
    }
  `);
});
```

### Running Tests

```bash
# Run all tests
vitest

# Run in watch mode
vitest watch

# Run with coverage
vitest run --coverage

# Run specific file
vitest path/to/test.ts

# Run tests matching pattern
vitest -t "should create user"

# UI mode
vitest --ui
```

---

## Jest (Legacy)

### Installation

```bash
npm install -D jest @types/jest ts-jest @jest/globals
```

### Configuration

```typescript
// jest.config.ts
import type { Config } from 'jest';

const config: Config = {
  preset: 'ts-jest',
  testEnvironment: 'jsdom',
  roots: ['<rootDir>/src'],
  testMatch: ['**/__tests__/**/*.ts', '**/*.test.ts'],
  moduleFileExtensions: ['ts', 'tsx', 'js', 'jsx', 'json'],
  collectCoverageFrom: [
    'src/**/*.{ts,tsx}',
    '!src/**/*.d.ts',
    '!src/**/*.test.ts',
  ],
  coverageThreshold: {
    global: {
      branches: 70,
      functions: 80,
      lines: 80,
    },
  },
  setupFilesAfterEnv: ['<rootDir>/src/test/setup.ts'],
};

export default config;
```

### Basic Usage

```typescript
import { describe, it, expect, jest, beforeEach, afterEach } from '@jest/globals';

describe('UserService', () => {
  let service: UserService;
  let mockRepo: any;

  beforeEach(() => {
    mockRepo = {
      save: jest.fn(),
      findById: jest.fn(),
    };
    service = new UserService(mockRepo);
  });

  afterEach(() => {
    jest.clearAllMocks();
  });

  it('should create user', () => {
    mockRepo.save.mockReturnValue({ id: '1', name: 'John' });

    const result = service.createUser({ name: 'John' });

    expect(result.id).toBe('1');
    expect(mockRepo.save).toHaveBeenCalledWith({ name: 'John' });
  });
});
```

### Mocking

```typescript
// Function mock
const mockFn = jest.fn();
mockFn.mockReturnValue('value');
mockFn.mockReturnValueOnce('first call');
mockFn.mockImplementation((arg) => arg * 2);

// Spy
const spy = jest.spyOn(object, 'method');
spy.mockReturnValue('mocked');

// Module mock
jest.mock('./module', () => ({
  default: jest.fn(),
  namedExport: jest.fn(),
}));

// Mock restoration
spy.mockRestore();
jest.restoreAllMocks();
```

### Running Tests

```bash
# Run all tests
jest

# Run in watch mode
jest --watch

# Run with coverage
jest --coverage

# Run specific file
jest path/to/test.ts

# Update snapshots
jest --updateSnapshot
```

---

## Migration Guide

### Jest to Vitest Migration

**Step 1: Install Vitest**

```bash
npm install -D vitest @vitest/ui
npm uninstall ts-jest @types/jest
```

**Step 2: Create Vitest Config**

```typescript
// vitest.config.ts
import { defineConfig } from 'vitest/config';

export default defineConfig({
  test: {
    globals: true,
    environment: 'jsdom',
    coverage: {
      provider: 'v8',
      reporter: ['text', 'json', 'html'],
    },
  },
});
```

**Step 3: Update Imports**

```typescript
// Before (Jest)
import { describe, it, expect, jest, beforeEach } from '@jest/globals';

// After (Vitest)
import { describe, it, expect, vi, beforeEach } from 'vitest';
```

**Step 4: Update Mocks**

```typescript
// Before (Jest)
jest.mock('./module');
jest.fn();
jest.spyOn(obj, 'method');
jest.useFakeTimers();

// After (Vitest)
vi.mock('./module');
vi.fn();
vi.spyOn(obj, 'method');
vi.useFakeTimers();
```

**Step 5: Update Package Scripts**

```json
{
  "scripts": {
    "test": "vitest",
    "test:run": "vitest run",
    "test:coverage": "vitest run --coverage",
    "test:ui": "vitest --ui"
  }
}
```

**Step 6: Update tsconfig (if needed)**

```json
{
  "compilerOptions": {
    "types": ["vitest/globals"]
  }
}
```

### Compatibility Notes

| Jest Feature | Vitest Equivalent |
|--------------|-------------------|
| `jest.fn()` | `vi.fn()` |
| `jest.mock()` | `vi.mock()` |
| `jest.spyOn()` | `vi.spyOn()` |
| `jest.useFakeTimers()` | `vi.useFakeTimers()` |
| `jest.setTimeout()` | `vi.setConfig({ testTimeout: ... })` |
| `jest.retryTimes()` | `vi.setConfig({ retry: ... })` |
| `expect.any()` | `expect.any()` (same) |
| `expect.objectContaining()` | `expect.objectContaining()` (same) |

---

## Playwright (E2E)

### Installation

```bash
npm install -D @playwright/test
npx playwright install
```

### Configuration

```typescript
// playwright.config.ts
import { defineConfig, devices } from '@playwright/test';

export default defineConfig({
  testDir: './e2e',
  fullyParallel: true,
  forbidOnly: !!process.env.CI,
  retries: process.env.CI ? 2 : 0,
  workers: process.env.CI ? 1 : undefined,
  reporter: 'html',
  use: {
    baseURL: 'http://localhost:3000',
    trace: 'on-first-retry',
  },
  projects: [
    {
      name: 'chromium',
      use: { ...devices['Desktop Chrome'] },
    },
    {
      name: 'firefox',
      use: { ...devices['Desktop Firefox'] },
    },
  ],
  webServer: {
    command: 'npm run dev',
    url: 'http://localhost:3000',
    reuseExistingServer: !process.env.CI,
  },
});
```

### Basic Test

```typescript
import { test, expect } from '@playwright/test';

test('user can login', async ({ page }) => {
  await page.goto('/login');

  await page.fill('[name="email"]', 'user@test.com');
  await page.fill('[name="password"]', 'password');
  await page.click('button[type="submit"]');

  await expect(page).toHaveURL('/dashboard');
  await expect(page.locator('h1')).toContainText('Welcome');
});
```

---

## Testing Library (DOM)

### Installation

```bash
npm install -D @testing-library/react @testing-library/user-event
```

### React Component Testing

```typescript
import { render, screen, fireEvent } from '@testing-library/react';
import userEvent from '@testing-library/user-event';
import { describe, it, expect, vi } from 'vitest';

describe('LoginForm', () => {
  it('should submit form with valid credentials', async () => {
    const user = userEvent.setup();
    const mockSubmit = vi.fn();

    render(<LoginForm onSubmit={mockSubmit} />);

    await user.type(screen.getByLabelText(/email/i), 'john@test.com');
    await user.type(screen.getByLabelText(/password/i), 'password123');
    await user.click(screen.getByRole('button', { name: /login/i }));

    expect(mockSubmit).toHaveBeenCalledWith({
      email: 'john@test.com',
      password: 'password123',
    });
  });

  it('should show error for invalid email', async () => {
    const user = userEvent.setup();

    render(<LoginForm onSubmit={vi.fn()} />);

    await user.type(screen.getByLabelText(/email/i), 'invalid');
    await user.click(screen.getByRole('button', { name: /login/i }));

    expect(screen.getByText(/invalid email/i)).toBeInTheDocument();
  });
});
```

### Query Priorities

Testing Library recommends this priority for queries:

1. **getByRole** - Most accessible, reflects user experience
2. **getByLabelText** - Good for form elements
3. **getByPlaceholderText** - For inputs without labels
4. **getByText** - For non-interactive elements
5. **getByTestId** - Last resort, requires test IDs

```typescript
// Preferred
screen.getByRole('button', { name: /submit/i });
screen.getByLabelText(/email/i);

// Avoid
screen.getByTestId('submit-button');
container.querySelector('.submit-btn');
```

### waitFor

```typescript
import { waitFor } from '@testing-library/react';

it('waits for async content', async () => {
  render(<Component />);

  await waitFor(() => {
    expect(screen.getByText('Loaded')).toBeInTheDocument();
  });

  // Or with specific options
  await waitFor(
    () => expect(screen.getByText('Loaded')).toBeInTheDocument(),
    { timeout: 3000, interval: 100 }
  );
});
```

---

## Quick Reference

### Framework Commands

```bash
# Vitest
vitest                  # Run in watch mode
vitest run              # Run once
vitest run --coverage   # Run with coverage
vitest --ui             # Open UI

# Jest
jest                    # Run tests
jest --watch            # Watch mode
jest --coverage         # With coverage
jest --updateSnapshot   # Update snapshots

# Playwright
npx playwright test     # Run E2E tests
npx playwright test --ui  # UI mode
npx playwright test --headed  # Run with browser visible
```

### Import Patterns

```typescript
// Vitest
import { describe, it, expect, vi, beforeEach, afterEach } from 'vitest';

// Jest
import { describe, it, expect, jest, beforeEach, afterEach } from '@jest/globals';

// Testing Library
import { render, screen, fireEvent, waitFor } from '@testing-library/react';
import userEvent from '@testing-library/user-event';
```
