import { vi } from 'vitest'
import { authStateScenario } from '../data/scenarios'

export function createAuthServiceHarness() {
  return {
    api: { post: vi.fn() },
    persistSession: vi.fn(),
    state: authStateScenario(),
  }
}
