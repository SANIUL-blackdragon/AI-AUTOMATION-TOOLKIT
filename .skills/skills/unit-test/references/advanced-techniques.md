# Advanced Testing Techniques

Deep dive into advanced testing methodologies for enhanced test quality and coverage.

## Table of Contents

- [Parameterized Testing](#parameterized-testing)
- [Property-Based Testing](#property-based-testing)
- [Mutation Testing](#mutation-testing)
- [Snapshot Testing](#snapshot-testing)
- [Contract Testing](#contract-testing)
- [Flaky Test Detection](#flaky-test-detection)
- [Test Observability](#test-observability)

---

## Parameterized Testing

Run the same test logic with multiple inputs to reduce code duplication and increase coverage.

### Basic Implementation

```typescript
describe('EmailValidator', () => {
  const testCases = [
    { input: 'user@example.com', expected: true, description: 'valid email' },
    { input: 'user.name@example.com', expected: true, description: 'email with dot' },
    { input: 'user+tag@example.com', expected: true, description: 'email with plus' },
    { input: 'invalid', expected: false, description: 'no @ symbol' },
    { input: '@example.com', expected: false, description: 'no local part' },
    { input: 'user@', expected: false, description: 'no domain' },
    { input: '', expected: false, description: 'empty string' },
    { input: null, expected: false, description: 'null value' },
  ];

  test.each(testCases)('should return $expected for $description', ({ input, expected }) => {
    expect(isValidEmail(input)).toBe(expected);
  });
});
```

### With Complex Test Data

```typescript
describe('Calculator', () => {
  const operations = [
    { a: 2, b: 3, op: 'add', expected: 5 },
    { a: 10, b: 4, op: 'subtract', expected: 6 },
    { a: 3, b: 4, op: 'multiply', expected: 12 },
    { a: 20, b: 5, op: 'divide', expected: 4 },
  ];

  test.each(operations)('$a $op $b = $expected', ({ a, b, op, expected }) => {
    const result = calculator[op](a, b);
    expect(result).toBe(expected);
  });
});
```

### Vitest describe.each

```typescript
describe.each([
  { input: 'hello', expected: 5 },
  { input: 'world', expected: 5 },
  { input: '', expected: 0 },
])('stringLength($input)', ({ input, expected }) => {
  it(`should return ${expected}`, () => {
    expect(stringLength(input)).toBe(expected);
  });
});
```

---

## Property-Based Testing

Test properties (invariants) that should hold for all inputs using generated random data.

### Installation

```bash
npm install -D fast-check
```

### Basic Usage

```typescript
import { fc } from 'fast-check';

describe('sort', () => {
  it('should return array of same length', () => {
    fc.assert(
      fc.property(fc.array(fc.integer()), (arr) => {
        expect(sort(arr)).toHaveLength(arr.length);
      })
    );
  });

  it('should be idempotent', () => {
    fc.assert(
      fc.property(fc.array(fc.integer()), (arr) => {
        expect(sort(sort(arr))).toEqual(sort(arr));
      })
    );
  });

  it('should contain same elements', () => {
    fc.assert(
      fc.property(fc.array(fc.integer()), (arr) => {
        const sorted = sort(arr);
        expect([...sorted].sort()).toEqual([...arr].sort());
      })
    );
  });
});
```

### Common Properties to Test

| Property | Description | Example |
|----------|-------------|---------|
| **Inverse** | Operation reverses itself | `decode(encode(x)) == x` |
| **Idempotent** | Repeated application same as once | `sort(sort(x)) == sort(x)` |
| **Commutative** | Order doesn't matter | `add(a, b) == add(b, a)` |
| **Associative** | Grouping doesn't matter | `add(add(a, b), c) == add(a, add(b, c))` |
| **Identity** | Has neutral element | `add(x, 0) == x` |

### Advanced Examples

```typescript
describe('string operations', () => {
  it('concatenation preserves length', () => {
    fc.assert(
      fc.property(fc.string(), fc.string(), (a, b) => {
        return (a + b).length === a.length + b.length;
      })
    );
  });

  it('substring is always within bounds', () => {
    fc.assert(
      fc.property(
        fc.string({ maxLength: 100 }),
        fc.nat(100),
        fc.nat(100),
        (str, start, end) => {
          const sub = str.substring(Math.min(start, end), Math.max(start, end));
          return sub.length <= str.length;
        }
      )
    );
  });
});

describe('JSON operations', () => {
  it('parse(stringify(x)) equals x for serializable values', () => {
    fc.assert(
      fc.property(
        fc.anything({ withBigInt: true, withDate: true, withMap: true, withSet: true }),
        (value) => {
          // Custom replacer for special types
          const str = JSON.stringify(value, replacer);
          const parsed = JSON.parse(str, reviver);
          expect(parsed).toEqual(value);
        }
      )
    );
  });
});
```

### With Custom Arbitraries

```typescript
// Define custom arbitrary for User type
const userArbitrary = fc.record({
  id: fc.string({ minLength: 1, maxLength: 10 }),
  name: fc.string({ minLength: 1, maxLength: 50 }),
  email: fc.string().filter(s => s.includes('@')),
  age: fc.integer({ min: 0, max: 120 }),
});

describe('UserService', () => {
  it('preserves user data on create', () => {
    fc.assert(
      fc.property(userArbitrary, (user) => {
        const saved = userService.create(user);
        expect(saved.name).toBe(user.name);
        expect(saved.email).toBe(user.email);
        expect(saved.age).toBe(user.age);
      })
    );
  });
});
```

---

## Mutation Testing

Measure test suite quality by introducing bugs and checking if tests detect them.

### How It Works

1. Mutation tool creates modified versions of code (mutants)
2. Each mutant has a small change (e.g., `+` → `-`, `true` → `false`)
3. Tests run against each mutant
4. If tests fail → mutant is "killed" (good!)
5. If tests pass → mutant "survived" (test gap!)

### Common Mutation Operators

| Operator | Original | Mutated |
|----------|----------|---------|
| Arithmetic | `a + b` | `a - b` |
| Conditional | `if (x)` | `if (!x)` |
| Relational | `a > b` | `a >= b` |
| Logical | `a && b` | `a \|\| b` |
| Return | `return x` | `return null` |
| Increment | `i++` | `i--` |

### Using Stryker (JavaScript/TypeScript)

```bash
npm install -D @stryker-mutator/core @stryker-mutator/vitest-runner
```

```javascript
// stryker.config.json
{
  "$schema": "./node_modules/@stryker-mutator/core/schema/stryker-schema.json",
  "packageManager": "npm",
  "testRunner": "vitest",
  "coverageAnalysis": "perTest",
  "mutate": ["src/**/*.ts", "!src/**/*.test.ts"],
  "thresholds": {
    "high": 85,
    "low": 70,
    "break": 60
  }
}
```

### Example: Detecting Weak Tests

```typescript
// Code under test
function discount(price: number, member: boolean): number {
  if (member) {
    return price * 0.9;
  }
  return price;
}

// ❌ WEAK TEST: Doesn't check discount amount
it('applies discount for members', () => {
  const result = discount(100, true);
  expect(result).toBeDefined(); // Mutation survives!
});

// ✅ STRONG TEST: Checks exact behavior
it('applies 10% discount for members', () => {
  expect(discount(100, true)).toBe(90); // Kills mutant
  expect(discount(100, false)).toBe(100); // Kills mutant
});
```

### Mutation Score Goals

- **< 50%**: Critical test gaps
- **50-70%**: Needs improvement
- **70-85%**: Good coverage
- **> 85%**: Excellent test suite

---

## Snapshot Testing

Capture and compare output against stored "snapshot."

### When to Use

- UI component rendering
- Large, complex output
- API response validation
- Configuration validation

### When NOT to Use

- Simple values (use explicit assertions)
- Tests that should have specific assertions
- Code that changes frequently

### Vitest Snapshots

```typescript
import { render } from '@testing-library/react';

describe('UserCard', () => {
  it('renders correctly', () => {
    const user = { name: 'John', email: 'john@test.com', role: 'admin' };
    const { container } = render(<UserCard user={user} />);
    expect(container).toMatchSnapshot();
  });

  it('matches inline snapshot', () => {
    const config = generateConfig();
    expect(config).toMatchInlineSnapshot(`
      {
        "apiUrl": "https://api.example.com",
        "timeout": 5000,
        "retries": 3
      }
    `);
  });
});
```

### Best Practices

```typescript
// ✅ Good: Named snapshots for clarity
expect(result).toMatchSnapshot('user-creation-response');

// ✅ Good: Property matchers for dynamic values
expect(result).toMatchSnapshot({
  id: expect.any(String),
  createdAt: expect.any(Date),
});

// ✅ Good: Review snapshot diffs carefully
// Don't blindly update with --updateSnapshot

// ❌ Bad: Snapshot everything
expect(everything).toMatchSnapshot(); // Too broad

// ❌ Bad: Snapshot implementation details
expect(internalState).toMatchSnapshot(); // Tests internals
```

---

## Contract Testing

Verify API compatibility between services without requiring both services to run simultaneously.

### Consumer-Driven Contract Testing

```
┌──────────────┐     ┌──────────────┐     ┌──────────────┐
│   Consumer   │────▶│    Broker    │◀────│   Provider   │
│   Service    │     │   (Pact)     │     │   Service    │
└──────────────┘     └──────────────┘     └──────────────┘
       │                    │                    │
       │ 1. Define          │                    │
       │    expectations    │ 2. Publish         │
       │                    │    contract        │
       │                    │                    │
       │                    │        3. Verify   │
       │                    │           contract │
       ▼                    ▼                    ▼
```

### Using Pact

```typescript
// Consumer Side
import { PactV3 } from '@pact-foundation/pact';

const provider = new PactV3({
  consumer: 'UserService',
  provider: 'PaymentService',
});

describe('Payment API Contract', () => {
  it('should process payment', async () => {
    await provider
      .given('user exists with id 123')
      .uponReceiving('a request to process payment')
      .withRequest({
        method: 'POST',
        path: '/payments',
        headers: { 'Content-Type': 'application/json' },
        body: { userId: '123', amount: 100 },
      })
      .willRespondWith({
        status: 200,
        headers: { 'Content-Type': 'application/json' },
        body: { transactionId: like('tx-123'), status: 'completed' },
      });

    await provider.executeTest(async (mockServer) => {
      const result = await processPayment(mockServer.url, {
        userId: '123',
        amount: 100,
      });
      expect(result.status).toBe('completed');
    });
  });
});
```

```typescript
// Provider Side
import { Verifier } from '@pact-foundation/pact';

describe('Pact Verification', () => {
  it('should verify consumer contracts', async () => {
    const verifier = new Verifier({
      providerBaseUrl: 'http://localhost:3000',
      pactBrokerUrl: 'https://broker.pactflow.io',
      provider: 'PaymentService',
      providerVersion: '1.0.0',
    });

    await verifier.verifyProvider();
  });
});
```

### Contract vs Integration Testing

| Aspect | Contract Testing | Integration Testing |
|--------|-----------------|-------------------|
| **Scope** | API contract only | Full integration |
| **Speed** | Very fast | Slower |
| **Dependencies** | None required | All services running |
| **Environment** | Isolated | Integrated |
| **Cost** | Low | High |

---

## Flaky Test Detection

### Common Causes

| Category | Cause | Example |
|----------|-------|---------|
| **Async Issues** | Race conditions | `setTimeout` timing |
| **State Leakage** | Shared mutable state | Global variables |
| **Environment** | External dependencies | Network, database |
| **Time Dependencies** | Date/time assumptions | `new Date()` |
| **Concurrency** | Parallel test interference | Port conflicts |
| **Randomness** | Non-seeded random | `Math.random()` |

### Detection Patterns

```typescript
// Run each test N times to detect flakiness
async function detectFlakyTests(tests: Test[], runs: number = 10): Promise<FlakyTest[]> {
  const results = new Map<string, { passed: number; failed: number }>();

  for (const test of tests) {
    for (let i = 0; i < runs; i++) {
      const result = await runTest(test);
      const stats = results.get(test.name) || { passed: 0, failed: 0 };
      result.passed ? stats.passed++ : stats.failed++;
      results.set(test.name, stats);
    }
  }

  const flakyTests: FlakyTest[] = [];
  for (const [name, stats] of results) {
    if (stats.passed > 0 && stats.failed > 0) {
      flakyTests.push({
        name,
        flakiness: stats.failed / (stats.passed + stats.failed),
      });
    }
  }

  return flakyTests.sort((a, b) => b.flakiness - a.flakiness);
}
```

### Fixing Flaky Tests

```typescript
// ❌ FLAKY: Race condition
it('updates UI', async () => {
  fetchData();
  await new Promise(r => setTimeout(r, 100)); // Arbitrary wait
  expect(screen.getByText('Loaded')).toBeInTheDocument();
});

// ✅ FIXED: Wait for condition
it('updates UI', async () => {
  fetchData();
  await waitFor(() => {
    expect(screen.getByText('Loaded')).toBeInTheDocument();
  });
});

// ❌ FLAKY: Shared state
let counter = 0;
it('test 1', () => { counter++; expect(counter).toBe(1); });
it('test 2', () => { counter++; expect(counter).toBe(1); }); // Depends on order

// ✅ FIXED: Isolated state
it('test 1', () => {
  const counter = new Counter();
  counter.increment();
  expect(counter.value).toBe(1);
});

// ❌ FLAKY: Real time
it('calculates age', () => {
  const age = calculateAge(new Date('1990-01-01'));
  expect(age).toBe(34); // Fails next year
});

// ✅ FIXED: Injected time
it('calculates age', () => {
  const now = new Date('2024-01-01');
  const age = calculateAge(new Date('1990-01-01'), now);
  expect(age).toBe(34); // Always passes
});
```

### Prevention Checklist

- [ ] Use fake timers for time-dependent tests
- [ ] Always `await` async operations
- [ ] Never share mutable state between tests
- [ ] Seed random generators
- [ ] Mock external dependencies
- [ ] Clean up resources in `afterEach`
- [ ] Use `waitFor` for UI changes
- [ ] Isolate database state
- [ ] Use unique identifiers for test resources

---

## Test Observability

### OpenTelemetry Integration

```typescript
import { trace } from '@opentelemetry/api';

const tracer = trace.getTracer('test-runner');

describe('UserService', () => {
  it('should create user', async () => {
    const span = tracer.startSpan('test:create-user');

    try {
      span.addEvent('setup-test-data');
      const userData = { name: 'John', email: 'john@test.com' };

      span.addEvent('execute-service-call');
      const result = await userService.createUser(userData);

      span.addEvent('verify-results');
      expect(result.id).toBeDefined();

      span.setStatus({ code: SpanStatusCode.OK });
    } catch (error) {
      span.setStatus({ code: SpanStatusCode.ERROR, message: error.message });
      throw error;
    } finally {
      span.end();
    }
  });
});
```

### Correlating Failures with Telemetry

```typescript
interface TestTelemetry {
  testId: string;
  duration: number;
  cpuUsage: number;
  memoryUsage: number;
  networkLatency: number;
  databaseQueries: number;
}

async function detectFlakyPatterns(testName: string): Promise<FlakyPattern[]> {
  const failures = await getTestFailures(testName);
  const patterns: FlakyPattern[] = [];

  for (const failure of failures) {
    const telemetry = await getTestTelemetry(failure.testRunId);

    if (telemetry.networkLatency > 500) {
      patterns.push({ type: 'network-latency', confidence: 0.8 });
    }

    if (telemetry.memoryUsage > 0.9) {
      patterns.push({ type: 'memory-pressure', confidence: 0.7 });
    }

    if (telemetry.databaseQueries > 100) {
      patterns.push({ type: 'database-contention', confidence: 0.6 });
    }
  }

  return patterns;
}
```

---

## Quick Reference

### When to Use Each Technique

| Technique | When to Use |
|-----------|-------------|
| **Parameterized** | Same logic, different inputs |
| **Property-Based** | Mathematical properties, edge cases |
| **Mutation** | Measure test quality, find gaps |
| **Snapshot** | UI components, large output |
| **Contract** | Microservices, API compatibility |
| **Observability** | Debug flaky tests, production correlation |

### Tool Selection

| Purpose | Tool |
|---------|------|
| Property-based | fast-check |
| Mutation | Stryker |
| Contract | Pact |
| E2E | Playwright |
| DOM Testing | Testing Library |
| Observability | OpenTelemetry |
