---
name: unit-test
description: "Comprehensive unit testing guidance for any project type (frontend, backend, full-stack, microservices, libraries). Covers test creation workflow, TDD, test doubles selection (mocks, stubs, spies, fakes), quality standards (FIRST principles, AAA pattern), framework detection (Vitest, Jest, Playwright), anti-patterns, and AI-assisted test generation. Use when: (1) Writing unit tests for any code, (2) Setting up testing infrastructure, (3) Choosing between test doubles, (4) Debugging test failures or flaky tests, (5) Improving test coverage and quality, (6) Queries containing \"test\", \"mock\", \"stub\", \"spy\", \"coverage\", \"TDD\", \"assert\", \"expect\", or \"how to test\"."
---

# Unit Testing

Expert guidance for writing high-quality unit tests across any project type and technology stack.

## Quick Start

**To write a unit test, follow this workflow:**

```
1. IDENTIFY → What is the System Under Test (SUT)?
2. DETECT   → What testing framework does this project use?
3. ISOLATE  → What dependencies need to be replaced with test doubles?
4. WRITE    → Apply AAA pattern (Arrange-Act-Assert)
5. NAME     → Use descriptive naming: should_[behavior]_when_[condition]
6. VERIFY   → Check against quality checklist
```

**Immediate Test Template:**

```typescript
describe('SystemUnderTest', () => {
  describe('methodName', () => {
    it('should [expected behavior] when [condition]', () => {
      // ARRANGE: Set up test preconditions
      const dependency = createTestDouble();
      const sut = new SystemUnderTest(dependency);

      // ACT: Execute the code under test
      const result = sut.methodName(input);

      // ASSERT: Verify the outcome
      expect(result).toEqual(expectedOutput);
    });
  });
});
```

---

## Core Workflow

### The AAA Pattern (Arrange-Act-Assert)

Every unit test must follow this three-phase structure:

| Phase | Purpose | Actions |
|-------|---------|---------|
| **Arrange** | Set up preconditions | Create objects, configure mocks, initialize data |
| **Act** | Execute code under test | Call method, trigger event, invoke function |
| **Assert** | Verify outcome | Check return values, verify state, confirm mock interactions |

**Well-Structured Example:**

```typescript
describe('OrderService', () => {
  describe('placeOrder', () => {
    it('should apply discount when valid promo code provided', () => {
      // ARRANGE
      const mockDiscountService = {
        validateCode: vi.fn().mockReturnValue({ valid: true, percentage: 10 })
      };
      const mockRepository = {
        save: vi.fn().mockReturnValue({ id: 'order-123' })
      };
      const service = new OrderService(mockDiscountService, mockRepository);
      const items = [{ productId: 'p1', price: 100, quantity: 2 }];
      const promoCode = 'SAVE10';

      // ACT
      const result = service.placeOrder(items, promoCode);

      // ASSERT
      expect(result.total).toBe(180); // 200 * 0.9
      expect(result.discountApplied).toBe(20);
      expect(mockDiscountService.validateCode).toHaveBeenCalledWith('SAVE10');
    });
  });
});
```

---

## FIRST Principles (Quality Standards)

Every unit test must satisfy these non-negotiable characteristics:

### F - Fast ⚡
- **Target**: < 10 seconds for full suite, < 100ms per test
- **How**: Mock all external dependencies (database, network, filesystem)
- **Killers**: Database calls, HTTP requests, file I/O, thread sleeps

### I - Isolated 🔒
- Each test runs independently
- No shared mutable state between tests
- Tests can run in any order
- Each test creates its own fixtures

### R - Repeatable 🔁
- Identical results every run, any environment
- No randomness without seeded generators
- No time dependencies without injected clocks
- No external state

### S - Self-Validating ✅
- Automatic pass/fail determination
- Clear assertions with expected values
- No manual verification or log inspection

### T - Timely ⏰
- Write tests close to production code
- Prefer TDD (test-first) when possible
- Tests drive better, more testable design

---

## Test Double Selection

**Critical Decision Matrix:**

```
What do you need from the dependency?
│
├─ Nothing (just fill parameter) → DUMMY
│   └─ Example: Logger that isn't used in test
│
├─ Fixed/canned response → STUB
│   └─ Example: Repository that returns predefined user
│
├─ Verify interactions → MOCK
│   └─ Example: Check email service was called with correct params
│
├─ Record all interactions → SPY
│   └─ Example: Capture all calls for later inspection
│
└─ Working implementation → FAKE
    └─ Example: In-memory database for CRUD operations
```

**Quick Reference Table:**

| Scenario | Use | Reason |
|----------|-----|--------|
| Parameter filler, never used | Dummy | Just satisfies type system |
| Need fixed return value | Stub | Simple, no behavior needed |
| Need to verify specific calls | Mock | Pre-set expectations |
| Need to capture interactions | Spy | Record everything |
| Need actual working behavior | Fake | Simulates real component |

**See [test-doubles.md](references/test-doubles.md) for detailed implementation patterns.**

---

## Framework Detection

Detect the appropriate testing framework based on project configuration:

### Vitest (Recommended for new projects)
**Detection signals:**
- `vite.config.ts` or `vitest.config.ts` exists
- `package.json` contains `vitest` dependency
- ESM-first codebase
- Vite-based project

**Syntax:**
```typescript
import { describe, it, expect, vi, beforeEach } from 'vitest';

// Mocking
vi.mock('./module');
vi.fn();
vi.spyOn(obj, 'method').mockReturnValue(value);

// Timers
vi.useFakeTimers();
vi.useRealTimers();
```

### Jest (Legacy projects)
**Detection signals:**
- `jest.config.js` or `jest.config.ts` exists
- `package.json` contains `jest` dependency
- React Native projects
- Large existing Jest codebase

**Syntax:**
```typescript
import { describe, it, expect, jest, beforeEach } from '@jest/globals';

// Mocking
jest.mock('./module');
jest.fn();
jest.spyOn(obj, 'method').mockReturnValue(value);
```

### Migration Note (2025)
Vitest offers 10x faster test execution. For new projects or Vite-based projects, prefer Vitest. See [frameworks.md](references/frameworks.md) for migration guide.

---

## Test Naming Conventions

**Standard Patterns:**

```
should_[expectedBehavior]_when_[condition]
[MethodName]_[Scenario]_[ExpectedResult]
given_[precondition]_when_[action]_then_[result]
```

**Examples:**

```typescript
// ✅ GOOD: Descriptive, complete
it('should_returnUser_whenValidId')
it('should_throwValidationException_whenEmailInvalid')
it('should_applyDiscount_whenPromoCodeValid')

// ❌ BAD: Vague, unhelpful
it('test1')
it('works')
it('test user')
```

**Scenario Templates:**

| Scenario Type | Naming Pattern |
|---------------|----------------|
| Happy path | `should_return_X_when_Y` |
| Validation error | `should_throw_X_when_Y_invalid` |
| Edge case | `should_handle_X_gracefully` |
| State change | `should_update_X_when_Y` |

---

## Quality Checklist

**Before committing any test, verify:**

- [ ] **Naming**: Test name describes the behavior being verified
- [ ] **Structure**: Follows AAA pattern with clear separation
- [ ] **Focus**: Tests exactly one behavior (one concept per test)
- [ ] **Independence**: Can run alone, in any order
- [ ] **Determinism**: Same result every time (no flakiness)
- [ ] **Speed**: Runs in milliseconds
- [ ] **Assertions**: Clear, specific expected values
- [ ] **No Logic**: Test contains no if/else, loops, or calculations

**Coverage targets (guidelines, not rules):**
- Line coverage: > 80%
- Branch coverage: > 70%
- Focus on critical paths, not arbitrary percentages

---

## Anti-Patterns to Avoid

| Anti-Pattern | Problem | Solution |
|--------------|---------|----------|
| **Liar Test** | Always passes | Include real assertions |
| **Giant Test** | Tests multiple things | Split into focused tests |
| **Mockery** | Everything mocked | Balance with real behavior tests |
| **Inspector** | Tests private methods | Test public interface only |
| **Slow Poke** | Takes too long | Remove I/O, mock dependencies |
| **Free Rider** | Depends on other tests | Make each test independent |
| **Happy Path Only** | No error cases | Add negative tests |
| **Local Hero** | Only works on dev machine | Remove environment dependencies |
| **Mystery Guest** | Uses hidden external data | Make test data visible in test |
| **Assertion Roulette** | Multiple assertions without context | Separate tests or use explicit messages |

---

## Handling Test Failures

**Debugging Workflow:**

```
Test failing?
│
├─ Is it flaky? (sometimes passes, sometimes fails)
│   ├─ Check for race conditions → Use waitFor() instead of arbitrary delays
│   ├─ Check for shared state → Ensure test isolation
│   ├─ Check for time dependencies → Inject clock, use fake timers
│   └─ Check for randomness → Seed random generators
│
├─ Is it a legitimate failure?
│   ├─ Verify the test is correct
│   ├─ Check if production code changed
│   └─ Review assertion logic
│
└─ Is it environment-related?
    ├─ Check for missing mocks
    ├─ Verify test configuration
    └─ Check for external dependencies
```

**Common Fixes:**

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
```

---

## TDD Workflow (Test-Driven Development)

**Red-Green-Refactor Cycle:**

```
    ┌─────────────────────────────────────┐
    │                                     │
    ▼                                     │
┌────────┐                           ┌────────┐
│  RED   │ ─────────────────────────▶│ GREEN  │
└────────┘   Write minimal code      └────────┘
     │        to pass the test            │
     │                                     │
     │     ┌───────────────────────────────┘
     │     │
     │     ▼
     │ ┌──────────┐
     └─│ REFACTOR │
       └──────────┘
```

**Three Laws of TDD:**
1. You may not write production code until you have written a failing unit test
2. You may not write more of a unit test than is sufficient to fail
3. You may not write more production code than is sufficient to pass the failing test

**When to use TDD:**
- New feature development
- Bug fixes (write test that reproduces bug first)
- Complex business logic
- APIs and libraries

---

## AI-Assisted Test Generation (2025)

**Best Practices for AI-Generated Tests:**

1. **Provide Context**: Include the function/class and its dependencies
2. **Specify Requirements**: Mention edge cases, error conditions, expected behavior
3. **Review Output**: Always validate AI-generated tests for correctness
4. **Strengthen Assertions**: AI may generate weak assertions—make them specific
5. **Add Missing Cases**: AI may miss domain-specific edge cases

**Effective Prompt Structure:**

```
Generate unit tests for [function/class]:

**Code:**
[paste the code]

**Requirements:**
- Test all happy paths
- Test edge cases (null, empty, boundary values)
- Test error conditions
- Use "should_X_when_Y" naming pattern
- Follow AAA pattern
- Framework: [Vitest/Jest]
```

**AI Testing Tools (2025):**
- GitHub Copilot: IDE-integrated test generation
- Cursor: AI IDE with test workflow
- Codium AI: Comprehensive test suite generation
- Diffblue Cover: Autonomous Java test generation

---

## Advanced Topics

**When to explore these references:**

- **Test Doubles Deep Dive**: [test-doubles.md](references/test-doubles.md)
  - Detailed implementation patterns for all double types
  - When to use each in specific scenarios

- **Framework Specifics**: [frameworks.md](references/frameworks.md)
  - Vitest vs Jest detailed comparison
  - Migration guide from Jest to Vitest
  - Framework-specific configuration

- **Advanced Techniques**: [advanced-techniques.md](references/advanced-techniques.md)
  - Property-based testing with fast-check
  - Mutation testing for test quality
  - Contract testing for microservices
  - Snapshot testing

---

## Test Organization

**File Structure:**

```
src/
├── services/
│   ├── UserService.ts
│   └── __tests__/
│       ├── UserService.test.ts        # Unit tests
│       ├── UserService.integration.ts # Integration tests
│       └── fixtures/
│           └── userFixtures.ts        # Test data builders
```

**Describe Block Hierarchy:**

```typescript
describe('UserService', () => {           // System Under Test
  describe('createUser', () => {          // Method
    describe('validation', () => {        // Feature/Concern
      it('should reject invalid email', () => {});
      it('should reject short password', () => {});
    });
    describe('persistence', () => {
      it('should save user to repository', () => {});
    });
  });
});
```

---

## Quick Reference Card

### Test Double Selection
```
Need to...                          → Use...
─────────────────────────────────────────────────────
Fill parameter list                  → Dummy
Return canned response               → Stub
Verify specific interactions         → Mock
Record all interactions              → Spy
Have working implementation          → Fake
```

### Common Assertions
```typescript
expect(result).toBe(value)                    // Exact match
expect(result).toEqual(object)                // Deep equality
expect(result).toContain(substring)           // Contains
expect(result).toHaveLength(n)                // Array/string length
expect(fn).toThrow(Error)                     // Exception
expect(mock).toHaveBeenCalled()               // Mock called
expect(mock).toHaveBeenCalledWith(arg)        // Mock called with
```

### Framework Detection
```
vitest.config.ts or vite.config.ts  → Vitest
jest.config.*                        → Jest
playwright.config.*                  → Playwright (E2E)
```
