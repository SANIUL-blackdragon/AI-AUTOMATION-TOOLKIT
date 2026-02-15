# Test Doubles: The Complete Guide

Test Doubles are objects that stand in for real dependencies during testing. Understanding when and how to use each type is crucial for effective unit testing.

## Table of Contents

- [Taxonomy Overview](#taxonomy-overview)
- [Dummy Objects](#dummy-objects)
- [Stubs](#stubs)
- [Spies](#spies)
- [Mocks](#mocks)
- [Fakes](#fakes)
- [Selection Decision Tree](#selection-decision-tree)
- [Mocking Best Practices](#mocking-best-practices)
- [Common Mistakes](#common-mistakes)

---

## Taxonomy Overview

```
                    Test Doubles
                         │
    ┌────────┬───────────┼───────────┬────────┐
    │        │           │           │        │
  Dummy    Stub        Fake        Spy      Mock
    │        │           │           │        │
    │        │           │           │        │
 Never    Canned     Working     Records   Pre-programmed
 used     answers   shortcut    calls     expectations
```

---

## Dummy Objects

**Purpose:** Fill parameter lists. Never actually used in the test.

**When to use:**
- Required parameter that doesn't affect test
- Satisfying type system requirements
- Constructor dependencies not invoked in test

**Implementation:**

```typescript
interface ILogger {
  log(message: string): void;
}

// Manual Dummy
class DummyLogger implements ILogger {
  log(message: string): void {
    // Do nothing - this is a dummy
  }
}

// Usage
it('should create user', () => {
  const dummyLogger = new DummyLogger();
  const service = new UserService(dummyLogger);
  // Test doesn't verify anything about logging
});
```

**With Mocking Library:**

```typescript
// Vitest/Jest - simplest dummy
const dummyLogger = {} as ILogger; // Just cast to satisfy type

// Or with vi.fn() (more explicit)
const dummyLogger = { log: vi.fn() };
```

---

## Stubs

**Purpose:** Provide canned (predefined) answers to calls made during the test.

**When to use:**
- Need a dependency to return specific value
- Simple query operations
- No need to verify interactions

**Implementation:**

```typescript
interface IUserRepository {
  findById(id: string): User | null;
  findAll(): User[];
}

// Manual Stub
class StubUserRepository implements IUserRepository {
  private users: User[];

  constructor(users: User[]) {
    this.users = users;
  }

  findById(id: string): User | null {
    return this.users.find(u => u.id === id) || null;
  }

  findAll(): User[] {
    return this.users;
  }
}

// Usage
it('should return user name', () => {
  const stubRepo = new StubUserRepository([
    { id: '1', name: 'John', email: 'john@test.com' }
  ]);
  const service = new UserService(stubRepo);

  expect(service.getUserName('1')).toBe('John');
});
```

**With Mocking Library:**

```typescript
// Vitest
const stubRepo = {
  findById: vi.fn().mockReturnValue({ id: '1', name: 'John' }),
  findAll: vi.fn().mockReturnValue([{ id: '1', name: 'John' }])
};

// Multiple return values (sequence)
const stubRepo = {
  findById: vi.fn()
    .mockReturnValueOnce({ id: '1', name: 'First' })
    .mockReturnValueOnce({ id: '2', name: 'Second' })
    .mockReturnValue(null) // Default for subsequent calls
};
```

**Conditional Responses:**

```typescript
const stubRepo = {
  findById: vi.fn((id) => {
    if (id === '1') return { id: '1', name: 'John' };
    if (id === '2') return { id: '2', name: 'Jane' };
    return null;
  })
};
```

---

## Spies

**Purpose:** Capture and record interactions for later verification. The real object is used, but interactions are tracked.

**When to use:**
- Need to verify interactions with real object
- Partial mocking (some methods real, some tracked)
- Testing without complete isolation

**Implementation:**

```typescript
interface IEmailService {
  sendEmail(to: string, subject: string, body: string): void;
}

// Manual Spy
class SpyEmailService implements IEmailService {
  public sentEmails: Array<{ to: string; subject: string; body: string }> = [];

  sendEmail(to: string, subject: string, body: string): void {
    this.sentEmails.push({ to, subject, body });
  }

  // Helper methods for verification
  getSentCount(): number {
    return this.sentEmails.length;
  }

  getLastEmail(): { to: string; subject: string; body: string } | undefined {
    return this.sentEmails[this.sentEmails.length - 1];
  }

  wasEmailSentTo(email: string): boolean {
    return this.sentEmails.some(e => e.to === email);
  }
}

// Usage
it('should send welcome email when user is created', () => {
  const spyEmail = new SpyEmailService();
  const service = new UserService(spyEmail);

  service.createUser({ name: 'John', email: 'john@test.com' });

  expect(spyEmail.getSentCount()).toBe(1);
  expect(spyEmail.getLastEmail()?.to).toBe('john@test.com');
  expect(spyEmail.getLastEmail()?.subject).toContain('Welcome');
});
```

**With Mocking Library:**

```typescript
// Vitest - Spy on existing object
const emailService = {
  sendEmail: (to: string, subject: string, body: string) => {
    // Real implementation or empty
  }
};

const spy = vi.spyOn(emailService, 'sendEmail');

// After execution
expect(spy).toHaveBeenCalledWith('john@test.com', 'Welcome!', expect.any(String));
expect(spy).toHaveBeenCalledTimes(1);

// Access all calls
console.log(spy.mock.calls); // Array of all call arguments
console.log(spy.mock.results); // Array of all return values
```

**Partial Spies:**

```typescript
// Spy on specific method while keeping others real
const service = new EmailService();
const sendSpy = vi.spyOn(service, 'sendEmail').mockImplementation(() => {
  // Custom behavior for this method
});

// Other methods still work normally
service.formatEmail('test'); // Real implementation
```

---

## Mocks

**Purpose:** Objects pre-programmed with expectations. Verify that specific interactions occurred.

**When to use:**
- Need to verify exact interactions
- Behavior verification (not just state)
- Strict contract verification

**Implementation:**

```typescript
// With Mocking Library (Vitest)
it('should call repository save with correct user', () => {
  // Create mock with expectations
  const mockRepo = {
    save: vi.fn().mockReturnValue({ id: '1', name: 'John' }),
    findById: vi.fn()
  };

  const service = new UserService(mockRepo);
  service.createUser({ name: 'John' });

  // Verify interactions
  expect(mockRepo.save).toHaveBeenCalledWith(
    expect.objectContaining({ name: 'John' })
  );
  expect(mockRepo.save).toHaveBeenCalledTimes(1);

  // Verify findById was NOT called
  expect(mockRepo.findById).not.toHaveBeenCalled();
});
```

**Mock with Return Values:**

```typescript
const mockPaymentGateway = {
  process: vi.fn()
    .mockResolvedValueOnce({ success: true, transactionId: 'tx-1' })
    .mockResolvedValueOnce({ success: false, error: 'Declined' })
};

// First call succeeds
const result1 = await mockPaymentGateway.process({ amount: 100 });
// Second call fails
const result2 = await mockPaymentGateway.process({ amount: 200 });
```

**Mock with Implementation:**

```typescript
const mockValidator = {
  validate: vi.fn((data) => {
    if (!data.email) throw new Error('Email required');
    if (!data.email.includes('@')) return { valid: false, error: 'Invalid email' };
    return { valid: true };
  })
};
```

**Advanced Matchers:**

```typescript
// Any value
expect(mock).toHaveBeenCalledWith(expect.anything());
expect(mock).toHaveBeenCalledWith(expect.any(String));

// Object containing
expect(mock).toHaveBeenCalledWith(
  expect.objectContaining({ name: 'John' })
);

// Array containing
expect(mock).toHaveBeenCalledWith(
  expect.arrayContaining([1, 2, 3])
);

// String matching
expect(mock).toHaveBeenCalledWith(
  expect.stringContaining('error')
);

// Custom matcher
expect(mock).toHaveBeenCalledWith(
  expect.stringMatching(/^[A-Z]{3}-\d{4}$/)
);
```

---

## Fakes

**Purpose:** Working implementations with shortcuts. Suitable for testing but not production.

**When to use:**
- Need actual behavior (CRUD operations)
- Complex interactions between operations
- Integration-style tests within unit test context

**Implementation:**

```typescript
interface IUserRepository {
  save(user: User): User;
  findById(id: string): User | null;
  findAll(): User[];
  delete(id: string): void;
}

// In-Memory Fake
class FakeUserRepository implements IUserRepository {
  private users: Map<string, User> = new Map();

  save(user: User): User {
    const savedUser = { ...user, id: user.id || this.generateId() };
    this.users.set(savedUser.id, savedUser);
    return savedUser;
  }

  findById(id: string): User | null {
    return this.users.get(id) || null;
  }

  findAll(): User[] {
    return Array.from(this.users.values());
  }

  delete(id: string): void {
    this.users.delete(id);
  }

  private generateId(): string {
    return `user-${Date.now()}-${Math.random().toString(36).substr(2, 9)}`;
  }

  // Test helpers
  clear(): void {
    this.users.clear();
  }

  count(): number {
    return this.users.size;
  }
}

// Usage - Full lifecycle test
it('should manage user lifecycle', () => {
  const fakeRepo = new FakeUserRepository();
  const service = new UserService(fakeRepo);

  // Create
  const created = service.createUser({ name: 'John' });
  expect(created.id).toBeDefined();

  // Read
  const found = service.getUser(created.id);
  expect(found.name).toBe('John');

  // Update
  const updated = service.updateUser(created.id, { name: 'Jane' });
  expect(updated.name).toBe('Jane');

  // Delete
  service.deleteUser(created.id);
  expect(service.getUser(created.id)).toBeNull();
});
```

**Fake with Query Capabilities:**

```typescript
class FakeOrderRepository {
  private orders: Map<string, Order> = new Map();

  save(order: Order): Order {
    this.orders.set(order.id, order);
    return order;
  }

  findById(id: string): Order | null {
    return this.orders.get(id) || null;
  }

  // Complex query support
  findByCustomer(customerId: string): Order[] {
    return this.findAll().filter(o => o.customerId === customerId);
  }

  findByStatus(status: OrderStatus): Order[] {
    return this.findAll().filter(o => o.status === status);
  }

  findPendingOrders(): Order[] {
    return this.findByStatus('PENDING');
  }

  findAll(): Order[] {
    return Array.from(this.orders.values());
  }
}
```

---

## Selection Decision Tree

```
What do you need from the dependency?
│
├─ Nothing (just fill parameter)
│   └─ Use DUMMY
│       └─ Example: Logger in test that doesn't log
│
├─ Fixed return value(s)
│   ├─ Need to verify calls?
│   │   ├─ Yes → Use MOCK
│   │   │   └─ Example: PaymentGateway.process()
│   │   └─ No → Use STUB
│   │       └─ Example: ConfigService.getValue()
│   │
│   └─ Multiple sequential returns?
│       └─ Use STUB with mockReturnValueOnce()
│
├─ Record interactions for verification
│   ├─ Need real implementation too?
│   │   ├─ Yes → Use SPY
│   │   │   └─ Example: EmailService.sendEmail()
│   │   └─ No → Use MOCK
│   │
│   └─ Need to capture ALL calls?
│       └─ Use SPY
│           └─ Example: Analytics.track()
│
└─ Need working behavior (CRUD, queries)
    └─ Use FAKE
        └─ Example: In-memory UserRepository
```

---

## Mocking Best Practices

### DO ✅

```typescript
// ✅ Mock at architectural boundaries
it('processes payment', () => {
  const mockPaymentGateway = {
    process: vi.fn().mockResolvedValue({ success: true })
  };
  const service = new PaymentService(mockPaymentGateway);
  // ...
});

// ✅ Use fakes for complex domain logic
const fakeRepo = new FakeUserRepository();
const service = new UserService(fakeRepo);

// ✅ Keep mock setup minimal and focused
const mockRepo = {
  save: vi.fn().mockReturnValue({ id: '1' })
};

// ✅ Verify behavior, not implementation details
expect(result.status).toBe('completed'); // Good
expect(mockRepo.save.mock.calls[0][0]).toHaveProperty('name'); // Too detailed
```

### DON'T ❌

```typescript
// ❌ Mock what you don't own (use adapters instead)
vi.mock('axios'); // Don't mock third-party libraries directly
// Better: Create adapter and mock the adapter

// ❌ Over-mock (indicates design issues)
const mock = {
  a: vi.fn().mockReturnValue({ b: vi.fn().mockReturnValue({ c: vi.fn() }) }
}; // Mock chain is a code smell

// ❌ Mock private methods
vi.spyOn(service as any, 'validateCard').mockReturnValue(true);
// Tests implementation detail - refactor to test public interface

// ❌ Mock value objects or data structures
const mockUser = vi.fn(); // Unnecessary - just use a plain object
const user = { id: '1', name: 'John' }; // Better
```

---

## Common Mistakes

### 1. Over-mocking

```typescript
// ❌ BAD: Everything is mocked - what are we testing?
it('creates user', () => {
  const mockRepo = { save: vi.fn(), findById: vi.fn() };
  const mockEmail = { send: vi.fn() };
  const mockLogger = { log: vi.fn() };
  const mockCache = { set: vi.fn() };
  const mockValidator = { validate: vi.fn().mockReturnValue(true) };

  // Test passes trivially because everything is mocked
});

// ✅ GOOD: Only mock external dependencies
it('creates user', () => {
  const mockRepo = { save: vi.fn().mockReturnValue({ id: '1' }) };
  const service = new UserService(mockRepo); // Only repo is external

  const result = service.createUser({ name: 'John' });
  expect(result.id).toBe('1');
});
```

### 2. Mock Chain

```typescript
// ❌ BAD: Mock returning mock returning mock
const mockA = {
  getB: vi.fn().mockReturnValue({
    getC: vi.fn().mockReturnValue({
      getD: vi.fn().mockReturnValue('value')
    })
  })
};

// ✅ GOOD: Use Law of Demeter, refactor
const mockDependency = { getValue: vi.fn().mockReturnValue('value') };
```

### 3. Testing Mocks Instead of Behavior

```typescript
// ❌ BAD: Testing that mocks work
it('calls mock', () => {
  const mock = vi.fn();
  mock('arg');
  expect(mock).toHaveBeenCalledWith('arg'); // Trivial - always passes
});

// ✅ GOOD: Testing actual behavior
it('validates user before saving', () => {
  const mockRepo = { save: vi.fn() };
  const service = new UserService(mockRepo);

  expect(() => service.createUser({ name: '' })).toThrow(ValidationError);
  expect(mockRepo.save).not.toHaveBeenCalled();
});
```

### 4. Fragile Mock Assertions

```typescript
// ❌ BAD: Exact object match - breaks on any property change
expect(mock).toHaveBeenCalledWith({
  id: '1',
  name: 'John',
  email: 'john@test.com',
  createdAt: '2024-01-01',
  updatedAt: '2024-01-01',
  role: 'user',
  status: 'active'
});

// ✅ GOOD: Match only relevant properties
expect(mock).toHaveBeenCalledWith(
  expect.objectContaining({
    name: 'John',
    email: 'john@test.com'
  })
);
```

---

## Quick Reference

| Double | Purpose | Created With | When to Use |
|--------|---------|--------------|-------------|
| **Dummy** | Fill parameter | `{ } as Type` | Never used in test |
| **Stub** | Return values | `vi.fn().mockReturnValue()` | Need fixed response |
| **Spy** | Record calls | `vi.spyOn()` | Need to verify interactions |
| **Mock** | Pre-set expectations | `vi.fn()` + `expect()` | Strict behavior verification |
| **Fake** | Working implementation | Custom class | Need actual behavior |
