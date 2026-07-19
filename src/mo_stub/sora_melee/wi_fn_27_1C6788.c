void* fn_27_1C6788(void* p, int i) {
    int idx = (*(int*)((char*)p + 24) >> 25) + i;
    if (idx >= 32) idx -= 32;
    return (char*)p + idx * 12 + 28;
}
