void* fn_27_1BD32C(void* p, int i) {
    int idx = (*(int*)((char*)p + 24) >> 26) + i;
    if (idx >= 24) idx -= 24;
    return (char*)p + idx * 12 + 28;
}
