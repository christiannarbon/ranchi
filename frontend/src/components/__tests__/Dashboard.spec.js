import { describe, it, expect, beforeEach, vi } from 'vitest'
import { mount, flushPromises } from '@vue/test-utils'
import { createPinia, setActivePinia } from 'pinia'
import Dashboard from '../Dashboard.vue'
import { useLunchStore } from '../../stores/lunch'
import { api } from '../../api/client'

// Mock the localStorage
const localStorageMock = (() => {
  let store = {}
  return {
    getItem: vi.fn((key) => store[key] || null),
    setItem: vi.fn((key, value) => {
      store[key] = value.toString()
    }),
    clear: vi.fn(() => {
      store = {}
    }),
    removeItem: vi.fn((key) => {
      delete store[key]
    })
  }
})()

Object.defineProperty(window, 'localStorage', {
  value: localStorageMock,
  writable: true
})

// Mock the api client
vi.mock('../../api/client', () => ({
  api: {
    patch: vi.fn().mockResolvedValue({ daily_status: 'Solo', id: 1 }),
    post: vi.fn().mockResolvedValue({ id: 1 }),
    get: vi.fn().mockResolvedValue([])
  }
}))

describe('Dashboard.vue', () => {
  beforeEach(() => {
    vi.clearAllMocks()
    window.localStorage.clear()
    window.localStorage.setItem('user_id', '1')
    setActivePinia(createPinia())
  })

  it('renders all three status buttons correctly', () => {
    const wrapper = mount(Dashboard)

    const text = wrapper.text()
    expect(text).toContain("Today's Lunch Status")
    expect(text).toContain('Looking for a Group')
    expect(text).toContain('Eating Solo')
    expect(text).toContain('Brought My Own')
  })

  it('updates the Pinia store status when a status button is clicked and renders loading state', async () => {
    const wrapper = mount(Dashboard)
    const store = useLunchStore()

    // Ensure the store is initialized with the correct mocked user ID
    expect(store.currentUserId).toBe('1')
    expect(store.currentUserStatus).toBe('Unknown')

    // Find the 'Eating Solo' button and click it
    const buttons = wrapper.findAll('button')
    const soloBtn = buttons.find((b) => b.text().includes('Eating Solo'))

    // Trigger the click synchronously
    soloBtn.trigger('click')

    // Immediately after click (before microtasks run), it should be loading, but status not updated yet
    expect(store.isStatusLoading).toBe(true)
    expect(store.currentUserStatus).toBe('Unknown')

    // Wait for the async API request to resolve
    await flushPromises()

    expect(store.isStatusLoading).toBe(false)
    expect(store.currentUserStatus).toBe('Solo')
    expect(api.patch).toHaveBeenCalledWith('/users/1/status', { daily_status: 'Solo' })
  })

  it('triggers group creation when the Create Group button is clicked', async () => {
    const wrapper = mount(Dashboard)
    const store = useLunchStore()

    // Ensure the store is initialized with the correct mocked user ID
    expect(store.currentUserId).toBe('1')

    // Set status to Looking so the Group section appears
    store.currentUserStatus = 'Looking'
    // Await reactivity
    await wrapper.vm.$nextTick()

    const buttons = wrapper.findAll('button')
    const createBtn = buttons.find((b) => b.text().includes('Create Group'))

    expect(createBtn).toBeDefined()

    // Trigger click synchronously
    createBtn.trigger('click')

    // Immediately after click, it should be loading
    expect(store.isGroupLoading).toBe(true)
    expect(store.currentGroupId).toBeNull()

    // Wait for the async API request to resolve
    await flushPromises()

    expect(store.isGroupLoading).toBe(false)
    expect(store.currentGroupId).toBe(1)
    expect(api.post).toHaveBeenCalledWith('/groups', {})
  })
})
