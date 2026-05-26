import { defineStore } from 'pinia'
import { ref } from 'vue'

export const useLunchStore = defineStore('lunch', () => {
  // State
  const currentUserStatus = ref('Unknown')
  const availableCoworkers = ref([
    { id: 1, name: 'Alice', status: 'Looking for group' },
    { id: 2, name: 'Bob', status: 'Already ate' },
    { id: 3, name: 'Charlie', status: 'Looking for group' }
  ])
  const currentGroupId = ref(null)

  // Actions
  function setStatus(status) {
    currentUserStatus.value = status
  }

  function createGroup() {
    // Mock creating a group
    currentGroupId.value = 'group-' + Math.random().toString(36).substr(2, 9)
  }

  return {
    currentUserStatus,
    availableCoworkers,
    currentGroupId,
    setStatus,
    createGroup
  }
})
