#include <gf/gf_heap_manager.h>
#include <gf/gf_memory_pool.h>
#include <memory.h>

int gfHeapManager::getMaxFreeSize(Heaps::HeapType heapType) {
    return g_HeapInfos[heapType].m_memoryPool->getMaxFreeBlockSize();
}

void gfHeapManager::free(void* ptr) {
    ::free(ptr);
}
