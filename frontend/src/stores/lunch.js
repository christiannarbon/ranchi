import { defineStore } from 'pinia'
import { ref } from 'vue'
import { api } from '../api/client'

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

  const currentUserId = ref(
    typeof window !== 'undefined' && window.localStorage
      ? window.localStorage.getItem('user_id')
      : null
  )
  const coworkers = ref([])
  const statusError = ref(null)
  const groupError = ref(null)

  // Actions
  async function setStatus(status) {
    if (currentUserStatus.value === status || isStatusLoading.value) return
  }

  async function createGroup() {
    if (isGroupLoading.value || currentGroupId.value) return
  }

  return {
    currentUserStatus,
    availableCoworkers,
    currentGroupId,
    isStatusLoading,
    isGroupLoading,
    currentUserId,
    coworkers,
    statusError,
    groupError,
    setStatus,
    createGroup
  }
})
