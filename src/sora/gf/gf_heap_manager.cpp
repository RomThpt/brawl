#include <gf/gf_heap_manager.h>
#include <gf/gf_memory_pool.h>

void* gfHeapManager::getHeap(Heaps::HeapType heapType) {
    return g_HeapInfos[heapType].m_memoryPool;
}

void* gfHeapManager::alloc(Heaps::HeapType heapType, size_t size) {
    return gfMemoryPool::alloc(g_HeapInfos[heapType].m_memoryPool, size, 32);
}

void* gfHeapManager::alloc(Heaps::HeapType heapType, size_t size, s32 align) {
    return gfMemoryPool::alloc(g_HeapInfos[heapType].m_memoryPool, size, align);
}
