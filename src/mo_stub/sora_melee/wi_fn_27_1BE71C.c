void* fn_27_1BE71C(void* p, int i) {
    int idx = (*(int*)((char*)p + 24) >> 26) + i;
    if (idx >= 18) idx -= 18;
    return (char*)p + idx * 12 + 28;
}
