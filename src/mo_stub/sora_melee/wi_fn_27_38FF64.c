void* fn_27_38FF64(void* p, int i) {
    int idx = (*(int*)((char*)p + 24) >> 26) + i;
    if (idx >= 19) idx -= 19;
    return (char*)p + idx * 12 + 28;
}
