void* fn_79_588C(void* p, int i) {
    int idx = (*(int*)((char*)p + 8) >> 26) + i;
    if (idx >= 30) idx -= 30;
    return (char*)p + idx * 56 + 12;
}
