void* fn_27_293F8C(void* p, int i) {
    int idx = (*(int*)((char*)p + 24) >> 27) + i;
    if (idx >= 9) idx -= 9;
    return (char*)p + idx * 12 + 28;
}
