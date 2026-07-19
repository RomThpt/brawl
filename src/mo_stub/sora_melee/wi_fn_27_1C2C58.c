void* fn_27_1C2C58(void* p, int i) {
    int idx = (*(int*)((char*)p + 24) >> 28) + i;
    if (idx >= 6) idx -= 6;
    return (char*)p + idx * 12 + 28;
}
