import { describe, it, expect, beforeEach, vi } from 'vitest'
import { mount } from '@vue/test-utils'
import { createPinia, setActivePinia } from 'pinia'
import Dashboard from '../Dashboard.vue'
import { useLunchStore } from '../../stores/lunch'

describe('Dashboard.vue', () => {
  beforeEach(() => {
    setActivePinia(createPinia())
    // Use fake timers so we can test the setTimeout behavior instantly
    vi.useFakeTimers()
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
    
    expect(store.currentUserStatus).toBe('Unknown')
    
    // Find the 'Eating Solo' button and click it
    const buttons = wrapper.findAll('button')
    const soloBtn = buttons.find(b => b.text().includes('Eating Solo'))
    
    await soloBtn.trigger('click')
    
    // Immediately after click, it should be loading, but status not updated yet
    expect(store.isStatusLoading).toBe(true)
    expect(store.currentUserStatus).toBe('Unknown')
    
    // Fast-forward timers to simulate API resolution
    vi.runAllTimers()
    
    expect(store.isStatusLoading).toBe(false)
    expect(store.currentUserStatus).toBe('Solo')
  })
  
  it('triggers group creation when the Create Group button is clicked', async () => {
    const wrapper = mount(Dashboard)
    const store = useLunchStore()
    
    // Set status to Looking so the Group section appears
    store.currentUserStatus = 'Looking'
    // Await reactivity
    await wrapper.vm.$nextTick()
    
    const buttons = wrapper.findAll('button')
    const createBtn = buttons.find(b => b.text().includes('Create Group'))
    
    expect(createBtn).toBeDefined()
    
    await createBtn.trigger('click')
    
    // Immediately after click, it should be loading
    expect(store.isGroupLoading).toBe(true)
    expect(store.currentGroupId).toBeNull()
    
    // Fast-forward timers to simulate API resolution
    vi.runAllTimers()
    
    expect(store.isGroupLoading).toBe(false)
    expect(store.currentGroupId).toContain('group-')
  })
})
