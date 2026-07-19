void* fn_27_1B0C38(void* p, int i) {
    int idx = (*(int*)((char*)p + 8) >> 26) + i;
    if (idx >= 20) idx -= 20;
    return (char*)p + idx * 20 + 12;
}
