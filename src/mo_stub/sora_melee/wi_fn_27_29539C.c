void* fn_27_29539C(void* p, int i) {
    int idx = (*(int*)((char*)p + 24) >> 26) + i;
    if (idx >= 20) idx -= 20;
    return (char*)p + idx * 12 + 28;
}
