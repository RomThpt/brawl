void* fn_71_9F18(void* p, int i) {
    int idx = (*(int*)((char*)p + 8) >> 30) + i;
    if (idx >= 1) idx -= 1;
    return (char*)p + idx * 160 + 12;
}
