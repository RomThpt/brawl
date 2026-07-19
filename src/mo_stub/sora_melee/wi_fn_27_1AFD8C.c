void* fn_27_1AFD8C(void* p, int i) {
    int idx = (*(int*)((char*)p + 8) >> 22) + i;
    if (idx >= 292) idx -= 292;
    return (char*)p + idx * 4 + 12;
}
