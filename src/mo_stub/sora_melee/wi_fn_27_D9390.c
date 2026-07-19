void* fn_27_D9390(void* p, int i) {
    int idx = (*(int*)((char*)p + 8) >> 25) + i;
    if (idx >= 34) idx -= 34;
    return (char*)p + idx * 48 + 12;
}
