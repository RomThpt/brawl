void* fn_61_E798(void* p, int i) {
    int idx = (*(int*)((char*)p + 8) >> 29) + i;
    if (idx >= 2) idx -= 2;
    return (char*)p + idx * 144 + 12;
}
