void* fn_27_1ACB54(void* p, int i) {
    int idx = (*(int*)((char*)p + 24) >> 28) + i;
    if (idx >= 6) idx -= 6;
    return (char*)p + idx * 16 + 28;
}
