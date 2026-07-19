void* fn_27_1B0EC4(void* p, int i) {
    int idx = (*(int*)((char*)p + 8) >> 28) + i;
    if (idx >= 5) idx -= 5;
    return (char*)p + idx * 8 + 12;
}
