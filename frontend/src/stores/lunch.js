import { defineStore } from 'pinia'
import { ref } from 'vue'

export const useLunchStore = defineStore('lunch', () => {
  // State
  const currentUserStatus = ref('Unknown')
  const availableCoworkers = ref([
    { id: 1, name: 'Alice', status: 'Looking' },
    { id: 2, name: 'Bob', status: 'Solo' },
    { id: 3, name: 'Charlie', status: 'Looking' }
  ])
  const currentGroupId = ref(null)

  const isStatusLoading = ref(false)
  const isGroupLoading = ref(false)

  // Actions
  function setStatus(status) {
    if (currentUserStatus.value === status || isStatusLoading.value) return
    isStatusLoading.value = true

    // Mock API call with setTimeout
    setTimeout(() => {
      currentUserStatus.value = status
      isStatusLoading.value = false
    }, 500)
  }

  function createGroup() {
    if (isGroupLoading.value || currentGroupId.value) return
    isGroupLoading.value = true

    // Mock creating a group via API
    setTimeout(() => {
      currentGroupId.value = 'group-' + Math.random().toString(36).substr(2, 9)
      isGroupLoading.value = false
    }, 800)
  }

  return {
    currentUserStatus,
    availableCoworkers,
    currentGroupId,
    isStatusLoading,
    isGroupLoading,
    setStatus,
    createGroup
  }
})
