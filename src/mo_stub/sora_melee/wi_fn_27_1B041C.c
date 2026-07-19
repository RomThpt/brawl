void* fn_27_1B041C(void* p, int i) {
    int idx = (*(int*)((char*)p + 8) >> 28) + i;
    if (idx >= 7) idx -= 7;
    return (char*)p + idx * 144 + 12;
}
