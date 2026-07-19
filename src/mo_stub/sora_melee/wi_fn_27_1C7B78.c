void* fn_27_1C7B78(void* p, int i) {
    int idx = (*(int*)((char*)p + 24) >> 25) + i;
    if (idx >= 33) idx -= 33;
    return (char*)p + idx * 12 + 28;
}
